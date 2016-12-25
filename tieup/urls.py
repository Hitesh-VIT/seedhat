"""tieup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from restro import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register_user),
    url(r'^user_info/(?P<pk>[-\w\d]+)', views.user_info, name= "user info"),
    url(r'^restaurant_login',views.Restaurant_login_view),
    url(r'^user_redeem/(?P<pk>[-\w\d]+)/(?P<rest_id>[-\w\d]+)',views.user_redeem, name='user_redeem'),
    url(r'^restaurant_redeem/',views.restaurant_redeem, name="restaurant_redeem"),
    url(r'/',views.user_homepage, name="homepage"),
    url(r'^restaurant_view',views.restaurant_view,name ="home")
]
