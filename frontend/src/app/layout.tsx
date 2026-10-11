import type { Metadata } from "next";

import "./globals.css";
import "./uiux.css";

export const metadata: Metadata = {
  title: "AI IP Description Generator",
  description: "Local human-review workspace for grounded patent description drafts.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi" data-theme="light" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
