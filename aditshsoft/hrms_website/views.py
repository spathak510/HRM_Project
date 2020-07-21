import csv
import json
# Django 
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q, Count, Max, Sum
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.forms import model_to_dict
from django.core import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db.models.functions import Lower
# Dango App Internal
from aditshsoft.common import CommonPagination, SendMail, SendSmsNotification
from aditshsoft.common import SaveCsvSheet
from aditshsoft.common import get_next_week_start_date, SiteUrl
from .forms import *
from hrms_management.models import *
from hrms_management.forms import UpdateAdministratorProfielForm
from hrms_website.send_notification import *
import datetime
from datetime import timedelta  

today = datetime.date.today()


class Index(View):

    """ CRM User Login """

    template = 'website/index.html'

    def get(self, request):
        if request.user.is_superuser:
            return redirect('admindashboard')
        if request.user.is_authenticated:
        	return redirect("crm_user_dashboard")
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None and (user.is_staff is True or user.is_sub_staff is True):
            if user.is_active:
                login(request, user)
                return redirect("crm_user_dashboard")
            else:
                messages.add_message(request, messages.ERROR, "Your account is deactivate. Please contact to admin user.")
                return redirect("crm_user_dashboard")
        else:
            try:
                user = User.objects.get(username=email)
                if user.is_active:
                    messages.add_message(request, messages.ERROR, "Your account is deactivate. Please contact to admin user.")
                    return redirect("crm_user_dashboard")
                else:
                    messages.add_message(request, messages.ERROR,"Your account is deactivate. Please contact to admin user.")
                return redirect("crm_user_dashboard")
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, "You have entered wrong detail.")
                return redirect("crm_user_dashboard")


class UserDashBoardView(View):

    """ User DashBoard """

    template = 'website/user_dashboard.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template)


class UserManagementDashboardView(View):

    """ User Data Management View """

    template = 'website/user_dashboard.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template)


class UserDataAllocationDashboardView(View):

    """ User Data Management View """

    template = 'website/user_dashboard.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template)


class LogoutView(View):

    def get(self, request):
        # User  Logout
        logout(request)
        return redirect('index')


class AllDataForSendingSMS(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        if request.is_ajax:
            if 'Third'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Thirdpartydatamanagement.objects.order_by().values_list('contact_number_2').distinct()
            elif 'Bulk'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Bulkdatamanagement.objects.order_by().values_list('contact_number_2').distinct()
            elif 'Referral'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Referralpartnerdatamanagement.objects.order_by().values_list('contact_number_2').distinct()
            elif 'Online'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Onlinevisitorsmanagement.objects.order_by().values_list('contact_number_2').distinct()
            elif 'Social'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Onlinechatsmanagement.objects.order_by().values_list('contact_number_2').distinct()
            convert_in_json = json.dumps(list(get_bulk_data))
            return JsonResponse({'data' : convert_in_json})


class MailAllDataForSendingView(View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        if request.is_ajax:
            if 'Third'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Thirdpartydatamanagement.objects.order_by().values_list('email_id').distinct()
            elif 'Bulk'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Bulkdatamanagement.objects.order_by().values_list('email_id').distinct()
            elif 'Referral'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Referralpartnerdatamanagement.objects.order_by().values_list('email_id').distinct()
            elif 'Online'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Onlinevisitorsmanagement.objects.order_by().values_list('email_id').distinct()
            elif 'Social'.lower() in request.POST['get_text'].lower():
                get_bulk_data  = Onlinechatsmanagement.objects.order_by().values_list('email_id').distinct()
            convert_in_json = json.dumps(list(get_bulk_data))
            return JsonResponse({'data' : convert_in_json})


class SendSMSForMobileAppView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        if request.is_ajax:
            try:
                get_detail = DefineTemplateForNotification.objects.get(predefined_notification = 9)
                if str(get_detail.notification_method.notification_method).lower() == "sms":
                    check_status = SendSmsNotification.SendSmsByTwilio(str(request.user.mobile_no), "Please install APP "+ str(SiteUrl.site_url(request))+str(request.POST['link_url']))
                    data = "1" if check_status else "0"
            except:
                data = "0"
            return JsonResponse({'data' : data})


# User Profile
class UserChangePassword(View):
    template = 'website/change_password.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template)
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        user = get_object_or_404(User, pk=request.user.id)
        oldpassword = request.POST['oldpassword']
        newpassword = request.POST['newpassword']
        makepasswordpwd = make_password(newpassword)
        passwordString = user.password
        checkPassword = check_password(oldpassword, passwordString)
        if checkPassword:
            user.password = makepasswordpwd
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, "Your password has been changed.")
        else:
            messages.add_message(request, messages.SUCCESS, "Your have entered wrong password.")
        return redirect('crm_web_user_change_password')         


# Update User Profile
class UpdateUserProfile(View):
    template = 'website/website_update_profile.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        get_user_instance = get_object_or_404(User, pk = request.user.id)
        context = {
            'form':UpdateAdministratorProfielForm(instance = get_user_instance)
        }
        return render(request, self.template, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        get_user_instance = get_object_or_404(User, pk = request.user.id)
        get_user_instance.email = request.POST['email']
        get_user_instance.username = request.POST['email']
        get_user_instance.name = request.POST['name']
        if request.FILES.get('user_pics', False):
            get_user_instance.user_pics = request.FILES.get('user_pics')
        get_user_instance.mobile_no = request.POST['mobile_no']
        get_user_instance.save()
        messages.add_message(request, messages.SUCCESS, "User profile updated successfully.")
        return redirect('crm_update_user_profile')