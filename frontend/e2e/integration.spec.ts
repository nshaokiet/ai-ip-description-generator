import { execFileSync } from "node:child_process";
import path from "node:path";

import { expect, test, type Download, type Page } from "@playwright/test";

const backend = `http://127.0.0.1:${process.env.PLAYWRIGHT_BACKEND_PORT ?? "8000"}`;
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => { window.localStorage.setItem("aiip.locale", "en"); });
});
const mediaTypes = {
  pdf: "application/pdf",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
};

function deferred() {
  let release!: () => void;
  const promise = new Promise<void>((resolve) => { release = resolve; });
  return { promise, release };
}

async function downloadedDocxText(download: Download): Promise<string> {
  const root = path.resolve(__dirname, "../..");
  const python = process.env.PLAYWRIGHT_PYTHON ??
    path.join(root, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const helper = path.join(root, "tests/e2e/inspect_docx.py");
  const output = execFileSync(python, [helper, await download.path()], { encoding: "utf8" });
  return (JSON.parse(output) as { text: string }).text;
}

async function uploadSynthetic(page: Page, format: "pdf" | "docx", options: { missing?: boolean; keyboard?: boolean } = {}) {
  await page.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.protocol.startsWith("http") && !["127.0.0.1", "localhost"].includes(url.hostname)) {
      await route.abort();
    } else {
      await route.continue();
    }
  });
  const fixture = await page.request.get(`${backend}/__test/${format}`);
  expect(fixture.ok()).toBeTruthy();
  await page.goto("/");
  const file = {
    name: options.missing ? "synthetic-missing.pdf" : `synthetic.${format}`,
    mimeType: mediaTypes[format],
    buffer: await fixture.body(),
  };
  if (options.keyboard) {
    const chooserPromise = page.waitForEvent("filechooser");
    const button = page.getByRole("button", { name: "Select document" });
    await button.focus();
    await expect(button).toBeFocused();
    await page.keyboard.press("Enter");
    await (await chooserPromise).setFiles(file);
  } else {
    await page.locator("#document-file").setInputFiles(file);
  }
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toBeVisible();
}

async function processSynthetic(page: Page, format: "pdf" | "docx", options: { missing?: boolean; keyboard?: boolean } = {}) {
  await uploadSynthetic(page, format, options);
  const processResponse = page.waitForResponse((response) => response.url().includes("/process") && response.request().method() === "POST");
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  const processed = await (await processResponse).json() as { draft: Record<string, unknown> };
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  await page.getByRole("tab", { name: "Patent Draft" }).click();
  await expect(page.getByRole("heading", { name: "Title: MISSING" })).toBeVisible();
  await expect(page.getByText("[AUTHOR CONFIRMATION REQUIRED]").first()).toBeVisible();
  return processed;
}

function firstParagraph(page: Page) {
  return page.getByLabel("Paragraph paragraph-field prose");
}

async function completeHumanReview(page: Page) {
  const controls = page.getByLabel(/^Session review status for /);
  const total = await controls.count();
  expect(total).toBeGreaterThan(0);
  for (let index = 0; index < total; index += 1) {
    await controls.nth(index).selectOption("REVIEWED");
  }
  await expect(page.getByText(`Review: 0 UNREVIEWED · ${total} REVIEWED (not approved) · 0 NEEDS_CHANGES`)).toBeVisible();
  return total;
}

async function enterValidation(page: Page, revisionId: string) {
  await page.getByRole("button", { name: `Continue to Validation → · ${revisionId}` }).click();
  await expect(page.getByRole("heading", { name: /Validate the selected revision|Validation complete/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /4\. Validation/ })).toHaveAttribute("aria-current", "step");
}

async function validateRevision(page: Page, revisionId: string) {
  await completeHumanReview(page);
  await enterValidation(page, revisionId);
  await page.getByRole("button", { name: `Validate ${revisionId}` }).click();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  await expect(page.getByRole("paragraph").filter({ hasText: "Technical validation only · not Human or legal approval" })).toBeVisible();
}

async function enterExport(page: Page) {
  await page.getByRole("button", { name: "Continue to DOCX Export →" }).click();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");
}

test("local document response includes defensive security headers", async ({ page }) => {
  const response = await page.goto("/");
  expect(response).not.toBeNull();
  expect(response?.headers()["cache-control"]).toBe("no-store");
  expect(response?.headers()["x-content-type-options"]).toBe("nosniff");
  expect(response?.headers()["referrer-policy"]).toBe("no-referrer");
  expect(response?.headers()["x-frame-options"]).toBe("DENY");
  expect(response?.headers()["permissions-policy"]).toBe("camera=(), geolocation=(), microphone=()");
});

