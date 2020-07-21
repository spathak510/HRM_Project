from django.conf.urls import include
from django.conf.urls import url
from hrms_website.views import *


urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^logout/$', LogoutView.as_view(), name='weblogout'),
    url(r'^hrms/update/user/profile/$', UpdateUserProfile.as_view(), name='crm_update_user_profile'),
    url(r'^hrms/dashboard/$', UserDashBoardView.as_view(), name='crm_user_dashboard'),
    url(r'^hrms/get/all/data/list/$', AllDataForSendingSMS.as_view(), name='crm_web_get_all_data'),
    url(r'^hrms/send/mobile/app/user/$', SendSMSForMobileAppView.as_view(), name='crm_web_send_mobile_app'),
    url(r'^hrms/mail/all/data/list/$', MailAllDataForSendingView.as_view(), name='crm_web_mail_all_data'),
    url(r'^hrms/user/change/password/list/$', UserChangePassword.as_view(), name='crm_web_user_change_password'),
]