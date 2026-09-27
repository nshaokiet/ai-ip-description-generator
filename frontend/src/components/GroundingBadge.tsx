import type { GroundingLabel } from "@/lib/types/contracts";

interface GroundingBadgeProps {
  label: GroundingLabel;
}

export function GroundingBadge({ label }: GroundingBadgeProps) {
  const readable = label.replace("_", " ");
  return (
    <span className={`grounding-badge grounding-${label.toLowerCase()}`}>
      {readable}
    </span>
  );
}
