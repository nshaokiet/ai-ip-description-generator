import { test, expect, type Page } from "@playwright/test";

const widths = [390, 768, 1280, 1440, 1920];
const savedThemes = ["light", "dark", "system"] as const;
const locales = ["vi", "en"] as const;
const backend = `http://127.0.0.1:${process.env.PLAYWRIGHT_BACKEND_PORT ?? "8000"}`;

async function overflow(page: Page) {
  const size = await page.evaluate(() => ({ width: innerWidth, body: document.body.scrollWidth, html: document.documentElement.scrollWidth }));
  expect(size.body).toBeLessThanOrEqual(size.width);
  expect(size.html).toBeLessThanOrEqual(size.width);
}
async function screenshot(page: Page, name: string) {
  const file = test.info().outputPath(`${name}.png`);
  await page.screenshot({ path: file, fullPage: true });
  await test.info().attach(name, { path: file, contentType: "image/png" });
}
async function contrast(page: Page, name: string) {
  const report = await page.evaluate(() => {
    const rgb = (value: string) => { const numbers = value.match(/[\d.]+/g)?.map(Number) ?? []; return [numbers[0] ?? 0, numbers[1] ?? 0, numbers[2] ?? 0, numbers[3] ?? 1]; };
    const mix = (front: number[], back: number[]) => front.slice(0, 3).map((v, i) => v * front[3] + back[i] * (1 - front[3])).concat(1);
    const luminance = (color: number[]) => color.slice(0, 3).map(v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((total, v, i) => total + v * [.2126, .7152, .0722][i], 0);
    const failures: Array<{ text: string; class: string; ratio: number; required: number; foreground: string; background: number[] }> = [];
    let checked = 0; let minimum = 21;
    for (const element of document.querySelectorAll<HTMLElement>("body *")) {
      if (!(element instanceof HTMLElement) || !Array.from(element.childNodes).some(node => node.nodeType === Node.TEXT_NODE && node.textContent?.trim())) continue;
      const css = getComputedStyle(element), box = element.getBoundingClientRect();
      if (!box.width || !box.height || css.visibility === "hidden" || element.closest(".sr-only,[aria-hidden=true],[inert],button:disabled,select:disabled,option,script,style")) continue;
      const ancestors: HTMLElement[] = []; let parent: HTMLElement | null = element;
      while (parent) { ancestors.unshift(parent); parent = parent.parentElement; }
      let background = [255,255,255,1];
      for (const ancestor of ancestors) background = mix(rgb(getComputedStyle(ancestor).backgroundColor), background);
      const foreground = mix(rgb(css.color), background);
      const a = luminance(foreground), b = luminance(background);
      const ratio = (Math.max(a,b) + .05) / (Math.min(a,b) + .05);
      const large = parseFloat(css.fontSize) >= 24 || (parseFloat(css.fontSize) >= 18.66 && parseInt(css.fontWeight) >= 700);
      const required = large ? 3 : 4.5;
      checked++; minimum = Math.min(minimum, ratio);
      if (ratio < required) failures.push({ text: element.textContent?.trim().slice(0,90) ?? "", class: element.className, ratio, required, foreground: css.color, background });
    }
    return { checked, minimum, failures };
  });
  await test.info().attach(`contrast-${name}`, { body: JSON.stringify(report, null, 2), contentType: "application/json" });
  expect(report.checked).toBeGreaterThan(0);
  expect(report.failures, JSON.stringify(report.failures, null, 2)).toEqual([]);
}

async function processSample(page: Page) {
  const fixture = await page.request.get(`${backend}/__test/pdf`);
  expect(fixture.ok()).toBeTruthy();
  await page.locator("#document-file").setInputFiles({ name: "synthetic.pdf", mimeType: "application/pdf", buffer: await fixture.body() });
  await page.locator(".upload-card .primary-button").last().click();
  await expect(page.locator(".upload-success-card")).toBeVisible();
  await page.locator(".upload-success-actions .primary-button").click();
  await expect(page.locator(".document-review-layout")).toBeVisible();
}

for (const width of widths) for (const theme of savedThemes) for (const locale of locales) {
  test(`presentation ${width} ${theme} ${locale}`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
    await page.addInitScript(({ theme, locale }) => { localStorage.setItem("aiip.theme", theme); localStorage.setItem("aiip.locale", locale); }, { theme, locale });
    const warnings: string[] = [];
    page.on("console", message => { if (/hydration|did not match/i.test(message.text())) warnings.push(message.text()); });
    await page.goto("/");
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    expect(await page.evaluate(() => localStorage.getItem("aiip.theme"))).toBe(theme);
    await expect(page.locator("html")).toHaveAttribute("lang", locale);
    await expect(page.locator(".preference-controls select")).toHaveCount(1);
    await expect(page.getByRole("combobox", { name: /Appearance|Giao diện/ })).toHaveCount(0);
    await expect(page.locator(".preference-controls select").last()).toHaveValue(locale);
    for (const control of await page.locator(".preference-controls select").all()) {
      const box = await control.boundingBox();
      expect(box?.height ?? 0).toBeGreaterThanOrEqual(44);
      expect(box?.width ?? 0).toBeGreaterThanOrEqual(44);
    }
    await expect(page.locator(".workflow-step")).toHaveCount(5);
    await expect(page.locator(".workflow-step").last().locator("button")).toBeDisabled();
    await overflow(page);
    const safe = await page.locator(".margin-motifs").evaluate(element => ({ hidden: element.getAttribute("aria-hidden"), events: getComputedStyle(element).pointerEvents, display: getComputedStyle(element).display }));
    expect(safe.hidden).toBe("true"); expect(safe.events).toBe("none");
    if (width === 390) expect(safe.display).toBe("none");
    else expect(safe.display).not.toBe("none");
    if (width >= 768) {
      const margins = await page.evaluate(() => {
        const content = document.querySelector(".workflow-shell")!.getBoundingClientRect();
        const left = document.querySelector(".motif-science")!.getBoundingClientRect();
        const right = document.querySelector(".motif-patent")!.getBoundingClientRect();
        return {left:right.width > 0 && left.right <= content.left, right:right.left >= content.right};
      });
      expect(margins).toEqual({left:true, right:true});
    }
    expect(await page.locator(".motif-secondary").first().evaluate(e=>getComputedStyle(e).stroke)).toBe("rgb(22, 150, 212)");
    expect(await page.locator(".motif-accent").first().evaluate(e=>getComputedStyle(e).stroke)).toBe("rgb(241, 95, 34)");
    const button = page.locator(".select-file-button");
    await button.scrollIntoViewIfNeeded();
    const hit = await button.evaluate(element => { const box = element.getBoundingClientRect(); return element.contains(document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2)); });
    expect(hit).toBeTruthy();
    const geometry = await page.evaluate(() => {
      const rect = (selector: string) => { const e = document.querySelector<HTMLElement>(selector)!; const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return { x:r.x, y:r.y, width:r.width, height:r.height, center:r.y+r.height/2, font:c.fontFamily, fontSize:parseFloat(c.fontSize), lineHeight:parseFloat(c.lineHeight), overflow:e.scrollWidth > e.clientWidth }; };
      return { logo:rect(".brand-logo"), divider:rect(".brand-divider"), title:rect(".product-name"), hero:rect(".hero h1"), steps:Array.from(document.querySelectorAll<HTMLElement>(".workflow-step button")).map(e => { const r=e.getBoundingClientRect(); const copy=e.querySelector<HTMLElement>(".step-copy")!; const cr=copy.getBoundingClientRect(); return {height:r.height, center:r.y+r.height/2, copyCenter:cr.y+cr.height/2, clipped:copy.scrollHeight>copy.clientHeight || copy.scrollWidth>copy.clientWidth, font:getComputedStyle(copy).fontFamily}; }) };
    });
    const baselineLogo = width <= 700 ? 140 : 190;
    const baselineTitle = width <= 700 ? 12.48 : 15.36;
    expect(geometry.logo.width / baselineLogo).toBeGreaterThanOrEqual(.85);
    expect(geometry.logo.width / baselineLogo).toBeLessThanOrEqual(.9);
    expect(geometry.title.fontSize / baselineTitle).toBeGreaterThanOrEqual(1.1);
    expect(geometry.title.fontSize / baselineTitle).toBeLessThanOrEqual(1.15);
    expect(Math.abs(geometry.logo.center-geometry.title.center)).toBeLessThan(1);
    expect(Math.abs(geometry.divider.center-geometry.title.center)).toBeLessThan(1);
    expect(geometry.title.font).toContain("sans-serif");
    expect(geometry.hero.font).toBe(geometry.title.font);
    expect(geometry.hero.overflow).toBe(false);
    expect(geometry.steps.every(e => !e.clipped && Math.abs(e.center-e.copyCenter)<1 && e.font===geometry.title.font)).toBe(true);
    expect(Math.max(...geometry.steps.map(e=>e.height))-Math.min(...geometry.steps.map(e=>e.height))).toBeLessThan(1);
    await test.info().attach("layout-measurements", {body:JSON.stringify(geometry,null,2),contentType:"application/json"});
    if (width === 1440 && theme === "light" && locale === "vi") {
      await page.locator(".site-header").screenshot({path:test.info().outputPath("header-closeup.png")});
      await page.locator(".workflow-progress").screenshot({path:test.info().outputPath("workflow-closeup.png")});
    }
    await screenshot(page, `home-${width}-${theme}-${locale}`);
    if (width === 1280) await contrast(page, `home-${theme}-${locale}`);
    expect(warnings).toEqual([]);
  });
}

