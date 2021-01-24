from django.urls import path, include

from users.views import CustomLoginView, AdvertiserLkView, ModeratorLkView, \
    AdminLkView

urlpatterns = [
    path('lk/advertiser/', AdvertiserLkView.as_view(), name='advertiser_lk'),
    path('lk/moderator/', ModeratorLkView.as_view(), name='moderator_lk'),
    path('lk/admin/', AdminLkView.as_view(), name='admin_lk'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('', include('allauth.urls')),
]
