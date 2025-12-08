import logging
import re
from typing import Dict, Optional
from qa_app.services import SemilatticeAPIClient
from .models import BrandTrackingScore, BrandTrackingCategoryScore, BrandTrackingQuestionScore, BrandTrackingQuestion, BrandTrackingCategory

logger = logging.getLogger(__name__)


class BrandTrackingScoringService:
    """Service to handle brand tracking scoring using Semilattice API"""
    
    def __init__(self):
        self.semilattice_client = SemilatticeAPIClient()
    
    def process_question_step(self, brand_tracking_score: BrandTrackingScore, question_number: int, max_wait_seconds: int = 25) -> Dict:
        """Start or continue processing a single question with a short server wait.
        Never blocks longer than max_wait_seconds to avoid platform timeouts.
        Returns dict with keys: pending(bool), done(bool), question_score(optional), answer_id(optional).
        """
        user = brand_tracking_score.created_by
        population_id = brand_tracking_score.population_id
        
        if not (1 <= question_number <= 10):
            raise ValueError("question_number must be between 1 and 10")
        
        # Get question from database
        question_obj = self._get_question_by_number(question_number)
        if not question_obj:
            raise ValueError(f"Question {question_number} not found in database")
        
        category_key = question_obj.category.category_key
        base_question = question_obj.question_text
        
        # Ensure CategoryScore exists
        category_obj, _ = BrandTrackingCategoryScore.objects.get_or_create(
            brand_tracking_score=brand_tracking_score,
            category_name=category_key,
            defaults={
                'category_display_name': question_obj.category.display_name,
                'score': 0,
            }
        )
        
        # Check if already completed
        qscore = BrandTrackingQuestionScore.objects.filter(
            category_score__brand_tracking_score=brand_tracking_score, 
            question_number=question_number
        ).first()
        
        if qscore and qscore.score is not None:
            logger.info(f"[STEP] score_id={brand_tracking_score.id} Q{question_number} already done")
            return {"pending": False, "done": True, "question_score": qscore.score}
        
        # If no record yet, create one with only metadata
        if not qscore:
            qscore = BrandTrackingQuestionScore.objects.create(
                category_score=category_obj,
                question_text=base_question,
                question_number=question_number,
                score=None,
            )
        
        # Ensure simulation started
        if not qscore.semilattice_answer_id:
            # Build full question with cleaned, truncated article text
            cleaned_article = self._clean_article_text(brand_tracking_score.article_text)
            truncated_article = self._truncate_article_text(cleaned_article)
            full_question = f"""Please read the following article/coverage:

{truncated_article}

And consider: {base_question}

Rate on a scale of 1 to 10, where:
1 = Very poor/negative
5 = Neutral/average
10 = Excellent/outstanding"""
            
            logger.info(f"[STEP] score_id={brand_tracking_score.id} Q{question_number} starting simulation")
            sim = self.semilattice_client.simulate_answer(
                population_id=population_id,
                question=full_question,
                question_type="single-choice",
                answer_options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            )
            
            if not sim or not sim.get("success") or not sim.get("answer_id"):
                logger.warning(f"[STEP] Q{question_number} simulate failed or no answer_id; will retry later: {sim}")
                return {"pending": True, "done": False}
            
            qscore.semilattice_answer_id = sim.get("answer_id")
            qscore.save(update_fields=["semilattice_answer_id"])
        
        # Poll for a short period
        ans_id = qscore.semilattice_answer_id
        import time
        poll_start = time.time()
        logger.info(f"[STEP] score_id={brand_tracking_score.id} Q{question_number} polling answer {ans_id} for up to {max_wait_seconds}s")
        result = self.semilattice_client.poll_until_complete(answer_id=ans_id, max_wait_seconds=max_wait_seconds)
        poll_elapsed = time.time() - poll_start
        logger.info(f"[STEP] Q{question_number} polling took {poll_elapsed:.1f}s")
        
        if result and result.get("success") and result.get("status") == "Predicted":
            # Extract score and finalize
            score_val = self._extract_score_from_response(result)
            qscore.score = score_val
            qscore.raw_response = result
            qscore.save(update_fields=["score", "raw_response"])
            
            # Update aggregates
            category_obj.score = (category_obj.score or 0) + score_val
            category_obj.save(update_fields=["score"])
            brand_tracking_score.total_score = (brand_tracking_score.total_score or 0) + score_val
            brand_tracking_score.processed_questions = (brand_tracking_score.processed_questions or 0) + 1
            brand_tracking_score.status = 'done' if brand_tracking_score.processed_questions >= 10 else 'running'
            brand_tracking_score.save(update_fields=["total_score", "processed_questions", "status"])
            
            logger.info(f"[STEP] Q{question_number} done with {score_val}/10; progress {brand_tracking_score.processed_questions}/10")
            return {"pending": False, "done": True, "question_score": score_val}
        
        # If here, it's not done yet; treat as pending (includes timeouts)
        logger.info(f"[STEP] Q{question_number} pending; result={result}")
        return {"pending": True, "done": False}
    
    def _get_question_by_number(self, question_number: int) -> Optional[BrandTrackingQuestion]:
        """Get question by its global number (1-10)"""
        # Get all active questions in order
        questions = BrandTrackingQuestion.objects.filter(is_active=True).order_by(
            'category__order', 'order'
        )
        
        if question_number <= len(questions):
            return list(questions)[question_number - 1]
        return None
    
    def _clean_article_text(self, text: str) -> str:
        """Clean article text to remove newlines, tabs, and excessive whitespace"""
        cleaned = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        return cleaned
    
    def _truncate_article_text(self, article_text: str, max_length: int = 1500) -> str:
        """Truncate article text if too long to avoid API character limits"""
        if len(article_text) <= max_length:
            return article_text
        
        truncated = article_text[:max_length].rsplit(' ', 1)[0]
        return truncated + "..."
    
    def _extract_score_from_response(self, api_response: Dict) -> int:
        """Extract the 1-10 score from Semilattice API response"""
        try:
            percentages = api_response.get('simulated_answer_percentages', {})
            
            if not percentages:
                logger.warning("No simulated_answer_percentages in response")
                return 5
            
            # Find the option with the highest percentage
            max_percentage = 0
            winning_score = 5
            
            for option, percentage in percentages.items():
                if percentage > max_percentage:
                    max_percentage = percentage
                    try:
                        winning_score = int(option)
                    except (ValueError, TypeError):
                        logger.warning(f"Could not parse score from option: {option}")
                        winning_score = 5
            
            # Ensure score is in valid range
            if 1 <= winning_score <= 10:
                return winning_score
            else:
                logger.warning(f"Score out of range: {winning_score}, defaulting to 5")
                return 5
                
        except Exception as e:
            logger.error(f"Error extracting score from response: {e}")
            return 5
