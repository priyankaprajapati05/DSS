from django.urls import path
from . import views

urlpatterns = [
    
    # Authentication
    path('', views.LoginPage, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.LogoutPage, name='logout'),
    path('check-username/', views.check_username, name='check_username'),

    # User Home & Documents
    path('home/', views.home, name='home'),

    # Credit System
    path('credits/', views.credits_home, name='credits_home'),
    path('credits/send/', views.send_credit_request, name='send_credit_request'),
    path('credits/status/', views.credit_request_status, name='credit_request_status'),

    # Admin Panel
    path('admin_login/', views.AdminLoginPage, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    # Handle credit request (accept/reject)
    path('dashboard/credit_request/<int:request_id>/<str:action>/', views.handle_credit_request, name='handle_credit_request'),

    # Accepted & Rejected Requests
    path('accepted-requests/', views.accepted_requests_view, name='accepted_requests'),
    path('rejected-requests/', views.rejected_requests_view, name='rejected_requests'),
]
