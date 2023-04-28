from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('profit_chart/', views.profit_chart, name='profit_chart'),
    path('profile/', views.profile, name='profile'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('refferals/', views.refferals, name='refferals'),
    path('profit_share/', views.profit_share, name='profit_share'),
    path('donations/', views.donations, name='donations'),
    path('promo_achievement/', views.promo_achievement, name='promo_achievement'),
    path('reinvest_portfolio/', views.reinvest_portfolio, name='reinvest_portfolio'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('admin/', views.admin_view, name='admin_view'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)