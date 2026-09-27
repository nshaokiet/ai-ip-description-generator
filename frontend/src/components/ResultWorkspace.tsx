"use client";

import { useRef, useState } from "react";

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
  WorkflowState,
} from "@/lib/types/contracts";

type ResultTab = "analysis" | "draft" | "review";

interface ResultWorkspaceProps {
  result: ProcessResult;
  state: WorkflowState;
  onExport: (request: ExportDocxRequest) => Promise<void>;
  onReset: () => void;
}

function safeValidationError(issue: unknown): NormalizedApiError {
  if (issue instanceof ApiClientError) return issue;
  return { status: 0, code: "unexpected_client_error", message: "Validation could not be completed safely." };
}

export function ResultWorkspace({ result, state, onExport, onReset }: ResultWorkspaceProps) {
  const [activeTab, setActiveTab] = useState<ResultTab>("analysis");
  const [session, setSession] = useState(() => createDraftSession(result.draft));
  const [editBuffer, setEditBuffer] = useState<PatentDraft | null>(null);
  const [validating, setValidating] = useState(false);
  const [validationError, setValidationError] = useState<NormalizedApiError | null>(null);
  const errorHeadingRef = useRef<HTMLHeadingElement>(null);
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
  const tabs: Array<{ key: ResultTab; label: string }> = [
    { key: "analysis", label: "Analysis" },
    { key: "draft", label: "Patent Draft" },
    { key: "review", label: "Review Items" },
  ];

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
    if (editing || busy) return;
    setValidationError(null);
    setValidating(true);
    try {
      const validation = await validateDraft(requestBody);
      if (!validation.valid || validation.revision_id !== revision.id) {
        throw new Error("Validation response does not match the selected revision.");
      }
      setSession((current) => setRevisionValidation(current, revision.id, validation));
    } catch (issue) {
      setSession((current) => setRevisionValidation(current, revision.id, null));
      setValidationError(safeValidationError(issue));
      setActiveTab("draft");
      window.requestAnimationFrame(() => errorHeadingRef.current?.focus());
    } finally {
      setValidating(false);
    }
  }

  function handleReviewChange(sectionId: string, status: ReviewStatus) {
    setSession((current) => setReviewStatus(current, sectionId, status));
  }

  function handleExport() {
    if (editing || busy || !revision.validation) return;
    void onExport({ ...requestBody, validated_digest: revision.validation.draft_digest });
  }

  return (
    <section className="results-workspace" aria-labelledby="results-heading">
      <div className="results-toolbar">
        <div>
          <p className="eyebrow">Processing complete</p>
          <h2 id="results-heading">Grounded draft workspace</h2>
          <p className="metadata-line">Reference ID: <code>{result.metadata.correlation_id}</code></p>
        </div>
        <div className="toolbar-actions">
          <button className="secondary-button" disabled={busy} onClick={onReset} type="button">New Document</button>
          <button className="primary-button" disabled={busy || editing || !revision.validation} onClick={handleExport} type="button">
            {state === "EXPORTING" ? "Preparing DOCX…" : `Export ${revision.id} DOCX`}
          </button>
        </div>
      </div>

      <div className="revision-workspace" aria-label="Session draft revisions">
        <div>
          <label htmlFor="revision-select">Selected revision</label>
          <select
            disabled={busy || editing}
            id="revision-select"
            onChange={(event) => { setSession((current) => ({ ...current, selectedId: event.target.value })); setValidationError(null); }}
            value={session.selectedId}
          >
            {session.revisions.map((item, index) => (
              <option key={item.id} value={item.id}>{item.id}{index === 0 ? " · generated" : " · edited"}</option>
            ))}
          </select>
          <p className="metadata-line">{session.revisions.length} immutable session revision(s). Reload or reset discards edits, validation and review status.</p>
        </div>
        <div className="revision-actions">
          {editing ? (
            <>
              <button className="primary-button" disabled={!dirty} onClick={saveEdit} type="button">Save new revision</button>
              <button className="secondary-button" onClick={cancelEdit} type="button">Cancel edit</button>
            </>
          ) : (
            <>
              <button className="secondary-button" disabled={busy} onClick={beginEdit} type="button">Edit prose</button>
              <button className="secondary-button" disabled={busy} onClick={() => void handleValidate()} type="button">
                {validating ? "Validating…" : `Validate ${revision.id}`}
              </button>
            </>
          )}
        </div>
      </div>

      <div className="revision-status" role="status" aria-live="polite">
        <strong>{revision.id}{editing ? (dirty ? " · Unsaved changes" : " · Editing") : " · Saved"}</strong>
        <span>Backend validation: {revision.validation ? "PASSED for this exact revision" : "NOT VALIDATED"}</span>
        <span>Review: {reviewCounts.UNREVIEWED} UNREVIEWED · {reviewCounts.REVIEWED} REVIEWED (not approved) · {reviewCounts.NEEDS_CHANGES} NEEDS_CHANGES</span>
        <span>Export target: {revision.id}{revision.validation ? " · eligible after server revalidation" : " · validation required"}</span>
      </div>

      {unverifiedPaths.length > 0 && (
        <p className="edit-support-warning" role="note">
          {unverifiedPaths.length} edited prose field(s) have unchanged evidence links, but semantic source support is unverified. Technical validation is not Human or legal approval.
        </p>
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
        </section>
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
            onClick={() => setActiveTab(tab.key)}
            role="tab"
            type="button"
          >{tab.label}</button>
        ))}
      </div>

      <div aria-labelledby={`tab-${activeTab}`} className="tab-panel" id={`panel-${activeTab}`} role="tabpanel">
        {activeTab === "analysis" && <AnalysisView analysis={result.analysis} />}
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
      </div>
    </section>
  );
}
