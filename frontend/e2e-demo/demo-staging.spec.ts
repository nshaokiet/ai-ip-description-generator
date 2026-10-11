import { expect, test, type Page } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => { localStorage.setItem("aiip.locale", "en"); });
});

async function runSampleFlow(page: Page, buttonName: string) {
  await page.goto("/");
  await page.getByRole("button", { name: buttonName }).click();
  await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Go back" })).toBeEnabled();
  await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
  await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
  await page.getByRole("tab", { name: "Patent Draft" }).click();
  await page.getByRole("button", { name: "Edit prose" }).first().click();
  await page.locator("textarea").first().fill(
    "A deterministic synthetic sensor description remains subject to Human review.",
  );
  await page.getByRole("button", { name: "Save new revision" }).click();
  const reviewControls = page.getByLabel(/^Session review status for /);
  const reviewTotal = await reviewControls.count();
  expect(reviewTotal).toBeGreaterThan(0);
  for (let index = 0; index < reviewTotal; index += 1) {
    await reviewControls.nth(index).selectOption("REVIEWED");
  }
  await page.getByRole("button", { name: "Continue to Validation → · revision-2" }).click();
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
  await page.getByRole("button", { name: "Continue to DOCX Export →" }).click();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
  await expect(page.getByRole("button", { name: /5\. DOCX Export/ })).toHaveAttribute("aria-current", "step");
}

test("static demo exposes PDF DOCX selection first and keeps controlled samples secondary", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", {
    name: "From Scientific Research Paper to USPTO-Style Patent Specification",
  })).toBeVisible();

  const logo = page.getByRole("img", { name: "VNUHCM Innovation Hub" });
  await expect(logo).toBeVisible();
  await logo.evaluate((image: HTMLImageElement) => image.decode());
  await expect(logo).toHaveCSS("object-fit", "contain");
  const logoBox = await logo.boundingBox();
  expect(logoBox?.width ?? 0).toBeGreaterThanOrEqual(175);
  expect(logoBox?.height ?? 0).toBeGreaterThanOrEqual(50);

  const input = page.locator('input[type="file"]');
  await expect(input).toHaveCount(1);
  await expect(input).toHaveAttribute(
    "accept",
    ".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  );
  await expect(page.getByRole("button", { name: "Select document" })).toBeVisible();
  await expect(page.getByText("PDF or DOCX · Max 10 MiB")).toBeVisible();
  const uploadCard = page.locator(".upload-card");
  expect((await uploadCard.boundingBox())?.width ?? 0).toBeGreaterThanOrEqual(900);

  const backButton = page.getByRole("button", { name: "Go back" });
  await expect(backButton).toBeVisible();
  await expect(backButton).toBeDisabled();

  await input.setInputFiles({
    name: "851932929-Bai-Bao-Cao-Nghien-Cứu-Khoa-Học.docx",
    mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    buffer: Buffer.from("ui-only-selection"),
  });
  await expect(page.getByText("851932929-Bai-Bao-Cao-Nghien-Cứu-Khoa-Học.docx", { exact: true })).toBeVisible();
  await expect(page.getByText("17 B", { exact: true })).toBeVisible();
  await expect(page.getByText("AI conversion pending funding", { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: "Remove selected file" })).toBeVisible();

  const width = await page.evaluate(() => ({ body: document.body.scrollWidth, viewport: innerWidth }));
  expect(width.body).toBeLessThanOrEqual(width.viewport);
  const headerWidth = await page.locator(".site-header").evaluate((header) => ({
    content: header.scrollWidth,
    viewport: window.innerWidth,
  }));
  expect(headerWidth.content).toBeLessThanOrEqual(headerWidth.viewport);

  await expect(page.getByRole("button", { name: "Use synthetic PDF demo" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Use synthetic DOCX demo" })).toBeVisible();
  await expect(page.locator(".demo-boundary-note")).toBeVisible();
  await expect(page.locator(".environment-badge")).toHaveCount(0);
});

test("public local PDF and DOCX selections can be removed and selected again without requests", async ({ page }) => {
  let arbitraryRequests = 0;
  page.on("request", (request) => {
    if (request.method() === "POST" && /\/backend\/api\/(documents|.*process)/.test(request.url())) {
      arbitraryRequests += 1;
    }
  });

  for (const file of [
    { name: "same-paper.pdf", mimeType: "application/pdf", buffer: Buffer.from("%PDF-1.7\nui-only") },
    {
      name: "same-paper.docx",
      mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      buffer: Buffer.from("ui-only-docx"),
    },
  ]) {
    await page.goto("/");
    const input = page.locator("#document-file");
    await input.setInputFiles(file);
    await expect(page.getByText(file.name, { exact: true })).toBeVisible();
    await expect(page.getByText("Selected locally · AI conversion pending funding", { exact: true })).toBeVisible();

    await page.getByRole("button", { name: "Remove selected file" }).click();
    await expect(page.getByText(file.name, { exact: true })).toHaveCount(0);
    await expect(page.getByText("Selected locally · AI conversion pending funding", { exact: true })).toHaveCount(0);
    await expect(input).toHaveValue("");

    await input.setInputFiles(file);
    await expect(page.getByText(file.name, { exact: true })).toBeVisible();
    await page.getByRole("button", { name: "Remove selected file" }).click();
    await expect(input).toHaveValue("");
  }

  expect(arbitraryRequests).toBe(0);
});

test("mobile selected-file layout and enlarged logo stay inside the viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await page.locator("#document-file").setInputFiles({
    name: "851932929-Bai-Bao-Cao-Nghien-Cứu-Khoa-Học.docx",
    mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    buffer: Buffer.from("mobile-ui-only-selection"),
  });

  const logo = page.getByRole("img", { name: "VNUHCM Innovation Hub" });
  await logo.evaluate((image: HTMLImageElement) => image.decode());
  const logoBox = await logo.boundingBox();
  expect(logoBox?.width ?? 0).toBeGreaterThanOrEqual(125);
  expect(logoBox?.height ?? 0).toBeGreaterThanOrEqual(42);

  const removeBox = await page.getByRole("button", { name: "Remove selected file" }).boundingBox();
  expect(removeBox?.width ?? 0).toBeGreaterThanOrEqual(40);
  expect(removeBox?.height ?? 0).toBeGreaterThanOrEqual(40);
  expect((removeBox?.x ?? 0) + (removeBox?.width ?? 0)).toBeLessThanOrEqual(390);
  const width = await page.evaluate(() => ({ body: document.body.scrollWidth, viewport: innerWidth }));
  expect(width.body).toBeLessThanOrEqual(width.viewport);
});

test("synthetic PDF demo supports analyze, edit, validate, and DOCX export", async ({ page }) => {
  await runSampleFlow(page, "Use synthetic PDF demo");
});

test("synthetic DOCX demo supports analyze, edit, validate, and DOCX export", async ({ page }) => {
  await runSampleFlow(page, "Use synthetic DOCX demo");
});
