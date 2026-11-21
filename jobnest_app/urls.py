
from django.urls import path

from jobnest_app import views

urlpatterns=[

    path("",views.job_list,name="job_list"),
    path("register",views.register,name="register"),
    path("login",views.user_login,name="login"),
    path('logout',views.user_logout,name="logout"),
    path('job/<int:id>/',views.job_details,name="job_details"),

    path('apply/<int:id>/',views.job_application,name="apply_job"),
    path('my_applications',views.my_applications,name="my_applications"),

    path('admin_job_listing',views.admin_job_listing,name="admin_job_listing"),
    path('add_job',views.add_job,name="add_job"),
    path('edit_job/<int:id>',views.edit_job,name="edit_job"),
    path('delete_job/<int:id>/',views.delete_job,name="delete_job"),
]