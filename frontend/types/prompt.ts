export type ApiResponse = {
  original_prompt: string;
  final_prompt: string;

  original_word_count: number;
  final_word_count: number;
  word_reduction: number;
  word_reduction_percent: number;

  original_token_count: number;
  final_token_count: number;
  token_reduction: number;
  token_reduction_percent: number;

  compression_ratio: number;

  original_candidate_count: number;
  final_candidate_count: number;

  role_coverage: Record<string, number>;
  role_coverage_percent: Record<string, number>;

  semantic_retention: number;

  prompt_length_chars_original: number;
  prompt_length_chars_final: number;
  prompt_length_reduction_percent: number;

  metadata: Record<string, unknown>;
};

export type UiResponse = {
  id: string;
  createdAt: string;
  
  improvedPrompt: string;
  originalTokens: number;
  improvedTokens: number;
  improvementPercentage: number;

  stats: {
    originalPrompt: string;
    finalPrompt: string;

    originalWordCount: number;
    finalWordCount: number;
    wordReduction: number;
    wordReductionPercent: number;

    tokenReduction: number;
    tokenReductionPercent: number;

    compressionRatio: number;

    originalCandidateCount: number;
    finalCandidateCount: number;

    roleCoverage: Record<string, number>;
    roleCoveragePercent: Record<string, number>;

    semanticRetention: number;

    promptLengthCharsOriginal: number;
    promptLengthCharsFinal: number;
    promptLengthReductionPercent: number;

    metadata: Record<string, unknown>;
  };
};

export function mapApiToUi(data: ApiResponse): UiResponse {
  return {
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),

    improvedPrompt: data.final_prompt,
    originalTokens: data.original_token_count,
    improvedTokens: data.final_token_count,
    improvementPercentage: data.token_reduction_percent,

    stats: {
      originalPrompt: data.original_prompt,
      finalPrompt: data.final_prompt,

      originalWordCount: data.original_word_count,
      finalWordCount: data.final_word_count,
      wordReduction: data.word_reduction,
      wordReductionPercent: data.word_reduction_percent,

      tokenReduction: data.token_reduction,
      tokenReductionPercent: data.token_reduction_percent,

      compressionRatio: data.compression_ratio,

      originalCandidateCount: data.original_candidate_count,
      finalCandidateCount: data.final_candidate_count,

      roleCoverage: data.role_coverage,
      roleCoveragePercent: data.role_coverage_percent,

      semanticRetention: data.semantic_retention,

      promptLengthCharsOriginal: data.prompt_length_chars_original,
      promptLengthCharsFinal: data.prompt_length_chars_final,
      promptLengthReductionPercent: data.prompt_length_reduction_percent,

      metadata: data.metadata,
    },
  };
}