const DRAFT_PROMPT_STORAGE_KEY = "promptCraftDraftPrompt";

export function getDraftPrompt(): string | null {
  if (typeof window === "undefined") return null;

  return localStorage.getItem(DRAFT_PROMPT_STORAGE_KEY);
}

export function saveDraftPrompt(prompt: string) {
  if (typeof window === "undefined") return;

  localStorage.setItem(DRAFT_PROMPT_STORAGE_KEY, prompt);
}

export function clearDraftPrompt() {
  if (typeof window === "undefined") return;

  localStorage.removeItem(DRAFT_PROMPT_STORAGE_KEY);
}