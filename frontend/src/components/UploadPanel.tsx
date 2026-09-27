"use client";

import { useRef, useState, type ChangeEvent, type DragEvent } from "react";

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

interface UploadPanelProps {
  state: WorkflowState;
  document: UploadedDocument | null;
  onUpload: (file: File) => Promise<void>;
  onProcess: () => Promise<void>;
}

export function UploadPanel({ state, document, onUpload, onProcess }: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [localError, setLocalError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
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

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragActive(false);
    if (event.dataTransfer.files.length !== 1) {
      setSelectedFile(null);
      setLocalError("Choose exactly one document.");
      return;
    }
    chooseFile(event.dataTransfer.files[0]);
  }

  if (document) {
    return (
      <section className="workspace-card" aria-labelledby="validated-document-heading">
        <div className="workspace-card-header">
          <div>
            <p className="eyebrow">Validated document</p>
            <h2 id="validated-document-heading">Ready for analysis</h2>
          </div>
          <span className="validation-badge">Validated</span>
        </div>
        <dl className="metadata-grid">
          <div><dt>File</dt><dd>{document.original_filename}</dd></div>
          <div><dt>Type</dt><dd>{document.media_type}</dd></div>
          <div><dt>Size</dt><dd>{formatBytes(document.size_bytes)}</dd></div>
          {document.page_count != null && (
            <div><dt>Pages</dt><dd>{document.page_count}</dd></div>
          )}
          <div className="metadata-wide">
            <dt>Document ID</dt>
            <dd><code>{document.document_id}</code></dd>
          </div>
        </dl>
        <div className="action-panel">
          <div>
            <h3>Analyze &amp; Generate Draft</h3>
            <p>
              Runs the synchronous local pipeline. The source is removed when processing
              completes or fails, according to the approved cleanup policy.
            </p>
          </div>
          <button
            className="primary-button"
            disabled={busy || state !== "UPLOADED"}
            onClick={() => void onProcess()}
            type="button"
          >
            {state === "PROCESSING" ? "Processing…" : "Analyze & Generate Draft"}
          </button>
        </div>
        {state === "PROCESSING" && (
          <div className="processing-callout" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>Analyzing the document and generating the patent draft…</strong>
              <p>This synchronous operation may take time. Please keep this page open.</p>
            </div>
          </div>
        )}
      </section>
    );
  }

  return (
    <section className="workspace-card" aria-labelledby="upload-heading">
      <div className="workspace-card-header">
        <div>
          <p className="eyebrow">Step 1</p>
          <h2 id="upload-heading">Upload a research document</h2>
        </div>
        <span className="file-limit">PDF or DOCX · 10 MiB max</span>
      </div>
      <div
        className={`drop-zone ${dragActive ? "drop-zone-active" : ""}`}
        onDragEnter={(event) => { event.preventDefault(); setDragActive(true); }}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <div className="upload-symbol" aria-hidden="true">↑</div>
        <h3>Choose a document or drop it here</h3>
        <p>One text-based PDF or DOCX. Scanned PDF and OCR are not supported.</p>
        <label className="sr-only" htmlFor="document-file">Research document</label>
        <input
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          className="sr-only"
          id="document-file"
          onChange={handleChange}
          ref={inputRef}
          type="file"
        />
        <button
          className="secondary-button"
          disabled={busy}
          onClick={() => inputRef.current?.click()}
          type="button"
        >
          Select document
        </button>
      </div>
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
      {localError && <p className="field-error" role="alert">{localError}</p>}
      <p className="source-of-truth-note">
        Client checks are for convenience. The backend remains the validation source of truth.
      </p>
    </section>
  );
}
