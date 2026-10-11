"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useSyncExternalStore, type ReactNode } from "react";

export type ThemePreference = "system" | "light" | "dark";
export type Locale = "vi" | "en";

const messages = {
  upload: ["Tải tài liệu", "Source Upload"],
  extraction: ["Trích xuất", "AI Extraction"],
  review: ["Rà soát và hoàn thiện", "Review & Refine"],
  validation: ["Xác thực cấu trúc", "Validation"],
  export: ["Xuất bản nháp", "DOCX Export"],
  uploadDescription: ["Tải lên PDF hoặc DOCX", "Upload PDF or DOCX"],
  extractionDescription: ["Trích xuất nội dung", "Extract key content"],
  reviewDescription: ["Kiểm tra bản dự thảo", "Review draft"],
  validationDescription: ["Kiểm tra các mục bắt buộc", "Check required sections"],
  exportDescription: ["Tải DOCX có thể chỉnh sửa", "Download editable file"],
  tagline: ["Quy trình dự thảo sáng chế có chứng cứ nguồn", "Evidence-grounded patent drafting workflow"],
  heroTitle: ["Từ bài báo khoa học đến bản dự thảo mô tả sáng chế theo cấu trúc USPTO", "From Scientific Research Paper to USPTO-Style Patent Specification"],
  heroDescription: ["Tải bài báo PDF hoặc DOCX, kiểm tra nội dung trích xuất, rà soát và sửa bản dự thảo, xác thực cấu trúc và xuất DOCX để chuyên gia tiếp tục đánh giá.", "Upload a PDF or DOCX research paper, review the extracted content and draft, validate its structure, then export an editable DOCX for expert review."],
  theme: ["Giao diện", "Appearance"],
  locale: ["Ngôn ngữ", "Language"],
  system: ["Theo hệ thống", "System"],
  light: ["Sáng", "Light"],
  dark: ["Tối", "Dark"],
  back: ["← Quay lại", "← Go back"],
  uploadTitle: ["Tải bài báo khoa học", "Upload a research document"],
  dragDrop: ["Kéo thả bài báo vào đây", "Drag & drop your research paper here"],
  selectFile: ["Chọn tài liệu", "Select document"],
  fileConstraints: ["PDF hoặc DOCX · Tối đa 10 MiB", "PDF or DOCX · Max 10 MiB"],
  localSelected: ["Đã chọn trên thiết bị · chưa tải lên", "Selected locally · not uploaded"],
  uploadValidate: ["Tải lên và kiểm tra", "Upload & Validate"],
  remove: ["Xóa tệp đã chọn", "Remove selected file"],
  processing: ["Đang xử lý tài liệu…", "Processing document…"],
  uploadedTitle: ["Đã tải bài báo thành công", "Paper uploaded successfully"],
  uploadedDescription: ["Dịch vụ đã chấp nhận tài liệu. Chuyển sang bước tiếp theo.", "The service accepted your document. Continue to the next stage."],
  continueExtraction: ["Tiếp tục trích xuất →", "Continue to AI Extraction →"],
  continueReview: ["Tiếp tục rà soát →", "Continue to Review & Refine →"],
  demo: ["Không sử dụng nhà cung cấp AI trực tiếp. Bản demo chỉ xử lý mẫu tổng hợp có sẵn. Tệp riêng chỉ được chọn trên giao diện; chưa chuyển đổi bằng AI.", "No live AI provider is used. This demo processes controlled synthetic samples only. Your own file can be selected, but is not AI-converted."],
  sample: ["Thử bài báo tổng hợp:", "Try a synthetic paper:"],
  draftWarning: ["Đây là bản dự thảo, không phải bằng sáng chế hoặc hồ sơ sẵn sàng nộp. Cần chuyên gia kỹ thuật và sở hữu trí tuệ rà soát.", "This is a draft, not an issued patent or filing-ready submission. Technical and IP specialist review is required."],
  newPaper: ["Tài liệu mới", "New paper"],
  revision: ["Phiên bản dự thảo", "Draft revision"],
  save: ["Lưu thành phiên bản mới", "Save new revision"],
  cancel: ["Hủy chỉnh sửa", "Cancel edit"],
  edit: ["Sửa nội dung", "Edit prose"],
  sectionList: ["Các mục dự thảo", "Draft sections"],
  evidence: ["Chứng cứ nguồn", "Source evidence"],
  noEvidence: ["Không có chứng cứ nguồn trong phụ lục.", "No source evidence in this appendix."],
  inspectEvidence: ["Xem chứng cứ nguồn", "Inspect source evidence"],
  reviewItems: ["Các mục cần rà soát", "Review Items"],
  analysis: ["Phân tích", "Analysis"],
  patentDraft: ["Bản dự thảo", "Patent Draft"],
  validationRequired: ["Cần xác thực", "Validation required"],
  validationComplete: ["Đã xác thực cấu trúc", "Validation complete"],
  exportAction: ["Xuất", "Export"],
  exportDocx: ["Tải DOCX dự thảo có thể chỉnh sửa (v1)", "Download editable DOCX draft (v1)"],
  exportUnavailable: ["PDF và các định dạng P2-006 chưa khả dụng tại giao diện này.", "PDF and P2-006 formats are not available in this interface."],
  technicalOnly: ["Xác thực cấu trúc không phải phê duyệt của con người hay kết luận pháp lý.", "Technical validation only · not Human or legal approval"],
  missing: ["Thiếu thông tin — cần tác giả xác nhận", "Missing information — author confirmation required"],
  unsaved: ["Có chỉnh sửa chưa lưu. Rời khỏi sẽ mất thay đổi.", "You have unsaved changes. Leaving will discard them."],
  stay: ["Tiếp tục chỉnh sửa", "Keep editing"],
  discard: ["Bỏ thay đổi và tiếp tục", "Discard changes and continue"],
  confirmTitle: ["Xác nhận thay đổi phiên làm việc", "Confirm session change"],
  validationFailed: ["Xác thực thất bại. Kiểm tra các trường bị báo lỗi.", "Validation failed. Inspect the affected fields."],
  error: ["Không thể hoàn thành thao tác", "We could not complete that operation"],
  errorGeneric: ["Thao tác không thành công. Vui lòng thử lại.", "The operation could not be completed. Please try again."],
  reference: ["Mã tham chiếu", "Reference ID"],
  unsupportedFile: ["Chỉ chấp nhận một tệp PDF hoặc DOCX.", "Choose one PDF or DOCX file."],
  tooLarge: ["Tệp vượt quá giới hạn 10 MiB.", "File exceeds the 10 MiB limit."],
  emptyFile: ["Tệp được chọn không có dữ liệu.", "The selected file is empty."],
  oneFile: ["Chỉ chọn một tài liệu.", "Choose exactly one document."],
  fileReplace: ["Chọn tệp khác", "Select a different file"],
  fileReset: ["Xóa phiên và bắt đầu lại", "Clear session and start over"],
  details: ["Chi tiết kỹ thuật", "Technical details"],
  legalFooter: ["Kết quả cần được chuyên gia kỹ thuật và sở hữu trí tuệ rà soát trước khi sử dụng chính thức.", "Technical and IP specialists must review this draft before any formal use."],
  saved: ["Đã lưu", "Saved"],
  editing: ["Đang chỉnh sửa", "Editing"],
  unsavedShort: ["Chưa lưu thay đổi", "Unsaved changes"],
  sessionOnly: ["Các phiên bản chỉ lưu trong phiên trình duyệt này. Tải lại trang sẽ mất dữ liệu rà soát và chỉnh sửa.", "Revisions are stored in this browser session only. Reloading loses reviews and edits."],
  resetQuestion: ["Xóa phiên hiện tại và bắt đầu tài liệu mới?", "Clear this session and start a new paper?"],
  resetDescription: ["Phân tích, phiên bản dự thảo, kết quả rà soát và xác thực sẽ bị xóa khỏi phiên này.", "Analysis, draft revisions, review status and validation will be cleared from this session."],
  selectedRevision: ["Phiên bản đang chọn", "Selected revision"],
  generated: ["bản tạo tự động", "generated"],
  revised: ["bản đã chỉnh sửa", "edited"],
  validationHeading: ["Xác thực phiên bản đã chọn", "Validate the selected revision"],
  validationPassed: ["Cấu trúc và các trường bắt buộc đã được backend xác thực cho phiên bản", "Structure and required fields passed server validation for revision"],
  validationInstruction: ["Chạy xác thực trên máy chủ cho đúng phiên bản đã lưu trước khi xuất.", "Run existing server validation against the exact saved revision before export."],
  validationAction: ["Xác thực", "Validate"],
  validating: ["Đang xác thực", "Validating"],
  validationBusy: ["Phiên bản đang chọn được giữ nguyên và yêu cầu trùng lặp bị chặn.", "The selected revision is preserved and duplicate requests are blocked."],
  validationPassedLabel: ["Xác thực cấu trúc đạt", "Structural validation passed"],
  validationErrorTitle: ["Xác thực dự thảo thất bại", "Draft validation failed"],
  validationRecover: ["Sửa phiên bản này", "Edit this revision"],
  validationRecoverHelp: ["Phiên bản đã lưu vẫn còn để chỉnh sửa.", "The saved revision remains available for correction."],
  affectedFields: ["Trường liên quan", "Affected fields"],
  goToField: ["Đi đến trường", "Go to field"],
  returnReview: ["Quay lại rà soát", "Return to Review & Refine"],
  reviewValidation: ["Xem xác thực", "Review validation"],
  continueValidation: ["Tiếp tục xác thực →", "Continue to Validation →"],
  continueExport: ["Tiếp tục xuất DOCX →", "Continue to DOCX Export →"],
  preparingDocx: ["Đang chuẩn bị DOCX…", "Preparing DOCX…"],
  exportBusy: ["Giữ trang mở trong khi tạo DOCX; không thể gửi yêu cầu xuất trùng.", "Keep this page open while DOCX is prepared; duplicate exports are blocked."],
  reviewIntro: ["Rà soát bản dự thảo, sửa nội dung và đối chiếu chứng cứ nguồn trước khi xác thực.", "Review the generated patent draft, refine prose, and inspect supporting evidence before validation."],
  reviewSummary: ["Rà soát", "Review"],
  statusUnreviewed: ["CHƯA RÀ SOÁT", "UNREVIEWED"],
  statusReviewed: ["ĐÃ RÀ SOÁT (chưa phê duyệt)", "REVIEWED (not approved)"],
  statusNeedsChanges: ["CẦN SỬA", "NEEDS_CHANGES"],
  reviewAll: ["Rà soát tất cả các mục trước khi xác thực", "Review all sections before validation"],
  reviewDone: ["Đã rà soát tất cả các mục của phiên bản này.", "All sections reviewed for this revision."],
  reviewRemaining: ["mục còn lại", "remaining"],
  validated: ["ĐÃ XÁC THỰC", "VALIDATED"],
  notValidated: ["CHƯA XÁC THỰC", "NOT VALIDATED"],
  exportTarget: ["Phiên bản xuất", "Export target"],
  eligible: ["đủ điều kiện", "eligible"],
  editorSupport: ["Nội dung sửa chưa được đối chiếu ngữ nghĩa với nguồn. Liên kết chứng cứ không tự thay đổi; cần người có chuyên môn rà soát.", "Edited prose has unverified semantic source support. Evidence links remain unchanged; specialist review is required."],
  missingTitle: ["Tiêu đề: THIẾU", "Title: MISSING"],
  missingContent: ["THIẾU", "MISSING"],
  missingRelated: ["Mục liên quan", "Related items"],
  abstract: ["Tóm tắt", "Abstract"],
  words: ["từ", "words"],
  maxWords: ["tối đa 150", "150 maximum"],
  paragraph: ["Đoạn", "Paragraph"],
  prose: ["nội dung", "prose"],
  groundingFor: ["Phân loại căn cứ cho", "Grounding for"],
  sourcePaths: ["Đường dẫn nguồn", "Source paths"],
  evidenceLabel: ["Chứng cứ", "Evidence"],
  fieldRejected: ["Backend từ chối trường này. Kiểm tra nội dung và căn cứ nguồn.", "Backend rejected this field. Check content and source support."],
  appendix: ["Phụ lục chứng cứ và tham chiếu", "Evidence and reference appendix"],
  reviewStatus: ["Trạng thái rà soát trong phiên cho", "Session review status for"],
  humanReviewDraft: ["Bản nháp AI cần con người rà soát", "AI-generated draft for human review"],
  notLegal: ["Không phải tư vấn pháp lý hoặc hồ sơ sẵn sàng nộp. Cần chuyên gia rà soát.", "Not legal advice or filing-ready. Specialist review is required."],
  editorWarning: ["Chỉnh sửa không tạo chứng cứ mới hay xác minh tuyên bố kỹ thuật. Nhãn và liên kết nguồn được giữ nguyên.", "Editing does not create evidence or verify technical claims. Grounding labels and source links remain unchanged."],
  missingCount: ["mục thiếu thông tin cần rà soát", "missing-information items require attention"],
  conflictCount: ["xung đột chưa giải quyết", "conflicts remain unresolved"],
  analysisTitle: ["Phân tích sáng chế có cấu trúc", "Structured invention analysis"],
  analysisIntro: ["Các phát biểu kỹ thuật giữ liên kết nguồn; phần suy luận được phân biệt với sự kiện trực tiếp.", "Technical statements retain source links; inferences are distinguished from direct source facts."],
  titleCandidates: ["Tiêu đề đề xuất", "Title candidates"],
  technicalField: ["Lĩnh vực kỹ thuật", "Technical field"],
  background: ["Bối cảnh kỹ thuật", "Background"],
  technicalProblems: ["Vấn đề kỹ thuật", "Technical problems"],
  technicalSolutions: ["Giải pháp kỹ thuật", "Technical solutions"],
  components: ["Thành phần", "Components"],
  processSteps: ["Các bước quy trình", "Process steps"],
  distinguishing: ["Đặc điểm có thể khác biệt", "Potential distinguishing features"],
  technicalEffects: ["Hiệu quả kỹ thuật", "Technical effects"],
  embodiments: ["Phương án thực hiện", "Embodiments"],
  experimentalData: ["Dữ liệu thực nghiệm", "Experimental data"],
  missingInformation: ["Thông tin còn thiếu", "Missing information"],
  authorQuestions: ["Câu hỏi dành cho tác giả", "Author questions"],
  unresolvedConflicts: ["Xung đột chưa giải quyết", "Unresolved conflicts"],
  inferenceContent: ["Nội dung suy luận", "Inference content"],
  reviewQueue: ["Danh sách rà soát của con người", "Human review queue"],
  attentionCount: ["mục cần xem xét", "items require attention"],
  noMissing: ["Không có mục thông tin thiếu nào.", "No missing-information items returned."],
  noConflicts: ["Không có xung đột nào.", "No unresolved conflicts returned."],
  noQuestions: ["Không có câu hỏi tác giả nào.", "No author questions returned."],
  noInferences: ["Không có nội dung gắn nhãn suy luận.", "No inference-labelled content returned."],
  fromAnalysis: ["Từ phân tích có cấu trúc", "From structured analysis"],
  affected: ["Mục bị ảnh hưởng", "Affected"],
  conditions: ["Điều kiện", "Conditions"],
  results: ["Kết quả", "Results"],
  rationale: ["Lý do", "Rationale"],
  owner: ["Phụ trách", "Owner"],
  relatedItem: ["Mục liên quan", "Related item"],
  usedBy: ["Được sử dụng bởi", "Used by"],
  sourceLocator: ["Vị trí trong nguồn", "Source locator"],
  page: ["Trang", "Page"],
  section: ["Mục", "Section"],
  chunk: ["Đoạn dữ liệu", "Chunk"],
  table: ["Bảng", "Table"],
  figure: ["Hình", "Figure"],
  processingUpload: ["Đang tải lên và kiểm tra tài liệu.", "Uploading and validating the document."],
  processingExtract: ["Đang trích xuất nội dung kỹ thuật và lập bản nháp có chứng cứ.", "Extracting technical content and preparing a grounded draft."],
  processingExport: ["Đang chuẩn bị DOCX để tải xuống.", "Preparing the editable DOCX download."],
  readyForReview: ["Bản nháp sẵn sàng để rà soát.", "The draft is ready for review."],
  returnResults: ["Quay lại kết quả", "Return to results"],
  chooseAnother: ["Chọn tài liệu khác", "Choose another document"],
  extractionDone: ["Đã trích xuất xong", "Extraction complete"],
  extractionCached: ["Kết quả phân tích và bản nháp đã có trong phiên. Tiếp tục sẽ không xử lý lại.", "Analysis and grounded draft are already available in this session. Continue will not rerun processing."],
  requestFailed: ["Yêu cầu không hoàn thành", "Request not completed"],
  workspaceNav: ["Quy trình tạo dự thảo", "Document workflow"],
  resultViews: ["Các chế độ xem kết quả", "Result views"],
  draftingWorkflow: ["Quy trình soạn thảo sáng chế", "Patent drafting workflow"],
  resetSourceDescription: ["Việc này sẽ xóa kết quả phân tích, bản dự thảo, các phiên bản, trạng thái rà soát và xác thực hiện tại.", "This clears the current analysis, drafts, revisions, review status, and validation."],
  anotherSample: ["Chọn mẫu khác", "Select another sample"],
  extractTitle: ["Đang trích xuất nội dung kỹ thuật", "Extracting invention-relevant content"],
  extractHelp: ["Xác định nội dung kỹ thuật và chuẩn bị bản dự thảo có chứng cứ nguồn.", "Identifying technical concepts and preparing a grounded draft for review."],
  or: ["hoặc", "or"],
  samplePdfLabel: ["Mẫu PDF (.pdf)", "Sample PDF (.pdf)"],
  sampleDocxLabel: ["Mẫu DOCX (.docx)", "Sample DOCX (.docx)"],
  localDemoFile: ["Đã chọn trên máy · AI đang chờ kinh phí", "Selected locally · AI conversion pending funding"],
  uploadBusyTitle: ["Đang tải và kiểm tra tài liệu…", "Uploading and checking the selected document…"],
  uploadBusyHelp: ["Không thể tải thêm cho đến khi yêu cầu hoàn tất.", "Another upload cannot start until this request finishes."],
  sessionScope: ["Tài liệu được xử lý trong phạm vi phiên làm việc.", "Document processing is scoped to this session."],
  serverAuthority: ["Kiểm tra trên trình duyệt chỉ hỗ trợ thao tác. Backend quyết định kết quả xác thực.", "Client checks are for convenience. The backend remains the validation source of truth."],
  attention: ["Cần chú ý", "Requires attention"],
  copyright: ["© 2026 VNUHCM Innovation Hub. Bảo lưu mọi quyền.", "© 2026 VNUHCM Innovation Hub. All rights reserved."],
  samplePdf: ["Dùng mẫu PDF tổng hợp", "Use synthetic PDF demo"],
  sampleDocx: ["Dùng mẫu DOCX tổng hợp", "Use synthetic DOCX demo"],
  mediaType: ["Loại tài liệu", "Media type"],
  documentId: ["Mã tài liệu", "Document ID"],
  serviceError: ["Dịch vụ cục bộ không thể hoàn thành yêu cầu.", "The local service could not complete the request."],
  uploadError: ["Tài liệu không được chấp nhận. Chọn một PDF hoặc DOCX hợp lệ.", "The document was rejected. Choose a valid PDF or DOCX."],
  revisionError: ["Phiên bản không khớp kết quả xác thực. Rà soát và xác thực lại.", "The revision does not match its validation. Review and validate again."],
  complete: ["Đã hoàn tất", "complete"],
  current: ["Đang thực hiện", "current"],
  upcoming: ["Chưa khả dụng", "unavailable"],
  reachable: ["Có thể truy cập", "available"],
} as const satisfies Record<string, readonly [string, string]>;

