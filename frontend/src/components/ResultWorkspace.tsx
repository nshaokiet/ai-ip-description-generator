"use client";

import { useCallback, useEffect, useRef, useState, type KeyboardEvent, type ReactNode } from "react";
import { createPortal } from "react-dom";

import { AnalysisView } from "@/components/AnalysisView";
import { EvidenceCard } from "@/components/EvidenceCard";
import { PatentDraftView } from "@/components/PatentDraftView";
import { ReviewItemsView } from "@/components/ReviewItemsView";
import { ApiClientError, validateDraft } from "@/lib/api/client";
import { useUi, localizedError, displayErrorCode } from "@/lib/uiPreferences";
import {
  createDraftSession,
  editAbstract,
  editedProsePaths,
  editParagraph,
  saveDraftRevision,
  selectedRevision,
  setReviewStatus,
  setRevisionValidation,
  type ReviewStatus,
} from "@/lib/draftRevisions";
import type {
  DraftRevisionRequest,
  ExportDocxRequest,
  NormalizedApiError,
  PatentDraft,
  ProcessResult,
  WorkflowPhase,
  WorkflowState,
} from "@/lib/types/contracts";

type ResultTab = "draft" | "review" | "analysis";

interface ResultWorkspaceProps {
  result: ProcessResult;
  state: WorkflowState;
  phase: WorkflowPhase;
  onExport: (request: ExportDocxRequest) => Promise<void>;
  onPhaseChange: (phase: WorkflowPhase) => void;
  onReviewEligibilityChange: (eligible: boolean) => void;
  onValidationEligibilityChange: (eligible: boolean) => void;
  onReset: () => void;
  onRegisterGuard: (guard: (proceed: () => void) => boolean) => void;
}

function safeValidationError(issue: unknown): NormalizedApiError {
  if (issue instanceof ApiClientError) return issue;
  return { status: 0, code: "unexpected_client_error", message: "Validation could not be completed safely." };
}

