import type { NextConfig } from "next";

const backendUrl = (process.env.BACKEND_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
const renderStaticExport = process.env.RENDER_STATIC_EXPORT === "1";

const localSecurityHeaders = [
  { key: "Cache-Control", value: "no-store" },
  { key: "Permissions-Policy", value: "camera=(), geolocation=(), microphone=()" },
  { key: "Referrer-Policy", value: "no-referrer" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
];

const nextConfig: NextConfig = renderStaticExport
  ? {
      output: "export",
      images: { unoptimized: true },
    }
  : {
      async headers() {
        return [{ source: "/:path*", headers: localSecurityHeaders }];
      },
      async rewrites() {
        return [
          {
            source: "/backend/:path*",
            destination: `${backendUrl}/:path*`,
          },
        ];
      },
    };

export default nextConfig;
