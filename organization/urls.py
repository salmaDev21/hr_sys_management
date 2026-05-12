# /urls.py
from django.urls import path
from .views import superadmin_dashboard,hrbp_home,manager_home,access_denied,form_detail,add_form,get_collab_info ,delete_form



urlpatterns = [
    path('dashboard/',superadmin_dashboard, name='superadmin_dashboard'),
    path('hrbp/home/',hrbp_home,name='hrbp_dashboard'),
    path('manager/home/',manager_home,name='manager_dashboard'),
    path('forbidden/', access_denied, name='forbidden'),
    path('manager/form/<int:pk>/',form_detail,name='form_detail'),
    path('manager/add_form/',add_form,name='add_form'),
    path('manager/get-collab-info/<str:collab_id>/',get_collab_info, name='get_collab_info'),
    path('manager/delete/<int:id>/',delete_form,name='delete_form')

    ]