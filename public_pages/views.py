from django.shortcuts import render, redirect


def landing_page(request):
    """Testlane.ai home page."""
    return render(request, 'public_pages/landing.html')


def case_study_msp_group(request):
    """Case Study: Transatlantic MSP Group: Multi-Entity QBO → BigQuery (Hidden temporarily)."""
    return redirect('/')


def case_study_energy_operator(request):
    """Case study: energy producer valuation model."""
    return render(request, 'public_pages/case-studies/energy-operator.html')


def case_study_sovereign_whisper(request):
    """Case study: private board minutes."""
    return render(request, 'public_pages/case-studies/sovereign-whisper.html')


def case_study_compliance_vault(request):
    """Case study: property compliance tracker."""
    return render(request, 'public_pages/case-studies/compliance-vault.html')


def playbook(request):
    """Playbook page retired: redirect to home."""
    return redirect('/')


def about(request):
    """About Testlane Ltd: company and contact."""
    return render(request, 'public_pages/about.html')

def old_whisper_redirect(request):
    """Old URL kept alive for any existing links."""
    return redirect('/case-studies/board-minutes/', permanent=True)


def case_study_freight(request):
    """Case study: carrier claims recovery."""
    return render(request, 'public_pages/case-studies/freight-recovery.html')


def how_we_build(request):
    """How we build page."""
    return render(request, 'public_pages/how-we-build.html')
