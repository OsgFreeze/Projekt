"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { UiResponse } from "@/types/prompt";
import {
  clearPromptHistory,
  deletePromptHistoryItem,
  getPromptHistory,
  savePromptResult,
} from "@/lib/promptResultStore";

function formatDate(value: string) {
  return new Intl.DateTimeFormat("de-DE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function truncate(value: string, maxLength = 140) {
  if (value.length <= maxLength) return value;

  return `${value.slice(0, maxLength)}...`;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<UiResponse[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    setHistory(getPromptHistory());
  }, []);

  const filteredHistory = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();

    if (!normalizedSearch) return history;

    return history.filter((item) => {
      return (
        item.stats.originalPrompt.toLowerCase().includes(normalizedSearch) ||
        item.improvedPrompt.toLowerCase().includes(normalizedSearch)
      );
    });
  }, [history, search]);

  function handleDelete(id: string) {
    deletePromptHistoryItem(id);
    setHistory(getPromptHistory());
  }

  function handleClear() {
    clearPromptHistory();
    setHistory([]);
  }

  function handleUseAsLatest(item: UiResponse) {
    savePromptResult(item);
  }

  return (
    <main className="page">
      <section className="hero historyHero">
        <div>
          <p className="eyebrow">Prompt Verlauf</p>
          <h1>Verlauf</h1>
          <p className="subtitle">
            Hier findest du deine letzten Prompt-Optimierungen.
          </p>
        </div>

        {history.length > 0 && (
          <button className="ghostDangerButton" onClick={handleClear}>
            Verlauf löschen
          </button>
        )}
      </section>

      {history.length === 0 ? (
        <section className="emptyState">
          <p className="eyebrow">Keine Einträge</p>
          <h1>Noch kein Verlauf vorhanden</h1>
          <p className="subtitle">
            Sobald du einen Prompt verbesserst, erscheint er hier automatisch.
          </p>

          <Link href="/" className="primaryButton emptyButton">
            Prompt verbessern
          </Link>
        </section>
      ) : (
        <>
          <section className="historyToolbar">
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Verlauf durchsuchen..."
              className="historySearch"
            />

            <span className="historyCount">
              {filteredHistory.length} von {history.length} Einträgen
            </span>
          </section>

          <section className="historyList">
            {filteredHistory.map((item) => (
              <article className="historyCard" key={item.id}>
                <div className="historyCardHeader">
                  <div>
                    <span className="historyDate">
                      {formatDate(item.createdAt)}
                    </span>
                    <h2>{truncate(item.stats.originalPrompt, 72)}</h2>
                  </div>

                  <div className="historyBadges">
                    <span className="tokenBadge purple">
                      {item.originalTokens} Tokens
                    </span>
                    <span className="tokenBadge green">
                      {item.improvedTokens} Tokens
                    </span>
                  </div>
                </div>

                <div className="historyPreviewGrid">
                  <div>
                    <h3>Original</h3>
                    <p>{truncate(item.stats.originalPrompt)}</p>
                  </div>

                  <div>
                    <h3>Improved</h3>
                    <p>{truncate(item.improvedPrompt)}</p>
                  </div>
                </div>

                <div className="historyMeta">
                  <div>
                    <span>Token Reduktion</span>
                    <strong>
                      {item.stats.tokenReductionPercent.toFixed(1)}%
                    </strong>
                  </div>

                  <div>
                    <span>Wort Reduktion</span>
                    <strong>{item.stats.wordReductionPercent.toFixed(1)}%</strong>
                  </div>

                  <div>
                    <span>Semantik</span>
                    <strong>{item.stats.semanticRetention.toFixed(1)}%</strong>
                  </div>
                </div>

                <div className="historyActions">
                  <Link
                    href="/stats"
                    className="secondaryButton compactButton"
                    onClick={() => handleUseAsLatest(item)}
                  >
                    Stats ansehen
                  </Link>

                  <button
                    className="secondaryButton compactButton"
                    onClick={() => {
                      navigator.clipboard.writeText(item.improvedPrompt);
                    }}
                  >
                    Kopieren
                  </button>

                  <button
                    className="dangerButton compactButton"
                    onClick={() => handleDelete(item.id)}
                  >
                    Löschen
                  </button>
                </div>
              </article>
            ))}
          </section>
        </>
      )}
    </main>
  );
}