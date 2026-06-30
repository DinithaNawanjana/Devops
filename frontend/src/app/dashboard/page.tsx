"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getMe, getProgress, clearToken, type User, type Progress } from "@/lib/api";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getMe(), getProgress()])
      .then(([u, p]) => {
        setUser(u);
        setProgress(p);
      })
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

  if (!user) return <p className="text-slate-500">Loading…</p>;

  const completed = progress.filter((p) => p.status === "completed");
  const xpInLevel = user.xp % 500;

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

      <div className="grid sm:grid-cols-3 gap-4 mb-8">
        <Stat label="Level" value={user.level} />
        <Stat label="Total XP" value={user.xp} />
        <Stat label="Completed" value={completed.length} />
      </div>

      <div className="bg-white border rounded-xl p-5 mb-8">
        <p className="text-sm text-slate-500 mb-1">Progress to level {user.level + 1}</p>
        <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
          <div className="h-full bg-brand" style={{ width: `${(xpInLevel / 500) * 100}%` }} />
        </div>
        <p className="text-xs text-slate-400 mt-1">{xpInLevel} / 500 XP</p>
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
              <span>{p.item_type}: {p.item_id}</span>
              <span className="text-green-600">+{p.score} XP</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-white border rounded-xl p-5 text-center">
      <div className="text-3xl font-bold text-brand">{value}</div>
      <div className="text-sm text-slate-500">{label}</div>
    </div>
  );
}