test("fixed light on first paint and OS changes; locale persists", async ({ page }) => {
  await page.emulateMedia({ colorScheme: "dark" });
  await page.goto("/");
  await expect(page.locator("html")).toHaveAttribute("lang", "vi");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await page.emulateMedia({ colorScheme: "light" });
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await page.locator(".preference-controls select").selectOption("en");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  expect(await page.evaluate(() => localStorage.getItem("aiip.locale"))).toBe("en");
  // No application JS: server markup and CSS must already be light in OS-dark.
  await page.route("**/_next/static/**/*.js", route => route.abort());
  await page.emulateMedia({ colorScheme: "dark" });
  await page.reload({ waitUntil: "domcontentloaded" });
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  expect(await page.locator("html").evaluate(e => getComputedStyle(e).colorScheme)).toBe("light");
});

test("safe localized upload errors update without losing file state", async ({ page }) => {
  await page.goto("/");
  await page.locator("#document-file").setInputFiles({ name: "bad.txt", mimeType: "text/plain", buffer: Buffer.from("synthetic") });
  await expect(page.locator(".upload-card .field-error")).toContainText("PDF");
  await page.locator(".preference-controls select").last().selectOption("en");
  await expect(page.locator(".upload-card .field-error")).toContainText("Choose one PDF or DOCX file.");
  await page.locator("#document-file").setInputFiles({ name: "synthetic.pdf", mimeType: "application/pdf", buffer: Buffer.from("synthetic") });
  await page.route("**/backend/api/documents", route => route.fulfill({ status: 422, contentType: "application/json", body: JSON.stringify({ error: { code: "unknown", message: "CONFIDENTIAL_INTERNAL_TEXT" } }) }));
  await page.locator(".upload-card .primary-button").last().click();
  await expect(page.locator(".error-banner")).not.toContainText("CONFIDENTIAL_INTERNAL_TEXT");
  await expect(page.locator(".error-banner")).toContainText("The local service could not complete the request.");
  await page.locator(".preference-controls select").last().selectOption("vi");
  await expect(page.locator(".error-banner")).toContainText("Dịch vụ cục bộ");
  await expect(page.locator(".selected-file")).toContainText("synthetic.pdf");
});

