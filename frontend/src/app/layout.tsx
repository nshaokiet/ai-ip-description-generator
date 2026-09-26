import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI IP Description Generator",
  description: "Local human-review workspace for grounded patent description drafts.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