export type MessageKey = keyof typeof messages;
const publicErrorCodes = new Set(["stale_draft_revision", "draft_digest_mismatch", "invalid_request", "invalid_file_type", "file_too_large", "empty_file", "invalid_pdf", "invalid_docx", "invalid_document", "document_validation_failed", "backend_unavailable", "draft_business_validation_failed", "draft_canonical_validation_failed", "edited_draft_validation_failed", "unexpected_client_error", "request_failed", "upstream_failure"]);
export function displayErrorCode(code: string): string { return publicErrorCodes.has(code) ? code : "request_failed"; }
export function localizedError(code: string, t: (key: MessageKey) => string): string {
  if (/^(?:invalid_file_type|file_too_large|empty_file|invalid_pdf|invalid_docx|invalid_document|document_validation_failed)$/.test(code)) return t("uploadError");
  if (/^(?:stale_draft_revision|draft_digest_mismatch|revision_mismatch)$/.test(code)) return t("revisionError");
  if (/^(?:draft_.*validation_failed|edited_draft_invalid|invalid_request)$/.test(code)) return t("validationFailed");
  return t("serviceError");
}
const preferenceContext = createContext<{
  theme: ThemePreference; setTheme: (value: ThemePreference) => void;
  locale: Locale; setLocale: (value: Locale) => void;
  t: (key: MessageKey) => string;
} | null>(null);