for (const width of widths) {
  test(`review edit guard evidence and export ${width}`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    const external: string[] = [];
    await page.route("**/*", async route => { const url = new URL(route.request().url()); if (url.protocol.startsWith("http") && !["127.0.0.1", "localhost"].includes(url.hostname)) { external.push(url.hostname); await route.abort(); } else await route.continue(); });
    await page.goto("/");
    await page.locator(".preference-controls select").last().selectOption("en");
    await processSample(page);
    const center = page.locator(".document-center");
    const node = await center.evaluate(element => { (window as unknown as { retainedCenter: Element }).retainedCenter = element; return true; });
    expect(node).toBeTruthy();
    await page.getByRole("button", { name: "Edit prose", exact: true }).click();
    const editor = page.getByLabel("Paragraph paragraph-field prose");
    const prose = "Synthetic sensor calibration " + "long-unbroken-text".repeat(20);
    await editor.fill(prose);
    await page.locator(".preference-controls select").last().selectOption("vi");
    await expect(editor).toHaveCount(0);
    await expect(page.locator("#edit-paragraph-field")).toHaveValue(prose);
    expect(await center.evaluate(element => (window as unknown as { retainedCenter: Element }).retainedCenter === element)).toBe(true);
    await overflow(page);
    await screenshot(page, `review-${width}-light-vi`);
    if (width === 390) await contrast(page, "editing-light-vi");
    await page.locator(".preference-controls select").last().selectOption("en");
    await page.getByRole("button", { name: "Cancel edit", exact: true }).click();
    const dialog = page.getByRole("dialog", { name: "Confirm session change" });
    await expect(dialog).toBeVisible();
    if (width === 390) await contrast(page, "dialog-light-en");
    await expect(page.getByRole("button", { name: "Keep editing", exact: true })).toBeFocused();
    await page.keyboard.press("Shift+Tab");
    await expect(page.getByRole("button", { name: "Discard changes and continue" })).toBeFocused();
    await page.keyboard.press("Tab");
    await expect(page.getByRole("button", { name: "Keep editing", exact: true })).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(dialog).toHaveCount(0);
    await expect(page.getByRole("button", { name: "Cancel edit", exact: true })).toBeFocused();
    await expect(editor).toHaveValue(prose);
    await page.getByRole("button", { name: "Save new revision" }).click();
    await expect(page.getByLabel("Selected revision", { exact: true })).toHaveValue("revision-2");
    await page.locator(".evidence-jump").first().click();
    await expect(page.locator("#evidence-inspector-heading")).toBeFocused();
    await expect(page.locator(".evidence-inspector blockquote")).toBeVisible();
    await overflow(page);
    await screenshot(page, `review-${width}-light-en`);
    if (width === 1440) await page.screenshot({path:test.info().outputPath("review-workspace-viewport.png"),fullPage:false});
    if (width === 390) await contrast(page, "review-light-en");
    const controls = page.getByLabel(/^Session review status for /);
    for (let i = 0; i < await controls.count(); i++) await controls.nth(i).selectOption("REVIEWED");
    await page.getByRole("button", { name: "Continue to Validation → · revision-2" }).click();
    await page.getByRole("button", { name: "Validate revision-2" }).click();
    await expect(page.getByRole("heading", { name: "Validation complete" })).toBeVisible();
    await page.locator(".preference-controls select").last().selectOption("vi");
    await expect(page.getByRole("heading", { name: "Đã xác thực cấu trúc" })).toBeVisible();
    await overflow(page);
    await screenshot(page, `validation-${width}-light-vi`);
    await page.getByRole("button", { name: "Tiếp tục xuất DOCX →" }).click();
    await expect(page.locator(".export-summary strong")).toHaveText("revision-2");
    await expect(page.locator(".card-supporting-copy").filter({ hasText: "PDF" })).toContainText("chưa khả dụng");
    const download = page.waitForEvent("download");
    await page.locator(".export-primary-button").click();
    expect((await download).suggestedFilename()).toBe("patent-description-draft.docx");
    await overflow(page);
    expect(external).toEqual([]);
  });
}

