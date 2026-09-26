"use client";

import { useState } from "react";

import { AnalysisView } from "@/components/AnalysisView";
import { PatentDraftView } from "@/components/PatentDraftView";
import { ReviewItemsView } from "@/components/ReviewItemsView";
import type { ProcessResult, WorkflowState } from "@/lib/types/contracts";

type ResultTab = "analysis" | "draft" | "review";

interface ResultWorkspaceProps {
  result: ProcessResult;
  state: WorkflowState;
  onExport: () => Promise<void>;
  onReset: () => void;
}

export function ResultWorkspace({ result, state, onExport, onReset }: ResultWorkspaceProps) {
  const [activeTab, setActiveTab] = useState<ResultTab>("analysis");
  const exporting = state === "EXPORTING";
  const tabs: Array<{ key: ResultTab; label: string }> = [
    { key: "analysis", label: "Analysis" },
    { key: "draft", label: "Patent Draft" },
    { key: "review", label: "Review Items" },
  ];

  return (
    <section className="results-workspace" aria-labelledby="results-heading">
      <div className="results-toolbar">
        <div>
          <p className="eyebrow">Processing complete</p>
          <h2 id="results-heading">Grounded draft workspace</h2>
          <p className="metadata-line">
            Reference ID: <code>{result.metadata.correlation_id}</code>
          </p>
        </div>
        <div className="toolbar-actions">
          <button className="secondary-button" onClick={onReset} type="button">
            New Document
          </button>
          <button
            className="primary-button"
            disabled={exporting}
            onClick={() => void onExport()}
            type="button"
          >
            {exporting ? "Preparing DOCX…" : "Export DOCX"}
          </button>
        </div>
      </div>

      <div className="tab-list" role="tablist" aria-label="Result views">
        {tabs.map((tab) => (
          <button
            aria-controls={`panel-${tab.key}`}
            aria-selected={activeTab === tab.key}
            className={activeTab === tab.key ? "tab-active" : ""}
            id={`tab-${tab.key}`}
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            role="tab"
            type="button"
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div
        aria-labelledby={`tab-${activeTab}`}
        className="tab-panel"
        id={`panel-${activeTab}`}
        role="tabpanel"
      >
        {activeTab === "analysis" && <AnalysisView analysis={result.analysis} />}
        {activeTab === "draft" && <PatentDraftView draft={result.draft} />}
        {activeTab === "review" && (
          <ReviewItemsView analysis={result.analysis} draft={result.draft} />
        )}
      </div>
    </section>
  );
}
