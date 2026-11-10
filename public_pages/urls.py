from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('case-studies/msp-group/', views.case_study_msp_group, name='case_study_msp'),
    path('case-studies/energy-operator/', views.case_study_energy_operator, name='case_study_energy'),
    path('case-studies/sovereign-whisper/', views.case_study_sovereign_whisper, name='case_study_whisper'),
    path('case-studies/compliance-vault/', views.case_study_compliance_vault, name='case_study_vault'),
    path('playbook/', views.playbook, name='playbook'),
    path('about/', views.about, name='about'),
]