import { expect, test, type Page } from "@playwright/test";

async function runSampleFlow(page: Page, buttonName: string) {
  await page.goto("/");
  await page.getByRole("button", { name: buttonName }).click();
  await expect(page.getByRole("heading", { name: "Ready for analysis" })).toBeVisible();
  await page.getByRole("button", { name: "Analyze & Generate Draft" }).click();
  await expect(page.getByRole("heading", { name: "Grounded draft workspace" })).toBeVisible();
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

test("static demo exposes only controlled synthetic choices and clear boundaries", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Synthetic Demo / Staging", { exact: true })).toBeVisible();
  await expect(
    page.getByText("Do not upload real, confidential, unpublished, or sensitive research."),
  ).toBeVisible();
  await expect(page.getByText("No live AI provider is used in this demo.", { exact: true })).toBeVisible();
  await expect(page.locator('input[type="file"]')).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Use synthetic PDF demo" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Use synthetic DOCX demo" })).toBeVisible();
});

test("synthetic PDF demo supports analyze, edit, validate, and DOCX export", async ({ page }) => {
  await runSampleFlow(page, "Use synthetic PDF demo");
});

test("synthetic DOCX demo supports analyze, edit, validate, and DOCX export", async ({ page }) => {
  await runSampleFlow(page, "Use synthetic DOCX demo");
});
