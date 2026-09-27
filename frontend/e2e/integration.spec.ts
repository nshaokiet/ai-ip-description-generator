import { expect, test, type Page } from "@playwright/test";

const backend = "http://127.0.0.1:8000";
const mediaTypes = {
  pdf: "application/pdf",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
};

async function processSynthetic(page: Page, format: "pdf" | "docx") {
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
  await page.locator("#document-file").setInputFiles({
    name: `synthetic.${format}`,
    mimeType: mediaTypes[format],
    buffer: await fixture.body(),
  });
  await page.getByRole("button", { name: "Upload & Validate" }).click();
  await expect(page.getByRole("heading", { name: "Ready for analysis" })).toBeVisible();
  const processResponse = page.waitForResponse((response) => response.url().includes("/process") && response.request().method() === "POST");
  await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
  const processed = await (await processResponse).json() as { draft: { output_notice: unknown; drawings: unknown } };
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

  const revised = `${original} The sensor remains temperature-aware.`;
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
  await saveParagraphRevision(page, "The optical sensor calibration uses a temperature coefficient.");
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
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
  await processSynthetic(page, "pdf");
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
