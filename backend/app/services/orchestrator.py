from app.services.preprocessing.preprocessing_service import PreprocessingService
from app.services.extraction.extraction_service import ExtractionService
from app.services.classification.classification_service import ClassificationService
from app.services.refinement.refinement_service import RefinementService
from app.services.prompt_generation.prompt_generation_service import PromptGenerationService
from app.services.evaluation.evaluation_service import EvaluationService
from app.services.transformation.transformation_service import TransformationService
from app.services.fullgen.generation_service import GenerationService

class ProcessingOrchestrator:
    def __init__(self):
        self.transformation = TransformationService()
        self.preprocessing = PreprocessingService()
        self.extraction = ExtractionService()
        self.classification = ClassificationService()
        self.refinement = RefinementService()
        self.prompt_generation = PromptGenerationService()
        self.evaluation = EvaluationService()
        self.generation = GenerationService()

    def process(self, text: str):
        preprocessed = self.preprocessing.preprocess(text)
        extracted = self.extraction.extract(preprocessed)
        classified = self.classification.classify(extracted)
        refined = self.refinement.refine(classified)
        generated_prompt = self.prompt_generation.generate(refined)
        evaluated = self.evaluation.evaluate(preprocessed, refined, generated_prompt)

        return evaluated
    
    def process_v2(self, text: str):
        transformed = self.transformation.transform(text)
        preprocessed = self.preprocessing.preprocess(transformed.transformed_text)
        extracted = self.extraction.extract(preprocessed)
        classified = self.classification.classify(extracted)
        refined = self.refinement.refine(classified)
        generated_prompt = self.prompt_generation.generate(refined)
        evaluated = self.evaluation.evaluate(preprocessed, refined, generated_prompt)

        return evaluated
    
    def process_v3(self, text: str):
        generated = self.generation.generate(text)
        
        return generated