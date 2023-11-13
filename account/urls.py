from django.urls import path
from . import views

urlpatterns=[
    path('', views.dashboard_view, name="dashboard"),
    path('login/', views.sign_in_view, name="sign_in"),
    path('register/', views.sign_up_view, name="sign_up"),
    path('logout/', views.log_out_view, name="log_out"),
    path('forgot_password/', views.forgot_password_view, name="forgot_password"),
    # Avec les éléments entre crochets on recupere les valeurs de ces variables à partir du navigateur, puis on va les
    # recuperer dans la vue pour les manipuler
    path('update_password/<str:token>/<str:user_id>/', views.update_password_view, name="update_password")
]