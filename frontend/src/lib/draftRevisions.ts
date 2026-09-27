import type { DraftValidationResult, PatentDraft } from "@/lib/types/contracts";

export type ReviewStatus = "UNREVIEWED" | "REVIEWED" | "NEEDS_CHANGES";

export interface SectionReviewRecord {
  revision_id: string;
  section_id: string;
  status: ReviewStatus;
  timestamp: string;
}

export interface DraftRevision {
  id: string;
  draft: PatentDraft;
  review: Record<string, SectionReviewRecord>;
  validation: DraftValidationResult | null;
}

export interface DraftSession {
  revisions: DraftRevision[];
  selectedId: string;
  nextNumber: number;
}

function initialReview(draft: PatentDraft, revisionId: string): Record<string, SectionReviewRecord> {
  const timestamp = new Date().toISOString();
  return Object.fromEntries(
    draft.draft_sections.map((section) => [
      section.section_id,
      { revision_id: revisionId, section_id: section.section_id, status: "UNREVIEWED", timestamp },
    ]),
  );
}

export function createDraftSession(generated: PatentDraft): DraftSession {
  const id = "revision-1";
  const draft = structuredClone(generated);
  return {
    revisions: [{ id, draft, review: initialReview(draft, id), validation: null }],
    selectedId: id,
    nextNumber: 2,
  };
}

export function selectedRevision(session: DraftSession): DraftRevision {
  const revision = session.revisions.find((item) => item.id === session.selectedId);
  if (!revision) throw new Error("Selected session revision is unavailable.");
  return revision;
}

export function saveDraftRevision(session: DraftSession, edited: PatentDraft): DraftSession {
  const id = `revision-${session.nextNumber}`;
  const draft = structuredClone(edited);
  return {
    revisions: [...session.revisions, { id, draft, review: initialReview(draft, id), validation: null }],
    selectedId: id,
    nextNumber: session.nextNumber + 1,
  };
}

export function setReviewStatus(
  session: DraftSession,
  sectionId: string,
  status: ReviewStatus,
): DraftSession {
  return {
    ...session,
    revisions: session.revisions.map((revision) => {
      if (revision.id !== session.selectedId || !revision.review[sectionId]) return revision;
      return {
        ...revision,
        review: {
          ...revision.review,
          [sectionId]: {
            revision_id: revision.id,
            section_id: sectionId,
            status,
            timestamp: new Date().toISOString(),
          },
        },
      };
    }),
  };
}

export function setRevisionValidation(
  session: DraftSession,
  revisionId: string,
  validation: DraftValidationResult | null,
): DraftSession {
  return {
    ...session,
    revisions: session.revisions.map((revision) =>
      revision.id === revisionId ? { ...revision, validation } : revision,
    ),
  };
}

export function countAbstractWords(text: string): number {
  return text.normalize("NFKC").match(/[\p{L}\p{N}_]+(?:[-'’][\p{L}\p{N}_]+)*/gu)?.length ?? 0;
}

export function editedProsePaths(original: PatentDraft, revision: PatentDraft): string[] {
  const paths: string[] = [];
  if (original.abstract.text !== revision.abstract.text) paths.push("/abstract/text");
  revision.draft_sections.forEach((section, sectionIndex) => {
    section.paragraphs.forEach((paragraph, paragraphIndex) => {
      if (paragraph.text !== original.draft_sections[sectionIndex].paragraphs[paragraphIndex]?.text) {
        paths.push(`/draft_sections/${sectionIndex}/paragraphs/${paragraphIndex}/text`);
      }
    });
    section.subsections.forEach((subsection, subsectionIndex) => {
      subsection.paragraphs.forEach((paragraph, paragraphIndex) => {
        if (paragraph.text !== original.draft_sections[sectionIndex].subsections[subsectionIndex]?.paragraphs[paragraphIndex]?.text) {
          paths.push(`/draft_sections/${sectionIndex}/subsections/${subsectionIndex}/paragraphs/${paragraphIndex}/text`);
        }
      });
    });
  });
  return paths;
}

export function editAbstract(draft: PatentDraft, text: string): PatentDraft {
  if (draft.abstract.status !== "PRESENT") return draft;
  return {
    ...draft,
    abstract: { ...draft.abstract, text, word_count: countAbstractWords(text) },
  };
}

export function editParagraph(
  draft: PatentDraft,
  sectionIndex: number,
  subsectionIndex: number | null,
  paragraphIndex: number,
  text: string,
): PatentDraft {
  return {
    ...draft,
    draft_sections: draft.draft_sections.map((section, index) => {
      if (index !== sectionIndex || section.status !== "PRESENT") return section;
      if (subsectionIndex === null) {
        return {
          ...section,
          paragraphs: section.paragraphs.map((paragraph, position) =>
            position === paragraphIndex ? { ...paragraph, text } : paragraph,
          ),
        };
      }
      return {
        ...section,
        subsections: section.subsections.map((subsection, position) => {
          if (position !== subsectionIndex || subsection.status !== "PRESENT") return subsection;
          return {
            ...subsection,
            paragraphs: subsection.paragraphs.map((paragraph, itemIndex) =>
              itemIndex === paragraphIndex ? { ...paragraph, text } : paragraph,
            ),
          };
        }),
      };
    }),
  };
}
