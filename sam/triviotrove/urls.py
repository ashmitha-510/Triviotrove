from django.urls import path
from triviotrove import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('start/', views.start, name='start'),
    path("logout/", views.logout_view, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('get_new_word/', views.get_new_word, name='get_new_word'),
    path('<uuid:uuid>/', views.play_share, name='play-game-share'),
]
