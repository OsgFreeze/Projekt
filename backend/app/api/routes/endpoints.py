from fastapi import APIRouter

from app.services.orchestrator import ProcessingOrchestrator

from app.services.preprocessing.preprocessing_service import PreprocessingService
from app.services.extraction.extraction_service import ExtractionService
from app.services.classification.classification_service import ClassificationService
from app.services.refinement.refinement_service import RefinementService
from app.services.prompt_generation.prompt_generation_service import PromptGenerationService
from app.services.transformation.transformation_service import TransformationService
from app.services.fullgen.generation_service import GenerationService

from app.models.response_models import PreprocessingResponse, ExtractionResponse, ClassificationResponse, RefinementResponse
from app.models.request_models import ProcessPromptRequest

router = APIRouter()
orchestrator = ProcessingOrchestrator()

@router.post("/process")
def process_prompt(request: ProcessPromptRequest):
    result = orchestrator.process(request.text)
    return result

@router.post("/process_v2")
def process_prompt_v2(request: ProcessPromptRequest):
    result = orchestrator.process_v2(request.text)
    return result

@router.post("/preprocessing")
def test_preprocessing(text: str):
    service = PreprocessingService()
    return service.preprocess(text)

@router.post("/extraction")
def test_extraction(preprocessing_response: PreprocessingResponse):
    service = ExtractionService()
    return service.extract(preprocessing_response)

@router.post("/classification")
def test_classification(extraction_response: ExtractionResponse):
    service = ClassificationService()
    return service.classify(extraction_response)

@router.post("/refinement")
def test_refinement(classification_response: ClassificationResponse):
    service = RefinementService()
    return service.refine(classification_response)

@router.post("/prompt_generation")
def test_prompt_generation(refinement_response: RefinementResponse):
    service = PromptGenerationService()
    return service.generate(refinement_response)

@router.post("/transform")
def test_transformation(text: str):
    service = TransformationService()
    return service.transform(text)

@router.post("/generate")
def test_generation(text: str):
    service = GenerationService()
    return service.generate(text)