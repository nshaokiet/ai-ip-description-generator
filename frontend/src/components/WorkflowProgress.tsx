import type { WorkflowPhase, WorkflowState } from "@/lib/types/contracts";
import { useUi, type MessageKey } from "@/lib/uiPreferences";

const STEPS = [
  { key: "upload", label: "upload", description: "uploadDescription" },
  { key: "analyze", label: "extraction", description: "extractionDescription" },
  { key: "review", label: "review", description: "reviewDescription" },
  { key: "validate", label: "validation", description: "validationDescription" },
  { key: "export", label: "export", description: "exportDescription" },
] as const satisfies ReadonlyArray<{ key: WorkflowPhase; label: MessageKey; description: MessageKey }>;

interface WorkflowProgressProps {
  phase: WorkflowPhase;
  state: WorkflowState;
  attention: boolean;
  reachablePhases: WorkflowPhase[];
  onNavigate: (phase: WorkflowPhase) => void;
}

export function WorkflowProgress({ phase, state, attention, reachablePhases, onNavigate }: WorkflowProgressProps) {
  const { t } = useUi();
  const current = STEPS.findIndex((step) => step.key === phase);
  return (
    <nav className="workflow-progress" aria-label={t("draftingWorkflow")}>
      <ol>
        {STEPS.map((step, index) => {
          const reachable = reachablePhases.includes(step.key);
          const status = index === current
            ? (state === "ERROR" ? "error" : ["UPLOADING", "PROCESSING", "EXPORTING"].includes(state) ? "processing" : "current")
            : reachable && index < current
              ? "complete"
              : reachable
                ? "reachable"
                : "upcoming";
          return (
            <li className={`workflow-step workflow-step-${status}`} key={step.key}>
              <button
                aria-current={index === current ? "step" : undefined}
                aria-label={`${index + 1}. ${t(step.label)}: ${t(step.description)}`}
                disabled={!reachable || index === current}
                onClick={() => onNavigate(step.key)}
                type="button"
              >
                <span className="step-marker" aria-hidden="true">
                  {status === "complete" ? "✓" : index + 1}
                </span>
                <span className="step-copy">
                  <strong>{t(step.label)}</strong>
                  <small>{t(step.description)}</small>
                  {step.key === "review" && attention && <small className="status-attention">{t("attention")}</small>}
                </span>
                <span className="sr-only">{t(status)}</span>
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
