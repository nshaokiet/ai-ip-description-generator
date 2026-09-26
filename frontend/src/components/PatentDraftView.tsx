import { EvidenceCard } from "@/components/EvidenceCard";
import { GroundingBadge } from "@/components/GroundingBadge";
import type {
  DraftHeadlineContent,
  DraftParagraph,
  DraftSection,
  PatentDraft,
} from "@/lib/types/contracts";

function MissingContent({ content }: { content: DraftHeadlineContent }) {
  return (
    <div className="missing-content" role="note">
      <strong>{content.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
      {content.missing_information_ids && (
        <p>Related items: {content.missing_information_ids.join(", ")}</p>
      )}
    </div>
  );
}

function DraftParagraphCard({ paragraph }: { paragraph: DraftParagraph }) {
  return (
    <div className="draft-paragraph">
      <p>{paragraph.text}</p>
      <details>
        <summary>Grounding details</summary>
        <div className="grounding-details">
          <GroundingBadge label={paragraph.grounding.label} />
          <span>Evidence: {paragraph.grounding.evidence_ids.join(", ")}</span>
          <span>Source paths: {paragraph.source_paths.join(", ")}</span>
        </div>
      </details>
    </div>
  );
}

function DraftSectionContent({ section }: { section: DraftSection }) {
  return (
    <section className="draft-section" aria-labelledby={`draft-${section.section_id}`}>
      <div className="draft-section-number">{String(section.sequence).padStart(2, "0")}</div>
      <div className="draft-section-body">
        <h3 id={`draft-${section.section_id}`}>{section.heading}</h3>
        {section.status === "MISSING" ? (
          <div className="missing-content" role="note">
            <strong>{section.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
            <p>Related items: {section.missing_information_ids.join(", ")}</p>
          </div>
        ) : (
          <>
            {section.paragraphs.map((paragraph) => (
              <DraftParagraphCard paragraph={paragraph} key={paragraph.paragraph_id} />
            ))}
            {section.subsections.map((subsection) => (
              <section className="draft-subsection" key={subsection.subsection_id}>
                <h4>{subsection.heading}</h4>
                {subsection.status === "MISSING" ? (
                  <div className="missing-content" role="note">
                    <strong>{subsection.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
                    <p>Related items: {subsection.missing_information_ids.join(", ")}</p>
                  </div>
                ) : (
                  subsection.paragraphs.map((paragraph) => (
                    <DraftParagraphCard paragraph={paragraph} key={paragraph.paragraph_id} />
                  ))
                )}
              </section>
            ))}
          </>
        )}
      </div>
    </section>
  );
}

export function PatentDraftView({ draft }: { draft: PatentDraft }) {
  const orderedSections = [...draft.draft_sections].sort((a, b) => a.sequence - b.sequence);

  return (
    <div className="result-view draft-document">
      <div className="draft-notice">
        <span className="status-dot" aria-hidden="true" />
        <div>
          <strong>AI-generated draft for human review</strong>
          <p>Not legal advice and not filing-ready. Specialist review is required.</p>
        </div>
      </div>

      <header className="draft-title-block">
        <p className="eyebrow">Patent description draft · v{draft.schema_version}</p>
        {draft.selected_title.status === "PRESENT" ? (
          <>
            <h2>{draft.selected_title.text}</h2>
            {draft.selected_title.grounding && (
              <GroundingBadge label={draft.selected_title.grounding.label} />
            )}
          </>
        ) : (
          <MissingContent content={draft.selected_title} />
        )}
      </header>

      <section className="draft-abstract" aria-labelledby="draft-abstract-heading">
        <p className="eyebrow">Abstract</p>
        <h3 className="sr-only" id="draft-abstract-heading">Abstract</h3>
        {draft.abstract.status === "PRESENT" ? (
          <>
            <p>{draft.abstract.text}</p>
            <div className="abstract-meta">
              <span>{draft.abstract.word_count} words</span>
              {draft.abstract.grounding && (
                <GroundingBadge label={draft.abstract.grounding.label} />
              )}
            </div>
          </>
        ) : (
          <MissingContent content={draft.abstract} />
        )}
      </section>

      <div className="draft-sections">
        {orderedSections.map((section) => (
          <DraftSectionContent section={section} key={section.section_id} />
        ))}
      </div>

      <section className="result-section" aria-labelledby="draft-evidence-appendix">
        <div className="section-heading">
          <h3 id="draft-evidence-appendix">Evidence and reference appendix</h3>
          <span>{draft.evidence_appendix.length}</span>
        </div>
        <div className="evidence-grid">
          {draft.evidence_appendix.map((evidence) => (
            <EvidenceCard evidence={evidence} key={evidence.evidence_id} />
          ))}
        </div>
      </section>
    </div>
  );
}
