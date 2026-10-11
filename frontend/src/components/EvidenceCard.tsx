"use client";

import { useUi } from "@/lib/uiPreferences";
import type { Evidence, EvidenceAppendixItem } from "@/lib/types/contracts";

function locatorParts(locator: Evidence["locator"], t: ReturnType<typeof useUi>["t"]): string[] {
  const parts: string[] = [];
  if (locator.page !== undefined) parts.push(`${t("page")} ${locator.page}`);
  if (locator.section) parts.push(`${t("section")}: ${locator.section}`);
  if (locator.paragraph_id) parts.push(`${t("paragraph")}: ${locator.paragraph_id}`);
  if (locator.chunk_id) parts.push(`${t("chunk")}: ${locator.chunk_id}`);
  if (locator.table_id) parts.push(`${t("table")}: ${locator.table_id}`);
  if (locator.figure_id) parts.push(`${t("figure")}: ${locator.figure_id}`);
  return parts;
}

interface EvidenceCardProps {
  evidence: Evidence | EvidenceAppendixItem;
}

export function EvidenceCard({ evidence }: EvidenceCardProps) {
  const { t } = useUi();
  const locations = locatorParts(evidence.locator, t);
  const usages = "usage_references" in evidence ? evidence.usage_references : [];

  return (
    <article className="evidence-card">
      <div className="card-heading-row">
        <code>{evidence.evidence_id}</code>
        <span className="subtle-badge">{evidence.evidence_type}</span>
      </div>
      {locations.length > 0 && (
        <p className="metadata-line" aria-label={t("sourceLocator")}>
          {locations.join(" · ")}
        </p>
      )}
      <blockquote>{evidence.excerpt}</blockquote>
      {usages.length > 0 && (
        <div className="usage-list">
          <span className="eyebrow">{t("usedBy")}</span>
          <ul className="inline-list">
            {usages.map((usage) => (
              <li key={`${usage.target_type}-${usage.target_id}`}>
                {usage.target_type}: {usage.target_id}
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}
