from django.urls import path
from . import views

app_name = 'brand_tracking'

urlpatterns = [
    path('', views.brand_tracking_scorer, name='scorer'),
    path('start/', views.start_scoring, name='start_scoring'),
    path('process-step/', views.process_question_step, name='process_question_step'),
    path('status/<int:score_id>/', views.score_status, name='score_status'),
    path('results/<int:score_id>/', views.brand_tracking_results, name='results'),
    path('history/', views.brand_tracking_history, name='history'),
    path('delete/<int:score_id>/', views.delete_brand_tracking_score, name='delete_score'),
]
