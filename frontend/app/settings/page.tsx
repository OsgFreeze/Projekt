"use client";

import { useEffect, useState } from "react";
import { AppSettings, defaultSettings } from "@/types/settings";
import {
  getSettings,
  resetSettings,
  saveSettings,
} from "@/lib/settingsStore";

export default function SettingsPage() {
  const [settings, setSettings] = useState<AppSettings>(defaultSettings);

  useEffect(() => {
    setSettings(getSettings());
  }, []);

  function updateSetting<Key extends keyof AppSettings>(
    key: Key,
    value: AppSettings[Key]
  ) {
    const nextSettings = {
      ...settings,
      [key]: value,
    };

    setSettings(nextSettings);
    saveSettings(nextSettings);
  }

  function handleReset() {
    resetSettings();
    setSettings(defaultSettings);
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Konfiguration</p>
        <h1>Einstellungen</h1>
        <p className="subtitle">
          Passe an, wie PromptCraft mit Ergebnissen und Verlauf umgehen soll.
        </p>
      </section>

      <section className="settingsGrid">
        <article className="settingsCard">
          <div>
            <h2>Verlauf speichern</h2>
            <p>
              Speichert erfolgreiche Prompt-Optimierungen automatisch auf der
              Verlauf-Seite.
            </p>
          </div>

          <label className="toggle">
            <input
              type="checkbox"
              checked={settings.saveHistory}
              onChange={(event) =>
                updateSetting("saveHistory", event.target.checked)
              }
            />
            <span />
          </label>
        </article>

        <article className="settingsCard">
          <div>
            <h2>Improved Prompt automatisch kopieren</h2>
            <p>
              Kopiert den verbesserten Prompt nach erfolgreicher Optimierung
              automatisch in die Zwischenablage.
            </p>
          </div>

          <label className="toggle">
            <input
              type="checkbox"
              checked={settings.copyAfterImprove}
              onChange={(event) =>
                updateSetting("copyAfterImprove", event.target.checked)
              }
            />
            <span />
          </label>
        </article>

        <article className="settingsCard">
          <div>
            <h2>Kompakte Statistikansicht</h2>
            <p>
              Platzhalter-Einstellung für eine spätere kompaktere Darstellung
              der Statistikseite.
            </p>
          </div>

          <label className="toggle">
            <input
              type="checkbox"
              checked={settings.compactStats}
              onChange={(event) =>
                updateSetting("compactStats", event.target.checked)
              }
            />
            <span />
          </label>
        </article>
      </section>

      <section className="settingsFooter">
        <button className="ghostDangerButton" onClick={handleReset}>
          Einstellungen zurücksetzen
        </button>
      </section>
    </main>
  );
}