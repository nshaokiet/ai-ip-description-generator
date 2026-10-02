"use client";

import { useRef, useState, type ChangeEvent, type DragEvent } from "react";

import type { DemoSampleId } from "@/lib/api/client";
import type { UploadedDocument, WorkflowState } from "@/lib/types/contracts";

const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED_EXTENSIONS = [".pdf", ".docx"];

function validateFile(file: File): string | null {
  const lowerName = file.name.toLowerCase();
  if (!ALLOWED_EXTENSIONS.some((extension) => lowerName.endsWith(extension))) {
    return "Choose one PDF or DOCX document.";
  }
  if (file.size > MAX_BYTES) return "The selected file exceeds the 10 MiB limit.";
  if (file.size === 0) return "The selected file is empty.";
  return null;
}

function formatBytes(value: number): string {
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KiB`;
  return `${(value / (1024 * 1024)).toFixed(2)} MiB`;
}

function fileKind(document: UploadedDocument): string {
  return document.original_filename.toLowerCase().endsWith(".pdf") ? "PDF" : "DOCX";
}

interface UploadPanelProps {
  state: WorkflowState;
  document: UploadedDocument | null;
  hasDownstreamResults: boolean;
  onUpload: (file: File) => Promise<void>;
  onReplace: (file: File) => Promise<void>;
  onRemove: () => void;
  onReset: () => void;
  onProcess: () => Promise<void>;
  onContinueReview: () => void;
  demoStaging?: boolean;
  onUseDemoSample?: (sampleId: DemoSampleId) => Promise<void>;
}

export function UploadPanel({
  state,
  document,
  hasDownstreamResults,
  onUpload,
  onReplace,
  onRemove,
  onReset,
  onProcess,
  onContinueReview,
  demoStaging = false,
  onUseDemoSample,
}: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const replaceInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [localError, setLocalError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [confirmAction, setConfirmAction] = useState<"remove" | "replace" | null>(null);
  const busy = state === "UPLOADING" || state === "PROCESSING";

  function chooseFile(file: File | undefined) {
    if (!file) return;
    const issue = validateFile(file);
    setLocalError(issue);
    setSelectedFile(issue ? null : file);
  }

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    chooseFile(event.target.files?.[0]);
  }

  async function handleReplacement(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    const issue = validateFile(file);
    if (issue) {
      setLocalError(issue);
      return;
    }
    await onReplace(file);
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragActive(false);
    if (busy) return;
    if (event.dataTransfer.files.length !== 1) {
      setSelectedFile(null);
      setLocalError("Choose exactly one document.");
      return;
    }
    chooseFile(event.dataTransfer.files[0]);
  }

  function requestRemove() {
    if (hasDownstreamResults) setConfirmAction("remove");
    else onRemove();
  }

  function requestReplace() {
    if (hasDownstreamResults) setConfirmAction("replace");
    else if (demoStaging) onRemove();
    else replaceInputRef.current?.click();
  }

  if (document) {
    return (
      <section aria-busy={busy} className="workspace-card upload-success-card" aria-labelledby="validated-document-heading">
        <span className="document-symbol document-symbol-success" aria-hidden="true">✓</span>
        <p className="eyebrow">Source Upload</p>
        <h2 id="validated-document-heading">Paper uploaded successfully</h2>
        <p className="card-supporting-copy">Your source is ready for the next workflow stage.</p>

        <div className="uploaded-file-row">
          <span className="file-type-icon" aria-hidden="true">{fileKind(document)}</span>
          <div className="uploaded-file-copy">
            <strong>{document.original_filename}</strong>
            <span>{fileKind(document)} · {formatBytes(document.size_bytes)}{document.page_count != null ? ` · ${document.page_count} pages` : ""}</span>
          </div>
          <button
            aria-label="Remove paper"
            className="icon-button danger-icon-button"
            disabled={busy}
            onClick={requestRemove}
            title="Remove paper"
            type="button"
          >
            <span aria-hidden="true">×</span>
          </button>
        </div>

        {!demoStaging && (
          <input
            accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            className="sr-only"
            id="replacement-document-file"
            onChange={(event) => void handleReplacement(event)}
            ref={replaceInputRef}
            type="file"
          />
        )}

        {confirmAction && (
          <div className="reset-confirmation" role="alert">
            <strong>Start over with a new paper?</strong>
            <p>Current analysis, draft revisions, review status, and validation will be cleared from this browser session.</p>
            <div>
              <button
                className="danger-button"
                onClick={() => {
                  const action = confirmAction;
                  setConfirmAction(null);
                  onReset();
                  if (action === "replace") window.requestAnimationFrame(() => inputRef.current?.click());
                }}
                type="button"
              >
                Clear session and start over
              </button>
              <button className="secondary-button" onClick={() => setConfirmAction(null)} type="button">Keep current paper</button>
            </div>
          </div>
        )}

        <div className="upload-success-actions">
          <button
            aria-label={hasDownstreamResults ? "Continue to Review & Refine" : "Continue to AI Extraction"}
            className="primary-button"
            disabled={busy || (!hasDownstreamResults && state !== "UPLOADED")}
            onClick={() => hasDownstreamResults ? onContinueReview() : void onProcess()}
            type="button"
          >
            {state === "PROCESSING" ? "Extracting…" : hasDownstreamResults ? "Continue to Review & Refine →" : "Continue to AI Extraction →"}
          </button>
          <button className="text-button" disabled={busy} onClick={requestReplace} type="button">
            {demoStaging ? "Select a different sample" : "Select a different file"}
          </button>
        </div>

        {state === "PROCESSING" && (
          <div className="processing-callout" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>Extracting invention-relevant content</strong>
              <p>Identifying technical concepts and preparing a grounded draft for review.</p>
            </div>
          </div>
        )}

        <details className="technical-details">
          <summary>Technical details</summary>
          <dl>
            <div><dt>Media type</dt><dd>{document.media_type}</dd></div>
            <div><dt>Document ID</dt><dd><code>{document.document_id}</code></dd></div>
          </dl>
        </details>
      </section>
    );
  }

  return (
    <section aria-busy={busy} className="workspace-card upload-card" aria-labelledby="upload-heading">
      <h2 className="sr-only" id="upload-heading">Upload a research document</h2>

      {demoStaging ? (
        <div className="demo-upload-state">
          <span className="document-symbol" aria-hidden="true">▤</span>
          <h3>Choose a controlled synthetic sample</h3>
          <p className="demo-boundary-note">Public demo: synthetic samples only. Do not use real, confidential, unpublished, or sensitive research. No live AI provider is used.</p>
          <div className="sample-actions" aria-label="Synthetic sample papers">
            <span>Thử nhanh bài báo mẫu:</span>
            <button
              aria-label="Use synthetic PDF demo"
              className="sample-link"
              disabled={busy}
              onClick={() => void onUseDemoSample?.("synthetic-pdf-v1")}
              type="button"
            >
              Sample PDF (.pdf)
            </button>
            <span aria-hidden="true">|</span>
            <button
              aria-label="Use synthetic DOCX demo"
              className="sample-link"
              disabled={busy}
              onClick={() => void onUseDemoSample?.("synthetic-docx-v1")}
              type="button"
            >
              Sample DOCX (.docx)
            </button>
          </div>
        </div>
      ) : (
        <>
          <div
            className={`drop-zone ${dragActive ? "drop-zone-active" : ""}`}
            onDragEnter={(event) => { event.preventDefault(); setDragActive(true); }}
            onDragOver={(event) => event.preventDefault()}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
          >
            <span className="document-symbol" aria-hidden="true">▤</span>
            <h3>Drag &amp; drop your research paper here</h3>
            <p>or</p>
            <label className="sr-only" htmlFor="document-file">Research document</label>
            <input
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              className="sr-only"
              id="document-file"
              disabled={busy}
              onChange={handleChange}
              ref={inputRef}
              type="file"
            />
            <button
              aria-label="Select document"
              className="primary-button select-file-button"
              disabled={busy}
              onClick={() => inputRef.current?.click()}
              type="button"
            >
              Select file
            </button>
            <span className="upload-constraints">PDF or DOCX · Max 10 MB</span>
          </div>
        </>
      )}

      {selectedFile && (
        <div className="selected-file" aria-live="polite">
          <div>
            <strong>{selectedFile.name}</strong>
            <span>{formatBytes(selectedFile.size)}</span>
          </div>
          <button
            className="primary-button"
            disabled={busy}
            onClick={() => void onUpload(selectedFile)}
            type="button"
          >
            {state === "UPLOADING" ? "Uploading…" : "Upload & Validate"}
          </button>
        </div>
      )}
      {state === "UPLOADING" && (
        <div className="processing-callout" role="status" aria-live="polite">
          <span className="spinner" aria-hidden="true" />
          <div>
            <strong>Uploading and checking the selected document…</strong>
            <p>Another upload cannot start until this request finishes.</p>
          </div>
        </div>
      )}
      {localError && <p className="field-error" role="alert">{localError}</p>}
      {!demoStaging && <p className="privacy-note"><span aria-hidden="true">⌁</span> Tài liệu được xử lý trong phạm vi phiên làm việc.</p>}
      <p className="source-of-truth-note">
        {demoStaging
          ? "The backend verifies the exact approved sample before accepting it."
          : "Client checks are for convenience. The backend remains the validation source of truth."}
      </p>
    </section>
  );
}
