from typing import List, Dict, Any, Optional
import re
from dataclasses import dataclass
from enum import Enum
import json
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

class EvaluationScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    SATISFACTORY = 3
    NEEDS_IMPROVEMENT = 2
    POOR = 1

class LLMEvaluation(BaseModel):
    """Pydantic model for LLM evaluation output"""
    feedback: str = Field(description="Detailed evaluation of the answer focusing on technical accuracy, completeness, and clarity")
    score: float = Field(description="Numerical score between 0 and 1 (where 1 is perfect)", ge=0, le=1)
    strengths: List[str] = Field(description="List of key strengths in the answer")
    areas_for_improvement: List[str] = Field(description="List of areas that need improvement")
    technical_depth: float = Field(description="Score for technical depth of the answer", ge=0, le=1)
    clarity: float = Field(description="Score for clarity and communication", ge=0, le=1)
    completeness: float = Field(description="Score for completeness of the answer", ge=0, le=1)

@dataclass
class Question:
    question_text: str
    category: str
    difficulty: str
    context: str
    expected_points: List[str]
    additional_context: Optional[Dict[str, Any]] = None

@dataclass
class EvaluationResult:
    score: EvaluationScore
    feedback: str
    missing_points: List[str]
    covered_points: List[str]
    llm_feedback: Optional[str] = None
    llm_score: Optional[float] = None
    llm_evaluation: Optional[LLMEvaluation] = None

class AnswerEvaluator:
    def __init__(self, question: Question, use_llm: bool = True):
        self.question = question
        self.expected_points = [point.lower() for point in question.expected_points]
        self.use_llm = use_llm
        self.parser = JsonOutputParser(pydantic_object=LLMEvaluation)
    
    def evaluate_answer(self, answer: str) -> EvaluationResult:
        answer_lower = answer.lower()
        
        # Check coverage of expected points
        covered_points = []
        missing_points = []
        
        for point in self.expected_points:
            if self._check_point_coverage(point, answer_lower):
                covered_points.append(point)
            else:
                missing_points.append(point)
        
        # Calculate score based on coverage
        coverage_ratio = len(covered_points) / len(self.expected_points)
        score = self._calculate_score(coverage_ratio)
        
        # Generate feedback
        feedback = self._generate_feedback(covered_points, missing_points, score)
        
        # Initialize LLM feedback as None
        llm_feedback = None
        llm_score = None
        llm_evaluation = None
        
        # If LLM evaluation is enabled, get LLM feedback
        if self.use_llm:
            llm_evaluation = self._get_llm_evaluation(answer)
            if llm_evaluation:
                llm_feedback = llm_evaluation['feedback']
                llm_score = llm_evaluation['score']
        
        return EvaluationResult(
            score=score,
            feedback=feedback,
            missing_points=missing_points,
            covered_points=covered_points,
            llm_feedback=llm_feedback,
            llm_score=llm_score,
            llm_evaluation=llm_evaluation
        )
    
    def _check_point_coverage(self, point: str, answer: str) -> bool:
        """Check if the answer covers a specific expected point."""
        keywords = re.findall(r'\w+', point.lower())
        return all(keyword in answer for keyword in keywords)
    
    def _calculate_score(self, coverage_ratio: float) -> EvaluationScore:
        """Calculate score based on coverage ratio."""
        if coverage_ratio >= 0.9:
            return EvaluationScore.EXCELLENT
        elif coverage_ratio >= 0.7:
            return EvaluationScore.GOOD
        elif coverage_ratio >= 0.5:
            return EvaluationScore.SATISFACTORY
        elif coverage_ratio >= 0.3:
            return EvaluationScore.NEEDS_IMPROVEMENT
        else:
            return EvaluationScore.POOR
    
    def _generate_feedback(self, covered_points: List[str], missing_points: List[str], 
                         score: EvaluationScore) -> str:
        """Generate detailed feedback for the answer."""
        feedback = []
        
        if score == EvaluationScore.EXCELLENT:
            feedback.append("Excellent answer! You've covered all the key points comprehensively.")
        elif score == EvaluationScore.GOOD:
            feedback.append("Good answer! You've covered most of the important points.")
        elif score == EvaluationScore.SATISFACTORY:
            feedback.append("Satisfactory answer. You've covered some key points but could be more comprehensive.")
        else:
            feedback.append("The answer needs improvement. Consider addressing the following points:")
        
        if missing_points:
            feedback.append("\nMissing points:")
            for point in missing_points:
                feedback.append(f"- {point}")
        
        if covered_points:
            feedback.append("\nWell covered points:")
            for point in covered_points:
                feedback.append(f"- {point}")
        
        return "\n".join(feedback)
    
    def _get_llm_evaluation(self, answer: str) -> Optional[LLMEvaluation]:
        """
        Get LLM-based evaluation of the answer using Ollama.
        """
        from llms.providers import llm_ollama_model
        ollama_model = llm_ollama_model()
        
        # Format the evaluation prompt
        prompt = f"""You are an expert technical interviewer evaluating a candidate's answer. 
                    Please evaluate the following answer based on the question and expected points.

                    Question: {self.question.question_text}
                    Category: {self.question.category}
                    Difficulty: {self.question.difficulty}
                    Context: {self.question.context}

                    Expected Points:
                    {chr(10).join(f"- {point}" for point in self.question.expected_points)}

                    Candidate's Answer:
                    {answer}

                    Please provide a comprehensive evaluation of the answer focusing on:
                    1. Technical accuracy and depth
                    2. Clarity of communication
                    3. Completeness of the answer
                    4. Key strengths
                    5. Areas for improvement
                    
                    evaluate answer will be strictly in json format mentioned in the below
                    
                    "feedback": "<Detailed evaluation of the answer in description way>",
                    "score": <Numerical score between 0 and 1 (where 1 is perfect)>,
                    "strengths": ["<Key strength 1>", "<Key strength 2>", "..."],
                    "areas_for_improvement": ["<Area needing improvement 1>", "<Area needing improvement 2>", "..."],
                    "technical_depth": <Score for technical depth between 0 and 1>,
                    "clarity": <Score for clarity and communication between 0 and 1>,
                    "completeness": <Score for completeness between 0 and 1>
                    """

        try:
            print('instrs : ', self.parser.get_format_instructions())
            # Get response from Ollama
            response = ollama_model.invoke(prompt)
            print('response : ', response)
            # Parse the response using PydanticOutputParser
            evaluation = self.parser.invoke(response)
            print(evaluation)
            return evaluation
            
        except Exception as e:
            print(e)
            print(f"Error in LLM evaluation: {str(e)}")
            return None

