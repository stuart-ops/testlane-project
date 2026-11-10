from django.shortcuts import render


def landing_page(request):
    """Sovereign AI landing page — main Testlane.ai site."""
    return render(request, 'public_pages/landing.html')


def case_study_msp_group(request):
    """Case Study: Transatlantic MSP Group — Multi-Entity QBO → BigQuery."""
    return render(request, 'public_pages/case-studies/msp-group.html')


def case_study_energy_operator(request):
    """Case Study: LSE-Listed Upstream Energy Producer — DCF Valuation Engine."""
    return render(request, 'public_pages/case-studies/energy-operator.html')


def case_study_sovereign_whisper(request):
    """Case Study: Sovereign Whisper — On-Premise Boardroom Intelligence."""
    return render(request, 'public_pages/case-studies/sovereign-whisper.html')


def case_study_compliance_vault(request):
    """Case Study: Sovereign Property & Compliance Vault."""
    return render(request, 'public_pages/case-studies/compliance-vault.html')


def playbook(request):
    """Sovereign Vibe Coding Playbook page."""
    return render(request, 'public_pages/playbook.html')


def about(request):
    """About Testlane Ltd — company and contact."""
    return render(request, 'public_pages/about.html')