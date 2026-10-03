"use client";

import { useEffect, useRef, useState, type KeyboardEvent, type ReactNode } from "react";

import { AnalysisView } from "@/components/AnalysisView";
import { PatentDraftView } from "@/components/PatentDraftView";
import { ReviewItemsView } from "@/components/ReviewItemsView";
import { ApiClientError, validateDraft } from "@/lib/api/client";
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
}: ResultWorkspaceProps) {
  const [activeTab, setActiveTab] = useState<ResultTab>("draft");
  const [session, setSession] = useState(() => createDraftSession(result.draft));
  const [editBuffer, setEditBuffer] = useState<PatentDraft | null>(null);
  const [validating, setValidating] = useState(false);
  const [validationError, setValidationError] = useState<NormalizedApiError | null>(null);
  const [resetConfirmation, setResetConfirmation] = useState(false);
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
    { key: "draft", label: "Patent Draft" },
    { key: "review", label: "Review Items" },
    { key: "analysis", label: "Analysis" },
  ];

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
    setValidationError(null);
    setActiveTab("draft");
  }

  function cancelEdit() {
    setEditBuffer(null);
    setValidationError(null);
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
    setSession((current) => ({ ...current, selectedId: revisionId }));
    setValidationError(null);
  }

  function renderNewPaperAction() {
    return (
      <div className="new-paper-action">
        {!resetConfirmation ? (
          <button className="secondary-button" disabled={busy} onClick={() => setResetConfirmation(true)} type="button">New paper</button>
        ) : (
          <div className="reset-confirmation reset-confirmation-compact" role="alert">
            <strong>Clear this session and start a new paper?</strong>
            <p>Analysis, revisions, review status, and validation will be removed from this frontend session.</p>
            <div>
              <button className="danger-button" onClick={onReset} type="button">Clear session and start over</button>
              <button className="secondary-button" onClick={() => setResetConfirmation(false)} type="button">Cancel</button>
            </div>
          </div>
        )}
      </div>
    );
  }

  function renderRevisionSelector(includeStatus = true) {
    return (
      <div className="revision-selector">
        <label htmlFor={`revision-select-${phase}`}>Selected revision</label>
        <select
          disabled={busy || editing}
          id={`revision-select-${phase}`}
          onChange={(event) => selectRevision(event.target.value)}
          value={session.selectedId}
        >
          {session.revisions.map((item, index) => (
            <option key={item.id} value={item.id}>{item.id}{index === 0 ? " · generated" : " · edited"}</option>
          ))}
        </select>
        {includeStatus && <span className={revision.validation ? "status-success" : "status-pending"}>{revision.validation ? "Validated" : "Validation required"}</span>}
      </div>
    );
  }

  function renderTechnicalDetails(children?: ReactNode) {
    return (
      <details className="technical-details result-technical-details">
        <summary>Technical details</summary>
        <div className="technical-detail-content">
          <p>Correlation ID: <code>{result.metadata.correlation_id}</code></p>
          <p>{session.revisions.length} immutable session revision(s). Reload or reset discards edits, validation, and review status.</p>
          {children}
        </div>
      </details>
    );
  }

  if (phase === "validate") {
    return (
      <section aria-busy={busy} className="stage-card validation-stage" aria-labelledby="validation-heading">
        {revision.validation && <span className="stage-icon stage-icon-success" aria-hidden="true">✓</span>}
        <p className="eyebrow">Validation</p>
        <h2 id="validation-heading">{revision.validation ? "Validation complete" : "Validate the selected revision"}</h2>
        <p>
          {revision.validation
            ? <>Structure and required fields passed server validation for <strong>{revision.id}</strong>.</>
            : "Run the existing server validation against the exact saved revision before export."}
        </p>
        {renderRevisionSelector()}

        {revision.validation ? (
          <>
            <div className="export-summary validation-summary" role="status">
              <span className="status-success">✓ Validation complete</span>
              <strong>{revision.id}</strong>
              <span>Technical validation only · not Human or legal approval</span>
            </div>
            <p className="card-supporting-copy">
              This confirms technical structure and required fields only. It is not Human or legal approval.
            </p>
            <button className="primary-button" onClick={() => onPhaseChange("export")} type="button">
              Continue to DOCX Export →
            </button>
          </>
        ) : validating ? (
          <div className="processing-callout workspace-operation" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>Validating {revision.id}…</strong>
              <p>The selected revision is preserved and duplicate validation requests are blocked.</p>
            </div>
          </div>
        ) : (
          <button
            className="primary-button"
            disabled={!reviewComplete || editing || busy}
            onClick={() => void handleValidate()}
            type="button"
          >
            Validate {revision.id}
          </button>
        )}

        {validationError && (
          <section className="error-banner" role="alert" aria-labelledby="draft-validation-error">
            <div>
              <h3 id="draft-validation-error" ref={errorHeadingRef} tabIndex={-1}>Draft validation failed · {validationError.code}</h3>
              <p>{validationError.message}</p>
              {validationError.paths?.length && <p>Fields: {validationError.paths.join(", ")}</p>}
              {validationError.correlation_id && <p>Reference ID: <code>{validationError.correlation_id}</code></p>}
              <p>The saved revision remains available for correction.</p>
            </div>
            <button className="secondary-button" onClick={() => { beginEdit(); onPhaseChange("review"); }} type="button">
              Edit this revision
            </button>
          </section>
        )}

        <div className="stage-secondary-actions">
          <button className="text-button" onClick={() => onPhaseChange("review")} type="button">Return to Review &amp; Refine</button>
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
        <p className="eyebrow">DOCX Export</p>
        <h2 id="export-heading">Validation complete</h2>
        <p>Structure and required fields passed server validation for <strong>{revision.id}</strong>. The output remains a draft requiring expert review.</p>
        <div className="export-summary">
          <span>Selected revision</span>
          <strong>{revision.id}</strong>
          <span className="status-success">Exact-revision validation passed</span>
        </div>
        <button
          aria-label={`Export ${revision.id} DOCX`}
          className="primary-button export-primary-button"
          disabled={busy || editing || !revision.validation}
          onClick={handleExport}
          type="button"
        >
          {state === "EXPORTING" ? "Preparing DOCX…" : "Download editable DOCX"}
        </button>
        {state === "EXPORTING" && (
          <div className="processing-callout workspace-operation" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>Preparing {revision.id} for DOCX download…</strong>
              <p>Keep this page open. Another export cannot start until this request finishes.</p>
            </div>
          </div>
        )}
        <div className="stage-secondary-actions">
          <button className="text-button" onClick={() => onPhaseChange("validate")} type="button">Review validation</button>
          {renderNewPaperAction()}
        </div>
        {renderTechnicalDetails(<p>Validated digest: <code>{revision.validation?.draft_digest}</code></p>)}
      </section>
    );
  }

  return (
    <section aria-busy={busy} className="results-workspace" aria-labelledby="results-heading">
      <div className="results-toolbar">
        <div>
          <p className="eyebrow">Review &amp; Refine</p>
          <h2 id="results-heading">Review &amp; Refine</h2>
          <p>Review the generated patent draft, refine prose, and inspect supporting evidence before validation.</p>
        </div>
        {renderNewPaperAction()}
      </div>

      <div className="revision-workspace" aria-label="Session draft revisions">
        {renderRevisionSelector(false)}
        <div className="revision-actions">
          {editing ? (
            <>
              <button className="primary-button" disabled={!dirty} onClick={saveEdit} type="button">Save new revision</button>
              <button className="secondary-button" onClick={cancelEdit} type="button">Cancel edit</button>
            </>
          ) : (
            <>
              <button className="secondary-button" disabled={busy} onClick={beginEdit} type="button">Edit prose</button>
              <button
                aria-label={`Continue ${revision.id} to Validation`}
                className="primary-button"
                disabled={busy || !reviewComplete}
                onClick={() => onPhaseChange("validate")}
                type="button"
              >
                Continue to Validation →
              </button>
            </>
          )}
        </div>
      </div>

      <div className="revision-status" role="status" aria-live="polite">
        <strong>{revision.id}{editing ? (dirty ? " · Unsaved changes" : " · Editing") : " · Saved"}</strong>
        <span>Backend validation: {revision.validation ? "PASSED for this exact revision" : "NOT VALIDATED"}</span>
        <span>Review: {reviewCounts.UNREVIEWED} UNREVIEWED · {reviewCounts.REVIEWED} REVIEWED (not approved) · {reviewCounts.NEEDS_CHANGES} NEEDS_CHANGES</span>
        <span>
          {reviewComplete
            ? "Human review complete for this selected revision."
            : `Review all sections before validation · ${reviewRemaining} remaining.`}
        </span>
        <span>Export target: {revision.id}{revision.validation && reviewComplete ? " · eligible" : " · review and validation required"}</span>
      </div>

      {unverifiedPaths.length > 0 && (
        <p className="edit-support-warning" role="note">
          {unverifiedPaths.length} edited prose field(s) have unchanged evidence links, but semantic source support is unverified. Technical validation is not Human or legal approval.
        </p>
      )}

      <div className="tab-list" role="tablist" aria-label="Result views">
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
            review={revision.review}
            unverifiedPaths={unverifiedPaths}
          />
        )}
        {activeTab === "review" && <ReviewItemsView analysis={result.analysis} draft={revision.draft} />}
        {activeTab === "analysis" && <AnalysisView analysis={result.analysis} />}
      </div>

      {renderTechnicalDetails()}
    </section>
  );
}
