"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { UiResponse } from "@/types/prompt";
import { getPromptResult } from "@/lib/promptResultStore";

function formatPercent(value?: number | null) {
  if (typeof value !== "number") return "--";

  return `${value.toFixed(1)}%`;
}

function formatNumber(value?: number |null) {
  if (typeof value !== "number") return "--";
  
  return Number.isInteger(value) ? value.toString() : value.toFixed(2);
}

export default function StatsPage() {
  const [result, setResult] = useState<UiResponse | null>(null);

  useEffect(() => {
    setResult(getPromptResult());
  }, []);

  if (!result) {
    return (
      <main className="page">
        <section className="emptyState">
          <p className="eyebrow">Statistiken</p>
          <h1>Noch keine Daten vorhanden</h1>
          <p className="subtitle">
            Verbessere zuerst einen Prompt, danach erscheinen hier alle
            Statistiken aus der API.
          </p>

          <Link href="/" className="primaryButton emptyButton">
            Prompt verbessern
          </Link>
        </section>
      </main>
    );
  }

  const stats = result.stats;

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Prompt Analyse</p>
        <h1>Statistiken</h1>
        <p className="subtitle">
          Alle Messwerte der letzten Prompt-Optimierung auf einen Blick.
        </p>
      </section>

      <section className="statsGrid">
        <div className="statTile highlightTile">
          <span>Token Reduktion</span>
          <strong>{formatPercent(stats.tokenReductionPercent)}</strong>
          <p>{stats.tokenReduction} Tokens weniger</p>
        </div>

        <div className="statTile highlightTile">
          <span>Wort Reduktion</span>
          <strong>{formatPercent(stats.wordReductionPercent)}</strong>
          <p>{stats.wordReduction} Wörter weniger</p>
        </div>

        <div className="statTile highlightTile">
          <span>Semantik erhalten</span>
          <strong>{formatPercent(stats.semanticRetention)}</strong>
          <p>Inhaltliche Nähe zum Original</p>
        </div>

        <div className="statTile">
          <span>Original Tokens</span>
          <strong>{stats.originalPrompt ? result.originalTokens : "--"}</strong>
        </div>

        <div className="statTile">
          <span>Final Tokens</span>
          <strong>{result.improvedTokens}</strong>
        </div>

        <div className="statTile">
          <span>Original Wörter</span>
          <strong>{stats.originalWordCount}</strong>
        </div>

        <div className="statTile">
          <span>Final Wörter</span>
          <strong>{stats.finalWordCount}</strong>
        </div>

        <div className="statTile">
          <span>Kompressionsrate</span>
          <strong>{formatNumber(stats.compressionRatio)}</strong>
        </div>

        <div className="statTile">
          <span>Original Kandidaten</span>
          <strong>{stats.originalCandidateCount}</strong>
        </div>

        <div className="statTile">
          <span>Final Kandidaten</span>
          <strong>{stats.finalCandidateCount}</strong>
        </div>

        <div className="statTile">
          <span>Original Zeichen</span>
          <strong>{stats.promptLengthCharsOriginal}</strong>
        </div>

        <div className="statTile">
          <span>Final Zeichen</span>
          <strong>{stats.promptLengthCharsFinal}</strong>
        </div>

        <div className="statTile">
          <span>Zeichen Reduktion</span>
          <strong>{formatPercent(stats.promptLengthReductionPercent)}</strong>
        </div>
      </section>

      <section className="detailsGrid">
        <div className="detailsCard">
          <h2>Prompt Vergleich</h2>

          <div className="promptCompare">
            <div>
              <h3>Original Prompt</h3>
              <p>{stats.originalPrompt}</p>
            </div>

            <div>
              <h3>Final Prompt</h3>
              <p>{stats.finalPrompt}</p>
            </div>
          </div>
        </div>

        <div className="detailsCard">
          <h2>Role Coverage</h2>

          <div className="tableLike">
            {Object.entries(stats.roleCoverage).length === 0 && (
              <p className="mutedText">Keine Role-Coverage-Daten vorhanden.</p>
            )}

            {Object.entries(stats.roleCoverage).map(([role, count]) => (
              <div className="tableRow" key={role}>
                <span>{role}</span>
                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="detailsCard">
          <h2>Role Coverage Prozent</h2>

          <div className="tableLike">
            {Object.entries(stats.roleCoveragePercent).length === 0 && (
              <p className="mutedText">
                Keine Role-Coverage-Prozentwerte vorhanden.
              </p>
            )}

            {Object.entries(stats.roleCoveragePercent).map(([role, percent]) => (
              <div className="tableRow" key={role}>
                <span>{role}</span>
                <strong>{formatPercent(percent)}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="detailsCard">
          <h2>Metadata</h2>

          <pre className="metadataBox">
            {JSON.stringify(stats.metadata, null, 2)}
          </pre>
        </div>
      </section>
    </main>
  );
}