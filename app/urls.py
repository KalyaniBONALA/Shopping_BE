from django.urls import path
from .views import Register,LoginView,Personal_View,Logoutview,Userdetails

urlpatterns = [
    path('sign_up/', Register.as_view(), name='Register'),
    path('sign_in/', LoginView.as_view(), name='LoginView'),
    path('logout/',Logoutview.as_view(),name='LogoutView'),
    # path('userview/', UserView.as_view(), name='userview'),
    path('user_details/', Userdetails.as_view(), name='Userdetails'),
    path('Personal_info/', Personal_View.as_view(), name='Personal'),
]
