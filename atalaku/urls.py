"""atalaku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.urls import path
from atalaku import settings
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from atalaku import views


urlpatterns_i18n = i18n_patterns( * [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', include('dashboard.urls')),

], prefix_default_language=False)

urlpatterns = [
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    #path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('terms-of-use/', views.terms_of_use, name="terms-of-use"),
    path('i18n/', include('django.conf.urls.i18n')),
    *urlpatterns_i18n

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
