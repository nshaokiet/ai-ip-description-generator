import { EvidenceCard } from "@/components/EvidenceCard";
import { GroundingBadge } from "@/components/GroundingBadge";
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
      {item.rationale && <p className="supporting-copy">Rationale: {item.rationale}</p>}
      {conditions.length > 0 && (
        <div className="nested-detail">
          <strong>Conditions</strong>
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
          <strong>Results</strong>
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
        Evidence: {item.grounding.evidence_ids.join(", ")}
      </p>
    </article>
  );
}

function AnalysisSection({
  title,
  items,
}: {
  title: string;
  items: AnalysisItem[];
}) {
  if (items.length === 0) return null;
  return (
    <section className="result-section" aria-labelledby={`analysis-${title.replaceAll(" ", "-")}`}>
      <div className="section-heading">
        <h3 id={`analysis-${title.replaceAll(" ", "-")}`}>{title}</h3>
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
  const technicalField = analysis.technical_field.item
    ? [analysis.technical_field.item]
    : [];

  return (
    <div className="result-view">
      <div className="view-introduction">
        <div>
          <p className="eyebrow">Canonical analysis · v{analysis.schema_version}</p>
          <h2>Structured invention analysis</h2>
        </div>
        <p>
          Technical statements remain linked to evidence. Inferences are visually separated
          from direct source facts.
        </p>
      </div>

      <AnalysisSection title="Title candidates" items={analysis.title_candidates} />
      <AnalysisSection title="Technical field" items={technicalField} />
      {analysis.technical_field.status === "MISSING" && (
        <p className="missing-marker">{analysis.technical_field.marker}</p>
      )}
      <AnalysisSection title="Background" items={analysis.background} />
      <AnalysisSection title="Technical problems" items={analysis.technical_problems} />
      <AnalysisSection title="Technical solutions" items={analysis.technical_solutions} />
      <AnalysisSection title="Components" items={analysis.components} />
      <AnalysisSection title="Process steps" items={analysis.process_steps} />
      <AnalysisSection
        title="Potential distinguishing features"
        items={analysis.potential_distinguishing_features}
      />
      <AnalysisSection title="Technical effects" items={analysis.technical_effects} />
      <AnalysisSection title="Embodiments" items={analysis.embodiments} />
      <AnalysisSection title="Experimental data" items={analysis.experimental_data} />

      {analysis.missing_information.length > 0 && (
        <section className="result-section" aria-labelledby="analysis-missing-information">
          <div className="section-heading">
            <h3 id="analysis-missing-information">Missing information</h3>
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
                <p className="metadata-line">{item.reason} · Owner: {item.owner}</p>
                <code className="path-code">{item.target_path}</code>
              </article>
            ))}
          </div>
        </section>
      )}

      {analysis.author_questions.length > 0 && (
        <section className="result-section" aria-labelledby="analysis-author-questions">
          <div className="section-heading">
            <h3 id="analysis-author-questions">Author questions</h3>
            <span>{analysis.author_questions.length}</span>
          </div>
          <div className="review-list">
            {analysis.author_questions.map((item) => (
              <article className="review-card" key={item.question_id}>
                <span className="priority-badge">{item.priority}</span>
                <p className="question-text">{item.question}</p>
                <p className="metadata-line">Related item: {item.missing_information_id}</p>
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="result-section" aria-labelledby="analysis-evidence">
        <div className="section-heading">
          <h3 id="analysis-evidence">Evidence</h3>
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