for (const width of widths) for (const locale of locales) {
  test(`fixed light OS-light ${width} ${locale}`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.emulateMedia({ colorScheme: "light" });
    await page.goto("/");
    await page.locator(".preference-controls select").last().selectOption(locale);
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    await expect(page.locator(".preference-controls select")).toHaveCount(1);
    await overflow(page);
    await screenshot(page, `home-${width}-system-oslight-${locale}`);
  });
}

test("corrupted preferences and denied storage retain safe defaults and session switching", async ({ page }) => {
  await page.addInitScript(() => { localStorage.setItem("aiip.locale", "corrupt"); localStorage.setItem("aiip.theme", "corrupt"); });
  await page.goto("/");
  await expect(page.locator(".preference-controls select")).toHaveCount(1);
  await expect(page.locator("html")).toHaveAttribute("lang", "vi");
  await page.evaluate(() => { Storage.prototype.setItem = () => { throw new Error("Storage writes unavailable"); }; });
  await page.locator(".preference-controls select").last().selectOption("en");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await page.evaluate(() => { Object.defineProperty(window, "localStorage", { get() { throw new Error("Storage unavailable"); } }); });
  await page.locator(".preference-controls select").last().selectOption("vi");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect(page.locator("html")).toHaveAttribute("lang", "vi");
});

