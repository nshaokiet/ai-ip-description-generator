export type WorkflowState =
  | "IDLE"
  | "UPLOADING"
  | "UPLOADED"
  | "PROCESSING"
  | "READY"
  | "EXPORTING"
  | "ERROR";

export type WorkflowPhase =
  | "upload"
  | "analyze"
  | "review"
  | "validate"
  | "export";

export type GroundingLabel = "SOURCE_FACT" | "PARAPHRASE" | "INFERENCE";

export interface Grounding {
  label: GroundingLabel;
  evidence_ids: string[];
}

export interface SourceDocumentMetadata {
  document_id: string;
  file_name: string;
  media_type: string;
  sha256?: string;
}

export interface UploadedDocument {
  document_id: string;
  original_filename: string;
  media_type: string;
  size_bytes: number;
  page_count?: number | null;
  validation_status: "validated";
}

export interface EvidenceLocator {
  page?: number;
  section?: string;
  paragraph_id?: string;
  chunk_id?: string;
  table_id?: string;
  figure_id?: string;
}

export interface Evidence {
  evidence_id: string;
  document_id: string;
  evidence_type: "TEXT" | "TABLE" | "FIGURE" | "METADATA";
  locator: EvidenceLocator;
  excerpt: string;
}

export interface AnalysisItem {
  title_id?: string;
  field_id?: string;
  statement_id?: string;
  problem_id?: string;
  solution_id?: string;
  component_id?: string;
  step_id?: string;
  feature_id?: string;
  effect_id?: string;
  embodiment_id?: string;
  experiment_id?: string;
  sequence?: number;
  title?: string;
  name?: string;
  text?: string;
  statement?: string;
  action?: string;
  description?: string;
  rationale?: string;
  conditions?: GroundedStatement[] | Measurement[];
  results?: Measurement[];
  grounding: Grounding;
}

export interface GroundedStatement {
  statement_id: string;
  text: string;
  grounding: Grounding;
}

export interface Measurement {
  parameter?: string;
  metric?: string;
  value: string | number;
  unit?: string;
}

export interface TechnicalField {
  status: "PRESENT" | "MISSING";
  item?: AnalysisItem;
  marker?: string;
  missing_information_ids?: string[];
}

export interface AnalysisMissingInformation {
  missing_id: string;
  target_path: string;
  description: string;
  reason: "NOT_FOUND" | "AMBIGUOUS" | "CONFLICTING" | "INSUFFICIENT_DETAIL";
  impact: "BLOCKING" | "HIGH" | "MEDIUM" | "LOW";
  owner: "AUTHOR" | "HUMAN_REVIEWER" | "IP_SPECIALIST";
  grounding_label: "MISSING";
}

export interface AnalysisAuthorQuestion {
  question_id: string;
  missing_information_id: string;
  question: string;
  priority: "HIGH" | "MEDIUM" | "LOW";
}

export interface InventionAnalysis {
  schema_version: "1.0.0";
  output_type: "STRUCTURED_INVENTION_ANALYSIS";
  output_notice: {
    status: "DRAFT";
    human_review_required: true;
    is_legal_advice: false;
    filing_ready: false;
    includes_patentability_assessment: false;
  };
  document_metadata: SourceDocumentMetadata;
  title_candidates: AnalysisItem[];
  technical_field: TechnicalField;
  background: AnalysisItem[];
  technical_problems: AnalysisItem[];
  technical_solutions: AnalysisItem[];
  components: AnalysisItem[];
  process_steps: AnalysisItem[];
  potential_distinguishing_features: AnalysisItem[];
  technical_effects: AnalysisItem[];
  embodiments: AnalysisItem[];
  experimental_data: AnalysisItem[];
  drawing_requirements: Array<{
    drawing_id: string;
    kind: "SOURCE_FIGURE" | "PROPOSED_DRAWING";
    title: string;
    status: "AVAILABLE" | "PROPOSED" | "MISSING";
    source_evidence_ids: string[];
    human_confirmation_required: boolean;
  }>;
  missing_information: AnalysisMissingInformation[];
  author_questions: AnalysisAuthorQuestion[];
  evidence: Evidence[];
}

export interface DraftParagraph {
  paragraph_id: string;
  sequence: number;
  text: string;
  source_paths: string[];
  grounding: Grounding;
}

export interface DraftSubsection {
  subsection_id: string;
  sequence: number;
  heading: string;
  status: "PRESENT" | "MISSING";
  paragraphs: DraftParagraph[];
  missing_information_ids: string[];
  marker?: string;
}

