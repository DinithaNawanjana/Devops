import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "DevOps Learning Platform",
  description: "Beginner → Expert DevOps with theory, browser labs, and projects",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="bg-slate-900 text-white">
          <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
            <Link href="/" className="font-bold text-lg">
              🚀 DevOps<span className="text-brand">Labs</span>
            </Link>
            <nav className="flex gap-4 text-sm">
              <Link href="/" className="hover:text-brand">Tracks</Link>
              <Link href="/dashboard" className="hover:text-brand">Dashboard</Link>
              <Link href="/login" className="hover:text-brand">Login</Link>
            </nav>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
