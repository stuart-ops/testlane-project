from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from qa_app.models import Population
from .models import BrandTrackingScore, BrandTrackingCategoryScore, BrandTrackingQuestionScore
from .services import BrandTrackingScoringService

logger = logging.getLogger(__name__)


@login_required
def brand_tracking_scorer(request):
    """Main brand tracking scoring page"""
    populations = Population.objects.filter(created_by=request.user).order_by('name')
    
    context = {
        'populations': populations,
    }
    
    if request.method == 'POST':
        messages.error(request, 'Long-running sync scoring is disabled. Please use the button to start and wait for progress.')
        return render(request, 'brand_tracking/scorer.html', context)
    
    return render(request, 'brand_tracking/scorer.html', context)


@login_required
@require_http_methods(["POST"])
def start_scoring(request):
    """Start a scoring session and return a score_id for incremental processing."""
    article_text = request.POST.get('article_text', '').strip()
    population_id = request.POST.get('population_id', '').strip()
    logger.info(f"[START] User={request.user.username} starting brand tracking scoring. Pop={population_id}")
    
    # Validation
    if not article_text or not population_id:
        return JsonResponse({'success': False, 'error': 'article_text and population_id are required.'}, status=400)
    if len(article_text) < 500 or len(article_text) > 10000:
        return JsonResponse({'success': False, 'error': 'Article must be between 500 and 10,000 characters.'}, status=400)
    cleaned_text = article_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    if not cleaned_text:
        return JsonResponse({'success': False, 'error': 'Invalid article content.'}, status=400)
    
    try:
        population = Population.objects.get(population_id=population_id, created_by=request.user)
    except Population.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid population selected.'}, status=400)
    
    # Create the score shell
    score = BrandTrackingScore.objects.create(
        article_text=cleaned_text,
        total_score=0,
        created_by=request.user,
        population_id=population_id,
        status='running',
        processed_questions=0,
    )
    logger.info(f"[START] Created score_id={score.id}")
    
    return JsonResponse({'success': True, 'score_id': score.id})


@login_required
@require_http_methods(["POST"]) 
def process_question_step(request):
    """Short non-blocking step for a single question. Returns pending/done."""
    try:
        score_id = int(request.POST.get('score_id'))
        question_number = int(request.POST.get('question_number'))
    except (TypeError, ValueError):
        return JsonResponse({'success': False, 'error': 'score_id and question_number are required integers.'}, status=400)

    score = get_object_or_404(BrandTrackingScore, id=score_id, created_by=request.user)
    service = BrandTrackingScoringService()
    try:
        step = service.process_question_step(score, question_number, max_wait_seconds=25)
        # Refresh aggregates after potential update
        score.refresh_from_db()
        payload = {
            'success': True,
            'pending': step.get('pending', False),
            'done': step.get('done', False),
            'question_score': step.get('question_score'),
            'total_score': score.total_score,
            'processed_questions': score.processed_questions,
            'status': score.status,
        }
        return JsonResponse(payload)
    except Exception as e:
        logger.error(f"[STEP] Error during step Q{question_number} for score {score_id}: {e}")
        score.status = 'failed'
        score.error_message = str(e)
        score.save(update_fields=['status', 'error_message'])
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"]) 
def score_status(request, score_id):
    """Return current status of a scoring session."""
    score = get_object_or_404(BrandTrackingScore, id=score_id, created_by=request.user)
    return JsonResponse({
        'success': True,
        'status': score.status,
        'processed_questions': score.processed_questions,
        'total_score': score.total_score,
        'score_percentage': round((score.total_score / 100) * 100, 1) if score.total_score else 0,
    })


@login_required
def brand_tracking_results(request, score_id):
    """Display brand tracking scoring results"""
    score = get_object_or_404(BrandTrackingScore, id=score_id, created_by=request.user)
    
    # Get categories in consistent order using the model method
    categories = score.get_ordered_categories()
    
    # Add population display name if available
    if score.population_id:
        try:
            population = Population.objects.get(
                population_id=score.population_id,
                created_by=request.user
            )
            score.population_display_name = f"{population.name} ({score.population_id})"
        except Population.DoesNotExist:
            score.population_display_name = score.population_id
    else:
        score.population_display_name = None
    
    context = {
        'score': score,
        'categories': categories,
        'total_questions': 10,
        'max_total_score': 100,
    }
    
    return render(request, 'brand_tracking/results.html', context)


@login_required
def brand_tracking_history(request):
    """Display user's brand tracking scoring history"""
    scores = BrandTrackingScore.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Get population names for scores that have population_ids
    population_ids = [score.population_id for score in scores if score.population_id]
    if population_ids:
        populations = Population.objects.filter(
            population_id__in=population_ids, 
            created_by=request.user
        )
        population_names = {pop.population_id: pop.name for pop in populations}
        
        # Add population names to score objects (temporary attribute)
        for score in scores:
            if score.population_id and score.population_id in population_names:
                score.population_display_name = f"{population_names[score.population_id]} ({score.population_id})"
            else:
                score.population_display_name = score.population_id if score.population_id else None
    else:
        for score in scores:
            score.population_display_name = score.population_id if score.population_id else None
    
    context = {
        'scores': scores
    }
    
    return render(request, 'brand_tracking/history.html', context)


@login_required
@require_http_methods(["POST"]) 
def delete_brand_tracking_score(request, score_id):
    """Delete a brand tracking score"""
    score = get_object_or_404(BrandTrackingScore, id=score_id, created_by=request.user)
    
    try:
        score.delete()
        messages.success(request, 'Brand tracking score deleted successfully.')
    except Exception as e:
        logger.error(f"Error deleting brand tracking score: {e}")
        messages.error(request, 'Failed to delete the brand tracking score.')
    
    return redirect('brand_tracking:history')
