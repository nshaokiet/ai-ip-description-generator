"use client";

import { EvidenceCard } from "@/components/EvidenceCard";
import { GroundingBadge } from "@/components/GroundingBadge";
import type { ReviewStatus, SectionReviewRecord } from "@/lib/draftRevisions";
import type { DraftHeadlineContent, DraftParagraph, PatentDraft } from "@/lib/types/contracts";

interface DraftViewProps {
  draft: PatentDraft;
  editing?: boolean;
  review?: Record<string, SectionReviewRecord>;
  errorPaths?: string[];
  unverifiedPaths?: string[];
  onAbstractChange?: (text: string) => void;
  onParagraphChange?: (section: number, subsection: number | null, paragraph: number, text: string) => void;
  onReviewChange?: (sectionId: string, status: ReviewStatus) => void;
}

function MissingContent({ content }: { content: DraftHeadlineContent }) {
  return (
    <div className="missing-content" role="note">
      <strong>MISSING · {content.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
      {content.missing_information_ids && <p>Related items: {content.missing_information_ids.join(", ")}</p>}
    </div>
  );
}

function FieldFeedback({ path, errors, unverified }: {
  path: string; errors: string[]; unverified: string[];
}) {
  return (
    <>
      {errors.some((item) => item === path || item.startsWith(`${path}/`)) && (
        <p className="field-error" role="alert">Backend rejected this field. Check its content and source support.</p>
      )}
      {unverified.includes(path) && (
        <p className="edit-support-warning" role="note">
          Edited prose: semantic support has not been verified. Evidence links and grounding labels are unchanged; Human review is required.
        </p>
      )}
    </>
  );
}

function Paragraph({ paragraph, path, editing, errors, unverified, onChange }: {
  paragraph: DraftParagraph;
  path: string;
  editing: boolean;
  errors: string[];
  unverified: string[];
  onChange?: (text: string) => void;
}) {
  return (
    <div className="draft-paragraph">
      {editing ? (
        <>
          <label htmlFor={`edit-${paragraph.paragraph_id}`}>Paragraph {paragraph.paragraph_id} prose</label>
          <textarea
            id={`edit-${paragraph.paragraph_id}`}
            onChange={(event) => onChange?.(event.target.value)}
            rows={4}
            value={paragraph.text}
          />
        </>
      ) : <p>{paragraph.text}</p>}
      <div className="grounding-details" aria-label={`Grounding for ${paragraph.paragraph_id}`}>
        <GroundingBadge label={paragraph.grounding.label} />
        <span>Evidence: {paragraph.grounding.evidence_ids.join(", ")}</span>
        <span>Source paths: {paragraph.source_paths.join(", ")}</span>
      </div>
      <FieldFeedback path={path} errors={errors} unverified={unverified} />
    </div>
  );
}

export function PatentDraftView({
  draft, editing = false, review = {}, errorPaths = [], unverifiedPaths = [],
  onAbstractChange, onParagraphChange, onReviewChange,
}: DraftViewProps) {
  return (
    <div className="result-view draft-document">
      <div className="draft-notice">
        <span className="status-dot" aria-hidden="true" />
        <div>
          <strong>AI-generated draft for human review</strong>
          <p>Not legal advice and not filing-ready. Specialist review is required.</p>
        </div>
      </div>
      {editing && (
        <div className="edit-support-warning" role="note">
          Editing does not create evidence or verify new technical claims. Grounding labels and source links remain unchanged.
          {draft.missing_information.length > 0 && <p>{draft.missing_information.length} missing-information item(s) still require attention.</p>}
          {draft.conflicts.length > 0 && <p>{draft.conflicts.length} conflict(s) remain unresolved.</p>}
        </div>
      )}

      <header className="draft-title-block">
        <p className="eyebrow">Patent description draft · v{draft.schema_version}</p>
        {draft.selected_title.status === "PRESENT" ? (
          <>
            <h2>{draft.selected_title.text}</h2>
            {draft.selected_title.grounding && <GroundingBadge label={draft.selected_title.grounding.label} />}
          </>
        ) : <><h2>Title: MISSING</h2><MissingContent content={draft.selected_title} /></>}
      </header>

      <section className="draft-abstract" aria-labelledby="draft-abstract-heading">
        <p className="eyebrow">Abstract</p>
        <h3 className="sr-only" id="draft-abstract-heading">Abstract</h3>
        {draft.abstract.status === "PRESENT" ? (
          <>
            {editing ? (
              <>
                <label htmlFor="edit-abstract">Abstract prose</label>
                <textarea id="edit-abstract" onChange={(event) => onAbstractChange?.(event.target.value)} rows={5} value={draft.abstract.text} />
              </>
            ) : <p>{draft.abstract.text}</p>}
            <div className="abstract-meta">
              <span>{draft.abstract.word_count} words · 150 maximum</span>
              {draft.abstract.grounding && <GroundingBadge label={draft.abstract.grounding.label} />}
            </div>
            <div className="grounding-details">
              <span>Evidence: {draft.abstract.grounding?.evidence_ids.join(", ")}</span>
              <span>Source paths: {draft.abstract.source_paths?.join(", ")}</span>
            </div>
            <FieldFeedback path="/abstract/text" errors={errorPaths} unverified={unverifiedPaths} />
            <FieldFeedback path="/abstract/word_count" errors={errorPaths} unverified={[]} />
          </>
        ) : <MissingContent content={draft.abstract} />}
      </section>

      <div className="draft-sections">
        {draft.draft_sections.map((section, sectionIndex) => (
          <section className="draft-section" aria-labelledby={`draft-${section.section_id}`} key={section.section_id}>
            <div className="draft-section-number">{String(section.sequence).padStart(2, "0")}</div>
            <div className="draft-section-body">
              <h3 id={`draft-${section.section_id}`}>{section.heading}</h3>
              <div className="section-review-control">
                <label htmlFor={`review-${section.section_id}`}>Session review status for {section.heading}</label>
                <select
                  disabled={editing || !onReviewChange}
                  id={`review-${section.section_id}`}
                  onChange={(event) => onReviewChange?.(section.section_id, event.target.value as ReviewStatus)}
                  value={review[section.section_id]?.status ?? "UNREVIEWED"}
                >
                  <option value="UNREVIEWED">UNREVIEWED</option>
                  <option value="REVIEWED">REVIEWED (not approved)</option>
                  <option value="NEEDS_CHANGES">NEEDS_CHANGES</option>
                </select>
              </div>
              {section.status === "MISSING" ? (
                <div className="missing-content" role="note">
                  <strong>{section.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
                  <p>Related items: {section.missing_information_ids.join(", ")}</p>
                </div>
              ) : (
                <>
                  {section.paragraphs.map((paragraph, paragraphIndex) => (
                    <Paragraph
                      editing={editing} errors={errorPaths} key={paragraph.paragraph_id}
                      onChange={(text) => onParagraphChange?.(sectionIndex, null, paragraphIndex, text)}
                      paragraph={paragraph} path={`/draft_sections/${sectionIndex}/paragraphs/${paragraphIndex}/text`}
                      unverified={unverifiedPaths}
                    />
                  ))}
                  {section.subsections.map((subsection, subsectionIndex) => (
                    <section className="draft-subsection" key={subsection.subsection_id}>
                      <h4>{subsection.heading}</h4>
                      {subsection.status === "MISSING" ? (
                        <div className="missing-content" role="note">
                          <strong>{subsection.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
                          <p>Related items: {subsection.missing_information_ids.join(", ")}</p>
                        </div>
                      ) : subsection.paragraphs.map((paragraph, paragraphIndex) => (
                        <Paragraph
                          editing={editing} errors={errorPaths} key={paragraph.paragraph_id}
                          onChange={(text) => onParagraphChange?.(sectionIndex, subsectionIndex, paragraphIndex, text)}
                          paragraph={paragraph}
                          path={`/draft_sections/${sectionIndex}/subsections/${subsectionIndex}/paragraphs/${paragraphIndex}/text`}
                          unverified={unverifiedPaths}
                        />
                      ))}
                    </section>
                  ))}
                </>
              )}
            </div>
          </section>
        ))}
      </div>

      <section className="result-section" aria-labelledby="draft-evidence-appendix">
        <div className="section-heading">
          <h3 id="draft-evidence-appendix">Evidence and reference appendix</h3>
          <span>{draft.evidence_appendix.length}</span>
        </div>
        <div className="evidence-grid">
          {draft.evidence_appendix.map((evidence) => <EvidenceCard evidence={evidence} key={evidence.evidence_id} />)}
        </div>
      </section>
    </div>
  );
}