test("P2-000 home presents the approved enterprise workflow and gated stages", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", {
    name: "From Scientific Research Paper to USPTO-Style Patent Specification",
  })).toBeVisible();
  const workflow = page.getByRole("navigation", { name: "Patent drafting workflow" });
  await expect(workflow.getByRole("button")).toHaveCount(5);
  for (const [index, label] of [
    "Source Upload",
    "AI Extraction",
    "Review & Refine",
    "Validation",
    "DOCX Export",
  ].entries()) {
    const step = workflow.getByRole("button", { name: new RegExp(`${index + 1}\\. ${label}`) });
    await expect(step).toBeVisible();
    if (index === 0) await expect(step).toHaveAttribute("aria-current", "step");
    else await expect(step).toBeDisabled();
  }
  await expect(page.locator(".hero-notice")).toHaveCount(0);
  await expect(page.locator(".environment-badge")).toHaveCount(0);
  const logo = page.getByRole("img", { name: "VNUHCM Innovation Hub" });
  await expect(logo).toBeVisible();
  await logo.evaluate((image: HTMLImageElement) => image.decode());
  await expect(logo).toHaveCSS("object-fit", "contain");
  const logoBox = await logo.boundingBox();
  // UIUX-003 explicitly reduces the UIUX-002 190px logo by 10–15%.
  expect(logoBox?.width ?? 0).toBeGreaterThanOrEqual(190 * .85);
  expect(logoBox?.width ?? 0).toBeLessThanOrEqual(190 * .9);
  expect(logoBox?.height ?? 0).toBeGreaterThanOrEqual(50);
  const uploadCardBox = await page.locator(".upload-card").boundingBox();
  expect(uploadCardBox?.width ?? 0).toBeGreaterThanOrEqual(900);
  await expect(page.locator("#document-file")).toHaveAttribute(
    "accept",
    ".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  );
  const headerWidth = await page.locator(".site-header").evaluate((header) => ({
    content: header.scrollWidth,
    viewport: window.innerWidth,
  }));
  expect(headerWidth.content).toBeLessThanOrEqual(headerWidth.viewport);
  const backButton = page.getByRole("button", { name: "Go back" });
  await expect(backButton).toBeVisible();
  await expect(backButton).toBeDisabled();
});