def evaluate_technical_answer(
    question_data: Dict[str, Any], 
    answer: str, 
    use_llm: bool = True,
    additional_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main function to evaluate a technical answer.
    
    Args:
        question_data: Dictionary containing question details
        answer: The candidate's answer to evaluate
        use_llm: Whether to use LLM for evaluation
        additional_context: Optional additional context for evaluation
    
    Returns:
        Dictionary containing evaluation results
    """
    question = Question(
        question_text=question_data["question_text"],
        category=question_data["category"],
        difficulty=question_data["difficulty"],
        context=question_data["context"],
        expected_points=question_data["expected_points"],
        additional_context=additional_context
    )
    
    evaluator = AnswerEvaluator(question, use_llm=use_llm)
    result = evaluator.evaluate_answer(answer)
    
    evaluation_result = {
        "score": result.score.name,
        "score_value": result.score.value,
        "feedback": result.feedback,
        "missing_points": result.missing_points,
        "covered_points": result.covered_points
    }
    
    if result.llm_evaluation:
        evaluation_result.update({
            "llm_feedback": result.llm_evaluation['feedback'],
            "llm_score": result.llm_evaluation['score'],
            "llm_strengths": result.llm_evaluation['strengths'],
            "llm_areas_for_improvement": result.llm_evaluation['areas_for_improvement'],
            "llm_technical_depth": result.llm_evaluation['technical_depth'],
            "llm_clarity": result.llm_evaluation['clarity'],
            "llm_completeness": result.llm_evaluation['completeness']
        })
    
    return evaluation_result
