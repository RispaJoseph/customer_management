from django.urls import path
from . import views

urlpatterns = [
    path('maker/register/', views.maker_registration, name='maker_registration'),
    path('checker/register/', views.checker_registration, name='checker_registration'),
    path('maker/login/', views.maker_login, name='maker_login'),
    path('checker/login/', views.checker_login, name='checker_login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_customer, name='upload_customer'),
    path('review/<int:customer_id>/', views.review_customer, name='review_customer'),
    path('maker/dashboard/', views.maker_dashboard, name='maker_dashboard'),
    path('checker/dashboard/', views.checker_dashboard, name='checker_dashboard'),
    path('approve_decline/<int:customer_id>/', views.approve_decline_customer, name='approve_decline_customer'),
    path('upload_customer/', views.upload_customer, name='upload_customer'),
]
