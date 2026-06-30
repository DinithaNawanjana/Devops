"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  getMe, getProgress, getStats, getBadges, clearToken,
  type User, type Progress, type Stats, type Badge,
} from "@/lib/api";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [badges, setBadges] = useState<Badge[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getMe(), getStats(), getProgress(), getBadges()])
      .then(([u, s, p, b]) => { setUser(u); setStats(s); setProgress(p); setBadges(b); })
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div>
        <p className="text-slate-600 mb-3">You need to log in to see your dashboard.</p>
        <Link href="/login" className="text-brand underline">Go to login →</Link>
      </div>
    );
  }
  if (!user || !stats) return <p className="text-slate-500">Loading…</p>;

  const completed = progress.filter((p) => p.status === "completed");

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Welcome, {user.username}</h1>
        <button
          onClick={() => { clearToken(); location.href = "/login"; }}
          className="text-sm text-slate-500 hover:text-slate-800"
        >
          Log out
        </button>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <Stat label="Level" value={stats.level} />
        <Stat label="Total XP" value={stats.xp} />
        <Stat label="🔥 Streak" value={`${stats.streak_days}d`} />
        <Stat label="Badges" value={stats.badges_earned} />
      </div>

      <div className="bg-white border rounded-xl p-5 mb-8">
        <p className="text-sm text-slate-500 mb-1">Progress to level {stats.level + 1}</p>
        <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-brand"
            style={{ width: `${(stats.xp_into_level / stats.xp_per_level) * 100}%` }}
          />
        </div>
        <p className="text-xs text-slate-400 mt-1">
          {stats.xp_into_level} / {stats.xp_per_level} XP
        </p>
      </div>

      <h2 className="text-lg font-semibold mb-3">Badges</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-8">
        {badges.map((b) => (
          <div
            key={b.slug}
            className={`border rounded-xl p-3 text-center ${
              b.earned ? "bg-amber-50 border-amber-300" : "bg-slate-50 border-slate-200 opacity-60"
            }`}
            title={b.description}
          >
            <div className="text-2xl">{b.earned ? "🏅" : "🔒"}</div>
            <div className="text-sm font-medium">{b.title}</div>
            <div className="text-xs text-slate-500">{b.description}</div>
          </div>
        ))}
      </div>

      <h2 className="text-lg font-semibold mb-3">Completed items</h2>
      {completed.length === 0 ? (
        <p className="text-slate-500 text-sm">
          Nothing yet — <Link href="/" className="text-brand underline">pick a lab</Link>.
        </p>
      ) : (
        <ul className="space-y-2">
          {completed.map((p) => (
            <li key={`${p.item_type}-${p.item_id}`} className="bg-white border rounded-lg px-4 py-2 flex justify-between text-sm">
              <span><span className="text-slate-400">{p.item_type}</span> · {p.item_id}</span>
              <span className="text-green-600">+{p.score} XP</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="bg-white border rounded-xl p-5 text-center">
      <div className="text-3xl font-bold text-brand">{value}</div>
      <div className="text-sm text-slate-500">{label}</div>
    </div>
  );
}
