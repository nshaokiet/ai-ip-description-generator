"use client";

import { useEffect, useRef, useState, type ChangeEvent, type DragEvent, type KeyboardEvent } from "react";
import { createPortal } from "react-dom";

import { useUi, type MessageKey } from "@/lib/uiPreferences";
import type { DemoSampleId } from "@/lib/api/client";
import type { UploadedDocument, WorkflowState } from "@/lib/types/contracts";

const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED_EXTENSIONS = [".pdf", ".docx"];

function validateFile(file: File): MessageKey | null {
  const lowerName = file.name.toLowerCase();
  if (!ALLOWED_EXTENSIONS.some((extension) => lowerName.endsWith(extension))) {
    return "unsupportedFile";
  }
  if (file.size > MAX_BYTES) return "tooLarge";
  if (file.size === 0) return "emptyFile";
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
  const { t } = useUi();
  const inputRef = useRef<HTMLInputElement>(null);
  const confirmDialogRef = useRef<HTMLDivElement>(null);
  const confirmTriggerRef = useRef<HTMLElement | null>(null);
  const replaceInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [localError, setLocalError] = useState<MessageKey | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [confirmAction, setConfirmAction] = useState<"remove" | "replace" | null>(null);
  const [pendingReplacement, setPendingReplacement] = useState<File | null>(null);
  const busy = state === "UPLOADING" || state === "PROCESSING";
  useEffect(() => {
    if (!confirmAction) return;
    const trigger = confirmTriggerRef.current;
    const previousOverflow = window.document.body.style.overflow;
    const shell = window.document.querySelector<HTMLElement>(".app-shell");
    if (shell) shell.inert = true;
    window.document.body.style.overflow = "hidden";
    const frame = requestAnimationFrame(() => confirmDialogRef.current?.querySelector("button")?.focus());
    return () => { cancelAnimationFrame(frame); window.document.body.style.overflow = previousOverflow; if (shell) shell.inert = false; trigger?.focus(); };
  }, [confirmAction]);
  function dismissConfirmation() { setConfirmAction(null); setPendingReplacement(null); }
  function dialogKeys(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") { event.preventDefault(); dismissConfirmation(); return; }
    if (event.key !== "Tab") return;
    const buttons = Array.from(confirmDialogRef.current?.querySelectorAll<HTMLButtonElement>("button:not(:disabled)") ?? []);
    if (!buttons.length) return;
    const first = buttons[0], last = buttons[buttons.length - 1];
    if (event.shiftKey && window.document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && window.document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
  function requestConfirmation(action: "remove" | "replace") {
    confirmTriggerRef.current = window.document.activeElement instanceof HTMLElement ? window.document.activeElement : null;
    setConfirmAction(action);
  }

  function chooseFile(file: File | undefined) {
    if (!file) return;
    const issue = validateFile(file);
    setLocalError(issue);
    setSelectedFile(issue ? null : file);
  }

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    chooseFile(event.target.files?.[0]);
  }

  function clearSelectedFile() {
    setSelectedFile(null);
    setLocalError(null);
    if (inputRef.current) inputRef.current.value = "";
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
    if (hasDownstreamResults) {
      setPendingReplacement(file);
      requestConfirmation("replace");
    } else {
      await onReplace(file);
    }
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragActive(false);
    if (busy) return;
    if (event.dataTransfer.files.length !== 1) {
      setSelectedFile(null);
      setLocalError("oneFile");
      return;
    }
    chooseFile(event.dataTransfer.files[0]);
  }

  function requestRemove() {
    if (hasDownstreamResults) requestConfirmation("remove");
    else onRemove();
  }

  function requestReplace() {
    if (demoStaging) {
      if (hasDownstreamResults) requestConfirmation("replace");
      else onRemove();
    } else replaceInputRef.current?.click();
  }

  if (document) {
    return (
      <section aria-busy={busy} className="workspace-card upload-success-card" aria-labelledby="validated-document-heading">
        <span className="document-symbol document-symbol-success" aria-hidden="true">✓</span>
        <p className="eyebrow">{t("upload")}</p>
        <h2 id="validated-document-heading">{t("uploadedTitle")}</h2>
        <p className="card-supporting-copy">{t("uploadedDescription")}</p>

        <div className="uploaded-file-row">
          <span className="file-type-icon" aria-hidden="true">{fileKind(document)}</span>
          <div className="uploaded-file-copy">
            <strong>{document.original_filename}</strong>
            <span>{fileKind(document)} · {formatBytes(document.size_bytes)}{document.page_count != null ? ` · ${document.page_count} pages` : ""}</span>
          </div>
          <button
            aria-label={t("remove")}
            className="icon-button danger-icon-button"
            disabled={busy}
            onClick={requestRemove}
            title={t("remove")}
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

        {confirmAction && createPortal(
          <div className="dialog-backdrop">
            <div ref={confirmDialogRef} className="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="upload-confirm-title" aria-describedby="upload-confirm-description" onKeyDown={dialogKeys}>
              <h3 id="upload-confirm-title">{t("confirmTitle")}</h3>
              <p id="upload-confirm-description">{t("resetSourceDescription")}</p>
              <div className="dialog-actions">
                <button className="danger-button" onClick={() => {
                  const action = confirmAction;
                  setConfirmAction(null);
                  const replacement = pendingReplacement;
                  setPendingReplacement(null);
                  if (action === "replace" && replacement) void onReplace(replacement);
                  else onReset();
                }} type="button">{t("fileReset")}</button>
                <button className="secondary-button" onClick={dismissConfirmation} type="button">{t("stay")}</button>
              </div>
            </div>
          </div>
        , window.document.body)}

        <div className="upload-success-actions">
          <button
            aria-label={hasDownstreamResults ? t("continueReview") : t("continueExtraction")}
            className="primary-button"
            disabled={busy || (!hasDownstreamResults && state !== "UPLOADED")}
            onClick={() => hasDownstreamResults ? onContinueReview() : void onProcess()}
            type="button"
          >
            {state === "PROCESSING" ? t("processing") : hasDownstreamResults ? t("continueReview") : t("continueExtraction")}
          </button>
          <button className="text-button" disabled={busy} onClick={requestReplace} type="button">
            {demoStaging ? (t("anotherSample")) : t("fileReplace")}
          </button>
        </div>

        {state === "PROCESSING" && (
          <div className="processing-callout" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true" />
            <div>
              <strong>{t("extractTitle")}</strong>
              <p>{t("extractHelp")}</p>
            </div>
          </div>
        )}

        <details className="technical-details">
          <summary>{t("details")}</summary>
          <dl>
            <div><dt>{t("mediaType")}</dt><dd>{document.media_type}</dd></div>
            <div><dt>{t("documentId")}</dt><dd><code>{document.document_id}</code></dd></div>
          </dl>
        </details>
      </section>
    );
  }

  return (
    <section aria-busy={busy} className="workspace-card upload-card" aria-labelledby="upload-heading">
      <h2 className="sr-only" id="upload-heading">{t("uploadTitle")}</h2>

      <div
        className={`drop-zone ${dragActive ? "drop-zone-active" : ""}`}
        onDragEnter={(event) => { event.preventDefault(); setDragActive(true); }}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <span className="document-symbol" aria-hidden="true">▤</span>
        <h3>{t("dragDrop")}</h3>
        <p>{t("or")}</p>
        <label className="sr-only" htmlFor="document-file">{t("uploadTitle")}</label>
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
          aria-label={t("selectFile")}
          className="primary-button select-file-button"
          disabled={busy}
          onClick={() => inputRef.current?.click()}
          type="button"
        >
          {t("selectFile")}
        </button>
        <span className="upload-constraints">{t("fileConstraints")}</span>
      </div>

      {demoStaging && (
        <div className="demo-upload-state">
          <div className="sample-actions" aria-label={t("sample")}>
            <span>{t("sample")}</span>
            <button
              aria-label={t("samplePdf")}
              className="sample-link"
              disabled={busy}
              onClick={() => void onUseDemoSample?.("synthetic-pdf-v1")}
              type="button"
            >
              {t("samplePdfLabel")}
            </button>
            <span aria-hidden="true">|</span>
            <button
              aria-label={t("sampleDocx")}
              className="sample-link"
              disabled={busy}
              onClick={() => void onUseDemoSample?.("synthetic-docx-v1")}
              type="button"
            >
              {t("sampleDocxLabel")}
            </button>
          </div>
          <p className="demo-boundary-note">
            {t("demo")}
          </p>
        </div>
      )}

      {selectedFile && (
        <div className="selected-file" aria-live="polite">
          <div className="selected-file-details">
            <strong>{selectedFile.name}</strong>
            <span>{formatBytes(selectedFile.size)}</span>
          </div>
          {demoStaging ? (
            <span className="upload-ui-only-note">{t("localDemoFile")}</span>
          ) : (
            <button
              className="primary-button selected-file-action"
              disabled={busy}
              onClick={() => void onUpload(selectedFile)}
              type="button"
            >
              {state === "UPLOADING" ? t("processing") : t("uploadValidate")}
            </button>
          )}
          <button
            aria-label={t("remove")}
            className="icon-button danger-icon-button selected-file-remove"
            disabled={busy}
            onClick={clearSelectedFile}
            title={t("remove")}
            type="button"
          >
            <span aria-hidden="true">×</span>
          </button>
        </div>
      )}
      {state === "UPLOADING" && (
        <div className="processing-callout" role="status" aria-live="polite">
          <span className="spinner" aria-hidden="true" />
          <div>
            <strong>{t("uploadBusyTitle")}</strong>
            <p>{t("uploadBusyHelp")}</p>
          </div>
        </div>
      )}
      {localError && <p className="field-error" role="alert">{t(localError)}</p>}
      {!demoStaging && <p className="privacy-note"><span aria-hidden="true">⌁</span> {t("sessionScope")}</p>}
      <p className="source-of-truth-note">
        {demoStaging
          ? t("demo")
          : (t("serverAuthority"))}
      </p>
    </section>
  );
}
