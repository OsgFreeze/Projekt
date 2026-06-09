from pydantic import BaseModel, Field
from typing import List, Dict, Optional

###  Transformation  ###


class TransformationResponse(BaseModel):
    original_text: str
    transformed_text: str


###  Preprocessing  ###


class SentenceData(BaseModel):
    sentence_index: int
    original_text: str
    cleaned_text: str


class ProtectedEntity(BaseModel):
    placeholder: str
    original: str
    entity_type: str


class PreprocessingResponse(BaseModel):
    original_text: str
    cleaned_text: str
    language: str
    sentences: List[SentenceData] = Field(default_factory=list)
    protected_entities: List[ProtectedEntity] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)


###  Extraction  ###


class Candidate(BaseModel):
    text: str
    action: Optional[str] = None
    target: Optional[str] = None
    modifiers: List[str] = Field(default_factory=list)
    source_sentence: str
    metadata: Dict = Field(default_factory=dict)


class ExtractionResponse(BaseModel):
    candidates: List[Candidate] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)


###  Classification  ###


class ClassificationResult(BaseModel):
    role: str
    confidence: float
    scores: Dict[str, float] = Field(default_factory=dict)


class ClassifiedCandidate(BaseModel):
    candidate: Candidate
    classification: ClassificationResult


class ClassificationResponse(BaseModel):
    classified_candidates: List[ClassifiedCandidate] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)


###  Refinement  ###


class RefinedCandidate(BaseModel):
    text: str
    role: str
    priority: float
    original_text: str
    metadata: Dict = Field(default_factory=dict)

class RefinementResponse(BaseModel):
    refined_candidates: List[RefinedCandidate]
    metadata: Dict = Field(default_factory=dict)


###  Prompt Generation  ###


class PromptGenerationResponse(BaseModel):
    final_prompt: str
    used_candidates: List[RefinedCandidate]
    metadata: Dict = Field(default_factory=dict)


###  Evaluation  ###


class EvaluationResponse(BaseModel):
    original_prompt: str
    final_prompt: str

    original_word_count: int
    final_word_count: int
    word_reduction: int
    word_reduction_percent: float

    original_token_count: int
    final_token_count: int
    token_reduction: int
    token_reduction_percent: float
    
    compression_ratio: float

    original_candidate_count: int
    final_candidate_count: int

    role_coverage: Dict[str, int] = Field(default_factory=dict)
    role_coverage_percent: Dict[str, float] = Field(default_factory=dict)

    semantic_retention: float

    prompt_length_chars_original: int
    prompt_length_chars_final: int
    prompt_length_reduction_percent: float

    metadata: Dict = Field(default_factory=dict)


###  Generation  ###

class GenerationResponse(BaseModel):
    original_prompt: str
    generated_prompt: str
