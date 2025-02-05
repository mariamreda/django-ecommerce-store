from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'), 
    path('update_info/', views.update_info, name='update_info'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),   
    path('dashboard2/', views.dashboard2, name='dashboard2'),
    path('dashboard3/', views.dashboard3, name='dashboard3'),
    path('ajax_add_review/<int:pid>/', views.ajax_add_review, name='ajax_add_review'),
    path('dashboard4/', views.dashboard4, name='dashboard4'),
   
]
