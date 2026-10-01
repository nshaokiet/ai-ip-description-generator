import type { WorkflowPhase } from "@/lib/types/contracts";

const STEPS = [
  { key: "upload", label: "Upload", description: "Choose and check source" },
  { key: "analyze", label: "Analyze", description: "Generate grounded draft" },
  { key: "review", label: "Review / Edit", description: "Inspect and revise prose" },
  { key: "validate", label: "Validate", description: "Check the exact revision" },
  { key: "export", label: "Export", description: "Download editable DOCX" },
] as const;

export function WorkflowProgress({ phase }: { phase: WorkflowPhase }) {
  const current = STEPS.findIndex((step) => step.key === phase);
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
