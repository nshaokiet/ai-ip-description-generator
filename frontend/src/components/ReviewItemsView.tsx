import { GroundingBadge } from "@/components/GroundingBadge";
import type {
  AnalysisItem,
  InventionAnalysis,
  PatentDraft,
} from "@/lib/types/contracts";

interface InferenceItem {
  id: string;
  text: string;
  evidenceIds: string[];
  source: string;
}

function analysisItemId(item: AnalysisItem, index: number): string {
  return (
    item.title_id ?? item.field_id ?? item.statement_id ?? item.problem_id ??
    item.solution_id ?? item.component_id ?? item.step_id ?? item.feature_id ??
    item.effect_id ?? item.embodiment_id ?? item.experiment_id ?? `inference-${index}`
  );
}

function analysisItemText(item: AnalysisItem): string {
  return item.title ?? item.name ?? item.statement ?? item.action ?? item.text ??
    item.description ?? "Inference content";
}

function collectInferences(
  analysis: InventionAnalysis,
  draft: PatentDraft,
): InferenceItem[] {
  const result: InferenceItem[] = [];
  const groups: Array<[string, AnalysisItem[]]> = [
    ["Analysis · title", analysis.title_candidates],
    ["Analysis · background", analysis.background],
    ["Analysis · technical problem", analysis.technical_problems],
    ["Analysis · technical solution", analysis.technical_solutions],
    ["Analysis · component", analysis.components],
    ["Analysis · process", analysis.process_steps],
    ["Analysis · potential feature", analysis.potential_distinguishing_features],
    ["Analysis · technical effect", analysis.technical_effects],
    ["Analysis · embodiment", analysis.embodiments],
    ["Analysis · experiment", analysis.experimental_data],
  ];
  if (analysis.technical_field.item) groups.push(["Analysis · technical field", [analysis.technical_field.item]]);

  groups.forEach(([source, items]) => {
    items.forEach((item, index) => {
      if (item.grounding.label === "INFERENCE") {
        result.push({
          id: analysisItemId(item, index),
          text: analysisItemText(item),
          evidenceIds: item.grounding.evidence_ids,
          source,
        });
      }
    });
  });

  if (draft.selected_title.grounding?.label === "INFERENCE" && draft.selected_title.text) {
    result.push({
      id: draft.selected_title.source_title_candidate_id ?? "draft-selected-title",
      text: draft.selected_title.text,
      evidenceIds: draft.selected_title.grounding.evidence_ids,
      source: "Draft · title",
    });
  }
  if (draft.abstract.grounding?.label === "INFERENCE" && draft.abstract.text) {
    result.push({
      id: "draft-abstract",
      text: draft.abstract.text,
      evidenceIds: draft.abstract.grounding.evidence_ids,
      source: "Draft · abstract",
    });
  }
  draft.draft_sections.forEach((section) => {
    const paragraphs = [
      ...section.paragraphs,
      ...section.subsections.flatMap((subsection) => subsection.paragraphs),
    ];
    paragraphs.forEach((paragraph) => {
      if (paragraph.grounding.label === "INFERENCE") {
        result.push({
          id: paragraph.paragraph_id,
          text: paragraph.text,
          evidenceIds: paragraph.grounding.evidence_ids,
          source: `Draft · ${section.heading}`,
        });
      }
    });
  });
  return result;
}

