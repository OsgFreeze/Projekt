import { UiResponse } from "@/types/prompt";

const LATEST_STORAGE_KEY = "latestPromptResult";
const HISTORY_STORAGE_KEY = "promptResultHistory";

export function savePromptResult(result: UiResponse, saveToHistory = true) {
  if (typeof window === "undefined") return;

  localStorage.setItem(LATEST_STORAGE_KEY, JSON.stringify(result));

  if (!saveToHistory) return;

  const history = getPromptHistory();

  const updatedHistory = [
    result,
    ...history.filter((item) => item.id !== result.id),
  ].slice(0, 50);

  localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(updatedHistory));
}

export function getPromptResult(): UiResponse | null {
  if (typeof window === "undefined") return null;

  const stored = localStorage.getItem(LATEST_STORAGE_KEY);

  if (!stored) return null;

  try {
    return JSON.parse(stored) as UiResponse;
  } catch {
    return null;
  }
}

export function getPromptHistory(): UiResponse[] {
  if (typeof window === "undefined") return [];

  const stored = localStorage.getItem(HISTORY_STORAGE_KEY);

  if (!stored) return [];

  try {
    const parsed = JSON.parse(stored);

    return Array.isArray(parsed) ? (parsed as UiResponse[]) : [];
  } catch {
    return [];
  }
}

export function getPromptHistoryItem(id: string): UiResponse | null {
  const history = getPromptHistory();

  return history.find((item) => item.id === id) ?? null;
}

export function deletePromptHistoryItem(id: string) {
  if (typeof window === "undefined") return;

  const history = getPromptHistory().filter((item) => item.id !== id);

  localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(history));

  const latest = getPromptResult();

  if (latest?.id === id) {
    const nextLatest = history[0] ?? null;

    if (nextLatest) {
      localStorage.setItem(LATEST_STORAGE_KEY, JSON.stringify(nextLatest));
    } else {
      localStorage.removeItem(LATEST_STORAGE_KEY);
    }
  }
}

export function clearPromptHistory() {
  if (typeof window === "undefined") return;

  localStorage.removeItem(HISTORY_STORAGE_KEY);
  localStorage.removeItem(LATEST_STORAGE_KEY);
}