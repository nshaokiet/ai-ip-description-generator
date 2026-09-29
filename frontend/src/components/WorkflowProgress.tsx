import type { WorkflowState } from "@/lib/types/contracts";

const STEPS = [
  { key: "upload", label: "Upload", description: "Validate source document" },
  { key: "process", label: "Process", description: "Analyze and generate draft" },
  { key: "review", label: "Review & export", description: "Inspect grounded output" },
] as const;

function activeIndex(state: WorkflowState): number {
  if (state === "IDLE" || state === "UPLOADING") return 0;
  if (state === "UPLOADED" || state === "PROCESSING") return 1;
  return 2;
}

export function WorkflowProgress({ state }: { state: WorkflowState }) {
  const current = activeIndex(state);
  return (
    <nav className="workflow-progress" aria-label="Document workflow">
      <ol>
        {STEPS.map((step, index) => {
          const status = index < current ? "complete" : index === current ? "current" : "upcoming";
          return (
            <li aria-current={index === current ? "step" : undefined} className={`workflow-step workflow-step-${status}`} key={step.key}>
              <span className="step-marker" aria-hidden="true">
                {index < current ? "✓" : index + 1}
              </span>
              <span>
                <strong>{step.label}</strong>
                <small>{step.description}</small>
              </span>
              <span className="sr-only">{status}</span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
