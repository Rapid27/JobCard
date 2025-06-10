
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobCard
from .forms import JobCardForm
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone


def submit_job_card(request):
    if request.method == 'POST':
        form = JobCardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Your job card was submitted successfully.')
            return redirect('submit_job_card')  # Redirect back to the form
        else:
            messages.error(request, '⚠️ There was an error. Please correct the highlighted fields.')
    else:
        form = JobCardForm()
    return render(request, 'tracker/submit_job_card.html', {'form': form})

def track_job_card(request):
    query = request.GET.get('query')
    job_cards = JobCard.objects.filter(reported_by__icontains=query) if query else None
    return render(request, 'tracker/track_job_card.html', {'job_cards': job_cards})

@login_required
def maintenance_dashboard(request):

    category_list = ['plumbing', 'electrical', 'carpentry', 'building', 'painting']
    category = request.GET.get('category', 'electrical')
    job_cards = JobCard.objects.filter(category=category)

    # Calculate stale cards
    stale_threshold = timezone.now() - timedelta(days=7)
    stale_cards = set(card.id for card in job_cards if card.last_updated < stale_threshold)


    # Map icons
    card_icon_map = {
        'plumbing': '🚿',
        'electrical': '💡',
        'carpentry': '🪚',
        'building': '🏗️',
        'painting': '🎨',
    }

    return render(request, 'tracker/dashboard.html', {
        'job_cards': job_cards,
        'category': category,
        'category_list': category_list,
        'card_icon_map': card_icon_map,
        'stale_cards': stale_cards,
    })






@login_required
def update_status(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobCard.STATUS_CHOICES):
            job_card.status = new_status
            job_card.save()
    return redirect('maintenance_dashboard')