test("mapped validation issue focuses the affected editor and rejects mismatched success", async ({ page }) => {
  await page.goto("/");
  await page.locator(".preference-controls select").last().selectOption("en");
  await processSample(page);
  const controls = page.getByLabel(/^Session review status for /);
  for (let i = 0; i < await controls.count(); i++) await controls.nth(i).selectOption("REVIEWED");
  await page.getByRole("button", { name: "Continue to Validation → · revision-1" }).click();
  await page.route("**/backend/api/drafts/validate", route => route.fulfill({ status: 422, contentType: "application/json", body: JSON.stringify({ error: { code: "draft_business_validation_failed", message: "HIDDEN_INTERNAL_MESSAGE", paths: ["/draft_sections/0/paragraphs/0/text", "/unmapped"] } }) }));
  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.locator(".error-banner")).not.toContainText("HIDDEN_INTERNAL_MESSAGE");
  await page.getByRole("button", { name: "Go to field: /draft_sections/0/paragraphs/0/text" }).click();
  await expect(page.locator("#edit-paragraph-field")).toBeFocused();
  await page.getByRole("button", { name: "Cancel edit", exact: true }).click();
  await page.getByRole("button", { name: "Continue to Validation → · revision-1" }).click();
  await page.unroute("**/backend/api/drafts/validate");
  await page.route("**/backend/api/drafts/validate", route => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ valid: true, revision_id: "wrong-revision", draft_digest: "invalid" }) }));
  await page.getByRole("button", { name: "Validate revision-1" }).click();
  await expect(page.getByRole("heading", { name: /Draft validation failed/ })).toBeVisible();
  await expect(page.locator(".workflow-step").last().locator("button")).toBeDisabled();
});

