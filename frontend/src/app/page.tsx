"use client";

import Image from "next/image";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ResultWorkspace } from "@/components/ResultWorkspace";
import { UploadPanel } from "@/components/UploadPanel";
import { WorkflowProgress } from "@/components/WorkflowProgress";
import {
  ApiClientError,
  exportDocx,
  fetchDemoSample,
  processDocument,
  uploadDocument,
} from "@/lib/api/client";
import type { DemoSampleId } from "@/lib/api/client";
import type {
  NormalizedApiError,
  ExportDocxRequest,
  ProcessResult,
  UploadedDocument,
  WorkflowPhase,
  WorkflowState,
} from "@/lib/types/contracts";

const DEMO_STAGING = process.env.NEXT_PUBLIC_DEMO_STAGING === "1";
const PHASES: WorkflowPhase[] = ["upload", "analyze", "review", "validate", "export"];

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
  const [reviewEligible, setReviewEligible] = useState(false);
  const [validationEligible, setValidationEligible] = useState(false);
  const operationRef = useRef<"upload" | "process" | "export" | null>(null);
  const errorHeadingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    if (!error) return;
    const frame = window.requestAnimationFrame(() => errorHeadingRef.current?.focus());
    return () => window.cancelAnimationFrame(frame);
  }, [error]);

  const reachablePhases = useMemo<WorkflowPhase[]>(() => {
    const reachable: WorkflowPhase[] = ["upload"];
    if (document || result) reachable.push("analyze");
    if (result) reachable.push("review");
    if (result && reviewEligible) reachable.push("validate");
    if (result && reviewEligible && validationEligible) reachable.push("export");
    return reachable;
  }, [document, result, reviewEligible, validationEligible]);

  const handleReviewEligibilityChange = useCallback((eligible: boolean) => {
    setReviewEligible(eligible);
    if (!eligible) {
      setWorkflowPhase((current) => current === "validate" || current === "export" ? "review" : current);
    }
  }, []);

  const handleValidationEligibilityChange = useCallback((eligible: boolean) => {
    setValidationEligible(eligible);
    if (!eligible) {
      setWorkflowPhase((current) => current === "export" ? "validate" : current);
    }
  }, []);

  function reset() {
    operationRef.current = null;
    setState("IDLE");
    setDocument(null);
    setResult(null);
    setError(null);
    setRecoveryState("IDLE");
    setReviewEligible(false);
    setValidationEligible(false);
    setWorkflowPhase("upload");
  }

  function clearUploadedSource() {
    if (result) return;
    setDocument(null);
    setError(null);
    setRecoveryState("IDLE");
    setState("IDLE");
    setWorkflowPhase("upload");
  }

  function showError(issue: unknown, recoverTo: WorkflowState) {
    setError(normalizeClientError(issue));
    setRecoveryState(recoverTo);
    setState("ERROR");
  }

  async function performUpload(file: File, sampleId?: DemoSampleId) {
    if (operationRef.current) return;
    operationRef.current = "upload";
    setError(null);
    setResult(null);
    setReviewEligible(false);
    setValidationEligible(false);
    setWorkflowPhase("upload");
    setState("UPLOADING");
    try {
      const uploaded = await uploadDocument(file, sampleId);
      setDocument(uploaded);
      setWorkflowPhase("analyze");
      setState("UPLOADED");
    } catch (issue) {
      setDocument(null);
      showError(issue, "IDLE");
    } finally {
      if (operationRef.current === "upload") operationRef.current = null;
    }
  }

  async function handleDemoSample(sampleId: DemoSampleId) {
    if (operationRef.current) return;
    operationRef.current = "upload";
    setError(null);
    setResult(null);
    setReviewEligible(false);
    setValidationEligible(false);
    setWorkflowPhase("upload");
    setState("UPLOADING");
    try {
      const sample = await fetchDemoSample(sampleId);
      const uploaded = await uploadDocument(sample, sampleId);
      setDocument(uploaded);
      setWorkflowPhase("analyze");
      setState("UPLOADED");
    } catch (issue) {
      setDocument(null);
      showError(issue, "IDLE");
    } finally {
      if (operationRef.current === "upload") operationRef.current = null;
    }
  }

  async function handleProcess() {
    if (!document || result || operationRef.current) return;
    operationRef.current = "process";
    setError(null);
    setWorkflowPhase("analyze");
    setState("PROCESSING");
    try {
      const processed = await processDocument(document.document_id);
      setResult(processed);
      setReviewEligible(false);
      setValidationEligible(false);
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

  function navigateTo(phase: WorkflowPhase) {
    if (reachablePhases.includes(phase)) setWorkflowPhase(phase);
  }

  function goBack() {
    const current = PHASES.indexOf(workflowPhase);
    for (let index = current - 1; index >= 0; index -= 1) {
      if (reachablePhases.includes(PHASES[index])) {
        setWorkflowPhase(PHASES[index]);
        return;
      }
    }
  }

  const statusMessage =
    state === "UPLOADING"
      ? "Uploading and validating the document."
      : state === "PROCESSING"
        ? "Extracting invention-relevant content and preparing a grounded draft."
        : state === "EXPORTING"
          ? "Preparing the editable DOCX download."
          : state === "READY"
            ? "The patent draft is ready for human review."
            : "";
  const canGoBack = workflowPhase !== "upload";
  const resultPhase = workflowPhase === "review" || workflowPhase === "validate" || workflowPhase === "export";

  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="header-inner">
          <div className="brand-group">
            <span className="brand-logo-frame">
              <Image
                alt="VNUHCM Innovation Hub"
                className="brand-logo"
                height={107}
                priority
                src="/brand/vnuhcm-innovation-hub-logo.png"
                width={190}
              />
            </span>
            <div className="brand-divider" aria-hidden="true" />
            <p className="product-name">AI IP Description Generator</p>
          </div>
        </div>
      </header>

      <main>
        <section className="hero" aria-labelledby="page-title">
          <p className="eyebrow">Evidence-grounded patent drafting workflow</p>
          <h1 id="page-title">From Scientific Research Paper to USPTO-Style Patent Specification</h1>
          <p>
            Upload one scientific research paper in PDF or DOCX format to extract invention-relevant content,
            review and refine the generated patent specification draft, validate required sections, and export
            an editable DOCX for further expert review.
          </p>
        </section>

        <section className="workflow-shell" aria-label="Patent drafting workflow">
          <div className="workflow-nav-row">
            <button
              className="back-button"
              disabled={!canGoBack}
              onClick={goBack}
              type="button"
            >
              ← Go back
            </button>
          </div>

          <WorkflowProgress
            phase={workflowPhase}
            reachablePhases={reachablePhases}
            onNavigate={navigateTo}
          />

          <p className="sr-only" aria-live="polite" aria-atomic="true">{statusMessage}</p>

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

          {workflowPhase === "upload" && (
            <UploadPanel
              demoStaging={DEMO_STAGING}
              document={document}
              hasDownstreamResults={Boolean(result)}
              onContinueReview={() => setWorkflowPhase("review")}
              onProcess={handleProcess}
              onRemove={result ? reset : clearUploadedSource}
              onReplace={result ? async (file) => { reset(); await performUpload(file); } : performUpload}
              onReset={reset}
              onUpload={performUpload}
              onUseDemoSample={handleDemoSample}
              state={state}
            />
          )}

          {workflowPhase === "analyze" && !result && (
            <UploadPanel
              demoStaging={DEMO_STAGING}
              document={document}
              hasDownstreamResults={false}
              onContinueReview={() => undefined}
              onProcess={handleProcess}
              onRemove={clearUploadedSource}
              onReplace={performUpload}
              onReset={reset}
              onUpload={performUpload}
              onUseDemoSample={handleDemoSample}
              state={state}
            />
          )}

          {workflowPhase === "analyze" && result && (
            <section className="stage-card extraction-complete" aria-labelledby="extraction-complete-heading">
              <span className="stage-icon stage-icon-success" aria-hidden="true">✓</span>
              <p className="eyebrow">AI Extraction</p>
              <h2 id="extraction-complete-heading">Extraction complete</h2>
              <p>The current analysis and grounded draft are already available in this session. Continuing will not run processing again.</p>
              <button className="primary-button" onClick={() => setWorkflowPhase("review")} type="button">
                Continue to Review &amp; Refine →
              </button>
            </section>
          )}

          {result && (
            <div hidden={!resultPhase}>
              <ResultWorkspace
                onExport={handleExport}
                onPhaseChange={setWorkflowPhase}
                onReviewEligibilityChange={handleReviewEligibilityChange}
                onReset={reset}
                onValidationEligibilityChange={handleValidationEligibilityChange}
                phase={workflowPhase}
                result={result}
                state={state}
              />
            </div>
          )}
        </section>
      </main>

      <footer className="site-footer">
        <p>© 2026 VNUHCM Innovation Hub. All rights reserved.</p>
        <p>Kết quả cần được chuyên gia kỹ thuật và sở hữu trí tuệ rà soát trước khi sử dụng chính thức.</p>
      </footer>
    </div>
  );
}
