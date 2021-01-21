from django.urls import path, include

from users.views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('', include('allauth.urls')),
]
