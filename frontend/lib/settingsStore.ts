import { AppSettings, defaultSettings } from "@/types/settings";

const SETTINGS_STORAGE_KEY = "promptCraftSettings";

export function getSettings(): AppSettings {
  if (typeof window === "undefined") return defaultSettings;

  const stored = localStorage.getItem(SETTINGS_STORAGE_KEY);

  if (!stored) return defaultSettings;

  try {
    return {
      ...defaultSettings,
      ...(JSON.parse(stored) as Partial<AppSettings>),
    };
  } catch {
    return defaultSettings;
  }
}

export function saveSettings(settings: AppSettings) {
  if (typeof window === "undefined") return;

  localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
}

export function resetSettings() {
  if (typeof window === "undefined") return;

  localStorage.removeItem(SETTINGS_STORAGE_KEY);
}