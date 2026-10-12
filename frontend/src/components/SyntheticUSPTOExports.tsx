"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  ApiClientError, downloadSyntheticUSPTOExport, getSyntheticUSPTOCapability,
  USPTO_EXPORT_FILES, type USPTOExportFilename,
} from "@/lib/api/client";
import { useUi } from "@/lib/uiPreferences";

type Availability = "checking" | "available" | "error";

export function SyntheticUSPTOExports() {
  const { t } = useUi();
  const [availability, setAvailability] = useState<Availability>("checking");
  const [downloading, setDownloading] = useState<USPTOExportFilename | null>(null);
  const [downloadError, setDownloadError] = useState(false);
  const mounted = useRef(true);

  const check = useCallback(async () => {
    setAvailability("checking");
    setDownloadError(false);
    try {
      await getSyntheticUSPTOCapability();
      if (mounted.current) setAvailability("available");
    } catch {
      if (mounted.current) setAvailability("error");
    }
  }, []);

  useEffect(() => {
    mounted.current = true;
    void getSyntheticUSPTOCapability().then(
      () => { if (mounted.current) setAvailability("available"); },
      () => { if (mounted.current) setAvailability("error"); },
    );
    return () => { mounted.current = false; };
  }, []);

  const download = async (filename: USPTOExportFilename) => {
    if (availability !== "available" || downloading) return;
    setDownloadError(false);
    setDownloading(filename);
    try {
      const blob = await downloadSyntheticUSPTOExport(filename);
      if (!blob.size || !mounted.current) throw new ApiClientError({
        status: 502, code: "empty_synthetic_download", message: "Empty synthetic export",
      });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = filename;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch {
      if (mounted.current) setDownloadError(true);
    } finally {
      if (mounted.current) setDownloading(null);
    }
  };

  const profiles = [
    { key: "B2_REFERENCE_PREVIEW", title: t("usptoPreview"), help: t("usptoPreviewHelp") },
    { key: "USPTO_APPLICATION_DRAFT", title: t("usptoDraft"), help: t("usptoDraftHelp") },
  ] as const;

  return (
    <section className="uspto-exports stage-card" aria-labelledby="uspto-exports-title">
      <p className="eyebrow">P2-006 · P2-005</p>
      <h2 id="uspto-exports-title">{t("usptoHeading")}</h2>
      <p>{t("usptoIntro")}</p>
      <p className="uspto-boundary">{t("usptoBoundary")}</p>
      <div aria-live="polite" role="status" className="uspto-export-status">
        {availability === "checking" && t("usptoLoading")}
        {availability === "available" && !downloadError && t("usptoReady")}
        {(availability === "error" || downloadError) && t("usptoUnavailable")}
      </div>
      {availability === "error" && (
        <button type="button" className="secondary-button" onClick={() => void check()}>
          {t("usptoRetry")}
        </button>
      )}
      <div className="uspto-profile-grid">
        {profiles.map((profile) => (
          <section key={profile.key} className="uspto-profile" aria-label={profile.title}>
            <h3>{profile.title}</h3>
            <p>{profile.help}</p>
            <div className="uspto-profile-actions">
              {(["pdf", "docx"] as const).map((extension) => {
                const filename = `${profile.key}.${extension}` as USPTOExportFilename;
                return (
                  <button
                    type="button"
                    className="secondary-button"
                    key={filename}
                    disabled={availability !== "available" || downloading !== null || !USPTO_EXPORT_FILES.includes(filename)}
                    onClick={() => void download(filename)}
                    aria-label={`${t("usptoDownload")} ${filename}`}
                  >
                    {downloading === filename ? t("usptoPreparing") : `${t("usptoDownload")} ${extension.toUpperCase()}`}
                  </button>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </section>
  );
}