export function ResultWorkspace({
  result,
  state,
  phase,
  onExport,
  onPhaseChange,
  onReviewEligibilityChange,
  onValidationEligibilityChange,
  onReset,
  onRegisterGuard,
}: ResultWorkspaceProps) {
  const { t } = useUi();
  const [activeTab, setActiveTab] = useState<ResultTab>("draft");
  const [session, setSession] = useState(() => createDraftSession(result.draft));
  const [editBuffer, setEditBuffer] = useState<PatentDraft | null>(null);
  const [validating, setValidating] = useState(false);
  const [validationError, setValidationError] = useState<NormalizedApiError | null>(null);
  const [resetConfirmation, setResetConfirmation] = useState(false);
  const [pendingAction, setPendingAction] = useState<(() => void) | null>(null);
  const [sectionRailOpen, setSectionRailOpen] = useState(false);
  const [evidenceOpen, setEvidenceOpen] = useState(false);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);
  const [activeSectionId, setActiveSectionId] = useState<string | null>(null);
  const dialogRef = useRef<HTMLDivElement>(null);
  const returnFocusRef = useRef<HTMLElement | null>(null);
  const sectionsTriggerRef = useRef<HTMLButtonElement>(null);
  const evidenceTriggerRef = useRef<HTMLButtonElement>(null);
  const validationLockRef = useRef(false);
  const exportLockRef = useRef(false);
  const errorHeadingRef = useRef<HTMLHeadingElement>(null);
  const tabRefs = useRef<Record<ResultTab, HTMLButtonElement | null>>({ draft: null, review: null, analysis: null });
  const revision = selectedRevision(session);
  const originalDraft = session.revisions[0].draft;
  const editing = editBuffer !== null;
  const dirty = editBuffer !== null && JSON.stringify(editBuffer) !== JSON.stringify(revision.draft);
  const busy = validating || state === "EXPORTING";
  const selectedTitleId = originalDraft.selected_title.status === "PRESENT"
    ? originalDraft.selected_title.source_title_candidate_id ?? null
    : null;
  const requestBody: DraftRevisionRequest = {
    revision_id: revision.id,
    analysis: result.analysis,
    original_draft: originalDraft,
    draft: revision.draft,
    selected_title_candidate_id: selectedTitleId,
  };
  const unverifiedPaths = editedProsePaths(originalDraft, editBuffer ?? revision.draft);
  const reviewCounts = { UNREVIEWED: 0, REVIEWED: 0, NEEDS_CHANGES: 0 };
  Object.values(revision.review).forEach((record) => { reviewCounts[record.status] += 1; });
  const reviewTotal = Object.keys(revision.review).length;
  const reviewRemaining = reviewCounts.UNREVIEWED + reviewCounts.NEEDS_CHANGES;
  const reviewComplete = reviewTotal > 0
    && reviewCounts.REVIEWED === reviewTotal
    && reviewRemaining === 0;
  const tabs: Array<{ key: ResultTab; label: string }> = [
    { key: "draft", label: t("patentDraft") },
    { key: "review", label: t("reviewItems") },
    { key: "analysis", label: t("analysis") },
  ];

  const guardNavigation = useCallback((proceed: () => void) => {
    if (!dirty) return true;
    returnFocusRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    setPendingAction(() => proceed);
    return false;
  }, [dirty]);

  useEffect(() => { onRegisterGuard(guardNavigation); }, [guardNavigation, onRegisterGuard]);

  useEffect(() => {
    if (!pendingAction) return;
    const priorOverflow = document.body.style.overflow;
    const shell = document.querySelector<HTMLElement>(".app-shell");
    if (shell) shell.inert = true;
    document.body.style.overflow = "hidden";
    const frame = requestAnimationFrame(() => dialogRef.current?.querySelector<HTMLButtonElement>("button")?.focus());
    return () => { cancelAnimationFrame(frame); document.body.style.overflow = priorOverflow; if (shell) shell.inert = false; returnFocusRef.current?.focus(); };
  }, [pendingAction]);

  function dismissPending() { setPendingAction(null); }
  function discardPending() {
    const action = pendingAction;
    setEditBuffer(null);
    setPendingAction(null);
    action?.();
  }

  function handleDialogKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") { event.preventDefault(); dismissPending(); return; }
    if (event.key !== "Tab") return;
    const buttons = Array.from(dialogRef.current?.querySelectorAll<HTMLButtonElement>("button:not(:disabled)") ?? []);
    if (!buttons.length) return;
    const first = buttons[0], last = buttons[buttons.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }

  const evidenceItems = revision.draft.evidence_appendix;
  const selectedEvidence = selectedEvidenceId === null ? evidenceItems[0] : evidenceItems.find((item) => item.evidence_id === selectedEvidenceId);

  function scrollToSection(sectionId: string) {
    setActiveTab("draft");
    setActiveSectionId(sectionId);
    setSectionRailOpen(false);
    window.requestAnimationFrame(() => {
      const heading = document.getElementById(`draft-${sectionId}`);
      heading?.setAttribute("tabindex", "-1");
      heading?.focus({ preventScroll: true });
      heading?.scrollIntoView({ block: "start" });
    });
  }

  useEffect(() => {
    onReviewEligibilityChange(reviewComplete);
    onValidationEligibilityChange(Boolean(revision.validation));
  }, [onReviewEligibilityChange, onValidationEligibilityChange, reviewComplete, revision.validation]);

  function handleTabKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (!["ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const enabledTabs = tabs.filter((tab) => !editing || tab.key === "draft");
    const currentIndex = enabledTabs.findIndex((tab) => tab.key === activeTab);
    const nextIndex = event.key === "Home" ? 0
      : event.key === "End" ? enabledTabs.length - 1
        : event.key === "ArrowRight" ? (currentIndex + 1) % enabledTabs.length
          : (currentIndex - 1 + enabledTabs.length) % enabledTabs.length;
    const nextTab = enabledTabs[nextIndex].key;
    setActiveTab(nextTab);
    tabRefs.current[nextTab]?.focus();
  }

  function beginEdit() {
    setEditBuffer(structuredClone(revision.draft));
    setActiveTab("draft");
  }

  function fieldId(path: string): string | null {
    if (path === "/abstract/text" || path === "/abstract/word_count") return "edit-abstract";
    const match = path.match(/^\/draft_sections\/(\d+)\/(?:subsections\/(\d+)\/)?paragraphs\/(\d+)\/text$/);
    if (!match) return null;
    const section = revision.draft.draft_sections[Number(match[1])];
    const paragraph = match[2] === undefined ? section?.paragraphs[Number(match[3])] : section?.subsections[Number(match[2])]?.paragraphs[Number(match[3])];
    return paragraph ? `edit-${paragraph.paragraph_id}` : null;
  }

  function recoverField(path: string) {
    const id = fieldId(path);
    if (!id) return;
    beginEdit();
    onPhaseChange("review");
    window.requestAnimationFrame(() => document.getElementById(id)?.focus());
  }

  function cancelEdit() {
    if (guardNavigation(() => { setEditBuffer(null); setValidationError(null); })) {
      setEditBuffer(null); setValidationError(null);
    }
  }

  function saveEdit() {
    if (!editBuffer || !dirty) return;
    setSession((current) => saveDraftRevision(current, editBuffer));
    setEditBuffer(null);
    setValidationError(null);
  }

  async function handleValidate() {
    if (!reviewComplete || editing || busy || validationLockRef.current) return;
    validationLockRef.current = true;
    setValidationError(null);
    setValidating(true);
    onPhaseChange("validate");
    try {
      const validation = await validateDraft(requestBody);
      if (!validation.valid || validation.revision_id !== revision.id) {
        throw new Error("Validation response does not match the selected revision.");
      }
      setSession((current) => setRevisionValidation(current, revision.id, validation));
      onValidationEligibilityChange(true);
    } catch (issue) {
      setSession((current) => setRevisionValidation(current, revision.id, null));
      onValidationEligibilityChange(false);
      setValidationError(safeValidationError(issue));
      setActiveTab("draft");
      onPhaseChange("validate");
      window.requestAnimationFrame(() => errorHeadingRef.current?.focus());
    } finally {
      validationLockRef.current = false;
      setValidating(false);
    }
  }

  function handleReviewChange(sectionId: string, status: ReviewStatus) {
    setSession((current) => setReviewStatus(current, sectionId, status));
  }

  function handleExport() {
    if (!reviewComplete || editing || busy || !revision.validation || exportLockRef.current) return;
    exportLockRef.current = true;
    void onExport({ ...requestBody, validated_digest: revision.validation.draft_digest })
      .finally(() => {
        exportLockRef.current = false;
      });
  }

  function selectRevision(revisionId: string) {
    const apply = () => {
      setEditBuffer(null);
      setSession((current) => ({ ...current, selectedId: revisionId }));
      setValidationError(null);
    };
    if (guardNavigation(apply)) apply();
  }

  function renderNewPaperAction() {
    return (
      <div className="new-paper-action">
        {!resetConfirmation ? (
          <button className="secondary-button" disabled={busy} onClick={() => setResetConfirmation(true)} type="button">{t("newPaper")}</button>
        ) : (
          <div className="reset-confirmation reset-confirmation-compact" role="alert">
            <strong>{t("resetQuestion")}</strong>
            <p>{t("resetDescription")}</p>
            <div>
              <button className="danger-button" onClick={onReset} type="button">{t("fileReset")}</button>
              <button className="secondary-button" onClick={() => setResetConfirmation(false)} type="button">{t("cancel")}</button>
            </div>
          </div>
        )}
      </div>
    );
  }

  function renderRevisionSelector(includeStatus = true) {
    return (
      <div className="revision-selector">
        <label htmlFor={`revision-select-${phase}`}>{t("selectedRevision")}</label>
        <select
          disabled={busy}
          id={`revision-select-${phase}`}
          onChange={(event) => selectRevision(event.target.value)}
          value={session.selectedId}
        >
          {session.revisions.map((item, index) => (
            <option key={item.id} value={item.id}>{item.id}{index === 0 ? ` · ${t("generated")}` : ` · ${t("revised")}`}</option>
          ))}
        </select>
        {includeStatus && <span className={revision.validation ? "status-success" : "status-pending"}>{revision.validation ? t("validated") : t("validationRequired")}</span>}
      </div>
    );
  }

  function renderTechnicalDetails(children?: ReactNode) {
    return (
      <details className="technical-details result-technical-details">
        <summary>{t("details")}</summary>
        <div className="technical-detail-content">
          <p>{t("reference")}: <code>{result.metadata.correlation_id}</code></p>
          <p>{session.revisions.length} · {t("sessionOnly")}</p>
          {children}
        </div>
      </details>
    );
  }

  if (phase === "validate") {
    return (
      <section aria-busy={busy} className="stage-card validation-stage" aria-labelledby="validation-heading">
        {revision.validation && <span className="stage-icon stage-icon-success" aria-hidden="true">✓</span>}
        <p className="eyebrow">{t("validation")}</p>
        <h2 id="validation-heading">{revision.validation ? t("validationComplete") : t("validationHeading")}</h2>
        <p>
          {revision.validation
            ? <>{t("validationPassed")} <strong>{revision.id}</strong>.</>
            : t("validationInstruction")}
        </p>
        {renderRevisionSelector()}

        {revision.validation ? (
          <>
            <div className="export-summary validation-summary" role="status">
              <span className="status-success">✓ {t("validationComplete")}</span>
              <strong>{revision.id}</strong>
              <span>{t("technicalOnly")}</span>
            </div>
            <p className="card-supporting-copy">
              {t("technicalOnly")}
            </p>
            <button className="primary-button" onClick={() => onPhaseChange("export")} type="button">
              {t("continueExport")}
            </button>
          </>
        ) : validating ? (
          <div className="processing-callout workspace-operation" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>{t("validating")} {revision.id}…</strong>
              <p>{t("validationBusy")}</p>
            </div>
          </div>
        ) : (
          <button
            className="primary-button"
            disabled={!reviewComplete || editing || busy}
            onClick={() => void handleValidate()}
            type="button"
          >
            {t("validationAction")} {revision.id}
          </button>
        )}

        {validationError && (
          <section className="error-banner" role="alert" aria-labelledby="draft-validation-error">
            <div>
              <h3 id="draft-validation-error" ref={errorHeadingRef} tabIndex={-1}>{t("validationErrorTitle")} · {displayErrorCode(validationError.code)}</h3>
              <p>{localizedError(validationError.code, t)}</p>
              {validationError.paths?.length ? <div><p>{t("affectedFields")}</p>{validationError.paths.filter((path) => fieldId(path)).map((path) => <button className="text-button" key={path} type="button" onClick={() => recoverField(path)}>{t("goToField")}: <code>{path}</code></button>)}</div> : null}
              {validationError.correlation_id && <p>{t("reference")}: <code>{validationError.correlation_id}</code></p>}
              <p>{t("validationRecoverHelp")}</p>
            </div>
            <button className="secondary-button" onClick={() => { beginEdit(); onPhaseChange("review"); }} type="button">
              {t("validationRecover")}
            </button>
          </section>
        )}

        <div className="stage-secondary-actions">
          <button className="text-button" onClick={() => onPhaseChange("review")} type="button">{t("returnReview")}</button>
          {renderNewPaperAction()}
        </div>
        {renderTechnicalDetails()}
      </section>
    );
  }

  if (phase === "export") {
    return (
      <section aria-busy={busy} className="stage-card export-stage" aria-labelledby="export-heading">
        <span className="stage-icon stage-icon-success" aria-hidden="true">✓</span>
        <p className="eyebrow">{t("export")}</p>
        <h2 id="export-heading">{t("validationComplete")}</h2>
        <p>{t("validationPassed")} <strong>{revision.id}</strong>. {t("draftWarning")}</p>
        <div className="export-summary">
          <span>{t("selectedRevision")}</span>
          <strong>{revision.id}</strong>
          <span className="status-success">{t("validationPassedLabel")}</span>
        </div>
        <button
          aria-label={`${t("exportAction")} ${revision.id} DOCX`}
          className="primary-button export-primary-button"
          disabled={busy || editing || !revision.validation}
          onClick={handleExport}
          type="button"
        >
          {state === "EXPORTING" ? t("preparingDocx") : t("exportDocx")}
        </button>
        <p className="card-supporting-copy">{t("exportUnavailable")}</p>
        <p className="card-supporting-copy">{t("draftWarning")}</p>
        {state === "EXPORTING" && (
          <div className="processing-callout workspace-operation" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>{t("preparingDocx")} · {revision.id}</strong>
              <p>{t("exportBusy")}</p>
            </div>
          </div>
        )}
        <div className="stage-secondary-actions">
          <button className="text-button" onClick={() => onPhaseChange("validate")} type="button">{t("reviewValidation")}</button>
          {renderNewPaperAction()}
        </div>
        {renderTechnicalDetails(<p>{t("validated")}: <code>{revision.validation?.draft_digest}</code></p>)}
      </section>
    );
  }

  return (
    <section aria-busy={busy} className="results-workspace" aria-labelledby="results-heading">
      <div className="results-toolbar">
        <div>
          <p className="eyebrow">{t("review")}</p>
          <h2 id="results-heading">{t("review")}</h2>
          <p>{t("reviewIntro")}</p>
        </div>
        {renderNewPaperAction()}
      </div>

      <div className="revision-workspace" aria-label={t("revision")}>
        {renderRevisionSelector(false)}
        <div className="revision-actions">
          {editing ? (
            <>
              <button className="primary-button" disabled={!dirty} onClick={saveEdit} type="button">{t("save")}</button>
              <button className="secondary-button" onClick={cancelEdit} type="button">{t("cancel")}</button>
            </>
          ) : (
            <>
              <button className="secondary-button" disabled={busy} onClick={beginEdit} type="button">{t("edit")}</button>
              <button
                aria-label={`${t("continueValidation")} · ${revision.id}`}
                className="primary-button"
                disabled={busy || !reviewComplete}
                onClick={() => onPhaseChange("validate")}
                type="button"
              >
                {t("continueValidation")}
              </button>
            </>
          )}
        </div>
      </div>

      <div className="revision-status" role="status" aria-live="polite">
        <strong>{revision.id} · {editing ? (dirty ? t("unsavedShort") : t("editing")) : t("saved")}</strong>
        <span>{t("validation")}: {revision.validation ? t("validated") : t("notValidated")}</span>
        <span>{t("reviewSummary")}: {reviewCounts.UNREVIEWED} {t("statusUnreviewed")} · {reviewCounts.REVIEWED} {t("statusReviewed")} · {reviewCounts.NEEDS_CHANGES} {t("statusNeedsChanges")}</span>
        <span>
          {reviewComplete
            ? t("reviewDone")
            : `${t("reviewAll")} · ${reviewRemaining} ${t("reviewRemaining")}.`}
        </span>
        <span>{t("exportTarget")}: {revision.id} · {revision.validation && reviewComplete ? t("eligible") : t("validationRequired")}</span>
      </div>

      {unverifiedPaths.length > 0 && (
        <p className="edit-support-warning" role="note">
          {unverifiedPaths.length} · {t("editorSupport")}
        </p>
      )}

      <div className="document-review-layout">
        <aside className={`section-rail ${sectionRailOpen ? "mobile-panel-open" : ""}`} aria-label={t("sectionList")}>
          <button ref={sectionsTriggerRef} className="mobile-panel-trigger secondary-button" type="button" aria-expanded={sectionRailOpen} onClick={() => setSectionRailOpen((value) => !value)}>{t("sectionList")} ▾</button>
          <div className="section-rail-content" onKeyDown={(event) => { if (event.key === "Escape") { setSectionRailOpen(false); sectionsTriggerRef.current?.focus(); } }}>
            <h3>{t("sectionList")}</h3>
            <button className="rail-link" type="button" onClick={() => { setActiveTab("draft"); window.requestAnimationFrame(() => document.getElementById("draft-abstract-heading")?.scrollIntoView()); }}>{t("abstract")}</button>
            {revision.draft.draft_sections.map((section, index) => <button className="rail-link" key={section.section_id} type="button" aria-current={activeSectionId === section.section_id ? "location" : undefined} onClick={() => scrollToSection(section.section_id)}>{String(section.sequence).padStart(2, "0")} · {section.heading} <small>{t(revision.review[section.section_id]?.status === "REVIEWED" ? "statusReviewed" : revision.review[section.section_id]?.status === "NEEDS_CHANGES" ? "statusNeedsChanges" : "statusUnreviewed")}{section.status === "MISSING" ? ` · ${t("missingContent")}` : ""}{validationError?.paths?.some((path) => path.startsWith(`/draft_sections/${index}/`)) ? ` · ${t("validationFailed")}` : ""}</small></button>)}
          </div>
        </aside>
        <div className="document-center">
      <div className="tab-list" role="tablist" aria-label={t("resultViews")}>
        {tabs.map((tab) => (
          <button
            aria-controls={`panel-${tab.key}`}
            aria-selected={activeTab === tab.key}
            className={activeTab === tab.key ? "tab-active" : ""}
            disabled={editing && tab.key !== "draft"}
            id={`tab-${tab.key}`}
            key={tab.key}
            onKeyDown={handleTabKeyDown}
            onClick={() => setActiveTab(tab.key)}
            ref={(node) => { tabRefs.current[tab.key] = node; }}
            role="tab"
            tabIndex={activeTab === tab.key ? 0 : -1}
            type="button"
          >{tab.label}</button>
        ))}
      </div>

      <div aria-labelledby={`tab-${activeTab}`} className="tab-panel" id={`panel-${activeTab}`} role="tabpanel">
        {activeTab === "draft" && (
          <PatentDraftView
            draft={editBuffer ?? revision.draft}
            editing={editing}
            errorPaths={validationError?.paths}
            onAbstractChange={(text) => setEditBuffer((current) => current ? editAbstract(current, text) : current)}
            onParagraphChange={(section, subsection, paragraph, text) =>
              setEditBuffer((current) => current ? editParagraph(current, section, subsection, paragraph, text) : current)}
            onReviewChange={handleReviewChange}
            onInspectEvidence={(id) => { setSelectedEvidenceId(id); setEvidenceOpen(true); window.requestAnimationFrame(() => { const inspector = document.getElementById("evidence-inspector-heading"); inspector?.focus({ preventScroll: true }); inspector?.scrollIntoView({ block: "nearest" }); }); }}
            review={revision.review}
            unverifiedPaths={unverifiedPaths}
          />
        )}
        {activeTab === "review" && <ReviewItemsView analysis={result.analysis} draft={revision.draft} />}
        {activeTab === "analysis" && <AnalysisView analysis={result.analysis} />}
      </div>
        </div>
        <aside className={`evidence-inspector ${evidenceOpen ? "mobile-panel-open" : ""}`} aria-label={t("evidence")}>
          <button ref={evidenceTriggerRef} className="mobile-panel-trigger secondary-button" type="button" aria-expanded={evidenceOpen} onClick={() => setEvidenceOpen((value) => !value)}>{t("evidence")} ▾</button>
          <div className="evidence-inspector-content" onKeyDown={(event) => { if (event.key === "Escape") { setEvidenceOpen(false); evidenceTriggerRef.current?.focus(); } }}>
            <h3 id="evidence-inspector-heading" tabIndex={-1}>{t("evidence")}</h3>
            <p className="inspector-note">{t("technicalOnly")}</p>
            {evidenceItems.length ? <>
              <div className="inspector-evidence-ids" role="group" aria-label={t("inspectEvidence")}>
                {evidenceItems.map((evidence) => <button type="button" key={evidence.evidence_id} aria-pressed={selectedEvidence?.evidence_id === evidence.evidence_id} onClick={() => setSelectedEvidenceId(evidence.evidence_id)}>{evidence.evidence_id}</button>)}
              </div>
              {selectedEvidence ? <EvidenceCard evidence={selectedEvidence} /> : <p>{t("noEvidence")}</p>}
            </> : <p>{t("noEvidence")}</p>}
          </div>
        </aside>
      </div>

      {pendingAction && createPortal(<div className="dialog-backdrop"><div className="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="dirty-dialog-title" aria-describedby="dirty-dialog-description" ref={dialogRef} onKeyDown={handleDialogKeyDown}>
        <h3 id="dirty-dialog-title">{t("confirmTitle")}</h3>
        <p id="dirty-dialog-description">{t("unsaved")}</p>
        <div className="dialog-actions"><button className="primary-button" type="button" onClick={dismissPending}>{t("stay")}</button><button className="danger-button" type="button" onClick={discardPending}>{t("discard")}</button></div>
      </div></div>, document.body)}

      {renderTechnicalDetails()}
    </section>
  );
}
