import "./globals.css";
import type { Metadata } from "next";
import Navbar from "../components/layout/Navbar"

export const metadata: Metadata = {
  title: "PromptCraft",
  description: "Verbessere Prompts mit KI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="de">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
