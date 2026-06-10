export type ApiEndpointMode = "process" | "reverse" | "fullgen" | "custom";

export type AppSettings = {
  saveHistory: boolean;
  copyAfterImprove: boolean;
  compactStats: boolean;

  apiEndpointMode: ApiEndpointMode;
  customApiEndpoint: string;
};

export const defaultSettings: AppSettings = {
  saveHistory: true,
  copyAfterImprove: false,
  compactStats: false,

  apiEndpointMode: "process",
  customApiEndpoint: "http://127.0.0.1:8000/api/process",
};

export const apiEndpointOptions: Record<
  Exclude<ApiEndpointMode, "custom">,
  string
> = {
  process: "http://127.0.0.1:8000/api/process",
  reverse: "http://127.0.0.1:8000/api/process_v2",
  fullgen: "http://127.0.0.1:8000/api/process_v3",
};

export function getActiveApiEndpoint(settings: AppSettings) {
  if (settings.apiEndpointMode === "custom") {
    return settings.customApiEndpoint;
  }

  return apiEndpointOptions[settings.apiEndpointMode];
}