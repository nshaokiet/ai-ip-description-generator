import { readFile } from "node:fs/promises";
import { expect, test } from "@playwright/test";

const filenames = [
  "B2_REFERENCE_PREVIEW.pdf",
  "B2_REFERENCE_PREVIEW.docx",
  "USPTO_APPLICATION_DRAFT.pdf",
  "USPTO_APPLICATION_DRAFT.docx",
] as const;

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem("aiip.locale", "en"));
});

test("four P2-006 downloads are genuine files with expected signatures and filenames", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", {name: "USPTO-format reference exports"})).toBeVisible();
  await expect(page.getByText("Sample provenance validated · four exports available")).toBeVisible();
  await expect(page.getByText(/SYNTHETIC SAMPLE ONLY · DRAFT · NOT ISSUED · CLAIMS INCOMPLETE/)).toBeVisible();
  for (const name of filenames) {
    const pending = page.waitForEvent("download");
    await page.getByRole("button", {name: `Download ${name}`}).click();
    const item = await pending;
    expect(item.suggestedFilename()).toBe(name);
    const bytes = await readFile(await item.path());
    expect(bytes.length).toBeGreaterThan(1000);
    expect(bytes.subarray(0, name.endsWith(".pdf") ? 5 : 4).toString("latin1"))
      .toBe(name.endsWith(".pdf") ? "%PDF-" : "PK\x03\x04");
  }
  await expect(page.getByRole("button", {name: "Use synthetic PDF demo"})).toBeVisible();
});

test("native Vietnamese locale, keyboard focus, and narrow mobile exports", async ({ page }) => {
  await page.setViewportSize({width: 390, height: 844});
  await page.goto("/");
  await page.getByRole("combobox", {name: "Language"}).selectOption("vi");
  await expect(page.getByRole("heading", {name: "Bản tham chiếu định dạng USPTO"})).toBeVisible();
  await expect(page.getByText(/CHỈ LÀ MẪU TỔNG HỢP · BẢN NHÁP/)).toBeVisible();
  const pdf = page.getByRole("button", {name: "Tải B2_REFERENCE_PREVIEW.pdf"});
  await expect(pdf).toBeEnabled();
  await pdf.focus();
  await expect(pdf).toBeFocused();
  const pending = page.waitForEvent("download");
  await page.keyboard.press("Enter");
  expect((await pending).suggestedFilename()).toBe("B2_REFERENCE_PREVIEW.pdf");
  const width = await page.evaluate(() => ({body: document.body.scrollWidth, viewport: innerWidth}));
  expect(width.body).toBeLessThanOrEqual(width.viewport);
});

test("unavailable synthetic source presents localizable retry without enabling downloads", async ({ page }) => {
  await page.route("**/backend/api/demo/uspto/exports", async (route) => {
    await route.fulfill({status: 503, contentType: "application/json", body: JSON.stringify({error:{code:"synthetic_export_unavailable",message:"Unavailable"}})});
  });
  await page.goto("/");
  await expect(page.getByText("The sample reference exports are unavailable. Please try again.")).toBeVisible();
  await expect(page.getByRole("button", {name: "Download B2_REFERENCE_PREVIEW.pdf"})).toBeDisabled();
  await expect(page.getByRole("button", {name: "Retry"})).toBeVisible();
  await page.unroute("**/backend/api/demo/uspto/exports");
  await page.getByRole("button", {name: "Retry"}).click();
  await expect(page.getByRole("button", {name: "Download USPTO_APPLICATION_DRAFT.docx"})).toBeEnabled();
});
