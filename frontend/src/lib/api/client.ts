import type {
  ExportedDocx,
  ExportDocxRequest,
  DraftRevisionRequest,
  DraftValidationResult,
  NormalizedApiError,
  ProcessResult,
  UploadedDocument,
} from "@/lib/types/contracts";

const API_BASE = "/backend";
const DOCX_FILENAME = "patent-description-draft.docx" as const;

interface ErrorEnvelope {
  error?: {
    code?: unknown;
    message?: unknown;
    correlation_id?: unknown;
    paths?: unknown;
  };
}

export class ApiClientError extends Error implements NormalizedApiError {
  readonly status: number;
  readonly code: string;
  readonly correlation_id?: string;
  readonly paths?: string[];

  constructor(error: NormalizedApiError) {
    super(error.message);
    this.name = "ApiClientError";
    this.status = error.status;
    this.code = error.code;
    this.correlation_id = error.correlation_id;
    this.paths = error.paths;
  }
}

function fallbackMessage(status: number): string {
  if (status === 404) return "The document is unknown or has expired.";
  if (status === 413) return "The selected file exceeds the 10 MiB limit.";
  if (status === 415) return "Select a supported PDF or DOCX document.";
  if (status === 422) return "The submitted data could not be validated.";
  if (status === 429) return "The local service is temporarily rate limited. Try again later.";
  if (status === 504) return "Processing timed out. Start again with a new document.";
  if (status >= 500) return "The local service could not complete the request.";
  return "The request could not be completed.";
}

function safeServerMessage(value: unknown, status: number): string {
  if (typeof value !== "string") return fallbackMessage(status);
  const message = value.trim();
  const exposesInternalDetail =
    message.length > 500 ||
    /\b(?:provider|openai|api[_ -]?key|traceback|stack trace)\b/i.test(message) ||
    /\b[A-Za-z]:\\/.test(message) ||
    /\/(?:Users|home|var|tmp|etc)\//i.test(message);
  return !message || exposesInternalDetail ? fallbackMessage(status) : message;
}

async function toApiError(response: Response): Promise<ApiClientError> {
  let envelope: ErrorEnvelope = {};
  try {
    envelope = (await response.json()) as ErrorEnvelope;
  } catch {
    // A proxy or unavailable backend can return non-JSON. Use a safe local fallback.
  }
  const candidate = envelope.error;
  const headerCorrelationId = response.headers.get("x-correlation-id") ?? undefined;
  return new ApiClientError({
    status: response.status,
    code: typeof candidate?.code === "string" ? candidate.code : "request_failed",
    message: safeServerMessage(candidate?.message, response.status),
    correlation_id:
      typeof candidate?.correlation_id === "string"
        ? candidate.correlation_id
        : headerCorrelationId,
    paths: Array.isArray(candidate?.paths)
      ? candidate.paths.filter((path): path is string => typeof path === "string")
      : undefined,
  });
}

async function request(input: string, init?: RequestInit): Promise<Response> {
  try {
    const response = await fetch(`${API_BASE}${input}`, {
      ...init,
      headers: {
        Accept: "application/json",
        ...init?.headers,
      },
    });
    if (!response.ok) throw await toApiError(response);
    return response;
  } catch (error) {
    if (error instanceof ApiClientError) throw error;
    throw new ApiClientError({
      status: 0,
      code: "backend_unavailable",
      message: "The local backend is unavailable. Confirm that FastAPI is running.",
    });
  }
}

export async function uploadDocument(file: File): Promise<UploadedDocument> {
  const form = new FormData();
  form.append("file", file);
  const response = await request("/api/documents", { method: "POST", body: form });
  return (await response.json()) as UploadedDocument;
}

export async function getDocument(documentId: string): Promise<UploadedDocument> {
  const response = await request(`/api/documents/${encodeURIComponent(documentId)}`);
  return (await response.json()) as UploadedDocument;
}

export async function processDocument(documentId: string): Promise<ProcessResult> {
  const response = await request(
    `/api/documents/${encodeURIComponent(documentId)}/process`,
    { method: "POST" },
  );
  return (await response.json()) as ProcessResult;
}

export async function validateDraft(requestBody: DraftRevisionRequest): Promise<DraftValidationResult> {
  const response = await request("/api/drafts/validate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody),
  });
  return (await response.json()) as DraftValidationResult;
}

export async function exportDocx(requestBody: ExportDocxRequest): Promise<ExportedDocx> {
  const response = await request("/api/exports/docx", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody),
  });
  return { blob: await response.blob(), filename: DOCX_FILENAME };
}