function isTheme(value: string | null): value is ThemePreference { return value === "system" || value === "light" || value === "dark"; }
function isLocale(value: string | null): value is Locale { return value === "vi" || value === "en"; }

const PREFERENCE_EVENT = "aiip-preferences-changed";
let transientTheme: ThemePreference = "system";
let transientLocale: Locale = "vi";
function subscribePreferences(listener: () => void) {
  window.addEventListener("storage", listener);
  window.addEventListener(PREFERENCE_EVENT, listener);
  return () => {
    window.removeEventListener("storage", listener);
    window.removeEventListener(PREFERENCE_EVENT, listener);
  };
}
function readTheme(): ThemePreference {
  try { const stored = localStorage.getItem("aiip.theme"); return isTheme(stored) ? stored : "system"; }
  catch { return transientTheme; }
}
function readLocale(): Locale {
  try { const stored = localStorage.getItem("aiip.locale"); return isLocale(stored) ? stored : "vi"; }
  catch { return transientLocale; }
}

export function UiPreferencesProvider({ children }: { children: ReactNode }) {
  const theme = useSyncExternalStore<ThemePreference>(subscribePreferences, readTheme, () => "system");
  const locale = useSyncExternalStore<Locale>(subscribePreferences, readLocale, () => "vi");
  const setTheme = useCallback((value: ThemePreference) => {
    transientTheme = value;
    try { localStorage.setItem("aiip.theme", value); } catch { /* Storage unavailable. */ }
    window.dispatchEvent(new Event(PREFERENCE_EVENT));
  }, []);
  const setLocale = useCallback((value: Locale) => {
    transientLocale = value;
    try { localStorage.setItem("aiip.locale", value); } catch { /* Storage unavailable. */ }
    window.dispatchEvent(new Event(PREFERENCE_EVENT));
  }, []);

  useEffect(() => {
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const sync = () => {
      document.documentElement.dataset.theme = theme === "system" ? (media.matches ? "dark" : "light") : theme;
    };
    sync();
    media.addEventListener("change", sync);
    return () => media.removeEventListener("change", sync);
  }, [theme]);

  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);

  const value = useMemo(() => ({ theme, setTheme, locale, setLocale, t: (key: MessageKey) => messages[key][locale === "vi" ? 0 : 1] }), [theme, locale, setTheme, setLocale]);
  return <preferenceContext.Provider value={value}>{children}</preferenceContext.Provider>;
}

export function useUi() {
  const context = useContext(preferenceContext);
  if (!context) throw new Error("UI preferences provider missing");
  return context;
}
