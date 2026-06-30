"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { useParams } from "next/navigation";
import {
  getLab, startLab, stopSession, checkSession, getSolution,
  terminalWsUrl, getToken,
  type LabDetail, type Session, type CheckResult,
} from "@/lib/api";

const Terminal = dynamic(() => import("@/components/Terminal"), { ssr: false });
const Editor = dynamic(() => import("@/components/Editor"), { ssr: false });

type Tab = "instructions" | "theory";
type Panel = "terminal" | "editor";

export default function LabPage() {
  const { id } = useParams<{ id: string }>();
  const [lab, setLab] = useState<LabDetail | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [tab, setTab] = useState<Tab>("instructions");
  const [panel, setPanel] = useState<Panel>("terminal");
  const [result, setResult] = useState<CheckResult | null>(null);
  const [solution, setSolution] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getLab(id).then(setLab).catch((e) => setError(e.message));
  }, [id]);

  // Tear down the sandbox when leaving the page.
  useEffect(() => {
    return () => {
      if (session) stopSession(session.id).catch(() => {});
    };
  }, [session]);

  async function handleStart() {
    setError("");
    if (!getToken()) {
      setError("Please log in first to start a lab.");
      return;
    }
    setBusy(true);
    try {
      setSession(await startLab(id));
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleCheck() {
    if (!session) return;
    setBusy(true);
    setError("");
    try {
      setResult(await checkSession(session.id));
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleReveal() {
    setError("");
    try {
      const s = await getSolution(id);
      setSolution(s.solution_html);
    } catch (e: any) {
      setError(e.message);
    }
  }

  if (!lab) {
    return <p className="text-slate-500">{error || "Loading lab…"}</p>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold">{lab.title}</h1>
          <p className="text-sm text-slate-500">
            {lab.track} · {lab.level} · ~{lab.estimated_minutes} min · {lab.points} pts
          </p>
        </div>
        <div className="flex gap-2">
          {!session ? (
            <button
              onClick={handleStart}
              disabled={busy}
              className="bg-brand hover:bg-brand-dark text-white px-4 py-2 rounded-lg disabled:opacity-50"
            >
              {busy ? "Starting…" : "▶ Start Lab"}
            </button>
          ) : (
            <button
              onClick={handleCheck}
              disabled={busy}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
            >
              {busy ? "Checking…" : "✓ Check"}
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>
      )}

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Left: lesson content */}
        <div className="bg-white border rounded-xl overflow-hidden">
          <div className="flex border-b text-sm">
            {(["instructions", "theory"] as Tab[]).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-4 py-2 capitalize ${
                  tab === t ? "border-b-2 border-brand font-medium" : "text-slate-500"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
          <div
            className="prose-lesson p-5 max-h-[70vh] overflow-y-auto"
            dangerouslySetInnerHTML={{
              __html: tab === "instructions" ? lab.instructions_html : lab.theory_html,
            }}
          />
        </div>

        {/* Right: terminal / editor + results */}
        <div className="space-y-4">
          {session && (
            <div className="flex gap-1 text-sm">
              {(["terminal", "editor"] as Panel[]).map((p) => (
                <button
                  key={p}
                  onClick={() => setPanel(p)}
                  className={`px-3 py-1 rounded-t-lg capitalize ${
                    panel === p ? "bg-slate-900 text-white" : "bg-slate-200 text-slate-600"
                  }`}
                >
                  {p === "terminal" ? "🖥 Terminal" : "📝 Editor"}
                </button>
              ))}
            </div>
          )}
          <div className="h-[55vh] overflow-hidden rounded-xl">
            {!session ? (
              <div className="bg-slate-900 h-full flex items-center justify-center text-slate-400 text-sm rounded-xl">
                Start the lab to open a terminal & editor
              </div>
            ) : panel === "terminal" ? (
              <div className="bg-slate-900 h-full p-2 rounded-xl">
                <Terminal wsUrl={terminalWsUrl(session.id)} />
              </div>
            ) : (
              <Editor sessionId={session.id} />
            )}
          </div>

          {result && (
            <div
              className={`rounded-xl p-4 border ${
                result.passed ? "bg-green-50 border-green-300" : "bg-amber-50 border-amber-300"
              }`}
            >
              <p className="font-semibold mb-2">
                {result.passed
                  ? `✅ Passed! +${result.score} XP`
                  : "⚠ Not quite — keep going"}
              </p>
              <ul className="space-y-1 text-sm">
                {result.steps.map((s, i) => (
                  <li key={i} className="flex gap-2">
                    <span>{s.passed ? "✓" : "✗"}</span>
                    <span>
                      {s.name}
                      {s.message && <span className="text-slate-500"> — {s.message}</span>}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {lab.has_solution && (
            <div className="text-sm">
              {!solution ? (
                <button onClick={handleReveal} className="text-slate-500 hover:text-slate-800 underline">
                  💡 Reveal solution
                </button>
              ) : (
                <details open className="bg-white border rounded-xl p-4">
                  <summary className="cursor-pointer font-medium">Solution</summary>
                  <div className="prose-lesson mt-2" dangerouslySetInnerHTML={{ __html: solution }} />
                </details>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
