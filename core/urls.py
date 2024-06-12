from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_customer, name='upload_customer'),
    path('review/<int:customer_id>/', views.review_customer, name='review_customer'),
]
