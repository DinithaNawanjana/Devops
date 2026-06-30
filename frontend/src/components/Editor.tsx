"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import MonacoEditor from "@monaco-editor/react";
import { listFiles, readFile, writeFile, type FileEntry } from "@/lib/api";

const langFor = (name: string): string => {
  if (/\.(sh|bash)$/.test(name)) return "shell";
  if (/\.ya?ml$/.test(name)) return "yaml";
  if (/\.py$/.test(name)) return "python";
  if (/\.(js|ts|tsx)$/.test(name)) return "typescript";
  if (/\.json$/.test(name)) return "json";
  if (/dockerfile/i.test(name)) return "dockerfile";
  if (/\.md$/.test(name)) return "markdown";
  return "plaintext";
};

// In-sandbox file browser + Monaco editor. Saves write straight into the
// running lab container so `validate.sh` sees them.
export default function Editor({ sessionId }: { sessionId: string }) {
  const [cwd, setCwd] = useState("/root");
  const [entries, setEntries] = useState<FileEntry[]>([]);
  const [openPath, setOpenPath] = useState<string | null>(null);
  const [content, setContent] = useState("");
  const [dirty, setDirty] = useState(false);
  const [status, setStatus] = useState("");
  // Refs hold the latest values so the Monaco ⌘S command (registered once on
  // mount) doesn't capture stale state.
  const contentRef = useRef("");
  const openPathRef = useRef<string | null>(null);
  contentRef.current = content;
  openPathRef.current = openPath;

  const refresh = useCallback((dir: string) => {
    listFiles(sessionId, dir)
      .then(setEntries)
      .catch((e) => setStatus(e.message));
  }, [sessionId]);

  useEffect(() => { refresh(cwd); }, [cwd, refresh]);

  async function open(entry: FileEntry) {
    if (entry.type === "dir") { setCwd(entry.path); return; }
    try {
      const f = await readFile(sessionId, entry.path);
      setOpenPath(entry.path);
      setContent(f.content);
      setDirty(false);
      setStatus("");
    } catch (e: any) { setStatus(e.message); }
  }

  const save = useCallback(async () => {
    const path = openPathRef.current;
    if (!path) return;
    setStatus("Saving…");
    try {
      await writeFile(sessionId, path, contentRef.current);
      setDirty(false);
      setStatus("Saved ✓");
    } catch (e: any) { setStatus(e.message); }
  }, [sessionId]);

  const parent = cwd !== "/" ? cwd.replace(/\/[^/]+\/?$/, "") || "/" : null;

  return (
    <div className="flex h-full border rounded-xl overflow-hidden bg-white">
      {/* File tree */}
      <div className="w-48 shrink-0 border-r bg-slate-50 overflow-y-auto text-sm">
        <div className="px-3 py-2 font-mono text-xs text-slate-500 truncate border-b">{cwd}</div>
        {parent !== null && (
          <button onClick={() => setCwd(parent)} className="block w-full text-left px-3 py-1 hover:bg-slate-200">📁 ..</button>
        )}
        {entries.map((e) => (
          <button
            key={e.path}
            onClick={() => open(e)}
            className={`block w-full text-left px-3 py-1 hover:bg-slate-200 truncate ${
              openPath === e.path ? "bg-blue-100" : ""
            }`}
          >
            {e.type === "dir" ? "📁" : "📄"} {e.name}
          </button>
        ))}
        {entries.length === 0 && <p className="px-3 py-2 text-xs text-slate-400">empty</p>}
      </div>

      {/* Editor */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="flex items-center justify-between px-3 py-1.5 border-b bg-slate-100 text-sm">
          <span className="font-mono text-xs truncate">
            {openPath ?? "no file open"} {dirty && <span className="text-amber-600">●</span>}
          </span>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">{status}</span>
            <button
              onClick={save}
              disabled={!openPath || !dirty}
              className="bg-brand text-white text-xs px-3 py-1 rounded disabled:opacity-40"
            >
              Save (⌘S)
            </button>
          </div>
        </div>
        <div className="flex-1 min-h-0">
          {openPath ? (
            <MonacoEditor
              language={langFor(openPath)}
              value={content}
              onChange={(v) => { setContent(v ?? ""); setDirty(true); }}
              onMount={(editor, monaco) => {
                editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, save);
              }}
              options={{ fontSize: 13, minimap: { enabled: false }, automaticLayout: true }}
            />
          ) : (
            <div className="h-full flex items-center justify-center text-slate-400 text-sm">
              Select a file to edit
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