test("local PDF and DOCX selections can be cleared and immediately re-selected", async ({ page }) => {
  let uploadRequests = 0;
  page.on("request", (request) => {
    if (request.method() === "POST" && request.url().endsWith("/backend/api/documents")) {
      uploadRequests += 1;
    }
  });

  for (const file of [
    { name: "same-local-paper.pdf", mimeType: mediaTypes.pdf, buffer: Buffer.from("%PDF-1.7\nlocal-selection") },
    { name: "same-local-paper.docx", mimeType: mediaTypes.docx, buffer: Buffer.from("local-docx-selection") },
  ]) {
    await page.goto("/");
    const input = page.locator("#document-file");
    await input.setInputFiles(file);
    await expect(page.getByText(file.name, { exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: "Upload & Validate" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Remove selected file" })).toBeVisible();

    await page.getByRole("button", { name: "Remove selected file" }).click();
    await expect(page.getByText(file.name, { exact: true })).toHaveCount(0);
    await expect(input).toHaveValue("");

    await input.setInputFiles(file);
    await expect(page.getByText(file.name, { exact: true })).toBeVisible();
    await page.getByRole("button", { name: "Remove selected file" }).click();
    await expect(input).toHaveValue("");
  }

  expect(uploadRequests).toBe(0);
});

test("uploaded paper can be removed before extraction", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  await expect(page.getByText("synthetic.pdf", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Remove selected file" }).click();
  await expect(page.getByRole("heading", { name: "Upload a research document" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Continue to AI Extraction" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /2\. AI Extraction/ })).toBeDisabled();
});

test("uploaded paper can be replaced before extraction without stale source state", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  const docx = await page.request.get(`${backend}/__test/docx`);
  expect(docx.ok()).toBeTruthy();
  await page.locator("#replacement-document-file").setInputFiles({
    name: "replacement.docx",
    mimeType: mediaTypes.docx,
    buffer: await docx.body(),
  });
  await expect(page.getByText("replacement.docx", { exact: true })).toBeVisible();
  await expect(page.getByText("synthetic.pdf", { exact: true })).toHaveCount(0);
});

test("reached-step navigation reuses results and product Go back does not reprocess", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  await expect(page.getByRole("button", { name: "Go back" })).toBeEnabled();
  let processRequests = 0;
  page.on("request", (request) => {
    if (request.method() === "POST" && request.url().includes("/process")) processRequests += 1;
  });
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  expect(processRequests).toBe(1);

  await page.getByRole("button", { name: /2\. AI Extraction/ }).click();
  await expect(page.getByRole("heading", { name: "Extraction complete" })).toBeVisible();
  await page.getByRole("button", { name: /3\. Review & Refine/ }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  await page.getByRole("button", { name: "Go back" }).click();
  await expect(page.getByRole("heading", { name: "Extraction complete" })).toBeVisible();
  expect(processRequests).toBe(1);
});

test("new paper and downstream source removal require explicit session reset", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await page.getByRole("button", { name: /1\. Source Upload/ }).click();
  await page.getByRole("button", { name: "Remove selected file" }).click();
  await expect(page.getByText("This clears the current analysis, drafts, revisions, review status, and validation.")).toBeVisible();
  await page.getByRole("button", { name: "Keep editing" }).click();
  await expect(page.getByText("synthetic.pdf", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: /3\. Review & Refine/ }).click();
  await page.getByRole("button", { name: "New paper" }).click();
  await expect(page.getByText("Clear this session and start a new paper?", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Clear session and start over" }).click();
  await expect(page.getByRole("heading", { name: "Upload a research document" })).toBeVisible();
  await expect(page.getByLabel("Selected revision")).toHaveCount(0);
});

async function saveParagraphRevision(page: Page, replacement: string) {
  await page.getByRole("button", { name: "Edit prose" }).click();
  await firstParagraph(page).fill(replacement);
  await expect(page.getByText("Unsaved changes")).toBeVisible();
  await page.getByRole("button", { name: "Save new revision" }).click();
  await expect(page.getByLabel("Selected revision", { exact: true })).toHaveValue("revision-2");
}

test("result tabs support roving focus and Arrow/Home/End navigation", async ({ page }) => {
  await processSynthetic(page, "pdf");
  const analysis = page.getByRole("tab", { name: "Analysis" });
  const draft = page.getByRole("tab", { name: "Patent Draft" });
  const review = page.getByRole("tab", { name: "Review Items" });

  await draft.focus();
  await expect(draft).toBeFocused();
  await expect(draft).toHaveAttribute("tabindex", "0");
  await expect(analysis).toHaveAttribute("tabindex", "-1");
  await page.keyboard.press("ArrowRight");
  await expect(review).toBeFocused();
  await expect(review).toHaveAttribute("aria-selected", "true");
  await expect(review).toHaveAttribute("tabindex", "0");
  await expect(draft).toHaveAttribute("aria-selected", "false");
  await page.keyboard.press("ArrowRight");
  await expect(analysis).toBeFocused();
  await expect(analysis).toHaveAttribute("aria-selected", "true");
  await page.keyboard.press("ArrowLeft");
  await expect(review).toBeFocused();
  await page.keyboard.press("Home");
  await expect(draft).toBeFocused();
  await page.keyboard.press("End");
  await expect(analysis).toBeFocused();
  await expect(analysis).toHaveAttribute("aria-selected", "true");
});

test("editing keeps keyboard navigation on the only enabled draft tab", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await page.getByRole("button", { name: "Edit prose" }).click();
  const draft = page.getByRole("tab", { name: "Patent Draft" });
  await expect(page.getByRole("tab", { name: "Analysis" })).toBeDisabled();
  await expect(page.getByRole("tab", { name: "Review Items" })).toBeDisabled();
  await draft.focus();
  for (const key of ["ArrowRight", "ArrowLeft", "Home", "End"]) {
    await page.keyboard.press(key);
    await expect(draft).toBeFocused();
    await expect(draft).toHaveAttribute("aria-selected", "true");
  }
});

test("new global operation error focuses its heading", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  await page.route("**/backend/api/documents/*/process", async (route) => {
    const processed = await route.fetch();
    expect(processed.ok()).toBeTruthy();
    await route.fulfill({ status: 502, contentType: "text/plain", body: "synthetic proxy fault" });
  });
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  const heading = page.getByRole("heading", { name: "We could not complete that operation" });
  await expect(heading).toBeVisible();
  await expect(heading).toBeFocused();
  await expect(heading).toHaveAttribute("tabindex", "-1");
  await expect(page.locator(".error-banner[role='alert']")).toContainText("The local service could not complete the request.");
});

test("backend error text is rendered as text and cannot inject HTML", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  const untrusted = '<img data-p1-003-injected src=x onerror="document.body.dataset.pwned=\'yes\'">';
  await page.route("**/backend/api/documents/*/process", async (route) => {
    const processed = await route.fetch();
    expect(processed.ok()).toBeTruthy();
    await route.fulfill({
      status: 422,
      contentType: "application/json",
      body: JSON.stringify({ error: { code: "synthetic_error", message: untrusted } }),
    });
  });
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.locator(".error-banner")).toContainText("The local service could not complete the request.");
  await expect(page.locator(".error-banner")).not.toContainText(untrusted);
  await expect(page.locator("[data-p1-003-injected]")).toHaveCount(0);
  await expect(page.locator("body")).not.toHaveAttribute("data-pwned", "yes");
});

test("only the current workflow step exposes aria-current", async ({ page }) => {
  await page.goto("/");
  const upload = page.getByRole("button", { name: /1\. Source Upload/ });
  const analyze = page.getByRole("button", { name: /2\. AI Extraction/ });
  const review = page.getByRole("button", { name: /3\. Review & Refine/ });
  const validate = page.getByRole("button", { name: /4\. Validation/ });
  const exportStep = page.getByRole("button", { name: /5\. DOCX Export/ });
  await expect(upload).toHaveAttribute("aria-current", "step");
  await expect(analyze).not.toHaveAttribute("aria-current");
  await expect(review).not.toHaveAttribute("aria-current");
  await expect(validate).not.toHaveAttribute("aria-current");
  await expect(exportStep).not.toHaveAttribute("aria-current");
  await uploadSynthetic(page, "pdf");
  await expect(upload).not.toHaveAttribute("aria-current");
  await expect(analyze).toHaveAttribute("aria-current", "step");
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  await expect(analyze).not.toHaveAttribute("aria-current");
  await expect(review).toHaveAttribute("aria-current", "step");
  await expect(validate).toBeDisabled();
  await expect(exportStep).toBeDisabled();
  await completeHumanReview(page);
  await enterValidation(page, "revision-1");
  await expect(review).not.toHaveAttribute("aria-current");
  await expect(validate).toHaveAttribute("aria-current", "step");
  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  await expect(validate).toHaveAttribute("aria-current", "step");
  await expect(exportStep).toBeEnabled();
});

test("selected-revision Human review gate blocks partial and NEEDS_CHANGES states without validating on navigation", async ({ page }) => {
  await processSynthetic(page, "pdf");
  const controls = page.getByLabel(/^Session review status for /);
  const total = await controls.count();
  expect(total).toBeGreaterThan(1);
  const continueButton = page.getByRole("button", { name: "Continue to Validation → · revision-1" });
  const validationStep = page.getByRole("button", { name: /4\. Validation/ });
  const exportStep = page.getByRole("button", { name: /5\. DOCX Export/ });

  await expect(page.getByText(`Review: ${total} UNREVIEWED · 0 REVIEWED (not approved) · 0 NEEDS_CHANGES`)).toBeVisible();
  await expect(page.getByText(`Review all sections before validation · ${total} remaining.`)).toBeVisible();
  await expect(continueButton).toBeDisabled();
  await expect(validationStep).toBeDisabled();
  await expect(exportStep).toBeDisabled();

  await controls.nth(0).selectOption("REVIEWED");
  await expect(page.getByText(`Review all sections before validation · ${total - 1} remaining.`)).toBeVisible();
  await expect(continueButton).toBeDisabled();
  await controls.nth(1).selectOption("NEEDS_CHANGES");
  await expect(page.getByText(`Review: ${total - 2} UNREVIEWED · 1 REVIEWED (not approved) · 1 NEEDS_CHANGES`)).toBeVisible();
  await expect(continueButton).toBeDisabled();
  await expect(validationStep).toBeDisabled();

  let validationRequests = 0;
  page.on("request", (request) => {
    if (request.method() === "POST" && request.url().includes("/backend/api/drafts/validate")) validationRequests += 1;
  });
  await completeHumanReview(page);
  await expect(continueButton).toBeEnabled();
  await expect(validationStep).toBeEnabled();
  await continueButton.click();
  await expect(page.getByRole("heading", { name: "Validate the selected revision" })).toBeVisible();
  expect(validationRequests).toBe(0);
  await expect(page.getByRole("button", { name: "Validate revision-1" })).toBeVisible();
  await page.getByRole("button", { name: "Go back" }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  expect(validationRequests).toBe(0);
});

test("upload, analysis, validation and export allow only one in-flight request", async ({ page }) => {
  const fixtureResponse = await page.request.get(`${backend}/__test/pdf`);
  expect(fixtureResponse.ok()).toBeTruthy();
  await page.goto("/");
  await page.locator("#document-file").setInputFiles({
    name: "synthetic.pdf", mimeType: mediaTypes.pdf, buffer: await fixtureResponse.body(),
  });

  const uploadGate = deferred();
  let uploadRequests = 0;
  await page.route("**/backend/api/documents", async (route) => {
    if (route.request().method() !== "POST") return route.continue();
    uploadRequests += 1;
    await uploadGate.promise;
    await route.continue();
  });
  const uploadButton = page.locator(".selected-file .primary-button");
  await uploadButton.evaluate((button: HTMLButtonElement) => { button.click(); button.click(); });
  await expect.poll(() => uploadRequests).toBe(1);
  await expect(uploadButton).toBeDisabled();
  await expect(page.getByText("Uploading and validating the document.")).toBeVisible();
  uploadGate.release();
  await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toBeVisible();
  expect(uploadRequests).toBe(1);
  await page.unroute("**/backend/api/documents");

  const processGate = deferred();
  let processRequests = 0;
  await page.route("**/backend/api/documents/*/process", async (route) => {
    processRequests += 1;
    await processGate.promise;
    await route.continue();
  });
  const processButton = page.getByRole("button", { name: "Continue to AI Extraction" });
  await processButton.evaluate((button: HTMLButtonElement) => { button.click(); button.click(); });
  await expect.poll(() => processRequests).toBe(1);
  await expect(processButton).toBeDisabled();
  await expect(page.getByText("Extracting invention-relevant content", { exact: true })).toBeVisible();
  processGate.release();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  expect(processRequests).toBe(1);
  await page.unroute("**/backend/api/documents/*/process");

  await completeHumanReview(page);
  await enterValidation(page, "revision-1");

  const validationGate = deferred();
  let validationRequests = 0;
  await page.route("**/backend/api/drafts/validate", async (route) => {
    validationRequests += 1;
    await validationGate.promise;
    await route.continue();
  });
  const validateButton = page.getByRole("button", { name: "Validate revision-1" });
  await validateButton.evaluate((button: HTMLButtonElement) => { button.click(); button.click(); });
  await expect.poll(() => validationRequests).toBe(1);
  await expect(page.getByText("Validating revision-1…")).toBeVisible();
  await expect(page.getByRole("button", { name: "Validate revision-1" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /4\. Validation/ })).toHaveAttribute("aria-current", "step");
  validationGate.release();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  expect(validationRequests).toBe(1);
  await page.unroute("**/backend/api/drafts/validate");

  await enterExport(page);

  const exportGate = deferred();
  let exportRequests = 0;
  await page.route("**/backend/api/exports/docx", async (route) => {
    exportRequests += 1;
    await exportGate.promise;
    await route.continue();
  });
  const downloadPromise = page.waitForEvent("download");
  const exportButton = page.getByRole("button", { name: "Export revision-1 DOCX" });
  await exportButton.evaluate((button: HTMLButtonElement) => { button.click(); button.click(); });
  await expect.poll(() => exportRequests).toBe(1);
  await expect(exportButton).toBeDisabled();
  await expect(page.getByText("Preparing DOCX… · revision-1")).toBeVisible();
  exportGate.release();
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
  expect(exportRequests).toBe(1);
});

test("six fresh synthetic runs keep deterministic shape and clean source/export storage", async ({ page }) => {
  const shapes = new Map<string, string>();
  const initialStorageResponse = await page.request.get(`${backend}/__test/storage`);
  expect(initialStorageResponse.ok()).toBeTruthy();
  const initialStorage = await initialStorageResponse.json() as { source_files: number; export_files: number };
  expect(initialStorage.export_files).toBe(0);
  for (const format of ["pdf", "docx"] as const) {
    for (let run = 1; run <= 3; run += 1) {
      const start = Date.now();
      await uploadSynthetic(page, format);
      const uploaded = Date.now();
      const processResponse = page.waitForResponse((response) => response.url().includes("/process") && response.request().method() === "POST");
      await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
      const processed = await (await processResponse).json() as { draft: {
        section_order: unknown; draft_sections: Array<{ section_id: string; status: string }>;
        missing_information: Array<{ missing_id: string }>; output_notice: unknown;
      } };
      await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
      const processedAt = Date.now();
      const shape = JSON.stringify({
        order: processed.draft.section_order,
        sections: processed.draft.draft_sections.map(({ section_id, status }) => ({ section_id, status })),
        missing: processed.draft.missing_information.map(({ missing_id }) => missing_id),
        notice: processed.draft.output_notice,
      });
      if (shapes.has(format)) expect(shape).toBe(shapes.get(format));
      else shapes.set(format, shape);
      await validateRevision(page, "revision-1");
      const validatedAt = Date.now();
      await enterExport(page);
      const downloadPromise = page.waitForEvent("download");
      await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
      const downloaded = await downloadedDocxText(await downloadPromise);
      expect(downloaded).toContain("AI-generated draft");
      const exportedAt = Date.now();
      const storage = await page.request.get(`${backend}/__test/storage`);
      expect(storage.ok()).toBeTruthy();
      expect(await storage.json()).toEqual({ source_files: initialStorage.source_files, export_files: 0 });
      console.log(`P0-007 stability ${JSON.stringify({
        format, run, upload_ms: uploaded - start, process_ms: processedAt - uploaded,
        validation_ms: validatedAt - processedAt, export_ms: exportedAt - validatedAt,
        total_ms: exportedAt - start, source_files: 0, export_files: 0,
      })}`);
    }
  }
});

test("PDF session: immutable revisions require selected-revision review before validation and export", async ({ page }) => {
  const processed = await processSynthetic(page, "pdf");
  const original = "The disclosure relates to calibration of an optical sensor across temperature bands.";
  await expect(page.getByText(original, { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Edit prose" }).click();
  await expect(page.getByLabel("Grounding for paragraph-field")).toContainText("Evidence: ev-core");
  await expect(page.getByLabel("Grounding for paragraph-field")).toContainText("Source paths: /technical_field/item");
  await firstParagraph(page).fill("Cancelled edit text.");
  await page.getByRole("button", { name: "Cancel edit" }).click();
  await expect(page.getByRole("dialog", { name: "Confirm session change" })).toBeVisible();
  await page.getByRole("button", { name: "Discard changes and continue" }).click();
  await expect(page.getByText(original, { exact: true })).toBeVisible();
  await expect(page.getByLabel("Selected revision").locator("option")).toHaveCount(1);

  const reviewTotal = await completeHumanReview(page);
  await enterValidation(page, "revision-1");
  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  await page.getByRole("button", { name: "Return to Review & Refine" }).click();

  const revised = "A calibrated optical sensor compensates for thermal drift in each measurement band.";
  await saveParagraphRevision(page, revised);
  await expect(page.getByText("Validation: NOT VALIDATED")).toBeVisible();
  await expect(page.getByText("6 UNREVIEWED", { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: /4\. Validation/ })).toBeDisabled();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toBeDisabled();
  await page.getByLabel("Selected revision").selectOption("revision-1");
  await expect(page.getByText(original, { exact: true })).toBeVisible();
  await expect(page.getByText("Validation: VALIDATED")).toBeVisible();
  await expect(page.getByText(`${reviewTotal} REVIEWED (not approved)`, { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: /4\. Validation/ })).toBeEnabled();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toBeEnabled();
  await page.getByLabel("Selected revision").selectOption("revision-2");
  await expect(page.getByText(revised, { exact: true })).toBeVisible();
  await expect(page.getByText("Validation: NOT VALIDATED")).toBeVisible();
  await expect(page.getByRole("button", { name: /4\. Validation/ })).toBeDisabled();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toBeDisabled();

  await completeHumanReview(page);
  await enterValidation(page, "revision-2");
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  await page.getByRole("button", { name: "Return to Review & Refine" }).click();
  await expect(page.locator(".edit-support-warning").filter({ hasText: "unverified semantic source support" }).first()).toBeVisible();

  await page.getByRole("button", { name: "Edit prose" }).click();
  await firstParagraph(page).fill("Unsaved export substitution.");
  await expect(page.getByRole("button", { name: "Export revision-2 DOCX" })).toHaveCount(0);
  await page.getByRole("button", { name: "Cancel edit" }).click();
  await expect(page.getByRole("dialog", { name: "Confirm session change" })).toBeVisible();
  await page.getByRole("button", { name: "Discard changes and continue" }).click();
  await enterValidation(page, "revision-2");
  await expect(page.getByRole("button", { name: "Validate revision-2" })).toHaveCount(0);
  await enterExport(page);

  let exported: Record<string, unknown> | undefined;
  page.on("request", (request) => {
    if (request.url().includes("/backend/api/exports/docx")) exported = request.postDataJSON();
  });
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe("patent-description-draft.docx");
  expect(exported?.revision_id).toBe("revision-2");
  expect((exported?.draft as { draft_sections: Array<{ paragraphs: Array<{ text: string }> }> }).draft_sections[0].paragraphs[0].text).toBe(revised);
  expect((exported?.draft as { output_notice: unknown }).output_notice).toEqual(processed.draft.output_notice);
  expect((exported?.draft as { drawings: unknown }).drawings).toEqual(processed.draft.drawings);
  const downloaded = await downloadedDocxText(download);
  expect(downloaded).toContain(revised);
  expect(downloaded).not.toContain(original);
  expect(downloaded).not.toContain("Unsaved export substitution.");
  expect(downloaded).not.toContain("Cancelled edit text.");
  expect(downloaded).toContain("AI-generated draft");
  expect(downloaded).toContain("[AUTHOR CONFIRMATION REQUIRED]");
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");
  const secondDownloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  expect((await secondDownloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");

  await page.getByRole("button", { name: "Go back" }).click();
  await expect(page.getByRole("button", { name: /4\. Validation/ })).toHaveAttribute("aria-current", "step");
  await expect(page.getByRole("button", { name: "Validate revision-2" })).toHaveCount(0);
  await enterExport(page);

  await page.getByRole("button", { name: /3\. Review & Refine/ }).click();
  await expect(page.getByRole("button", { name: "Download editable DOCX" })).toHaveCount(0);
  const review = page.getByLabel("Session review status for Technical Field");
  await review.selectOption("NEEDS_CHANGES");
  await expect(page.getByText("1 NEEDS_CHANGES", { exact: false })).toBeVisible();
  await expect(page.getByText("Validation: VALIDATED")).toBeVisible();
  await expect(review).toHaveValue("NEEDS_CHANGES");
  await expect(page.getByRole("button", { name: "Continue to Validation → · revision-2" })).toBeDisabled();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toBeDisabled();
  await review.selectOption("REVIEWED");
  await expect(page.getByRole("button", { name: "Continue to Validation → · revision-2" })).toBeEnabled();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toBeEnabled();

  await page.reload();
  await expect(page.getByRole("heading", { name: "Upload a research document" })).toBeVisible();
  await expect(page.getByLabel("Selected revision")).toHaveCount(0);
});

test("DOCX upload and edited revision export over the real local HTTP boundary", async ({ page }) => {
  await processSynthetic(page, "docx");
  const revised = "A temperature coefficient calibrates the optical sensor across defined bands.";
  await saveParagraphRevision(page, revised);
  await validateRevision(page, "revision-2");
  await enterExport(page);
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe("patent-description-draft.docx");
  const downloaded = await downloadedDocxText(download);
  expect(downloaded).toContain(revised);
  expect(downloaded).not.toContain("The disclosure relates to calibration of an optical sensor across temperature bands.");
  expect(downloaded).toContain("AI-generated draft");
  expect(downloaded).toContain("[AUTHOR CONFIRMATION REQUIRED]");
});

test("non-title missing information and linked question survive browser and DOCX", async ({ page }) => {
  const processed = await processSynthetic(page, "pdf", { missing: true });
  const draft = processed.draft as {
    selected_title: { status: string };
    abstract: { status: string; missing_information_ids: string[] };
    author_questions: Array<{ question: string; related_missing_information_ids: string[] }>;
  };
  expect(draft.selected_title.status).toBe("MISSING");
  expect(draft.abstract.status).toBe("MISSING");
  expect(draft.abstract.missing_information_ids).toContain("missing-abstract");
  expect(draft.author_questions.find((item) => item.question.includes("Abstract"))?.related_missing_information_ids).toContain("missing-abstract");
  await expect(page.getByText("Related items: missing-abstract")).toBeVisible();
  await page.getByRole("tab", { name: "Review Items" }).click();
  await expect(page.getByText("Can the author provide supported technical content for the Abstract?")).toBeVisible();
  await page.getByRole("tab", { name: "Patent Draft" }).click();
  await validateRevision(page, "revision-1");
  await enterExport(page);
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
  const downloaded = await downloadedDocxText(await downloadPromise);
  expect(downloaded).toContain("[AUTHOR CONFIRMATION REQUIRED]");
  expect(downloaded).toContain("Can the author provide supported technical content for the Abstract?");
  expect(downloaded).not.toContain("The disclosure relates to calibration of an optical sensor across temperature bands.");
});

test("invalid edit and rejected export preserve selected revision", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await saveParagraphRevision(page, "This invention is patentable.");
  await completeHumanReview(page);
  await enterValidation(page, "revision-2");
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  const validationFailureHeading = page.getByRole("heading", { name: /Draft validation failed/ });
  await expect(validationFailureHeading).toBeVisible();
  await expect(validationFailureHeading).toBeFocused();
  await expect(page.getByRole("button", { name: "Export revision-2 DOCX" })).toHaveCount(0);
  await expect(page.getByLabel("Selected revision", { exact: true })).toHaveValue("revision-2");
  await page.getByRole("button", { name: "Edit this revision" }).click();
  await expect(page.getByText("This invention is patentable.", { exact: true })).toBeVisible();

  await firstParagraph(page).fill("The optical sensor is calibrated across temperature bands.");
  await page.getByRole("button", { name: "Save new revision" }).click();
  await validateRevision(page, "revision-3");
  await enterExport(page);
  await page.route("**/backend/api/exports/docx", async (route) => {
    const body = route.request().postDataJSON();
    body.revision_id = "stale-revision";
    await route.continue({ postData: JSON.stringify(body) });
  });
  await page.getByRole("button", { name: "Export revision-3 DOCX" }).click();
  await expect(page.getByText("stale_draft_revision")).toBeVisible();
  await expect(page.locator(".export-summary strong")).toHaveText("revision-3");
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");
});

test("keyboard-only edit, validate, review and export controls", async ({ page }) => {
  await processSynthetic(page, "pdf", { keyboard: true });
  await page.getByRole("button", { name: "Edit prose" }).focus();
  await page.keyboard.press("Enter");
  await firstParagraph(page).focus();
  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.type("The sensor uses a temperature coefficient for calibration.");
  await page.getByRole("button", { name: "Save new revision" }).focus();
  await page.keyboard.press("Enter");
  const reviewControls = page.getByLabel(/^Session review status for /);
  const reviewTotal = await reviewControls.count();
  for (let index = 0; index < reviewTotal; index += 1) {
    await reviewControls.nth(index).focus();
    await page.keyboard.press("ArrowDown");
  }
  const continueValidation = page.getByRole("button", { name: "Continue to Validation → · revision-2" });
  await continueValidation.focus();
  await page.keyboard.press("Enter");
  await page.getByRole("button", { name: "Validate revision-2" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  const continueExport = page.getByRole("button", { name: "Continue to DOCX Export →" });
  await continueExport.focus();
  await page.keyboard.press("Enter");
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).focus();
  await page.keyboard.press("Enter");
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
});

test("narrow viewport keeps editing, warnings, validation and export usable", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await processSynthetic(page, "pdf");
  await saveParagraphRevision(page, "The sensor uses a temperature coefficient for calibration.");
  await expect(page.locator(".edit-support-warning").filter({ hasText: "unverified semantic source support" }).first()).toBeVisible();
  await validateRevision(page, "revision-2");
  const width = await page.evaluate(() => ({ body: document.body.scrollWidth, viewport: innerWidth }));
  expect(width.body).toBeLessThanOrEqual(width.viewport);
  await enterExport(page);
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  await downloadPromise;
  await page.route("**/backend/api/exports/docx", (route) =>
    route.fulfill({ status: 503, contentType: "text/plain", body: "synthetic proxy fault" }));
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  const errorWidth = await page.evaluate(() => ({ body: document.body.scrollWidth, viewport: innerWidth }));
  expect(errorWidth.body).toBeLessThanOrEqual(errorWidth.viewport);
  await page.getByRole("button", { name: "Return to results" }).click();
  await expect(page.locator(".export-summary strong")).toHaveText("revision-2");
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");
});

test("corrupt upload is rejected safely and a valid synthetic document can be retried", async ({ page }) => {
  await page.goto("/");
  await page.locator("#document-file").setInputFiles({
    name: "synthetic-corrupt.pdf", mimeType: mediaTypes.pdf, buffer: Buffer.from("%PDF-1.7\nnot a valid PDF"),
  });
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await expect(page.getByRole("heading", { name: "We could not complete that operation" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toHaveCount(0);
  await expect(page.locator(".error-banner")).not.toContainText("not a valid PDF");
  await page.getByRole("button", { name: "Choose another document" }).click();
  const fixture = await page.request.get(`${backend}/__test/pdf`);
  expect(fixture.ok()).toBeTruthy();
  const chooserPromise = page.waitForEvent("filechooser");
  const select = page.getByRole("button", { name: "Select document" });
  await select.focus();
  await expect(select).toBeFocused();
  await page.keyboard.press("Enter");
  await (await chooserPromise).setFiles({
    name: "synthetic.pdf", mimeType: mediaTypes.pdf, buffer: await fixture.body(),
  });
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toBeVisible();
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
});

test("process proxy failure is safe and requires a new upload before retry", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  await page.route("**/backend/api/documents/*/process", async (route) => {
    const processed = await route.fetch();
    expect(processed.ok()).toBeTruthy();
    await route.fulfill({
      status: 502,
      contentType: "application/json",
      body: JSON.stringify({ error: { code: "upstream_failure", message: "Provider OpenAI failed at C:\\private\\paper.pdf" } }),
    });
  });
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toHaveCount(0);
  await expect(page.locator(".error-banner")).not.toContainText("C:\\private");
  await expect(page.locator(".error-banner")).not.toContainText("OpenAI");
  await page.unroute("**/backend/api/documents/*/process");
  await page.getByRole("button", { name: "Choose another document" }).click();
  const fixture = await page.request.get(`${backend}/__test/pdf`);
  await page.locator("#document-file").setInputFiles({
    name: "synthetic-retry.pdf", mimeType: mediaTypes.pdf, buffer: await fixture.body(),
  });
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
});

test("export failure creates no download and preserves the validated revision for retry", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await validateRevision(page, "revision-1");
  await enterExport(page);
  const downloads: Download[] = [];
  page.on("download", (download) => downloads.push(download));
  await page.route("**/backend/api/exports/docx", (route) =>
    route.fulfill({ status: 503, contentType: "text/plain", headers: { "x-correlation-id": "synthetic-reference-123" }, body: "raw C:\\private\\export.docx" }));
  await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByText("Reference ID: synthetic-reference-123")).toBeVisible();
  expect(downloads).toHaveLength(0);
  await expect(page.locator(".error-banner")).not.toContainText("C:\\private");
  await expect(page.locator(".export-summary strong")).toHaveText("revision-1");
  await page.unroute("**/backend/api/exports/docx");
  await page.getByRole("button", { name: "Return to results" }).click();
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
});

test("non-JSON and network backend failures are safe and keep the revision", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await saveParagraphRevision(page, "The sensor uses a temperature coefficient for calibration.");
  await completeHumanReview(page);
  await enterValidation(page, "revision-2");
  await page.route("**/backend/api/drafts/validate", (route) => route.fulfill({ status: 502, body: "proxy fault with no JSON" }));
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByRole("heading", { name: /Draft validation failed/ })).toBeVisible();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByText("proxy fault with no JSON")).toHaveCount(0);
  await expect(page.getByLabel("Selected revision", { exact: true })).toHaveValue("revision-2");
  await page.unroute("**/backend/api/drafts/validate");
  await page.route("**/backend/api/drafts/validate", (route) => route.abort());
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByLabel("Selected revision", { exact: true })).toHaveValue("revision-2");
});
