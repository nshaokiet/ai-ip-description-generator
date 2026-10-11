import fs from "node:fs";
import { performance } from "node:perf_hooks";
import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }) => { await page.addInitScript(() => localStorage.setItem("aiip.locale", "en")); });

const backend = `http://127.0.0.1:${process.env.PLAYWRIGHT_BACKEND_PORT ?? "8000"}`;

test("P1-005 synthetic local browser workflow measurement", async ({ page }) => {
  await page.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.protocol.startsWith("http") && !["127.0.0.1", "localhost"].includes(url.hostname)) {
      await route.abort();
    } else {
      await route.continue();
    }
  });

  const fixtureResponse = await page.request.get(`${backend}/__test/pdf`);
  expect(fixtureResponse.ok()).toBeTruthy();
  const fixture = await fixtureResponse.body();
  const warmups = Number.parseInt(process.env.P1_005_BROWSER_WARMUPS ?? "0", 10);
  const sampleCount = Number.parseInt(process.env.P1_005_BROWSER_SAMPLES ?? "1", 10);
  expect(warmups).toBeGreaterThanOrEqual(0);
  expect(sampleCount).toBeGreaterThan(0);

  const samples: number[] = [];
  for (let index = 0; index < warmups + sampleCount; index += 1) {
    const started = performance.now();
    await page.goto("/");
    await page.locator("#document-file").setInputFiles({
      name: "p1-005-synthetic.pdf",
      mimeType: "application/pdf",
      buffer: fixture,
    });
    await page.getByRole("button", { name: "Upload & Validate" }).click();
    await expect(page.getByRole("heading", { name: "Paper uploaded successfully" })).toBeVisible();
    await page.getByRole("button", { name: "Continue to AI Extraction" }).click();
    await expect(page.getByRole("heading", { name: "Review & Refine" })).toBeVisible();
    await page.getByRole("tab", { name: "Patent Draft" }).click();
    const reviewControls = page.getByLabel(/^Session review status for /);
    const reviewTotal = await reviewControls.count();
    expect(reviewTotal).toBeGreaterThan(0);
    for (let reviewIndex = 0; reviewIndex < reviewTotal; reviewIndex += 1) {
      await reviewControls.nth(reviewIndex).selectOption("REVIEWED");
    }
    await page.getByRole("button", { name: "Continue to Validation → · revision-1" }).click();
    await page.getByRole("button", { name: "Validate revision-1" }).click();
    await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
    await page.getByRole("button", { name: "Continue to DOCX Export →" }).click();
    const downloadPromise = page.waitForEvent("download");
    await page.getByRole("button", { name: "Export revision-1 DOCX" }).click();
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toBe("patent-description-draft.docx");
    if (index >= warmups) samples.push(performance.now() - started);
  }

  const output = process.env.P1_005_BROWSER_RESULT;
  if (output) {
    fs.writeFileSync(output, JSON.stringify({
      workload: { format: "PDF", file_size_bytes: fixture.length, workflow: "upload-process-validate-export" },
      observed: { completed_downloads: sampleCount, outbound_network: "BLOCKED", provider_api_calls: "NONE" },
      samples_ms: samples,
    }, null, 2));
  }
});
