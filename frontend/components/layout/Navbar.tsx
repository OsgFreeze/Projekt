"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <Link href="/" className="logo" title="Prompt verbessern">
        ✦
      </Link>

      <nav className="navItems">
        <Link
          href="/"
          className={`navItem ${pathname === "/" ? "active" : ""}`}
          title="Verbessern"
        >
          ✨
        </Link>

        <Link
          href="/stats"
          className={`navItem ${pathname === "/stats" ? "active" : ""}`}
          title="Statistiken"
        >
          📊
        </Link>

        <Link
          href="/history"
          className={`navItem ${pathname === "/history" ? "active" : ""}`}
          title="Verlauf"
        >
          🕒
        </Link>

        <Link
          href="/settings"
          className={`navItem ${pathname === "/settings" ? "active" : ""}`}
          title="Einstellungen"
        >
          ⚙️
        </Link>
      </nav>
    </aside>
  );
}