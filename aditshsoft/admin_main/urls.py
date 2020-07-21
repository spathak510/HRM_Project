from admin_main.views import *
from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^$', AdminLogin.as_view(), name='adminlogin'),
    url(r'^logout/$', AdminLogout.as_view(), name='adminlogout'),
    url(r'^dashboard/$', AdminDashBoard.as_view(), name='admindashboard'),
    url(r'^change-password/$', CrmSuperUserChangePassword.as_view(), name='super_user_change_password'),
    url(r'^update/profile/$', UpdateAdministratorProfile.as_view(), name='administrator_update_profile'),
    # HRMS Management URLS
    url(r'^hrms/', include('hrms_management.urls')),
    url(r'^hrms/', include('hrms_employees.urls')),
    url(r'^hrms/', include('knowleage_tranning.urls')),
]