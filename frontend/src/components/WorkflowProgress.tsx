import type { WorkflowPhase } from "@/lib/types/contracts";

const STEPS = [
  { key: "upload", label: "Source Upload", description: "Upload PDF or DOCX" },
  { key: "analyze", label: "AI Extraction", description: "Extract key content" },
  { key: "review", label: "Review & Refine", description: "Rà soát & hoàn thiện" },
  { key: "validate", label: "Validation", description: "Check required sections" },
  { key: "export", label: "DOCX Export", description: "Download editable file" },
] as const satisfies ReadonlyArray<{ key: WorkflowPhase; label: string; description: string }>;

interface WorkflowProgressProps {
  phase: WorkflowPhase;
  reachablePhases: WorkflowPhase[];
  onNavigate: (phase: WorkflowPhase) => void;
}

export function WorkflowProgress({ phase, reachablePhases, onNavigate }: WorkflowProgressProps) {
  const current = STEPS.findIndex((step) => step.key === phase);
  return (
    <nav className="workflow-progress" aria-label="Document workflow">
      <ol>
        {STEPS.map((step, index) => {
          const reachable = reachablePhases.includes(step.key);
          const status = index === current
            ? "current"
            : reachable && index < current
              ? "complete"
              : reachable
                ? "reachable"
                : "upcoming";
          return (
            <li className={`workflow-step workflow-step-${status}`} key={step.key}>
              <button
                aria-current={index === current ? "step" : undefined}
                aria-label={`${index + 1}. ${step.label}: ${step.description}`}
                disabled={!reachable || index === current}
                onClick={() => onNavigate(step.key)}
                type="button"
              >
                <span className="step-marker" aria-hidden="true">
                  {status === "complete" ? "✓" : index + 1}
                </span>
                <span className="step-copy">
                  <strong>{step.label}</strong>
                  <small>{step.description}</small>
                </span>
                <span className="sr-only">{status}</span>
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
