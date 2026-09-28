import { execFileSync } from "node:child_process";
import path from "node:path";

import { expect, test, type Download, type Page } from "@playwright/test";

const backend = "http://127.0.0.1:8000";
const mediaTypes = {
  pdf: "application/pdf",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
};

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
  await expect(page.getByRole("heading", { name: "Ready for analysis" })).toBeVisible();
}

async function processSynthetic(page: Page, format: "pdf" | "docx", options: { missing?: boolean; keyboard?: boolean } = {}) {
  await uploadSynthetic(page, format, options);
  const processResponse = page.waitForResponse((response) => response.url().includes("/process") && response.request().method() === "POST");
  await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
  const processed = await (await processResponse).json() as { draft: Record<string, unknown> };
  await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toBeVisible();
  await page.getByRole("tab", { name: "Patent Draft" }).click();
  await expect(page.getByRole("heading", { name: "Title: MISSING" })).toBeVisible();
  await expect(page.getByText("[AUTHOR CONFIRMATION REQUIRED]").first()).toBeVisible();
  return processed;
}

function firstParagraph(page: Page) {
  return page.getByLabel("Paragraph paragraph-field prose");
}

async function saveParagraphRevision(page: Page, replacement: string) {
  await page.getByRole("button", { name: "Edit prose" }).click();
  await firstParagraph(page).fill(replacement);
  await expect(page.getByText("Unsaved changes")).toBeVisible();
  await page.getByRole("button", { name: "Save new revision" }).click();
  await expect(page.getByLabel("Selected revision")).toHaveValue("revision-2");
}

test("six fresh synthetic runs keep deterministic shape and clean source/export storage", async ({ page }) => {
  const shapes = new Map<string, string>();
  for (const format of ["pdf", "docx"] as const) {
    for (let run = 1; run <= 3; run += 1) {
      const start = Date.now();
      await uploadSynthetic(page, format);
      const uploaded = Date.now();
      const processResponse = page.waitForResponse((response) => response.url().includes("/process") && response.request().method() === "POST");
      await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
      const processed = await (await processResponse).json() as { draft: {
        section_order: unknown; draft_sections: Array<{ section_id: string; status: string }>;
        missing_information: Array<{ missing_id: string }>; output_notice: unknown;
      } };
      await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toBeVisible();
      const processedAt = Date.now();
      const shape = JSON.stringify({
        order: processed.draft.section_order,
        sections: processed.draft.draft_sections.map(({ section_id, status }) => ({ section_id, status })),
        missing: processed.draft.missing_information.map(({ missing_id }) => missing_id),
        notice: processed.draft.output_notice,
      });
      if (shapes.has(format)) expect(shape).toBe(shapes.get(format));
      else shapes.set(format, shape);
      await page.getByRole("button", { name: "Validate revision-1" }).click();
      await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
      const validatedAt = Date.now();
      const downloadPromise = page.waitForEvent("download");
      await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
      const downloaded = await downloadedDocxText(await downloadPromise);
      expect(downloaded).toContain("AI-generated draft");
      const exportedAt = Date.now();
      const storage = await page.request.get(`${backend}/__test/storage`);
      expect(storage.ok()).toBeTruthy();
      expect(await storage.json()).toEqual({ source_files: 0, export_files: 0 });
      console.log(`P0-007 stability ${JSON.stringify({
        format, run, upload_ms: uploaded - start, process_ms: processedAt - uploaded,
        validation_ms: validatedAt - processedAt, export_ms: exportedAt - validatedAt,
        total_ms: exportedAt - start, source_files: 0, export_files: 0,
      })}`);
    }
  }
});

