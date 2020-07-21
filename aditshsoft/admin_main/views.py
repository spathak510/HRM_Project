from __future__ import unicode_literals
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from django.template import Template
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.db.models import Q
from django.views.decorators.cache import cache_control
from admin_main.models import *
from hrms_management.models import *
from aditshsoft.common import CommonPagination
from aditshsoft.common import Getmonthlist
from aditshsoft.common import Getyearlist
from hrms_management.forms import *


''' ----------Admin basic functionality----------- '''
class AdminLogin(View):

    ''' Admin login functionality '''

    template = 'admin_template/login.html'
    template1 = 'admin_template/test.html'

    def get(self, request):
        if request.user.is_superuser:
            return redirect('admindashboard')
        return render(request, self.template)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # Check user authentication
        user = authenticate(username=username, password=password, is_superuser=0)
        if user is not None and user.is_superuser is True:
            if user.is_active:
                login(request, user)
                return redirect('admindashboard')
        else:
            messages.add_message(request, messages.ERROR, "Invalid Credential")
            return redirect('adminlogin')

class AdminDashBoard(View):
    template = 'admin_template/dashboard.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        return render(request, self.template)


class AdminLogout(View):

    def get(self, request):
        ''' User logout action '''
        logout(request)
        return redirect('adminlogin')

# User Profile
class CrmSuperUserChangePassword(View):
    template = 'admin_template/crm_management/change_password.html'

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
            messages.add_message(request, messages.ERROR, "Your have entered wrong password.")
        return redirect('super_user_change_password')


class UpdateAdministratorProfile(View):
    template = 'admin_template/update_administrator_profile.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_user_instance = get_object_or_404(User, pk = request.user.id)
        context = {
            'form':UpdateAdministratorProfielForm(instance = get_user_instance)
        }
        return render(request, self.template, context)

    def post(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_user_instance = get_object_or_404(User, pk = request.user.id)
        get_user_instance.email = request.POST['email']
        get_user_instance.username = request.POST['email']
        get_user_instance.name = request.POST['name']
        if request.FILES.get('user_pics', False):
            get_user_instance.user_pics = request.FILES.get('user_pics')
        get_user_instance.mobile_no = request.POST['mobile_no']
        get_user_instance.save()
        messages.add_message(request, messages.SUCCESS, "Administrator profile updated successfully.")
        return redirect('administrator_update_profile')


