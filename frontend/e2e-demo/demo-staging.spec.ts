import { expect, test, type Page } from "@playwright/test";

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
  await page.getByRole("button", { name: "Validate revision-2" }).click();
  await expect(page.getByText("Backend validation: PASSED for this exact revision")).toBeVisible();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export revision-2 DOCX" }).click();
  expect((await downloadPromise).suggestedFilename()).toBe("patent-description-draft.docx");
}

test("static demo exposes PDF DOCX selection first and keeps controlled samples secondary", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", {
    name: "From Scientific Research Paper to USPTO-Style Patent Specification",
  })).toBeVisible();

  const logo = page.getByRole("img", { name: "VNUHCM Innovation Hub" });
  await expect(logo).toBeVisible();
  await expect(logo).toHaveCSS("object-fit", "contain");

  await expect(page.locator('input[type="file"]')).toHaveCount(1);
  await expect(page.getByRole("button", { name: "Select document" })).toBeVisible();
  await expect(page.getByText("PDF or DOCX · Max 10 MB")).toBeVisible();

  const backButton = page.getByRole("button", { name: "Go back" });
  await expect(backButton).toBeVisible();
  await expect(backButton).toBeDisabled();

  await page.locator("#document-file").setInputFiles({
    name: "research-paper.docx",
    mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    buffer: Buffer.from("ui-only-selection"),
  });
  await expect(page.getByText("research-paper.docx", { exact: true })).toBeVisible();
  await expect(page.getByText("AI conversion pending funding", { exact: false })).toBeVisible();

  await expect(page.getByRole("button", { name: "Use synthetic PDF demo" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Use synthetic DOCX demo" })).toBeVisible();
  await expect(page.getByText("No live AI provider is used", { exact: false })).toBeVisible();
  await expect(page.locator(".environment-badge")).toHaveCount(0);
});

test("synthetic PDF demo supports analyze, edit, validate, and DOCX export", async ({ page }) => {
  await runSampleFlow(page, "Use synthetic PDF demo");
});

test("synthetic DOCX demo supports analyze, edit, validate, and DOCX export", async ({ page }) => {
  await runSampleFlow(page, "Use synthetic DOCX demo");
});
