"use client";

import Link from "next/link";
import { useState } from "react";
import { ApiResponse, UiResponse, mapApiToUi } from "@/types/prompt";
import { savePromptResult } from "@/lib/promptResultStore";
import { getSettings } from "@/lib/settingsStore";

export default function Home() {
  const [prompt, setPrompt] = useState(
    ""
  );

  const [result, setResult] = useState<UiResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function improvePrompt() {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: prompt
        }),
      });

      if (!response.ok){
        throw new Error("Fehler beim Senden an das Backend")
      }

      const data: ApiResponse = await response.json()
      const uiResult = mapApiToUi(data);
      const settings = getSettings();

      setResult(uiResult);
      savePromptResult(uiResult, settings.saveHistory);

      if (settings.copyAfterImprove) {
        await navigator.clipboard.writeText(uiResult.improvedPrompt);
      }
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Prompt Optimizer</p>
        <h1>Prompt verbessern</h1>
        <p className="subtitle">
          Verwandle deinen Prompt in eine klarere, stärkere und effektivere
          Version.
        </p>
      </section>

      <section className="workspace">
        <div className="promptCard inputCard">
          <div className="cardHeader">
            <h2>Original Prompt</h2>
            <span className="tokenBadge purple">
              {result?.originalTokens ?? ""} Tokens
            </span>
          </div>

          <textarea
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Gib deinen Prompt ein..."
          />

          <div className="cardActions">
            <button className="ghostButton" onClick={() => setPrompt("")}>
              Zurücksetzen
            </button>

            <button
              className="primaryButton"
              onClick={improvePrompt}
              disabled={loading || !prompt.trim()}
            >
              {loading ? "Verbessere..." : "Verbessern ✨"}
            </button>
          </div>
        </div>

        <div className="promptCard outputCard">
          <div className="cardHeader">
            <h2>Improved Prompt</h2>
            <span className="tokenBadge green">
              {result?.improvedTokens ?? ""} Tokens
            </span>
          </div>

          <div className="resultBox">
            {result?.improvedPrompt ?? "Hier erscheint der verbesserte Prompt."}
          </div>

          <div className="iconActions">
            <button
              title="Kopieren"
              onClick={() =>
                result?.improvedPrompt &&
                navigator.clipboard.writeText(result.improvedPrompt)
              }
            >
              ⧉
            </button>
          </div>
        </div>

        <aside className="statsCard">
          <h2>Übersicht</h2>

          <div className="statRow">
            <span>Original Tokens</span>
            <strong>{result?.originalTokens ?? "--"}</strong>
          </div>

          <div className="statRow">
            <span>Improved Tokens</span>
            <strong>{result?.improvedTokens ?? "--"}</strong>
          </div>

          <div className="growthBox">
            <span>Verbesserung</span>
            <strong>
              {result ? `${result.improvementPercentage.toFixed(1)}%` : "--"}
            </strong>

            <div className="miniChart">
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>
          </div>

          <Link
            href="/stats"
            className={`secondaryButton linkButton ${
              !result ? "disabledLink" : ""
            }`}
          >
            Alle Statistiken ›
          </Link>
        </aside>
      </section>
    </main>
  );
}