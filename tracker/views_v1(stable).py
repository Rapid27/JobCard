
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobCard
from .forms import JobCardForm

def submit_job_card(request):
    if request.method == 'POST':
        form = JobCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('track_job_card')
    else:
        form = JobCardForm()
    return render(request, 'tracker/submit_job_card.html', {'form': form})

def track_job_card(request):
    query = request.GET.get('query')
    job_cards = JobCard.objects.filter(reported_by__icontains=query) if query else None
    return render(request, 'tracker/track_job_card.html', {'job_cards': job_cards})

@login_required
def maintenance_dashboard(request):
    category_list = [ 'plumbing', 'electrical', 'carpentry', 'building', 'painting' ]
    category = request.GET.get('category', 'electrical')
    job_cards = JobCard.objects.filter(category=category)
    return render(request, 'tracker/dashboard.html', {'job_cards': job_cards, 'category': category, 'category_list' : category_list})

@login_required
def update_status(request, pk):
    job_card = get_object_or_404(JobCard, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobCard.STATUS_CHOICES):
            job_card.status = new_status
            job_card.save()
    return redirect('maintenance_dashboard')
