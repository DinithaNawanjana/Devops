"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { getTracks, getLabs, getProjects, type Track, type Lab } from "@/lib/api";

const LEVEL_ORDER = ["beginner", "intermediate", "advanced", "expert"];
const LEVEL_STYLE: Record<string, string> = {
  beginner: "bg-green-100 text-green-800",
  intermediate: "bg-yellow-100 text-yellow-800",
  advanced: "bg-orange-100 text-orange-800",
  expert: "bg-red-100 text-red-800",
};

export default function Home() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [labs, setLabs] = useState<Lab[]>([]);
  const [projects, setProjects] = useState<Lab[]>([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getTracks(), getLabs(), getProjects()])
      .then(([t, l, p]) => { setTracks(t); setLabs(l); setProjects(p); })
      .catch((e) => setError(e.message));
  }, []);

  const items = useMemo(() => [...labs, ...projects], [labs, projects]);
  const q = query.trim().toLowerCase();
  const matches = (it: Lab) =>
    !q || it.title.toLowerCase().includes(q) || it.track.toLowerCase().includes(q);

  return (
    <div>
      <section className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Learn DevOps by doing</h1>
        <p className="text-slate-600">
          Theory, real browser terminals, and portfolio-worthy projects — from
          Linux basics to GitOps and SRE.
        </p>
      </section>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="🔍 Search labs & projects…"
        className="w-full border rounded-lg px-4 py-2 mb-6 bg-white"
      />

      {error && (
        <div className="bg-red-50 text-red-700 p-3 rounded mb-6 text-sm">
          {error} — is the API running on port 8000?
        </div>
      )}

      {LEVEL_ORDER.map((level) => {
        const levelTracks = tracks.filter((t) => t.level === level);
        if (levelTracks.length === 0) return null;
        // Hide tracks with no matching items when searching.
        const visible = levelTracks.filter(
          (t) => !q || items.some((it) => it.track === t.slug && matches(it)),
        );
        if (visible.length === 0) return null;
        return (
          <section key={level} className="mb-8">
            <h2 className="text-xl font-semibold mb-3 capitalize">{level}</h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {visible.map((t) => {
                const trackItems = items.filter((it) => it.track === t.slug && matches(it));
                return (
                  <div key={t.slug} className="bg-white rounded-xl border p-5 shadow-sm">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">{t.title}</h3>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${LEVEL_STYLE[level]}`}>
                        {level}
                      </span>
                    </div>
                    <p className="text-sm text-slate-600 mb-3">{t.description}</p>
                    <ul className="space-y-1">
                      {trackItems.map((it) => (
                        <li key={it.id}>
                          <Link
                            href={`/labs/${it.id}`}
                            className="text-sm text-brand hover:underline flex justify-between gap-2"
                          >
                            <span>{it.type === "project" ? "🚀" : "🧪"} {it.title}</span>
                            <span className="text-slate-400 shrink-0">{it.estimated_minutes}m</span>
                          </Link>
                        </li>
                      ))}
                      {trackItems.length === 0 && (
                        <li className="text-xs text-slate-400">Content coming soon</li>
                      )}
                    </ul>
                  </div>
                );
              })}
            </div>
          </section>
        );
      })}

      {tracks.length === 0 && !error && <p className="text-slate-500">Loading catalog…</p>}
    </div>
  );
}
