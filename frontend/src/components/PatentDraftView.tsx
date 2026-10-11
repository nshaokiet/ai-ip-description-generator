"use client";

import { EvidenceCard } from "@/components/EvidenceCard";
import { GroundingBadge } from "@/components/GroundingBadge";
import { useUi } from "@/lib/uiPreferences";
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
  onInspectEvidence?: (evidenceId: string) => void;
}

function MissingContent({ content }: { content: DraftHeadlineContent }) {
  const { t } = useUi();
  return (
    <div className="missing-content" role="note">
      <strong>{t("missingContent")} · {content.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
      {content.missing_information_ids && <p>{t("missingRelated")}: {content.missing_information_ids.join(", ")}</p>}
    </div>
  );
}

function FieldFeedback({ path, errors, unverified }: {
  path: string; errors: string[]; unverified: string[];
}) {
  const { t } = useUi();
  return (
    <>
      {errors.some((item) => item === path || item.startsWith(`${path}/`)) && (
        <p className="field-error" role="alert">{t("fieldRejected")}</p>
      )}
      {unverified.includes(path) && (
        <p className="edit-support-warning" role="note">
          {t("editorSupport")}
        </p>
      )}
    </>
  );
}

function Paragraph({ paragraph, path, editing, errors, unverified, onChange, onInspectEvidence }: {
  paragraph: DraftParagraph;
  path: string;
  editing: boolean;
  errors: string[];
  unverified: string[];
  onChange?: (text: string) => void;
  onInspectEvidence?: (evidenceId: string) => void;
}) {
  const { t } = useUi();
  return (
    <div className="draft-paragraph">
      {editing ? (
        <>
          <label htmlFor={`edit-${paragraph.paragraph_id}`}>{t("paragraph")} {paragraph.paragraph_id} {t("prose")}</label>
          <textarea
            id={`edit-${paragraph.paragraph_id}`}
            onChange={(event) => onChange?.(event.target.value)}
            rows={4}
            value={paragraph.text}
          />
        </>
      ) : <p>{paragraph.text}</p>}
      <div className="grounding-details" aria-label={`${t("groundingFor")} ${paragraph.paragraph_id}`}>
        <GroundingBadge label={paragraph.grounding.label} />
        <span>{t("evidenceLabel")}: {paragraph.grounding.evidence_ids.map((id) => <button className="evidence-jump" type="button" onClick={() => onInspectEvidence?.(id)} key={id}>{id}</button>)}</span>
        <span>{t("sourcePaths")}: {paragraph.source_paths.join(", ")}</span>
      </div>
      <FieldFeedback path={path} errors={errors} unverified={unverified} />
    </div>
  );
}

export function PatentDraftView({
  draft, editing = false, review = {}, errorPaths = [], unverifiedPaths = [],
  onAbstractChange, onParagraphChange, onReviewChange, onInspectEvidence,
}: DraftViewProps) {
  const { t } = useUi();
  return (
    <div className="result-view draft-document">
      <div className="draft-notice">
        <span className="status-dot" aria-hidden="true" />
        <div>
          <strong>{t("humanReviewDraft")}</strong>
          <p>{t("notLegal")}</p>
        </div>
      </div>
      {editing && (
        <div className="edit-support-warning" role="note">
          {t("editorWarning")}
          {draft.missing_information.length > 0 && <p>{draft.missing_information.length} {t("missingCount")}.</p>}
          {draft.conflicts.length > 0 && <p>{draft.conflicts.length} {t("conflictCount")}.</p>}
        </div>
      )}

      <header className="draft-title-block">
        <p className="eyebrow">{t("patentDraft")} · v{draft.schema_version}</p>
        {draft.selected_title.status === "PRESENT" ? (
          <>
            <h2>{draft.selected_title.text}</h2>
            {draft.selected_title.grounding && <GroundingBadge label={draft.selected_title.grounding.label} />}
          </>
        ) : <><h2>{t("missingTitle")}</h2><MissingContent content={draft.selected_title} /></>}
      </header>

      <section className="draft-abstract" aria-labelledby="draft-abstract-heading">
        <p className="eyebrow">{t("abstract")}</p>
        <h3 className="sr-only" id="draft-abstract-heading">{t("abstract")}</h3>
        {draft.abstract.status === "PRESENT" ? (
          <>
            {editing ? (
              <>
                <label htmlFor="edit-abstract">{t("abstract")} {t("prose")}</label>
                <textarea id="edit-abstract" onChange={(event) => onAbstractChange?.(event.target.value)} rows={5} value={draft.abstract.text} />
              </>
            ) : <p>{draft.abstract.text}</p>}
            <div className="abstract-meta">
              <span>{draft.abstract.word_count} {t("words")} · {t("maxWords")}</span>
              {draft.abstract.grounding && <GroundingBadge label={draft.abstract.grounding.label} />}
            </div>
            <div className="grounding-details">
              <span>{t("evidenceLabel")}: {draft.abstract.grounding?.evidence_ids.map((id) => <button className="evidence-jump" type="button" onClick={() => onInspectEvidence?.(id)} key={id}>{id}</button>)}</span>
              <span>{t("sourcePaths")}: {draft.abstract.source_paths?.join(", ")}</span>
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
                <label htmlFor={`review-${section.section_id}`}>{t("reviewStatus")} {section.heading}</label>
                <select
                  disabled={editing || !onReviewChange}
                  id={`review-${section.section_id}`}
                  onChange={(event) => onReviewChange?.(section.section_id, event.target.value as ReviewStatus)}
                  value={review[section.section_id]?.status ?? "UNREVIEWED"}
                >
                  <option value="UNREVIEWED">{t("statusUnreviewed")}</option>
                  <option value="REVIEWED">{t("statusReviewed")}</option>
                  <option value="NEEDS_CHANGES">{t("statusNeedsChanges")}</option>
                </select>
              </div>
              {section.status === "MISSING" ? (
                <div className="missing-content" role="note">
                  <strong>{section.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
                  <p>{t("missingRelated")}: {section.missing_information_ids.join(", ")}</p>
                </div>
              ) : (
                <>
                  {section.paragraphs.map((paragraph, paragraphIndex) => (
                    <Paragraph
                      editing={editing} errors={errorPaths} key={paragraph.paragraph_id}
                      onChange={(text) => onParagraphChange?.(sectionIndex, null, paragraphIndex, text)}
                      paragraph={paragraph} path={`/draft_sections/${sectionIndex}/paragraphs/${paragraphIndex}/text`}
                      onInspectEvidence={onInspectEvidence}
                      unverified={unverifiedPaths}
                    />
                  ))}
                  {section.subsections.map((subsection, subsectionIndex) => (
                    <section className="draft-subsection" key={subsection.subsection_id}>
                      <h4>{subsection.heading}</h4>
                      {subsection.status === "MISSING" ? (
                        <div className="missing-content" role="note">
                          <strong>{subsection.marker ?? "[AUTHOR CONFIRMATION REQUIRED]"}</strong>
                          <p>{t("missingRelated")}: {subsection.missing_information_ids.join(", ")}</p>
                        </div>
                      ) : subsection.paragraphs.map((paragraph, paragraphIndex) => (
                        <Paragraph
                          editing={editing} errors={errorPaths} key={paragraph.paragraph_id}
                          onChange={(text) => onParagraphChange?.(sectionIndex, subsectionIndex, paragraphIndex, text)}
                          paragraph={paragraph}
                          path={`/draft_sections/${sectionIndex}/subsections/${subsectionIndex}/paragraphs/${paragraphIndex}/text`}
                          onInspectEvidence={onInspectEvidence}
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
          <h3 id="draft-evidence-appendix">{t("appendix")}</h3>
          <span>{draft.evidence_appendix.length}</span>
        </div>
        <div className="evidence-grid">
          {draft.evidence_appendix.map((evidence) => <EvidenceCard evidence={evidence} key={evidence.evidence_id} />)}
        </div>
      </section>
    </div>
  );
}
