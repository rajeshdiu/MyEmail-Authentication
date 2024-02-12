from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signupPage, name='signupPage'),
    path('logoutPage/', logoutPage, name='logoutPage'),
    path('mySigninPage/', mySigninPage, name='mySigninPage'),
    path('dashboardPage/', dashboardPage, name='dashboardPage'),
    path('activate/<uid64>/<token>', activate,name='activate'),
]