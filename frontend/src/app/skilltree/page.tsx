"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getSkillTree, type SkillNode } from "@/lib/api";

const STATUS_STYLE: Record<string, string> = {
  completed: "bg-green-100 border-green-400 text-green-800",
  available: "bg-white border-brand text-slate-800 hover:shadow",
  locked: "bg-slate-100 border-slate-300 text-slate-400",
};
const ICON: Record<string, string> = { completed: "✅", available: "🔓", locked: "🔒" };

export default function SkillTreePage() {
  const [nodes, setNodes] = useState<SkillNode[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getSkillTree().then(setNodes).catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div>
        <p className="text-slate-600 mb-3">Log in to see your personalized skill tree.</p>
        <Link href="/login" className="text-brand underline">Go to login →</Link>
      </div>
    );
  }

  const byTrack = nodes.reduce<Record<string, SkillNode[]>>((acc, n) => {
    (acc[n.track] ??= []).push(n);
    return acc;
  }, {});

  return (
    <div>
      <h1 className="text-2xl font-bold mb-1">Skill Tree</h1>
      <p className="text-slate-600 mb-6 text-sm">
        🔒 Locked items unlock once you complete their prerequisites.
      </p>

      {Object.entries(byTrack).map(([track, items]) => (
        <section key={track} className="mb-6">
          <h2 className="font-semibold mb-2 capitalize">{track.replace(/-/g, " ")}</h2>
          <div className="flex flex-wrap gap-3">
            {items.map((n) => {
              const card = (
                <div className={`rounded-xl border px-4 py-3 w-56 ${STATUS_STYLE[n.status]}`}>
                  <div className="flex items-center justify-between">
                    <span className="text-xs uppercase tracking-wide">{n.type}</span>
                    <span>{ICON[n.status]}</span>
                  </div>
                  <p className="font-medium text-sm mt-1">{n.title}</p>
                  <p className="text-xs mt-1">{n.points} pts · {n.level}</p>
                  {n.status === "locked" && n.prerequisites.length > 0 && (
                    <p className="text-[11px] mt-1">needs: {n.prerequisites.join(", ")}</p>
                  )}
                </div>
              );
              return n.status === "locked" ? (
                <div key={n.id}>{card}</div>
              ) : (
                <Link key={n.id} href={`/labs/${n.id}`}>{card}</Link>
              );
            })}
          </div>
        </section>
      ))}

      {nodes.length === 0 && !error && <p className="text-slate-500">Loading…</p>}
    </div>
  );
}
