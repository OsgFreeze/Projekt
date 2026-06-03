export type AppSettings = {
  saveHistory: boolean;
  copyAfterImprove: boolean;
  compactStats: boolean;
};

export const defaultSettings: AppSettings = {
  saveHistory: true,
  copyAfterImprove: false,
  compactStats: false,
};