export interface DraftSection {
  section_id: string;
  sequence: number;
  heading: string;
  status: "PRESENT" | "MISSING";
  paragraphs: DraftParagraph[];
  subsections: DraftSubsection[];
  missing_information_ids: string[];
  marker?: string;
}

export interface DraftHeadlineContent {
  status: "PRESENT" | "MISSING";
  text?: string;
  word_count?: number;
  source_title_candidate_id?: string;
  source_paths?: string[];
  grounding?: Grounding;
  marker?: string;
  missing_information_ids?: string[];
}

export interface DraftMissingInformation {
  missing_id: string;
  origin: "SOURCE_ANALYSIS" | "DRAFT_VALIDATION";
  source_missing_information_id?: string;
  rule_id?: "TITLE_SELECTION_REQUIRED" | "ABSTRACT_SOURCE_INSUFFICIENT" | "SECTION_SOURCE_INSUFFICIENT" | "CONFLICT_REQUIRES_RESOLUTION";
  target_path: string;
  description: string;
  reason: "NOT_FOUND" | "AMBIGUOUS" | "CONFLICTING" | "INSUFFICIENT_DETAIL";
  impact: "BLOCKING" | "HIGH" | "MEDIUM" | "LOW";
  owner: "AUTHOR" | "HUMAN_REVIEWER" | "IP_SPECIALIST";
  grounding_label: "MISSING";
  affected_section_ids: string[];
  marker: "[AUTHOR CONFIRMATION REQUIRED]";
}

export interface DraftConflict {
  conflict_id: string;
  summary: string;
  source_paths: string[];
  evidence_ids: string[];
  affected_section_ids: string[];
  resolution_status: "UNRESOLVED";
  author_question_ids: string[];
  marker: "[AUTHOR CONFIRMATION REQUIRED]";
}

export interface DraftAuthorQuestion {
  question_id: string;
  origin: "SOURCE_ANALYSIS" | "DRAFT_VALIDATION";
  source_question_id?: string;
  question: string;
  priority: "HIGH" | "MEDIUM" | "LOW";
  source_paths: string[];
  related_missing_information_ids: string[];
  related_conflict_ids: string[];
  affected_section_ids: string[];
}

export interface EvidenceUsageReference {
  target_type: string;
  target_id: string;
}

export interface EvidenceAppendixItem extends Evidence {
  usage_references: EvidenceUsageReference[];
}

export interface DraftDrawing {
  drawing_id: string;
  source_drawing_id: string;
  kind: "SOURCE_FIGURE" | "PROPOSED_DRAWING";
  title: string;
  status: "AVAILABLE" | "PROPOSED" | "MISSING";
  source_paths: string[];
  evidence_ids: string[];
  human_confirmation_required: boolean;
}

export interface PatentDraft {
  schema_version: "1.0.0";
  output_type: "PATENT_DESCRIPTION_DRAFT";
  output_notice: {
    status: "DRAFT";
    notice: "AI-generated draft — requires human review.";
    human_review_required: true;
    is_legal_advice: false;
    filing_ready: false;
    includes_patentability_assessment: false;
    includes_claims: false;
  };
  document_metadata: {
    draft_id: string;
    language: string;
    source_schema_id: string;
    source_schema_version: string;
    source_output_type: string;
    source_document: SourceDocumentMetadata;
  };
  section_order: string[];
  selected_title: DraftHeadlineContent;
  abstract: DraftHeadlineContent;
  draft_sections: DraftSection[];
  drawings: DraftDrawing[];
  missing_information: DraftMissingInformation[];
  conflicts: DraftConflict[];
  author_questions: DraftAuthorQuestion[];
  evidence_appendix: EvidenceAppendixItem[];
}

export interface ProcessMetadata {
  document_id: string;
  correlation_id: string;
  source_cleanup_performed: boolean;
}

export interface ProcessResult {
  analysis: InventionAnalysis;
  draft: PatentDraft;
  metadata: ProcessMetadata;
}

export interface NormalizedApiError {
  status: number;
  code: string;
  message: string;
  correlation_id?: string;
  paths?: string[];
}

export interface DraftRevisionRequest {
  revision_id: string;
  analysis: InventionAnalysis;
  original_draft: PatentDraft;
  draft: PatentDraft;
  selected_title_candidate_id: string | null;
}

export interface DraftValidationResult {
  valid: true;
  revision_id: string;
  draft_digest: string;
  unverified_prose_paths: string[];
  correlation_id: string;
}

export interface ExportDocxRequest extends DraftRevisionRequest {
  validated_digest: string;
}

export interface ExportedDocx {
  blob: Blob;
  filename: "patent-description-draft.docx";
}
