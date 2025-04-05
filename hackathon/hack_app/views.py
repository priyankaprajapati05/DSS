from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count

from .models import (
    UploadedDocument,
    CreditRequest,
    AcceptedCreditRequest,
    RejectedCreditRequest,
    UserProfile
)
from django.contrib.auth.models import User

# ---------- User Auth Views ----------

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password1, email=email)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'signup.html')


def check_username(request):
    username = request.GET.get('username', None)
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})


def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


# ---------- Home & Document Upload ----------

@login_required
def home(request):
    user_docs = UploadedDocument.objects.filter(user=request.user)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)  # <-- FIXED HERE

    # Check max limit
    total_allowed = 20 + user_profile.credits
    if request.method == 'POST' and request.FILES.get('document'):
        if user_docs.count() >= total_allowed:
            messages.error(request, f"You've reached your upload limit ({total_allowed}). Please request more credits.")
        elif request.FILES['document'].name.endswith('.txt'):
            UploadedDocument.objects.create(user=request.user, file=request.FILES['document'])
            messages.success(request, "Document uploaded successfully.")
            return redirect('home')
        else:
            messages.error(request, "Only .txt files are allowed.")

    return render(request, 'home.html', {
        'documents': user_docs,
        'user_profile': user_profile
    })



# ---------- Credits Functionality ----------

@login_required
def credits_home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    total_uploaded = UploadedDocument.objects.filter(user=request.user).count()
    total_allowed = 20 + user_profile.credits
    remaining = max(total_allowed - total_uploaded, 0)

    credit_requests = CreditRequest.objects.filter(user=request.user)
    total_requests = credit_requests.count()
    accepted_requests = credit_requests.filter(status='accepted').count()
    rejected_requests = credit_requests.filter(status='rejected').count()

    return render(request, 'credits_home.html', {
        'user_profile': user_profile,
        'remaining_credits': remaining,
        'total_requests': total_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests
    })




@login_required
def send_credit_request(request):
    CreditRequest.objects.create(user=request.user)
    messages.success(request, "Request sent successfully.")
    return redirect('credits_home')


@login_required
def credit_request_status(request):
    requests = CreditRequest.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'credit_status.html', {'requests': requests})


@login_required
def credits_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    credit_requests = CreditRequest.objects.filter(user=request.user)
    return render(request, 'credits.html', {
        'user_profile': user_profile,
        'credit_requests': credit_requests
    })


# ---------- Admin Views ----------

def AdminLoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials.")
            return redirect('admin_login')

    return render(request, 'admin_login.html')


@user_passes_test(lambda u: u.is_staff)
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    documents = UploadedDocument.objects.select_related('user').order_by('-uploaded_at')
    credit_requests = CreditRequest.objects.filter(status=CreditRequest.STATUS_PENDING)
    
    today = timezone.now().date()
    scans_today = UploadedDocument.objects.filter(uploaded_at__date=today).count()

    top_users = (
        User.objects.annotate(upload_count=Count('documents'))
        .order_by('-upload_count')[:5]
    )

    return render(request, 'admin_dashboard.html', {
        'documents': documents,
        'credit_requests': credit_requests,
        'scans_today': scans_today,
        'top_users': top_users,
    })


# ---------- Handle Accept / Reject ----------

@user_passes_test(lambda u: u.is_staff)
def handle_credit_request(request, request_id, action):
    credit_request = get_object_or_404(CreditRequest, id=request_id)

    if credit_request.status != CreditRequest.STATUS_PENDING:
        return redirect('admin_dashboard')

    if action == 'accept':
        # Update profile credits
        profile, _ = UserProfile.objects.get_or_create(user=credit_request.user)
        profile.credits += 1
        profile.save()

        # Create AcceptedCreditRequest entry
        AcceptedCreditRequest.objects.create(user=credit_request.user)

    elif action == 'reject':
        # Create RejectedCreditRequest entry
        RejectedCreditRequest.objects.create(user=credit_request.user)

    # Delete from main CreditRequest table
    credit_request.delete()

    return redirect('admin_dashboard')


# ---------- Accepted & Rejected Pages ----------

@user_passes_test(lambda u: u.is_staff)
def accepted_requests_view(request):
    accepted_requests = AcceptedCreditRequest.objects.select_related('user').order_by('-approved_at')
    return render(request, 'accepted_requests.html', {
        'accepted_requests': accepted_requests
    })


@user_passes_test(lambda u: u.is_staff)
def rejected_requests_view(request):
    rejected_requests = RejectedCreditRequest.objects.select_related('user').order_by('-rejected_at')
    return render(request, 'rejected_requests.html', {
        'rejected_requests': rejected_requests
    })
