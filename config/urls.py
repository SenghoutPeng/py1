from django.urls import path,include

urlpatterns=[path('',include('homepage.urls')),path('adminpanel/',include('adminpanel.urls'))]
