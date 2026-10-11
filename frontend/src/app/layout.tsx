import type { Metadata } from "next";

import "./globals.css";
import "./uiux.css";

export const metadata: Metadata = {
  title: "AI IP Description Generator",
  description: "Local human-review workspace for grounded patent description drafts.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: `(function(){try{var p=localStorage.getItem('aiip.theme');if(p!=='light'&&p!=='dark')p='system';var m=matchMedia('(prefers-color-scheme: dark)');document.documentElement.dataset.theme=p==='system'?(m.matches?'dark':'light'):p;}catch(e){document.documentElement.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}})();` }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
