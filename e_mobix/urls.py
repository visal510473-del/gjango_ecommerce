"""
URL configuration for e_mobix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cart.views import add_to_cart, cart_view
from dashboard import views
from dashboard.views import dashboard
from accounts import views as accounts_views
from products.views import home
from cart import views as cart_views
# pong
from orders import views as orders_views
# pong

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('cart/', cart_views.cart_view, name='cart_view'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    # pong
    path('checkout/', orders_views.checkout, name='checkout'),
    path('cart/remove/<str:cart_key>/', cart_views.remove_from_cart, name='remove_from_cart'),
    # pong
    path('login/', accounts_views.login_view, name='login'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', accounts_views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
