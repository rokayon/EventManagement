from django.urls import path
from users.views import user_sign_up,user_sign_in,user_sign_out,activate_user_account,admin_dashboard,assign_role,create_group,group_list
urlpatterns =[
    path('sign-up/',user_sign_up,name='sign-up'),
    path('sign-in/',user_sign_in,name='sign-in'),
    path('sign-out/',user_sign_out,name='logout'),
    path('activate/<int:user_id>/<str:token>/',activate_user_account),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list/',group_list,name='group-list'),

]