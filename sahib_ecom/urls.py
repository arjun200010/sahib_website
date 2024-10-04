
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact/', views.contact, name='contact'),
    path('verify/<str:verification_code>/', views.verify_email, name='verify_email'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('customerpage/',views.customerpage,name='customerpage'),
]
