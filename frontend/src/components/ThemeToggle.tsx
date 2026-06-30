"use client";

import { useEffect, useState } from "react";

// Toggles the `dark` class on <html> and persists the choice.
export default function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("theme") === "dark";
    setDark(saved);
    document.documentElement.classList.toggle("dark", saved);
  }, []);

  function toggle() {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem("theme", next ? "dark" : "light");
  }

  return (
    <button onClick={toggle} className="hover:text-brand" title="Toggle theme">
      {dark ? "☀️" : "🌙"}
    </button>
  );
}
