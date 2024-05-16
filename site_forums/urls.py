from django.urls import path, include
from site_forums import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('claims/', views.claims, name='claims'),
    path('claim/<int:pk>/', views.claim, name='claim'),
    path('make_claim/', views.make_claim, name='make_claim'),
    path('forums/', views.forums, name='forums'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)