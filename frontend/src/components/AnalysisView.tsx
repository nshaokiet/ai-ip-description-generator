"use client";

import { EvidenceCard } from "@/components/EvidenceCard";
import { GroundingBadge } from "@/components/GroundingBadge";
import { useUi, type MessageKey } from "@/lib/uiPreferences";
import type {
  AnalysisItem,
  GroundedStatement,
  InventionAnalysis,
  Measurement,
} from "@/lib/types/contracts";

function itemKey(item: AnalysisItem, index: number): string {
  return (
    item.title_id ??
    item.field_id ??
    item.statement_id ??
    item.problem_id ??
    item.solution_id ??
    item.component_id ??
    item.step_id ??
    item.feature_id ??
    item.effect_id ??
    item.embodiment_id ??
    item.experiment_id ??
    `item-${index}`
  );
}

function itemLead(item: AnalysisItem): string {
  return (
    item.title ??
    item.name ??
    item.statement ??
    item.action ??
    item.text ??
    item.description ??
    "Structured item"
  );
}

function isGroundedStatement(value: GroundedStatement | Measurement): value is GroundedStatement {
  return "grounding" in value;
}

function AnalysisCard({ item, index }: { item: AnalysisItem; index: number }) {
  const { t } = useUi();
  const lead = itemLead(item);
  const description = item.description && item.description !== lead ? item.description : undefined;
  const conditions = item.conditions ?? [];

  return (
    <article className="result-card">
      <div className="card-heading-row">
        <h4>{lead}</h4>
        <GroundingBadge label={item.grounding.label} />
      </div>
      {description && <p>{description}</p>}
      {item.rationale && <p className="supporting-copy">{t("rationale")}: {item.rationale}</p>}
      {conditions.length > 0 && (
        <div className="nested-detail">
          <strong>{t("conditions")}</strong>
          <ul>
            {conditions.map((condition, conditionIndex) => (
              <li key={`${itemKey(item, index)}-condition-${conditionIndex}`}>
                {isGroundedStatement(condition)
                  ? condition.text
                  : `${condition.parameter ?? condition.metric}: ${condition.value}${condition.unit ? ` ${condition.unit}` : ""}`}
              </li>
            ))}
          </ul>
        </div>
      )}
      {item.results && item.results.length > 0 && (
        <div className="nested-detail">
          <strong>{t("results")}</strong>
          <ul>
            {item.results.map((result, resultIndex) => (
              <li key={`${itemKey(item, index)}-result-${resultIndex}`}>
                {result.metric}: {result.value}{result.unit ? ` ${result.unit}` : ""}
              </li>
            ))}
          </ul>
        </div>
      )}
      <p className="evidence-links">
        {t("evidenceLabel")}: {item.grounding.evidence_ids.join(", ")}
      </p>
    </article>
  );
}

function AnalysisSection({
  title,
  items,
}: {
  title: MessageKey;
  items: AnalysisItem[];
}) {
  const { t } = useUi();
  if (items.length === 0) return null;
  return (
    <section className="result-section" aria-labelledby={`analysis-${title}`}>
      <div className="section-heading">
        <h3 id={`analysis-${title}`}>{t(title)}</h3>
        <span>{items.length}</span>
      </div>
      <div className="result-card-grid">
        {items.map((item, index) => (
          <AnalysisCard item={item} index={index} key={itemKey(item, index)} />
        ))}
      </div>
    </section>
  );
}

export function AnalysisView({ analysis }: { analysis: InventionAnalysis }) {
  const { t } = useUi();
  const technicalField = analysis.technical_field.item
    ? [analysis.technical_field.item]
    : [];

  return (
    <div className="result-view">
      <div className="view-introduction">
        <div>
          <p className="eyebrow">{t("analysis")} · v{analysis.schema_version}</p>
          <h2>{t("analysisTitle")}</h2>
        </div>
        <p>
          {t("analysisIntro")}
        </p>
      </div>

      <AnalysisSection title="titleCandidates" items={analysis.title_candidates} />
      <AnalysisSection title="technicalField" items={technicalField} />
      {analysis.technical_field.status === "MISSING" && (
        <p className="missing-marker">{analysis.technical_field.marker}</p>
      )}
      <AnalysisSection title="background" items={analysis.background} />
      <AnalysisSection title="technicalProblems" items={analysis.technical_problems} />
      <AnalysisSection title="technicalSolutions" items={analysis.technical_solutions} />
      <AnalysisSection title="components" items={analysis.components} />
      <AnalysisSection title="processSteps" items={analysis.process_steps} />
      <AnalysisSection
        title="distinguishing"
        items={analysis.potential_distinguishing_features}
      />
      <AnalysisSection title="technicalEffects" items={analysis.technical_effects} />
      <AnalysisSection title="embodiments" items={analysis.embodiments} />
      <AnalysisSection title="experimentalData" items={analysis.experimental_data} />

      {analysis.missing_information.length > 0 && (
        <section className="result-section" aria-labelledby="analysis-missing-information">
          <div className="section-heading">
            <h3 id="analysis-missing-information">{t("missingInformation")}</h3>
            <span>{analysis.missing_information.length}</span>
          </div>
          <div className="review-list">
            {analysis.missing_information.map((item) => (
              <article className="review-card review-card-warning" key={item.missing_id}>
                <div className="card-heading-row">
                  <code>{item.missing_id}</code>
                  <span className="priority-badge">{item.impact}</span>
                </div>
                <p>{item.description}</p>
                <p className="metadata-line">{item.reason} · {t("owner")}: {item.owner}</p>
                <code className="path-code">{item.target_path}</code>
              </article>
            ))}
          </div>
        </section>
      )}

      {analysis.author_questions.length > 0 && (
        <section className="result-section" aria-labelledby="analysis-author-questions">
          <div className="section-heading">
            <h3 id="analysis-author-questions">{t("authorQuestions")}</h3>
            <span>{analysis.author_questions.length}</span>
          </div>
          <div className="review-list">
            {analysis.author_questions.map((item) => (
              <article className="review-card" key={item.question_id}>
                <span className="priority-badge">{item.priority}</span>
                <p className="question-text">{item.question}</p>
                <p className="metadata-line">{t("relatedItem")}: {item.missing_information_id}</p>
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="result-section" aria-labelledby="analysis-evidence">
        <div className="section-heading">
          <h3 id="analysis-evidence">{t("evidenceLabel")}</h3>
          <span>{analysis.evidence.length}</span>
        </div>
        <div className="evidence-grid">
          {analysis.evidence.map((evidence) => (
            <EvidenceCard evidence={evidence} key={evidence.evidence_id} />
          ))}
        </div>
      </section>
    </div>
  );
}