export function ReviewItemsView({
  analysis,
  draft,
}: {
  analysis: InventionAnalysis;
  draft: PatentDraft;
}) {
  const inferences = collectInferences(analysis, draft);
  const total =
    analysis.missing_information.length +
    draft.missing_information.length +
    draft.conflicts.length +
    analysis.author_questions.length +
    draft.author_questions.length +
    inferences.length;

  return (
    <div className="result-view">
      <div className="view-introduction">
        <div>
          <p className="eyebrow">Human review queue</p>
          <h2>Review items</h2>
        </div>
        <p>{total} item{total === 1 ? "" : "s"} require attention or contextual review.</p>
      </div>

      <section className="result-section" aria-labelledby="review-missing">
        <div className="section-heading">
          <h3 id="review-missing">Missing information</h3>
          <span>{analysis.missing_information.length + draft.missing_information.length}</span>
        </div>
        <div className="review-list">
          {analysis.missing_information.map((item) => (
            <article className="review-card review-card-warning" key={`analysis-${item.missing_id}`}>
              <div className="card-heading-row">
                <code>{item.missing_id}</code>
                <span className="priority-badge">{item.impact}</span>
              </div>
              <p>{item.description}</p>
              <p className="missing-marker">[AUTHOR CONFIRMATION REQUIRED]</p>
              <p className="metadata-line">Analysis · {item.reason} · {item.owner}</p>
            </article>
          ))}
          {draft.missing_information.map((item) => (
            <article className="review-card review-card-warning" key={`draft-${item.missing_id}`}>
              <div className="card-heading-row">
                <code>{item.missing_id}</code>
                <span className="priority-badge">{item.impact}</span>
              </div>
              <p>{item.description}</p>
              <p className="missing-marker">{item.marker}</p>
              <p className="metadata-line">Draft · {item.reason} · {item.owner}</p>
            </article>
          ))}
          {analysis.missing_information.length + draft.missing_information.length === 0 && (
            <p className="empty-state">No missing-information items were returned.</p>
          )}
        </div>
      </section>

      <section className="result-section" aria-labelledby="review-conflicts">
        <div className="section-heading">
          <h3 id="review-conflicts">Unresolved conflicts</h3>
          <span>{draft.conflicts.length}</span>
        </div>
        <div className="review-list">
          {draft.conflicts.map((conflict) => (
            <article className="review-card review-card-conflict" key={conflict.conflict_id}>
              <div className="card-heading-row">
                <code>{conflict.conflict_id}</code>
                <span className="unresolved-badge">{conflict.resolution_status}</span>
              </div>
              <p>{conflict.summary}</p>
              <p className="missing-marker">{conflict.marker}</p>
              <p className="metadata-line">Evidence: {conflict.evidence_ids.join(", ")}</p>
            </article>
          ))}
          {draft.conflicts.length === 0 && (
            <p className="empty-state">No unresolved conflicts were returned.</p>
          )}
        </div>
      </section>

      <section className="result-section" aria-labelledby="review-questions">
        <div className="section-heading">
          <h3 id="review-questions">Author questions</h3>
          <span>{analysis.author_questions.length + draft.author_questions.length}</span>
        </div>
        <div className="review-list">
          {analysis.author_questions.map((question) => (
            <article className="review-card" key={`analysis-${question.question_id}`}>
              <span className="priority-badge">{question.priority}</span>
              <p className="question-text">{question.question}</p>
              <p className="metadata-line">From structured analysis</p>
            </article>
          ))}
          {draft.author_questions.map((question) => (
            <article className="review-card" key={`draft-${question.question_id}`}>
              <span className="priority-badge">{question.priority}</span>
              <p className="question-text">{question.question}</p>
              <p className="metadata-line">Affected: {question.affected_section_ids.join(", ")}</p>
            </article>
          ))}
          {analysis.author_questions.length + draft.author_questions.length === 0 && (
            <p className="empty-state">No author questions were returned.</p>
          )}
        </div>
      </section>

      <section className="result-section" aria-labelledby="review-inferences">
        <div className="section-heading">
          <h3 id="review-inferences">Inference content</h3>
          <span>{inferences.length}</span>
        </div>
        <div className="review-list">
          {inferences.map((item) => (
            <article className="review-card review-card-inference" key={`${item.source}-${item.id}`}>
              <div className="card-heading-row">
                <GroundingBadge label="INFERENCE" />
                <span className="metadata-line">{item.source}</span>
              </div>
              <p>{item.text}</p>
              <p className="evidence-links">Evidence: {item.evidenceIds.join(", ")}</p>
            </article>
          ))}
          {inferences.length === 0 && (
            <p className="empty-state">No inference-labelled content was returned.</p>
          )}
        </div>
      </section>
    </div>
  );
}