test("PDF session: cancel, immutable save, validate, review and exact UNREVIEWED export", async ({ page }) => {
  const processed = await processSynthetic(page, "pdf");
  const original = "The disclosure relates to calibration of an optical sensor across temperature bands.";
  await expect(page.getByText(original, { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Edit prose" }).click();
  await expect(page.getByLabel("Grounding for paragraph-field")).toContainText("Evidence: ev-core");
  await expect(page.getByLabel("Grounding for paragraph-field")).toContainText("Source paths: /technical_field/item");
  await firstParagraph(page).fill("Cancelled edit text.");
  await page.getByRole("button", { name: "Cancel edit" }).click();
  await expect(page.getByText(original, { exact: true })).toBeVisible();
  await expect(page.getByLabel("Selected revision").locator("option")).toHaveCount(1);

  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  await page.getByLabel("Session review status for Technical Field").selectOption("REVIEWED");

  const revised = "A calibrated optical sensor compensates for thermal drift in each measurement band.";
  await saveParagraphRevision(page, revised);
  await expect(page.getByText("Backend validation: NOT VALIDATED")).toBeVisible();
  await expect(page.getByText("6 UNREVIEWED", { exact: false })).toBeVisible();
  await page.getByLabel("Selected revision").selectOption("revision-1");
  await expect(page.getByText(original, { exact: true })).toBeVisible();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  await expect(page.getByText("1 REVIEWED (not approved)", { exact: false })).toBeVisible();
  await page.getByLabel("Selected revision").selectOption("revision-2");
  await expect(page.getByText(revised, { exact: true })).toBeVisible();
  await expect(page.getByText("Backend validation: NOT VALIDATED")).toBeVisible();

  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  await expect(page.getByText("semantic source support is unverified", { exact: false })).toBeVisible();

  await page.getByRole("button", { name: "Edit prose" }).click();
  await firstParagraph(page).fill("Unsaved export substitution.");
  await expect(page.getByRole("button", { name: "Export revision-2 DOCX" })).toBeDisabled();
  await page.getByRole("button", { name: "Cancel edit" }).click();

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
  await expect(page.getByText("6 UNREVIEWED", { exact: false })).toBeVisible();

  const review = page.getByLabel("Session review status for Technical Field");
  await review.selectOption("REVIEWED");
  await expect(page.getByText("1 REVIEWED (not approved)", { exact: false })).toBeVisible();
  await review.selectOption("NEEDS_CHANGES");
  await expect(page.getByText("1 NEEDS_CHANGES", { exact: false })).toBeVisible();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  await expect(review).toHaveValue("NEEDS_CHANGES");

  await page.reload();
  await expect(page.getByRole("heading", { name: "Upload a research document" })).toBeVisible();
  await expect(page.getByLabel("Selected revision")).toHaveCount(0);
});

test("DOCX upload and edited revision export over the real local HTTP boundary", async ({ page }) => {
  await processSynthetic(page, "docx");
  const revised = "A temperature coefficient calibrates the optical sensor across defined bands.";
  await saveParagraphRevision(page, revised);
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
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
  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
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
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByRole("heading", { name: /Draft validation failed/ })).toBeVisible();
  await expect(page.getByText("This invention is patentable.", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Export revision-2 DOCX" })).toBeDisabled();

  await page.getByRole("button", { name: "Edit prose" }).click();
  await firstParagraph(page).fill("The optical sensor is calibrated across temperature bands.");
  await page.getByRole("button", { name: "Save new revision" }).click();
  await page.getByRole("button", { name: "Validate revision-3" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  await page.route("**/backend/api/exports/docx", async (route) => {
    const body = route.request().postDataJSON();
    body.revision_id = "stale-revision";
    await route.continue({ postData: JSON.stringify(body) });
  });
  await page.getByRole("button", { name: "Export revision-3 DOCX" }).click();
  await expect(page.getByText("stale_draft_revision")).toBeVisible();
  await expect(page.getByLabel("Selected revision")).toHaveValue("revision-3");
  await expect(page.getByText("The optical sensor is calibrated across temperature bands.", { exact: true })).toBeVisible();
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
  await page.getByRole("button", { name: "Validate revision-2" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  const review = page.getByLabel("Session review status for Technical Field");
  await review.focus();
  await page.keyboard.press("ArrowDown");
  await expect(review).toHaveValue("REVIEWED");
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).focus();
  await page.keyboard.press("Enter");
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
});

test("narrow viewport keeps editing, warnings, validation and export usable", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await processSynthetic(page, "pdf");
  await saveParagraphRevision(page, "The sensor uses a temperature coefficient for calibration.");
  await expect(page.getByText("semantic source support is unverified", { exact: false })).toBeVisible();
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  const width = await page.evaluate(() => ({ body: document.body.scrollWidth, viewport: innerWidth }));
  expect(width.body).toBeLessThanOrEqual(width.viewport);
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
  await expect(page.getByLabel("Selected revision")).toHaveValue("revision-2");
});

test("corrupt upload is rejected safely and a valid synthetic document can be retried", async ({ page }) => {
  await page.goto("/");
  await page.locator("#document-file").setInputFiles({
    name: "synthetic-corrupt.pdf", mimeType: mediaTypes.pdf, buffer: Buffer.from("%PDF-1.7\nnot a valid PDF"),
  });
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await expect(page.getByRole("heading", { name: "We could not complete that operation" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ready for analysis" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toHaveCount(0);
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
  await expect(page.getByRole("heading", { name: "Ready for analysis" })).toBeVisible();
  await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
  await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toBeVisible();
});

test("process proxy failure is safe and requires a new upload before retry", async ({ page }) => {
  await uploadSynthetic(page, "pdf");
  await page.route("**/backend/api/documents/*/process", async (route) => {
    const processed = await route.fetch();
    expect(processed.ok()).toBeTruthy();
    await route.fulfill({ status: 502, contentType: "text/plain", body: "raw C:\\private\\paper.pdf" });
  });
  await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ready for analysis" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toHaveCount(0);
  await expect(page.locator(".error-banner")).not.toContainText("C:\\private");
  await page.unroute("**/backend/api/documents/*/process");
  await page.getByRole("button", { name: "Choose another document" }).click();
  const fixture = await page.request.get(`${backend}/__test/pdf`);
  await page.locator("#document-file").setInputFiles({
    name: "synthetic-retry.pdf", mimeType: mediaTypes.pdf, buffer: await fixture.body(),
  });
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
  await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toBeVisible();
});

test("export failure creates no download and preserves the validated revision for retry", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  const downloads: Download[] = [];
  page.on("download", (download) => downloads.push(download));
  await page.route("**/backend/api/exports/docx", (route) =>
    route.fulfill({ status: 503, contentType: "text/plain", headers: { "x-correlation-id": "synthetic-reference-123" }, body: "raw C:\\private\\export.docx" }));
  await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByText("Reference ID: synthetic-reference-123")).toBeVisible();
  expect(downloads).toHaveLength(0);
  await expect(page.locator(".error-banner")).not.toContainText("C:\\private");
  await expect(page.getByLabel("Selected revision")).toHaveValue("revision-1");
  await page.unroute("**/backend/api/exports/docx");
  await page.getByRole("button", { name: "Return to results" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
});

test("non-JSON and network backend failures are safe and keep the revision", async ({ page }) => {
  await processSynthetic(page, "pdf");
  await saveParagraphRevision(page, "The sensor uses a temperature coefficient for calibration.");
  await page.route("**/backend/api/drafts/validate", (route) => route.fulfill({ status: 502, body: "proxy fault with no JSON" }));
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByRole("heading", { name: /Draft validation failed/ })).toBeVisible();
  await expect(page.getByText("The local service could not complete the request.")).toBeVisible();
  await expect(page.getByText("proxy fault with no JSON")).toHaveCount(0);
  await expect(page.getByLabel("Selected revision")).toHaveValue("revision-2");
  await page.unroute("**/backend/api/drafts/validate");
  await page.route("**/backend/api/drafts/validate", (route) => route.abort());
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("The local backend is unavailable. Confirm that FastAPI is running.")).toBeVisible();
  await expect(page.getByLabel("Selected revision")).toHaveValue("revision-2");
});