test("measured control boundaries and keyboard focus exceed 3 to 1", async ({ page }) => {
  await page.goto("/");
  const measurements: unknown[] = [];
  for (const scheme of ["light", "dark"] as const) {
    await page.emulateMedia({ colorScheme: scheme });
    const button = page.locator(".select-file-button");
    await button.focus();
    await page.keyboard.press("Shift+Tab");
    await page.keyboard.press("Tab");
    const report = await page.evaluate(() => {
      const lum = (value: string) => { const rgb = value.match(/[\d.]+/g)!.slice(0,3).map(Number).map(v => { v /= 255; return v <= .04045 ? v/12.92 : ((v+.055)/1.055)**2.4; }); return rgb.reduce((sum,v,i) => sum + v*[.2126,.7152,.0722][i],0); };
      const ratio = (a: string, b: string) => (Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
      const controls = Array.from(document.querySelectorAll<HTMLElement>(".preference-controls select,.drop-zone"));
      const surface = getComputedStyle(document.documentElement).getPropertyValue("--color-surface").trim();
      const parser = document.createElement("span"); parser.style.color = surface; document.body.append(parser); const bg = getComputedStyle(parser).color; parser.remove();
      const borders = controls.map(e => ratio(getComputedStyle(e).borderTopColor,bg));
      const focused = getComputedStyle(document.activeElement!);
      return { borders, outline: focused.outlineStyle, outlineWidth: focused.outlineWidth, focusRatio: ratio(focused.outlineColor,bg) };
    });
    expect(report.borders.every(ratio => ratio >= 3), JSON.stringify(report)).toBe(true);
    expect(report.outline).toBe("solid");
    expect(parseFloat(report.outlineWidth)).toBeGreaterThanOrEqual(3);
    expect(report.focusRatio).toBeGreaterThanOrEqual(3);
    measurements.push({ scheme, ...report });
  }
  await test.info().attach("nontext-contrast", { body: JSON.stringify(measurements,null,2), contentType: "application/json" });
});

test("upload rejects empty oversized and multiple dropped synthetic files locally", async ({ page }) => {
  await page.goto("/");
  await page.locator(".preference-controls select").last().selectOption("en");
  const submissions: string[] = [];
  page.on("request", request => { if (request.method() === "POST") submissions.push(request.url()); });
  await page.locator("#document-file").setInputFiles({ name: "empty.pdf", mimeType: "application/pdf", buffer: Buffer.alloc(0) });
  await expect(page.locator(".field-error")).toHaveText("The selected file is empty.");
  await page.locator("#document-file").setInputFiles({ name: "large.pdf", mimeType: "application/pdf", buffer: Buffer.alloc(10*1024*1024+1) });
  await expect(page.locator(".field-error")).toHaveText("File exceeds the 10 MiB limit.");
  const dataTransfer = await page.evaluateHandle(() => { const data = new DataTransfer(); data.items.add(new File(["synthetic"],"one.pdf")); data.items.add(new File(["synthetic"],"two.pdf")); return data; });
  await page.locator(".drop-zone").dispatchEvent("drop", { dataTransfer });
  await expect(page.locator(".field-error")).toHaveText("Choose exactly one document.");
  expect(submissions).toEqual([]);
});

test("dirty stage navigation can retain edits or discard before a clean new session", async ({ page }) => {
  await page.goto("/");
  await page.locator(".preference-controls select").last().selectOption("en");
  await processSample(page);
  await page.getByRole("button", { name: "Edit prose", exact: true }).click();
  await page.locator("#edit-paragraph-field").fill("Unsaved synthetic navigation text.");
  await page.getByRole("button", { name: /1\. Source Upload/ }).click();
  await page.getByRole("button", { name: "Keep editing", exact: true }).click();
  await expect(page.locator("#edit-paragraph-field")).toHaveValue("Unsaved synthetic navigation text.");
  await page.getByRole("button", { name: /1\. Source Upload/ }).click();
  await page.getByRole("button", { name: "Discard changes and continue" }).click();
  await expect(page.locator(".upload-success-card")).toBeVisible();
  await page.getByRole("button", { name: /3\. Review & Refine/ }).click();
  await expect(page.locator(".document-center")).not.toContainText("Unsaved synthetic navigation text.");
  await page.getByRole("button", { name: "New paper", exact: true }).click();
  await page.getByRole("button", { name: "Clear session and start over" }).click();
  await expect(page.locator(".upload-card")).toBeVisible();
  await processSample(page);
  await expect(page.getByLabel("Selected revision", { exact: true }).locator("option")).toHaveCount(1);
});
