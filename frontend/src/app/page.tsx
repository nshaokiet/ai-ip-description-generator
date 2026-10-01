"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";

import { ResultWorkspace } from "@/components/ResultWorkspace";
import { UploadPanel } from "@/components/UploadPanel";
import { WorkflowProgress } from "@/components/WorkflowProgress";
import {
  ApiClientError,
  exportDocx,
  processDocument,
  uploadDocument,
} from "@/lib/api/client";
import type {
  NormalizedApiError,
  ExportDocxRequest,
  ProcessResult,
  UploadedDocument,
  WorkflowPhase,
  WorkflowState,
} from "@/lib/types/contracts";

function normalizeClientError(error: unknown): NormalizedApiError {
  if (error instanceof ApiClientError) return error;
  return {
    status: 0,
    code: "unexpected_client_error",
    message: "The operation could not be completed safely.",
  };
}

export default function Home() {
  const [state, setState] = useState<WorkflowState>("IDLE");
  const [document, setDocument] = useState<UploadedDocument | null>(null);
  const [result, setResult] = useState<ProcessResult | null>(null);
  const [error, setError] = useState<NormalizedApiError | null>(null);
  const [recoveryState, setRecoveryState] = useState<WorkflowState>("IDLE");
  const [workflowPhase, setWorkflowPhase] = useState<WorkflowPhase>("upload");
  const operationRef = useRef<"upload" | "process" | "export" | null>(null);
  const errorHeadingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    if (!error) return;
    const frame = window.requestAnimationFrame(() => errorHeadingRef.current?.focus());
    return () => window.cancelAnimationFrame(frame);
  }, [error]);

  function reset() {
    setState("IDLE");
    setDocument(null);
    setResult(null);
    setError(null);
    setRecoveryState("IDLE");
    setWorkflowPhase("upload");
  }

  function showError(issue: unknown, recoverTo: WorkflowState) {
    setError(normalizeClientError(issue));
    setRecoveryState(recoverTo);
    setState("ERROR");
  }

  async function handleUpload(file: File) {
    if (operationRef.current) return;
    operationRef.current = "upload";
    setError(null);
    setWorkflowPhase("upload");
    setState("UPLOADING");
    try {
      const uploaded = await uploadDocument(file);
      setDocument(uploaded);
      setWorkflowPhase("analyze");
      setState("UPLOADED");
    } catch (issue) {
      showError(issue, "IDLE");
    } finally {
      if (operationRef.current === "upload") operationRef.current = null;
    }
  }

  async function handleProcess() {
    if (!document || operationRef.current) return;
    operationRef.current = "process";
    setError(null);
    setWorkflowPhase("analyze");
    setState("PROCESSING");
    try {
      const processed = await processDocument(document.document_id);
      setResult(processed);
      setWorkflowPhase("review");
      setState("READY");
    } catch (issue) {
      // APP-003 may have removed the source once processing began. A new upload is required.
      setDocument(null);
      setWorkflowPhase("upload");
      showError(issue, "IDLE");
    } finally {
      if (operationRef.current === "process") operationRef.current = null;
    }
  }

  async function handleExport(requestBody: ExportDocxRequest) {
    if (!result || operationRef.current) return;
    operationRef.current = "export";
    setError(null);
    setWorkflowPhase("export");
    setState("EXPORTING");
    try {
      const exported = await exportDocx(requestBody);
      const objectUrl = URL.createObjectURL(exported.blob);
      const anchor = window.document.createElement("a");
      anchor.href = objectUrl;
      anchor.download = exported.filename;
      window.document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 0);
      setState("READY");
    } catch (issue) {
      showError(issue, "READY");
    } finally {
      if (operationRef.current === "export") operationRef.current = null;
    }
  }

  function dismissError() {
    setError(null);
    setState(recoveryState);
  }

  const statusMessage =
    state === "UPLOADING"
      ? "Uploading and validating the document."
      : state === "PROCESSING"
        ? "Analyzing the document and generating the patent draft."
        : state === "EXPORTING"
          ? "Preparing the editable DOCX download."
          : state === "READY"
            ? "Analysis and patent draft are ready for human review."
            : "";

  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="header-inner">
          <div className="brand-group">
            <Image
              alt="VNUHCM Innovation Hub"
              className="brand-logo"
              height={72}
              priority
              src="/brand/vnuhcm-innovation-hub-logo.png"
              width={128}
            />
            <div className="brand-divider" aria-hidden="true" />
            <div>
              <p className="brand-kicker">VNUHCM Innovation Hub</p>
              <p className="product-name">AI IP Description Generator</p>
            </div>
          </div>
          <div className="environment-badge">
            <span aria-hidden="true" />
            Local MVP
          </div>
        </div>
      </header>

      <main>
        <section className="hero" aria-labelledby="page-title">
          <div>
            <p className="eyebrow">Grounded invention documentation</p>
            <h1 id="page-title">From research document to reviewable patent draft</h1>
            <p>
              Upload one supported document, run the local evidence-grounded pipeline,
              inspect every review item, and export an editable DOCX.
            </p>
          </div>
          <aside className="hero-notice" aria-label="Important use notice">
            <strong>Human review required</strong>
            <p>AI-generated draft for human review. Not legal advice and not filing-ready.</p>
          </aside>
        </section>

        <WorkflowProgress phase={workflowPhase} />

        <p className="sr-only" aria-live="polite" aria-atomic="true">
          {statusMessage}
        </p>

        {error && (
          <section className="error-banner" role="alert" aria-labelledby="error-heading">
            <div>
              <p className="eyebrow">Request not completed · {error.code}</p>
              <h2 id="error-heading" ref={errorHeadingRef} tabIndex={-1}>We could not complete that operation</h2>
              <p>{error.message}</p>
              {error.correlation_id && (
                <p className="reference-id">Reference ID: <code>{error.correlation_id}</code></p>
              )}
            </div>
            <button className="secondary-button" onClick={dismissError} type="button">
              {recoveryState === "READY" ? "Return to results" : "Choose another document"}
            </button>
          </section>
        )}

        {!result ? (
          <UploadPanel
            document={document}
            onProcess={handleProcess}
            onUpload={handleUpload}
            state={state}
          />
        ) : (
          <ResultWorkspace
            onExport={handleExport}
            onProgressChange={setWorkflowPhase}
            onReset={reset}
            result={result}
            state={state}
          />
        )}
      </main>

      <footer className="site-footer">
        <div>
          <strong>AI-generated draft for human review.</strong>
          <span>Not legal advice and not filing-ready.</span>
        </div>
        <p>Local single-tenant MVP · Session data is not persisted by this frontend.</p>
      </footer>
    </div>
  );
}
