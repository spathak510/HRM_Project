from __future__ import unicode_literals
import csv
import json
import os
from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Template
from django.template.loader import get_template

from django.db.models import Q,Count
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils.encoding import smart_str
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from aditshsoft.common import CommonPagination, SaveCsvSheet
from aditshsoft.common import Getmonthlist, SiteUrl, UserPermission
from aditshsoft.common import Getyearlist, time_slots, Getyearlist1
from hrms_management.models import *
from admin_main.models import *
from .forms import *

# Create Your Views Here.

class CrmDashBoard(View):
    template = 'admin_template/crm_management/crm_dashboard.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, string = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        return render(request, self.template)


# ============================ Bind Coutry, State and City ============================
class CrmBindData(View):
    def post(self, request, *args, **kwargs):
        ServicesHtml = ''
        if request.is_ajax:
            if str(request.POST.get('key')) == "map_city":
                ServicesHtml += '<option value="">Select City</option>'
                get_all_state = [data for data in State.objects.filter(country_id=request.POST['id'])]
                cities = City.objects.filter(state_id__in =get_all_state).order_by('name')
                for city in cities:
                    ServicesHtml += '<option value="' + \
                                str(city.id) + '">' + city.name + '</option>'
            else:
                ServicesHtml += '<option value="">Select State</option>'
                states = State.objects.filter(country_id=request.POST['id']).order_by('name')
                if states:
                    for state in states:
                        ServicesHtml += '<option value="' + \
                                    str(state.id) + '">' + state.name + '</option>'
            return JsonResponse({'data': ServicesHtml})


class CrmBindDataCity(View):
    def post(self, request, *args, **kwargs): 
        ServicesHtml = ''
        if request.is_ajax:
            ServicesHtml += '<option value="">Select City</option>'
            cities = City.objects.filter(state_id=request.POST['id']).order_by('name')
            if cities:
                for city in cities:
                    ServicesHtml += '<option value="' + \
                                str(city.id) + '">' + city.name + '</option>'

            return JsonResponse({'data': ServicesHtml})
            

class CrmBindHeadOfficeData(View):
    def post(self, request, *args, **kwargs): 
        ServicesHtml = ''
        if request.is_ajax:
            get_office = ManageHeadOfficeSetup.objects.filter(parent_company_id =request.POST['id']).order_by('-id')
            if get_office:
                ServicesHtml += '<option value="" selected> Select Head Office </option>'
                for head_oofice in get_office:
                    ServicesHtml += '<option value="' + \
                                str(head_oofice.id) + '">' + head_oofice.hod_id + '</option>'
            return JsonResponse({'data': ServicesHtml})


class CrmBindBranchesData(View):
    def post(self, request, *args, **kwargs): 
        ServicesHtml = ''
        if request.is_ajax:

            get_branches = ManageBranch.objects.filter(head_office_id =request.POST['id']).order_by('-id')
            if get_branches:
                ServicesHtml += '<option value="" selected> Select Branch </option>'
                for bra in get_branches:
                    ServicesHtml += '<option value="' + \
                                str(bra.id) + '">' + bra.branch_id + '</option>'

            return JsonResponse({'data': ServicesHtml})


#============================ CRM ComPany Set Up ============================
class CrmCompanySetUpList(View):
    template = 'admin_template/crm_management/company_set_up/crm_company_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self,request):
        responselistquery = CompanySetup.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddCompanySetUp(request):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':   
        form = CrmProductForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            for lo_crncy_id in  dict(request.POST)['local_currency']:
                location_curn_setup = CompanyLocalCurrency()
                location_curn_setup.parent_company_id = form.id
                location_curn_setup.local_currency_id = lo_crncy_id
                location_curn_setup.save()

            for repo_crncy_id in  dict(request.POST)['reporting_currency']:
                repo_curn_setup = CompanyReportingCurrency()
                repo_curn_setup.parent_company_id = form.id
                repo_curn_setup.reporting_currency_id = repo_crncy_id
                repo_curn_setup.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING,'Company with this Company id already exists!!')
        return redirect('crmparentcompanylist')
    else:
        form = CrmProductForm()
    context = {
        'form': form
    }
    return render(request, 'admin_template/crm_management/company_set_up/crm_company_add.html', context)


def CrmEditCompanySetUp(request, company_id):
    company = get_object_or_404(CompanySetup, pk=company_id)
    if request.method == "POST":
        form = UpdateCrmProductForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            CompanyLocalCurrency.objects.filter(parent_company_id = company_id).delete()
            CompanyReportingCurrency.objects.filter(parent_company_id = company_id).delete()
            for lo_crncy_id in  dict(request.POST)['local_currency']:
                location_curn_setup = CompanyLocalCurrency()
                location_curn_setup.parent_company_id = company_id
                location_curn_setup.local_currency_id = lo_crncy_id
                location_curn_setup.save()
            for repo_crncy_id in  dict(request.POST)['reporting_currency']:
                repo_curn_setup = CompanyReportingCurrency()
                repo_curn_setup.parent_company_id = company_id
                repo_curn_setup.reporting_currency_id = repo_crncy_id
                repo_curn_setup.save()
            messages.add_message(request, messages.SUCCESS, "Company added Successfully.")
        else:
            messages.add_message(request, messages.ERROR, form.errors)
        return redirect('crmparentcompanylist')
    else:
        form = UpdateCrmProductForm(instance=company)
    context =  {
        'form': form,
        'details': company,
        'local_curncy': TypeofCurrency.objects.filter(is_active = True),
        'reporting_curncy': TypeofCurrency.objects.filter(is_active = True)
    }
    return render(request, 'admin_template/crm_management/company_set_up/crm_company_edit.html', context)


class CrmCompanyDataDelete(View):
    
    def get(self, request, company_id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = CompanySetup.objects.filter(id = company_id).delete()
        messages.add_message(request, messages.SUCCESS, "Company deleted Successfully.")
        return redirect('crmparentcompanylist')


# ============================ Manage CRM Head Office ============================
class CrmManageHeadOfficeList(View):
    template = 'admin_template/crm_management/company_set_up/crm_manage_head_office_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageHeadOfficeSetup.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmManageHeadOfficeAdd(View):
    template = 'admin_template/crm_management/company_set_up/add_crm_manage_head_office.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self,request):
        form = CrmAddHeadofficeForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)             


    def post(self, request, hod_id = None):
        form = CrmUpdateHeadofficeForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            for lo_crncy_id in  dict(request.POST)['local_currency']:
                location_curn_setup = ManageHeadofficeLocalCurrency()
                location_curn_setup.head_office_id = form.id
                location_curn_setup.local_currency_id = lo_crncy_id
                location_curn_setup.save()
            for repo_crncy_id in  dict(request.POST)['reporting_currency']:
                repo_curn_setup = ManageHeadofficeReportingCurrency()
                repo_curn_setup.head_office_id = form.id
                repo_curn_setup.reporting_currency_id = repo_crncy_id
                repo_curn_setup.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!!')
        else:
            messages.add_message(request, messages.WARNING, 'Office Detail Not Added!!')
        return redirect('crmmanageheadoffice')



def CrmManageHeadOfficeEdit(request, hod_id):
    manageoffice = get_object_or_404(ManageHeadOfficeSetup, pk=hod_id)
    if request.method == "POST":
        form = CrmUpdateHeadofficeForm(request.POST, request.FILES, instance=manageoffice)
        if form.is_valid():
            form.save()
            ManageHeadofficeLocalCurrency.objects.filter(head_office_id = hod_id).delete()
            ManageHeadofficeReportingCurrency.objects.filter(head_office_id = hod_id).delete()
            for lo_crncy_id in  dict(request.POST)['local_currency']:
                location_curn_setup = ManageHeadofficeLocalCurrency()
                location_curn_setup.head_office_id = hod_id
                location_curn_setup.local_currency_id = lo_crncy_id
                location_curn_setup.save()

            for repo_crncy_id in  dict(request.POST)['reporting_currency']:
                repo_curn_setup = ManageHeadofficeReportingCurrency()
                repo_curn_setup.head_office_id = hod_id
                repo_curn_setup.reporting_currency_id = repo_crncy_id
                repo_curn_setup.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!')
        else:
            messages.add_message(request, messages.WARNING, 'Office Detail Not Added!!')
        return redirect('crmmanageheadoffice')
    else:
        form = CrmUpdateHeadofficeForm(instance=manageoffice)
    context =  {
        'form': form,
        'details': manageoffice,
        'local_curncy': TypeofCurrency.objects.filter(is_active = True),
        'reporting_curncy': TypeofCurrency.objects.filter(is_active = True)
    }
    return render(request, 'admin_template/crm_management/company_set_up/edit_crm_manage_head_office.html', context)


class CrmOfficeDataDelete(View):

    def get(self, request, hod_id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageHeadOfficeSetup.objects.filter(id = hod_id).delete()
        messages.add_message(request, messages.SUCCESS, "Office deleted Successfully.")
        return redirect('crmmanageheadoffice')


#============================ Manage Branch ============================
class CrmManageBranchList(View):
    template = 'admin_template/crm_management/company_set_up/manage_branch/manage_branch_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageBranch.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmManageBranchAdd(View):
    template = 'admin_template/crm_management/company_set_up/manage_branch/add-branch.html'

    def get(self,request):
        form = CrmAddBranchForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            

    def post(self, request, hod_id = None):
        if request.method == 'POST':
            form = CrmUpdateBranchForm(request.POST, request.FILES)
            if form.is_valid():
                form  = form.save()
                for lo_crncy_id in  dict(request.POST)['local_currency']:
                    location_curn_setup = ManageBranchLocalCurrency()
                    location_curn_setup.branch_id_id = form.id
                    location_curn_setup.local_currency_id = lo_crncy_id
                    location_curn_setup.save()

                for repo_crncy_id in  dict(request.POST)['reporting_currency']:
                    repo_curn_setup = ManageBranchReportingCurrency()
                    repo_curn_setup.branch_id_id = form.id
                    repo_curn_setup.reporting_currency_id = repo_crncy_id
                    repo_curn_setup.save()
                messages.add_message(request, messages.SUCCESS, ('Successfully added!! ')) 
            else:
                messages.add_message(request, messages.WARNING, ('Branch with this Company id already exists!!'))
            return redirect('crmmanagebranchlist')
        else:
            form = CrmAddBranchForm()
            context = {
                'form': form    
            }
            return render(request, self.template, context)


def CrmManageBranchEdit(request, branch_id):
    managebranch = get_object_or_404(ManageBranch, pk=branch_id)
    form = CrmUpdateBranchForm(request.POST, request.FILES, instance=managebranch)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            ManageBranchLocalCurrency.objects.filter(branch_id_id = branch_id).delete()
            ManageBranchReportingCurrency.objects.filter(branch_id_id = branch_id).delete()
            for lo_crncy_id in  dict(request.POST)['local_currency']:
                location_curn_setup = ManageBranchLocalCurrency()
                location_curn_setup.branch_id_id = branch_id
                location_curn_setup.local_currency_id = lo_crncy_id
                location_curn_setup.save()

            for repo_crncy_id in  dict(request.POST)['reporting_currency']:
                repo_curn_setup = ManageBranchReportingCurrency()
                repo_curn_setup.branch_id_id = branch_id
                repo_curn_setup.reporting_currency_id = repo_crncy_id
                repo_curn_setup.save()
            messages.add_message(request, messages.SUCCESS, "Branch Edit Successfully.")
        else:
            messages.add_message(request, messages.ERROR, "Something Went Wrong.")
        return redirect('crmmanagebranchlist')
    else:
        form = CrmUpdateBranchForm(instance=managebranch)
    context =  {
        'form': form,
        'details': managebranch,
        'local_curncy': TypeofCurrency.objects.filter(is_active = True),
        'reporting_curncy': TypeofCurrency.objects.filter(is_active = True)
    }
    return render(request, 'admin_template/crm_management/company_set_up/manage_branch/edit_branch.html', context)


class CrmBranchDataDelete(View):
    def get(self, request, branch_id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageBranch.objects.filter(id = branch_id).delete()
        messages.add_message(request, messages.SUCCESS, "Branch deleted Successfully.")
        return redirect('crmmanagebranchlist')


#  --------------------------------- Manage City With Branches ------------------------------------------
class CrmManageCountryAdd(View):
    template = 'admin_template/crm_management/company_set_up/manage_city/manage_city_add.html'

    def get(self,request):
        form = CountryAddForm()
        context = {'form': form}
        return render(request, self.template, context)            
    
    def post(self, request, hod_id = None):
        if request.method == 'POST':
            form = CountryAddForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Country Added Successfully.")
                return redirect("crmmanagecitycountryadd")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
                return redirect("crmmanagecitycountryadd")
        else:
            form = CountryAddForm()
        context = {
            'form': form
        }
        return render(request, self.template , )


class CrmManageStateAdd(View):
    template = 'admin_template/crm_management/company_set_up/manage_city/manage_city_add.html'

    def get(self,request):
        form = CrmStateAddForm()
        context = {'form': form}
        return render(request, self.template, context)            
    
    def post(self, request, hod_id = None):
        if request.method == 'POST':
            form = CrmStateAddForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Country Added Successfully.")
                return redirect("crmmanagecitystateadd")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
                return redirect("crmmanagecitystateadd")
        else:
            form = CrmStateAddForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)


class CrmManageCityList(View):
    template = 'admin_template/crm_management/company_set_up/manage_city/manage_city_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ''
        if request.GET.get('search'):
            get_report = City.objects.filter(name__icontains = request.GET.get('search')).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmManageCitiesAdd(View):
    template = 'admin_template/crm_management/company_set_up/manage_city/manage_city_add.html'

    def get(self,request):
        form = CrmCityForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            

    def post(self, request, hod_id = None):
        if request.method == 'POST':
            if City.objects.filter( state_id = request.POST['state'], name = request.POST.get('name')):
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect("crmmanagecitylist")
            print("***", request.POST)
            save_city = City()
            save_city.name = request.POST.get('name')
            save_city.state_id = request.POST['state']
            save_city.district = request.POST['district']
            save_city.country_id = request.POST['country']
            save_city.country_id = request.POST['country']
            save_city.uploaded_by_admin = True
            save_city.save()
            messages.add_message(request, messages.SUCCESS, "City Added Successfully.")
            return redirect("crmmanagecitylist")
        else:
            form = CrmCityForm()
        return render(request, self.template , {'form': form})


def CrmManageCityEdit(request, id):
    managecity = get_object_or_404(City, pk=id)
    if request.method == "POST":
        if City.objects.filter(id = id, state_id = request.POST['state'], name = request.POST.get('name')):
            pass
        else:
            if City.objects.filter(state_id = request.POST['state'], name = request.POST.get('name')):
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect("crmmanagecitylist")
        managecity.name = request.POST.get('name')
        managecity.state_id = request.POST['state']
        managecity.district = request.POST['district']
        managecity.country_id = request.POST['country']
        managecity.uploaded_by_admin = True
        managecity.save()
        messages.add_message(request, messages.SUCCESS, "City Added Successfully.")
        return redirect("crmmanagecitylist")
    else:
        form = CrmCityEditForm(instance=managecity)
    return render(request, 'admin_template/crm_management/company_set_up/manage_city/edit_city.html', {'form': form})


class CrmCityDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = City.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "City deleted Successfully.")
        return redirect('crmmanagecitylist')


#  ----------------- Manage Mapping Cites With Branches ------------------------------------
class CrmMapCityList(View):
    template = 'admin_template/crm_management/company_set_up/manage_map_city/map_city_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = MapCityBranches.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmMapCityAdd(View):
    template = 'admin_template/crm_management/company_set_up/manage_map_city/map_city_add.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, branch_id_id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if branch_id_id is None:
            data = ''
            branch_id_id = None
            get_mapped_city = ''
        else:
            data = get_object_or_404(MapCityBranches, pk=branch_id_id)
            get_mapped_city = MapCityMultipleWithBranches.objects.filter(city_map_id = branch_id_id)
            branch_id_id = branch_id_id
            get_all_state = [data for data in State.objects.filter(country_id=data.country_id)]
            cities = City.objects.filter(state_id__in =get_all_state).order_by('name')
        context = {
            'data': data,
            'branch_id_id': branch_id_id,
            'country': Country.objects.all(),
            'state': State.objects.filter(country_id = data.country_id) if branch_id_id  else '',
            'city': cities if branch_id_id  else '',
            'branch': ManageBranch.objects.filter(is_active = True),
            'headoffice': ManageHeadOfficeSetup.objects.filter(is_active = True),
            'get_mapped_city': get_mapped_city
        }
        return render(request, self.template, context)            


    def post(self, request, branch_id_id = None):
        if request.POST['branch_id_id'] is None or request.POST['branch_id_id'] == "None":
            save_fina_year = MapCityBranches()
            save_fina_year.country_id =  request.POST['contry']
            if 'is_active' in request.POST:
                save_fina_year.is_active =  True
            else:
                save_fina_year.is_active =  False
            save_fina_year.head_office_id =  request.POST['head_offce']
            save_fina_year.branch_id =  request.POST['branch_name']
            save_fina_year.save()
            collec_appli = []
            for p in  dict(request.POST)['city']:
                collec_appli.append(p)
                try:
                    save_aplica = MapCityMultipleWithBranches.objects.get(city_id = p)
                    save_aplica.city_map_id = save_fina_year.id
                    save_aplica.city_id = p
                    save_aplica.save()
                except:
                    save_aplica = MapCityMultipleWithBranches()
                    save_aplica.city_map_id = save_fina_year.id
                    save_aplica.city_id = p
                    save_aplica.save()
            messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
        else:
            branch_id_id = request.POST['branch_id_id']
            save_fina_year = get_object_or_404(MapCityBranches, pk=branch_id_id)
            messages.add_message(request, messages.SUCCESS, "Record updated Successfully.")
            save_fina_year.country_id =  request.POST['contry']
            if 'is_active' in request.POST:
                save_fina_year.is_active =  True
            else:
                save_fina_year.is_active =  False
            save_fina_year.head_office_id =  request.POST['head_offce']
            save_fina_year.branch_id =  request.POST['branch_name']
            save_fina_year.save()
            collec_appli = []
            for p in  dict(request.POST)['city']:
                collec_appli.append(p)
                try:
                    save_aplica = MapCityMultipleWithBranches.objects.get(city_id = p)
                    save_aplica.city_map_id = save_fina_year.id
                    save_aplica.city_id = p
                    save_aplica.save()
                except:
                    save_aplica = MapCityMultipleWithBranches()
                    save_aplica.city_map_id = save_fina_year.id
                    save_aplica.city_id = p
                    save_aplica.save()
            MapCityMultipleWithBranches.objects.filter(~Q(city_id__in = collec_appli), city_map_id = branch_id_id).delete()
        return redirect('crmmapcitylist')


class CrmMapCityDelete(View):
    def get(self, request, branch_id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = MapCityBranches.objects.filter(id = branch_id).delete()
        messages.add_message(request, messages.SUCCESS, "Mapped City deleted Successfully.")
        return redirect('crmmapcitylist')


# ---------------------------------- Manage User Set Up ------------------------------------
class CrmUserSetupList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/list_user.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = User.objects.filter(is_superuser = 0, manual_create_admin = 1).order_by('-id')
        if request.GET.get('user_type') is not None and str(request.GET.get('user_type')) != "":
            if str(request.GET.get('user_type')) == "1":
                get_report = get_report.filter(is_staff = True)
            else:
                get_report = get_report.filter(is_sub_staff = True)
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmUserAdd(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/user_add.html'

    def get(self,request):
        form = CrmUserSetupForm()
        context = {
            'form': form, 
            'branches': ManageBranch.objects.filter(is_active = True)
        }
        return render(request, self.template, context)            


    def post(self, request, id = None):
        form = CrmUserSetupForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                save_data = form.save()
                if str(request.POST.get('user_type')) == "1":
                    save_data.is_staff = True
                    save_data.is_sub_staff = False
                else:
                    save_data.is_sub_staff = True
                    save_data.is_staff = False
                save_data.password = make_password(save_data.gen_password)
                save_data.username = save_data.email
                save_data.email = save_data.email
                save_data.user_uniqueid = "AD"+str(save_data.id)
                save_data.save()
                # SAVED BRANCHES
                id = save_data.id
                if user in request.POST:
                    for p in  dict(request.POST)['user']:
                        try:
                            save_data = UserMultipleBranch.objects.get(branch_allocated_id= p, user_id = id)
                            save_data.user_id = id
                            save_data.branch_allocated_id = p
                            save_data.save()
                        except:
                            save_data = UserMultipleBranch()
                            save_data.user_id = id
                            save_data.branch_allocated_id = p
                            save_data.save()
                # Save USER ROLE
                if 'user_role' in request.POST:
                    for p in  dict(request.POST)['user_role']:
                        try:
                            save_data = ManageUserMultipleRole.objects.get(user_role_id = p, user_id = id)
                            save_data.user_id = id
                            save_data.user_role_id = p
                            save_data.save()
                        except:
                            save_data = ManageUserMultipleRole()
                            save_data.user_id = id
                            save_data.user_role_id = p
                            save_data.save()
                messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
                
            else:
                messages.add_message(request, messages.WARNING, 'User Not Added!!')
                                    
            return redirect('crmusersetuplist')
        except:
            pass
        return redirect('crmusersetuplist')


def CrmManageUserEdit(request, id):
    manageuser = get_object_or_404(User, pk=id)
    form = CrmUserSetupForm(request.POST,  request.FILES, instance=manageuser)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            if str(request.POST.get('user_type')) == "1":
                user.is_staff = True
                user.is_sub_staff = False
            else:
                user.is_sub_staff = True
                user.is_staff = False
            user.password = make_password(user.gen_password)
            user.username = user.email
            user.email = user.email
            user.user_uniqueid = "AD"+str(user.id)
            user.save()
            
            # update_session_auth_hash(request, user)
            value_append = []
            if 'user' in request.POST:
                for p in  dict(request.POST)['user']:
                    value_append.append(p)
                    try:
                        save_data = UserMultipleBranch.objects.get(branch_allocated_id= p, user_id = id)
                        save_data.user_id = id
                        save_data.branch_allocated_id = p
                        save_data.save()
                    except:
                        save_data = UserMultipleBranch()
    #123
                        save_data.user_id = id
                        save_data.branch_allocated_id = p
                        save_data.save()
            # SAVE USER ROLE
            user_append = []
            if 'user_role' in request.POST:
                for p in  dict(request.POST)['user_role']:
                    user_append.append(p)
                    try:
                        save_data = ManageUserMultipleRole.objects.get(user_role_id = p, user_id = id)
                        save_data.user_id = id
                        save_data.user_role_id = p
                        save_data.save()
                    except:
                        save_data = ManageUserMultipleRole()
                        save_data.user_id = id
                        save_data.user_role_id = p
                        save_data.save()
            UserMultipleBranch.objects.filter(~Q(branch_allocated_id__in = value_append), user_id = id).delete()
            ManageUserMultipleRole.objects.filter(~Q(user_role_id__in = user_append), user_id = id).delete()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!! ')
            return redirect('crmusersetuplist')
        else:
            messages.add_message(request, messages.ERROR, 'Something Went Wrong.')
            return redirect('crmusersetuplist')
    else:
        form = CrmUserSetupEditForm(instance=manageuser)
    get_user_branches = UserMultipleBranch.objects.filter(user_id = manageuser.id)
    context ={
        'form': form,
        'get_user_branches': get_user_branches,
        'branches': ManageBranch.objects.filter(is_active = True),
        'id': id,
        'manageuser': manageuser
    }
    return render(request, 'admin_template/crm_management/company_set_up/user_set_up/edit_user.html', context)


class CrmUserDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = User.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crmusersetuplist')


# ***************************** Create Administrator User *************************
class CrmAdministratorSetupList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/administrator_user_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = User.objects.filter(~Q(id = request.user.id), is_superuser = 1).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmCreateAdministratorUserAddEdit(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/add_administrator_user.html'
    template1 = 'admin_template/crm_management/company_set_up/user_set_up/edit_administrator_user.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = UpdateAdministratorProfielForm()
            id = ''
        else:
            data = get_object_or_404(User, pk=id)
            id = id
            form = UpdateSuperUserAdministratorProfielForm(instance=data)
        context = {
            'form': form,
            'id':id
        }
        template = self.template if id is None else self.template1
        return render(request, template, context)

    def post(self, request, id = None):
        # import pdb;pdb.set_trace()
        if id is None:
            get_user_instance = User()
            get_user_instance.email = request.POST['email']
            get_user_instance.username = request.POST['email']
            get_user_instance.name = request.POST['name']
            get_user_instance.mobile_no = request.POST['mobile_no']
            get_user_instance.is_superuser = 1
            get_user_instance.user_pics = request.FILES.get('user_pics')
            # get_user_instance.save()
            get_user_instance.password = make_password(get_user_instance.gen_password)
            get_user_instance.save()
            messages.add_message(request, messages.SUCCESS, "Administrator profile added successfully.")
        else:
            get_user_instance = get_object_or_404(User, pk = id)
            get_user_instance.email = request.POST['email']
            get_user_instance.username = request.POST['email']
            get_user_instance.name = request.POST['name']
            get_user_instance.mobile_no = request.POST['mobile_no']
            if request.FILES.get('user_pics', False):
                get_user_instance.user_pics = request.FILES.get('user_pics')
            get_user_instance.password = make_password(request.POST['gen_password'])
            get_user_instance.gen_password = request.POST['gen_password']
            if 'is_active' in request.POST:
                get_user_instance.is_active = True
            else:
                get_user_instance.is_active = False
            get_user_instance.save()
            messages.add_message(request, messages.SUCCESS, "Administrator profile updated successfully.")
        return redirect('crm_administrator_setup_list')


class CrmAdministratorUserDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = User.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_administrator_setup_list')


# Master For UserSet Up
class CrmDepartmentList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/depart_ment_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDepartment.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(department__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmDepartmentAdd(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/department_add.html'
    def get(self,request):
        form = CrmDepartmentAddForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = CrmDepartmentAddForm(request.POST)
        if form.is_valid(): 
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Department already exists!!')
        return redirect('crmdepartmentlist')


def CrmDepartmentEdit(request, delete):
    company = get_object_or_404(ManageDepartment, pk=delete)
    if request.method == "POST":
        form = CrmDepartmentAddForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ') 
            return redirect('crmdepartmentlist')
        else:
            messages.add_message(request, messages.WARNING, 'Department already exists!!')
            return redirect('crmdepartmentlist')
    else:
        form = CrmDepartmentAddForm(instance=company)
    return render(request, 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/department_add.html', {'form': form})


class CrmDepartmentdelete(View):
    def get(self, request, delete):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDepartment.objects.filter(id = delete).delete()
        messages.add_message(request, messages.SUCCESS, "Data Deleted Successfully.")
        return redirect('crmdepartmentlist')


class CrmDesignationList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/designation_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDesignation.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(designation__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmDesignationAdd(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/designation_add.html'

    def get(self,request):
        form = CrmDesignationAddForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)
    def post(self, request, branch_id = None):
        form = CrmDesignationAddForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Already exists!!')
        return redirect('crmdesignationlist')


def CrmDesignationEdit(request, delete):
    company = get_object_or_404(ManageDesignation, pk=delete)
    if request.method == "POST":
        form = CrmDesignationAddForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!! ') 
            return redirect('crmdesignationlist')
        else:
            messages.add_message(request, messages.WARNING, 'Already exists!!')
            return redirect('crmdesignationlist')
    else:
        form = CrmDesignationAddForm(instance=company)
    return render(request, 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/designation_add.html', {'form': form})


class CrmDesignationdelete(View):
    def get(self, request, delete):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDesignation.objects.filter(id = delete).delete()
        messages.add_message(request, messages.SUCCESS, "Data Deleted Successfully.")
        return redirect('crmdesignationlist')


class CrmResponsibilityList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/responsibility_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageResponsibility.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(responsibilities__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template, {'responselistquery': report_paginate})


class CrmResposibilityAdd(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/add_responsibility_add.html'

    def get(self,request):
        form = CrmResponsibilityAddForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            

    def post(self, request, branch_id = None):
        form = CrmResponsibilityAddForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ') 
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Already exists!!')
    
        return redirect('crmresposibilitylist')        


def CrmResponsibilityEdit(request, delete):
    company = get_object_or_404(ManageResponsibility, pk=delete)
    if request.method == "POST":
        form = CrmResponsibilityAddForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!! ')
            return redirect('crmresposibilitylist')
        else:
            messages.add_message(request, messages.WARNING, 'Already exists!!')
            return redirect('crmresposibilitylist')
    else:
        form = CrmResponsibilityAddForm(instance=company)
    return render(request, 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/add_responsibility_add.html', {'form': form})


class CrmResponsibilitydelete(View):
    def get(self, request, delete):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageResponsibility.objects.filter(id = delete).delete()
        messages.add_message(request, messages.SUCCESS, "Data Deleted Successfully.")
        return redirect('crmresposibilitylist')


class RoleManagementList(View):
    template = 'admin_template/crm_management/company_set_up/role_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = RoleMangement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditUserRoleManagement(View):
    template = 'admin_template/crm_management/company_set_up/add_edit_role.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, responseid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if responseid is None:
            data = ''
            responseid = None
        else:
            data = get_object_or_404(RoleMangement, pk=responseid)
            responseid = responseid
        context = {
            'data': data, 
            'responseid': responseid,
        }
        return render(request, self.template, context)

    def post(self, request, responseid = None):
        if request.POST['responseid'] is None or request.POST['responseid'] == "None":
            save_update_data = RoleMangement()
            messages.add_message(request, messages.SUCCESS, "Response added Successfully.")
        else:
            responseid = request.POST['responseid']
            save_update_data = get_object_or_404(RoleMangement, pk=responseid)
            messages.add_message(request, messages.SUCCESS, "Role Created Successfully.")
        save_update_data.name =  request.POST['response_name']
        if 'is_active' in request.POST:
            save_update_data.is_active =  True
        else:
            save_update_data.is_active =  False
        save_update_data.save()
        return redirect('crmrolelist')


class CrmRoleManagementDelete(View):
    def get(self, request, delete):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RoleMangement.objects.filter(id = delete).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crmrolelist')


# ---------------------------- Product Set Up -------------------------------------
class CrmProductSetupList(View):
    template = 'admin_template/crm_management/product_set_up/product_setup_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageProductType.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmProductAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_setup_add.html'

    def get(self,request):
        form = CrmProductSetupForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = CrmProductSetupForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
            return redirect('crmproductsetuplist')
        else:
            messages.add_message(request, messages.WARNING, 'Data already exists!!')
        return redirect('crmproductsetuplist')


def CrmManageProductEdit(request, id):
    manageproduct = get_object_or_404(ManageProductType, pk=id)
    if request.method == "POST":
        form = CrmProductSetupForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Updated!! ')
            return redirect('crmproductsetuplist')
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists.')
            return redirect('crmproductsetuplist')
    else:
        form = CrmProductSetupForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/edit_product.html', {'form': form})


class CrmProductDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageProductType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crmproductsetuplist')


# ****************** new renue Product Management **************************
class CrmManageUpdateRevenueList(View):
    template = 'admin_template/crm_management/product_set_up/product_category_list.html'
    pagesize = 10
   
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageUpdateRevenue.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmManageUpdateRevenueAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_category_add.html'

    def get(self,request):
        form = ManageUpdateRevenueForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)           

    def post(self, request, branch_id = None):
        form = ManageUpdateRevenueForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Data already exists!!')
        return redirect('crm_productcategorylist')


def CrmManageUpdateRevenueEdit(request, id):
    manageproduct = get_object_or_404(ManageUpdateRevenue, pk=id)
    if request.method == "POST":
        form = ManageUpdateRevenueForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!')
            return redirect('crm_productcategorylist')
        else:
            messages.add_message(request, messages.SUCCESS, 'Data already exists!!')
            return redirect('crm_productcategorylist')
    else:
        form = ManageUpdateRevenueForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/product_category_add.html', {'form': form})


class CrmManageUpdateRevenueDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageUpdateRevenue.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_productcategorylist')

######## new product management
class ManageProductNameList(View):
    template = 'admin_template/crm_management/product_set_up/product_name_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageProducts.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ManageProductNameAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_name_add.html'

    def get(self,request):
        form = ManageProductsForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)


    def post(self, request, branch_id = None):
        form = ManageProductsForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Data already exists!!')
        return redirect('productnamelist')


def ManageProductNameEdit(request, id):
    manageproduct = get_object_or_404(ManageProducts, pk=id)
    if request.method == "POST":
        form = ManageProductsForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!! ')
            return redirect('productnamelist')
        else:
            messages.add_message(request, messages.WARNING, 'Data already exists!!')
            return redirect('productnamelist')
    else:
        form = ManageProductsForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/product_name_add.html', {'form': form})


class ManageProductNameDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageProducts.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('productnamelist')

class ManageProductFacilityList(View):
    template = 'admin_template/crm_management/product_set_up/product_facility_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ProductFacility.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ManageProductFacilityAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_facility_add.html'

    def get(self,request):
        form = ProductFacilityForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):

        form = ProductFacilityForm(request.POST, request.FILES)
        if form.is_valid():
             
            messages.add_message(request, messages.SUCCESS,
                                 ('Successfully added!! ')) 
            form.save()

            
        else:
            messages.add_message(request, messages.WARNING,
                                 ('Data already exists!!'))
        return redirect('productfacilitylist')


def ManageProductFacilityEdit(request, id):

    manageproduct = get_object_or_404(ProductFacility, pk=id)
    if request.method == "POST":
        form = ProductFacilityForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('productfacilitylist')
    else:
        form = ProductFacilityForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/product_facility_add.html', {'form': form})


class ManageProductFacilityDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ProductFacility.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('productfacilitylist')




# ------------------------------- Calender Set UP(CRM) -------------------------------------
class FinancialYearListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_financial_year_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageFinancialYear.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddFinancialYearView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_financial_year.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, financialid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        month_list = Getmonthlist.month_list()
        year_list = Getyearlist.year_list()
        if financialid is None:
            data = ''
            financialid = None
        else:
            data = get_object_or_404(ManageFinancialYear, pk=financialid)
            financialid = financialid
        context = {
            'data': data, 
            'financialid': financialid,
            'month_list': month_list,
            'year_list': year_list
        }
        return render(request, self.template, context)

    def post(self, request, financialid = None):
        if request.POST['financialid'] is None or request.POST['financialid'] == "None":
            if ManageFinancialYear.objects.filter(to_month =  request.POST['to_month'], from_month =  request.POST['from_month'], to_year =  request.POST['to_year'], from_year =  request.POST['from_year']):
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
                return redirect('crm_list_financial_year')
            save_fina_year = ManageFinancialYear()
            messages.add_message(request, messages.SUCCESS, "Financial Year added Successfully.")
        else:
            financialid = request.POST['financialid']
            if ManageFinancialYear.objects.filter(~Q(id= financialid),to_month =  request.POST['to_month'], from_month =  request.POST['from_month'], to_year =  request.POST['to_year'], from_year =  request.POST['from_year']):
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
                return redirect('crm_list_financial_year')
            save_fina_year = get_object_or_404(ManageFinancialYear, pk=financialid)
            messages.add_message(request, messages.SUCCESS, "Financial Year updated Successfully.")
        save_fina_year.to_month =  request.POST['to_month']
        save_fina_year.from_month =  request.POST['from_month']
        save_fina_year.to_year =  request.POST['to_year']
        save_fina_year.from_year =  request.POST['from_year']
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        return redirect('crm_list_financial_year')


class CrmFinancialYearDeletView(View):
    def get(self, request, financialreportid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageFinancialYear.objects.filter(id = financialreportid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_financial_year')


class FinancialReportListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_reporting_period_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageFinancialReport.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddFinancialReportView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_reporting_period.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, financialreportid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        month_list = Getmonthlist.month_list()
        year_list = Getyearlist.year_list()
        if financialreportid is None:
            data = ''
            financialreportid = None
        else:
            data = get_object_or_404(ManageFinancialReport, pk=financialreportid)
            financialreportid = financialreportid
        context = {
            'data': data, 
            'financialreportid': financialreportid,
            'month_list': month_list,
            'year_list': year_list
        }
        return render(request, self.template, context)

    def post(self, request, financialreportid = None):
        if request.POST['financialreportid'] is None or request.POST['financialreportid'] == "None":
            if ManageFinancialReport.objects.filter(to_month =  request.POST['to_month'], from_month =  request.POST['from_month'], to_year =  request.POST['to_year'], from_year =  request.POST['from_year']):
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
                return redirect('crm_list_financial_report_year')
            save_fina_year = ManageFinancialReport()
            messages.add_message(request, messages.SUCCESS, "Financial Report added Successfully.")
        else:
            financialreportid = request.POST['financialreportid']
            if ManageFinancialReport.objects.filter(~Q(id= financialreportid),to_month =  request.POST['to_month'], from_month =  request.POST['from_month'], to_year =  request.POST['to_year'], from_year =  request.POST['from_year']):
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
                return redirect('crm_list_financial_report_year')
            save_fina_year = get_object_or_404(ManageFinancialReport, pk=financialreportid)
            messages.add_message(request, messages.SUCCESS, "Financial Report updated Successfully.")
        save_fina_year.to_month =  request.POST['to_month']
        save_fina_year.from_month =  request.POST['from_month']
        save_fina_year.to_year =  request.POST['to_year']
        save_fina_year.from_year =  request.POST['from_year']
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        return redirect('crm_list_financial_report_year')


class CrmFinancialReportDeletView(View):
    def get(self, request, financialreportid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageFinancialReport.objects.filter(id = financialreportid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_financial_report_year')


class WorkingHoursListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_working_hours_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageWorkingHours.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddWorkingHoursView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_working_hours.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, workinghoursid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if workinghoursid is None:
            data = ''
            workinghoursid = None
        else:
            data = get_object_or_404(ManageWorkingHours, pk=workinghoursid)
            workinghoursid = workinghoursid
        get_time = list(time_slots())
        context = {
            'data': data, 
            'workinghoursid': workinghoursid,
            'working_days' : WORKINGDAYS, 
            'get_time_slot': get_time
        }
        return render(request, self.template, context)

    def post(self, request, workinghoursid = None):
        if request.POST['workinghoursid'] is None or request.POST['workinghoursid'] == "None":
            save_fina_year = ManageWorkingHours()
            mes = "Working Hours added Successfully."
            try:
                save_fina_year.working_days =  request.POST['working_hours']
                save_fina_year.start_date_time =  request.POST['start_date_time']
                save_fina_year.end_date_time =  request.POST['end_date_time']
                save_fina_year.lunch_break_from =  request.POST['lunch_break']
                save_fina_year.lunch_break_to =  request.POST['to_lunch_break']
                save_fina_year.logout_time =  request.POST['logout_time']
                if 'is_active' in request.POST:
                    save_fina_year.is_active =  True
                else:
                    save_fina_year.is_active =  False
                save_fina_year.save()
                messages.add_message(request, messages.SUCCESS, mes)
            except:
                mes = "Data already exists."
                messages.add_message(request, messages.WARNING, mes)
        else:
            workinghoursid = request.POST['workinghoursid']
            save_fina_year = get_object_or_404(ManageWorkingHours, pk=workinghoursid)
            mes = "Working Hours updated Successfully."
            try:
                save_fina_year.working_days =  request.POST['working_hours']
                save_fina_year.start_date_time =  request.POST['start_date_time']
                save_fina_year.end_date_time =  request.POST['end_date_time']
                save_fina_year.lunch_break_from =  request.POST['lunch_break']
                save_fina_year.lunch_break_to =  request.POST['to_lunch_break']
                save_fina_year.logout_time =  request.POST['logout_time']
                if 'is_active' in request.POST:
                    save_fina_year.is_active =  True
                else:
                    save_fina_year.is_active =  False
                save_fina_year.save()
                messages.add_message(request, messages.SUCCESS, mes)
            except:
                mes = "Data already exists."
                messages.add_message(request, messages.WARNING, mes)
        return redirect('crm_list_working_hours')


class CrmWorkingHoursDeletView(View):
    def get(self, request, workinghoursid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageWorkingHours.objects.filter(id = workinghoursid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_working_days')


class WorkingDaysListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_working_days_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageWorkingDays.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddWorkingDaysView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_working_days.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, workingdaysid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if workingdaysid is None:
            data = ''
            workingdaysid = None;weekly_off_days = '';weekly_workin_days = '';
            half_days = '';alternate_week_days = ''
        else:
            data = get_object_or_404(ManageWorkingDays, pk=workingdaysid)
            workingdaysid = workingdaysid
            weekly_off_days = str(data.weekly_off_working_days).split(",")
            weekly_workin_days = str(data.weekly_working_days).split(",")
            half_days = str(data.half_days).split(",")
            alternate_week_days = str(data.alternate_week_days).split(",")
        context = {
            'data': data, 
            'workingdaysid': workingdaysid,
            'working_days_name': WORKINGDAYS1,
            'weekly_off_days': weekly_off_days, 
            'weekly_workin_days': weekly_workin_days,
            'half_days': half_days,
            'alternate_week_days': alternate_week_days,
        }
        return render(request, self.template, context)

    def post(self, request, workingdaysid = None):
        if request.POST['workingdaysid'] is None or request.POST['workingdaysid'] == "None":
            save_fina_year = ManageWorkingDays()
            messages.add_message(request, messages.SUCCESS, "Working Days added Successfully.")
        else:
            workingdaysid = request.POST['workingdaysid']
            save_fina_year = get_object_or_404(ManageWorkingDays, pk=workingdaysid)
            messages.add_message(request, messages.SUCCESS, "Working Days updated Successfully.")
        
        weekly_working_days1 = ''
        if 'weekly_working_days' in request.POST:
            for p in  dict(request.POST)['weekly_working_days']:
                weekly_working_days1 += p +','
            save_fina_year.weekly_working_days =  weekly_working_days1.strip(',')
        else:
            save_fina_year.weekly_working_days = weekly_working_days1

        weekly_off_working = ''
        if 'weekly_off_working_days' in request.POST:
            for p in  dict(request.POST)['weekly_off_working_days']:
                weekly_off_working += p +','
            save_fina_year.weekly_off_working_days =  weekly_off_working.strip(',')
        else:
            save_fina_year.weekly_off_working_days = weekly_off_working

        half_days = ''
        if 'half_days' in request.POST:
            for p in  dict(request.POST)['half_days']:
                half_days += p +','
            save_fina_year.half_days =  half_days.strip(',')
        else:
            save_fina_year.half_days = half_days

        alternate_week = ''
        if 'alternate_week_days' in request.POST:
            for p in  dict(request.POST)['alternate_week_days']:
                alternate_week += p +','
            save_fina_year.alternate_week_days =  alternate_week.strip(',')
        else:
            save_fina_year.alternate_week_days = alternate_week
        save_fina_year.alternate_week = request.POST.get('alternate_week')
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        return redirect('crm_list_working_days') 


class CrmWorkingDaysDeletView(View):
    def get(self, request, workingdaysid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageWorkingDays.objects.filter(id = workingdaysid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_working_days')


class HolidaysListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_manage_holidays_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageHolidays.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddUpdateHoliDaysView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_holidays.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, holidaysdaysid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if holidaysdaysid is None:
            data = ''
            holidaysdaysid = None
        else:
            data = get_object_or_404(ManageHolidays, pk=holidaysdaysid)
            holidaysdaysid = holidaysdaysid
        context = {
            'data': data, 
            'holidaysdaysid': holidaysdaysid,
            'impace_on_salary': YESNO,
            'parent_company': CompanySetup.objects.filter(is_active = True).order_by('-id'),
            'head_offce': ManageHeadOfficeSetup.objects.filter(is_active = True).order_by('-id'),
            'branches': ManageBranch.objects.filter(is_active = True).order_by('-id'),
        }
        return render(request, self.template, context)

    def post(self, request, holidaysdaysid = None):
        if request.POST['holidaysdaysid'] is None or request.POST['holidaysdaysid'] == "None":
            save_fina_year = ManageHolidays()
            messages.add_message(request, messages.SUCCESS, "Holiday added Successfully.")
        else:
            holidaysdaysid = request.POST['holidaysdaysid']
            save_fina_year = get_object_or_404(ManageHolidays, pk=holidaysdaysid)
            messages.add_message(request, messages.SUCCESS, "Holiday updated Successfully.")
        save_fina_year.holidays_type =  request.POST['holidays_type']
        save_fina_year.holidays_date =  request.POST['holidays_date']
        save_fina_year.parent_company_id =  request.POST['parent_company']
        save_fina_year.head_office_id =  request.POST['head_offce']
        save_fina_year.implact_on_salry =  request.POST['implact_on_salry']
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        append_data = []
        if 'branches' in request.POST:
            for p in  dict(request.POST)['branches']:
                append_data.append(p)
                try:
                    saved_data = ManageHolidaysBranches.objects.get(holiday_id = save_fina_year.id, branch_id = p)
                except ManageHolidaysBranches.DoesNotExist:
                    saved_data = ManageHolidaysBranches()
                    saved_data.holiday_id = save_fina_year.id
                    saved_data.branch_id = p
                    saved_data.save()
        ManageHolidaysBranches.objects.filter(~Q(branch_id__in = append_data), holiday_id = save_fina_year.id).delete()
        return redirect('crm_list_holi_days')


class HolidaysDeleteView(View):
    def get(self, request, holidaysdaysid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageHolidays.objects.filter(id = holidaysdaysid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_holi_days')


class OvertimeListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_over_time_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageOverTime.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddUpdateOvertimeView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_over_time.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, overtimeid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if overtimeid is None:
            data = ''
            overtimeid = None
        else:
            data = get_object_or_404(ManageOverTime, pk=overtimeid)
            overtimeid = overtimeid
        get_time = list(time_slots())
        context = {
            'data': data, 
            'overtimeid': overtimeid,
            'get_time':get_time,
            'impace_on_salary':YESNO,
            'working_days': WORKINGDAYS3,
            'name_of_office': ManageHeadOfficeSetup.objects.all(),
            'parent_company': CompanySetup.objects.filter(is_active = True).order_by('-id'),
            'head_offce': ManageHeadOfficeSetup.objects.filter(is_active = True).order_by('-id'),
            'branches': ManageBranch.objects.filter(is_active = True).order_by('-id'),
        }
        return render(request, self.template, context)

    def post(self, request, overtimeid = None):
        if request.POST['overtimeid'] is None or request.POST['overtimeid'] == "None":
            save_fina_year = ManageOverTime()
            messages.add_message(request, messages.SUCCESS, "Over time added Successfully.")
        else:
            overtimeid = request.POST['overtimeid']
            save_fina_year = get_object_or_404(ManageOverTime, pk=overtimeid)
            messages.add_message(request, messages.SUCCESS, "Over time updated Successfully.")
        save_fina_year.start_date_time =  request.POST['start_date_time']
        save_fina_year.end_date_time =  request.POST['end_date_time']
        save_fina_year.impact_on_salary =  request.POST['implact_on_salry']
        save_fina_year.days =  request.POST['over_time_days']
        save_fina_year.parent_com_id =  request.POST['parent_company']
        save_fina_year.head_office_id =  request.POST['head_offce']
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        collec_appli = []
        if 'branches' in request.POST:
            for p in  dict(request.POST)['branches']:
                collec_appli.append(p)
                try:
                    save_aplica = ManageOvertimeApplicable.objects.get(brach_id = p, over_time_id = save_fina_year.id)
                except:
                    save_aplica = ManageOvertimeApplicable()
                    save_aplica.over_time_id = save_fina_year.id
                    save_aplica.brach_id = p
                    save_aplica.save()
        ManageOvertimeApplicable.objects.filter(~Q(brach_id__in = collec_appli), over_time_id = save_fina_year.id).delete()
        return redirect('crm_list_over_time')


class CrmOvertimeDeletView(View):
    def get(self, request, overtimeid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageOverTime.objects.filter(id = overtimeid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_over_time')

##############rajesh
# ------------------------------- Assessment Year Set UP(CRM) -------------------------------------
class AssessmentYearListView(View):
    template = 'admin_template/crm_management/manage_calender/manage_assessment_year_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageAssessmentYear.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddAssessmentYearView(View):
    template = 'admin_template/crm_management/manage_calender/add_manage_assessment_year.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, financialid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        month_list = Getmonthlist.month_list()
        year_list = Getyearlist.year_list()
        if financialid is None:
            data = ''
            financialid = None
        else:
            data = get_object_or_404(ManageAssessmentYear, pk=financialid)
            financialid = financialid
        context = {
            'data': data, 
            'financialid': financialid,
            'month_list': month_list,
            'year_list': year_list
        }
        return render(request, self.template, context)

    def post(self, request, financialid = None):
        if request.POST['financialid'] is None or request.POST['financialid'] == "None":
            if ManageAssessmentYear.objects.filter(to_month =  request.POST['to_month'], from_month =  request.POST['from_month'], to_year =  request.POST['to_year'], from_year =  request.POST['from_year']):
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
                return redirect('crm_list_financial_year')
            save_fina_year = ManageAssessmentYear()
            messages.add_message(request, messages.SUCCESS, "Financial Year added Successfully.")
        else:
            financialid = request.POST['financialid']
            if ManageAssessmentYear.objects.filter(~Q(id= financialid),to_month =  request.POST['to_month'], from_month =  request.POST['from_month'], to_year =  request.POST['to_year'], from_year =  request.POST['from_year']):
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
                return redirect('crm_list_financial_year')
            save_fina_year = get_object_or_404(ManageAssessmentYear, pk=financialid)
            messages.add_message(request, messages.SUCCESS, "Financial Year updated Successfully.")
        save_fina_year.to_month =  request.POST['to_month']
        save_fina_year.from_month =  request.POST['from_month']
        save_fina_year.to_year =  request.POST['to_year']
        save_fina_year.from_year =  request.POST['from_year']
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        return redirect('crm_list_assessment_year')


class CrmAssessmentYearDeletView(View):
    def get(self, request, financialreportid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageAssessmentYear.objects.filter(id = financialreportid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_list_assessment_year')


#  ----------------------------------------- Response Management --------------------------------
class ResponseManagementList(View):
    template = 'admin_template/crm_management/response_management/assessment_year_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ResponseMangement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddUpdateResponseManagement(View):
    template = 'admin_template/crm_management/response_management/add_response.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, responseid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if responseid is None:
            data = ''
            responseid = None
        else:
            data = get_object_or_404(ResponseMangement, pk=responseid)
            responseid = responseid
        context = {
            'data': data, 
            'responseid': responseid,
        }
        return render(request, self.template, context)

    def post(self, request, responseid = None):
        if request.POST['responseid'] is None or request.POST['responseid'] == "None":
            save_update_data = ResponseMangement()
            messages.add_message(request, messages.SUCCESS, "Response added Successfully.")
        else:
            responseid = request.POST['responseid']
            save_update_data = get_object_or_404(ResponseMangement, pk=responseid)
            messages.add_message(request, messages.SUCCESS, "Response updated Successfully.")

        save_update_data.name =  request.POST['response_name']
        save_update_data.type_of_response =  request.POST['response_type']
        save_update_data.description =  request.POST['response_description']
        save_update_data.impace_on_data =  request.POST['response_impact_on_data']
        if 'is_active' in request.POST:
            save_update_data.is_active =  True
        else:
            save_update_data.is_active =  False

        save_update_data.save()
        return redirect('responselist')


class CrmResponseManagementDelete(View):
    def get(self, request, responseid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ResponseMangement.objects.filter(id = responseid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('responselist')


# -------------------- Data Allocation ---------------------------
class DefineClientypeList(View):
    template = 'admin_template/crm_management/data_allocation/define_client_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageClientType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddDefineClientType(View):
    template = 'admin_template/crm_management/data_allocation/add_define_client_type.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if defineclientid is None:
            data = ''
            defineclientid = None
        else:
            data = get_object_or_404(ManageClientType, pk=defineclientid)
            defineclientid = defineclientid
        context = {
            'data': data, 
            'defineclientid': defineclientid,
        }
        return render(request, self.template, context)

    def post(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['defineclientid'] is None or request.POST['defineclientid'] == "None":
            try:
                save_data = ManageClientType()
                save_data.client_type = request.POST['define_client_type']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()
                messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
            except:
                messages.add_message(request, messages.WARNING, "Already Exists.")
        else:
            defineclientid = request.POST['defineclientid']
            save_data = get_object_or_404(ManageClientType, pk=defineclientid)
            try:
                save_data.client_type = request.POST['define_client_type']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()
                messages.add_message(request, messages.SUCCESS, "Record updated Successfully.")
            except:
                messages.add_message(request, messages.WARNING, "Already Exists.")
        return redirect('defineclienttypelist')


class CrmDefineClientTypeDelete(View):
    def get(self, request, defineclientid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageClientType.objects.filter(id = defineclientid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('defineclienttypelist')


class DefineClientCategoryList(View):
    template = 'admin_template/crm_management/data_allocation/add_client_category_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageClientCategory.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddDefineClientCategory(View):
    template = 'admin_template/crm_management/data_allocation/add_define_client_category.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if defineclientid is None:
            data = ''
            defineclientid = None
        else:
            data = get_object_or_404(ManageClientCategory, pk=defineclientid)
            defineclientid = defineclientid
        context = {
            'data': data, 
            'defineclientid': defineclientid,
        }
        return render(request, self.template, context)

    def post(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['defineclientid'] is None or request.POST['defineclientid'] == "None":
            try:
                save_data = ManageClientCategory()
                save_data.client_category = request.POST['define_client_category']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()
                messages.add_message(request, messages.SUCCESS, "Record  added Successfully.")
            except:
                messages.add_message(request, messages.WARNING, "Already Exists.")
        else:
            defineclientid = request.POST['defineclientid']
            try:
                save_data = get_object_or_404(ManageClientCategory, pk=defineclientid)
                messages.add_message(request, messages.SUCCESS, "Record updated Successfully.")
                save_data.client_category = request.POST['define_client_category']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()
            except:
                messages.add_message(request, messages.WARNING, "Already Exists.")
        return redirect('defineclientcategorylist')


class CrmDefineClientCategoryeDelete(View):
    def get(self, request, defineclientid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageClientCategory.objects.filter(id = defineclientid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('defineclientcategorylist')


class DefineClientLeadList(View):
    template = 'admin_template/crm_management/data_allocation/define_client_lead_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageClientLead.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddDefineClientLead(View):
    template = 'admin_template/crm_management/data_allocation/add_define_client_lead.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if defineclientid is None:
            data = ''
            defineclientid = None
        else:
            data = get_object_or_404(ManageClientLead, pk=defineclientid)
            defineclientid = defineclientid
        context = {
            'data': data, 
            'defineclientid': defineclientid,
        }
        return render(request, self.template, context)

    def post(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['defineclientid'] is None or request.POST['defineclientid'] == "None":
            save_data = ManageClientLead()
            messages.add_message(request, messages.SUCCESS, "Record  added Successfully.")
        else:
            defineclientid = request.POST['defineclientid']
            save_data = get_object_or_404(ManageClientLead, pk=defineclientid)
            messages.add_message(request, messages.SUCCESS, "Record updated Successfully.")
        save_data.lead_values = request.POST['define_lead_values']
        if 'is_active' in request.POST:
            save_data.is_active =  True
        else:
            save_data.is_active =  False

        save_data.save()
        return redirect('defineclientleadlist')


class CrmDefineClientLeadeDelete(View):
    def get(self, request, defineclientid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageClientLead.objects.filter(id = defineclientid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('defineclientleadlist')


class DefineClientTypeOfdataList(View):
    template = 'admin_template/crm_management/data_allocation/define_client_type_of_data_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageClientTypeofData.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddDefineClientTypeOfdata(View):
    template = 'admin_template/crm_management/data_allocation/add_define_client_type_of_data.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if defineclientid is None:
            data = ''
            defineclientid = None
        else:
            data = get_object_or_404(ManageClientTypeofData, pk=defineclientid)
            defineclientid = defineclientid
        context = {
            'data': data, 
            'defineclientid': defineclientid,
        }
        return render(request, self.template, context)

    def post(self, request, defineclientid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['defineclientid'] is None or request.POST['defineclientid'] == "None":
            try:
                save_data = ManageClientTypeofData()
                save_data.type_of_Data = request.POST['define_type_of_Data']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()
                messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
            except:
                messages.add_message(request, messages.WARNING, "Already Exists.")
        else:
            defineclientid = request.POST['defineclientid']
            try:
                save_data = get_object_or_404(ManageClientTypeofData, pk=defineclientid)
                messages.add_message(request, messages.SUCCESS, "Record update Successfully.")
                save_data.type_of_Data = request.POST['define_type_of_Data']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()
            except:
                messages.add_message(request, messages.WARNING, "Already Exists.")
        return redirect('defineclienttypeoflistlist')


class CrmDefineTypeOfDataDelete(View):
    def get(self, request, defineclientid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageClientTypeofData.objects.filter(id = defineclientid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('defineclienttypeoflistlist')

#11
class CrmAllocationMatrixClientSupportAllocationList(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/client_support_allocate_matrix.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AllocationMatrixClientSupport.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template, {'responselistquery': report_paginate})

#@@
class CrmAddAllocationMatrixClientSupportAllocation(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/add_client_support_allocate_matrix.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, allocationsetuid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_all_mapped_cities = ''
        if allocationsetuid is None:
            data = ''
            allocationsetuid = None
            city = ''
        else:
            data = get_object_or_404(AllocationMatrixClientSupport, pk=allocationsetuid)
            allocationsetuid = allocationsetuid
            map_cities = []
            append_branch_ids = [ data.branch_allocated_id for data in UserMultipleBranch.objects.filter(user_id=data.user.id)] 
            get_all_mapped_cities =[ p.id for p in MapCityBranches.objects.filter(branch_id__in = append_branch_ids)]
            city = MapCityMultipleWithBranches.objects.filter(city_map__in = get_all_mapped_cities).order_by('-id')
        context = {
            'data': data, 
            'allocationsetuid': allocationsetuid,
            'user_set_up': User.objects.filter(is_active =True, is_superuser=0).order_by('-id'),
            'product_set_up': ManageProductType.objects.filter(is_active =True).order_by('-id'),
            'client_type': ManageClientType.objects.filter(is_active =True).order_by('-id'),
            'client_category': ManageClientCategory.objects.filter(is_active=True).order_by('-id'),
            'product_category': ManageProductCategory.objects.filter(is_active=True).order_by('-id'),
            'product_name': ManageProductName.objects.filter(is_active=True).order_by('-id'),
            'city':   city,
            'get_all_cities': AllocationClientSupportUserCity.objects.filter(client_support_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_product_type': AllocationUserClientSupportProductType.objects.filter(client_support_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_product_category': AllocationClientSupportProductCategory.objects.filter(client_support_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_product_name': AllocationClientSupportProductName.objects.filter(client_support_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_client_type': AllocationClientSupportClientType.objects.filter(client_support_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_client_category': AllocationClientSupportClientCategory.objects.filter(client_support_allocation_id= data.id).order_by('-id') if data != "" else "",
        }
        return render(request, self.template, context)

    def post(self, request, allocationsetuid = None):
        
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['allocationsetuid'] is None or request.POST['allocationsetuid'] == "None":
            if AllocationMatrixClientSupport.objects.filter(user_id = request.POST['user']):
                messages.add_message(request, messages.WARNING, "User Already Exists.")
                return redirect('clientsupportsupportallocationallocationmatrixlist')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != ""]  if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            if AllocationClientSupportUserCity.objects.filter(city_id__in = extra_list).exists() and AllocationUserClientSupportProductType.objects.filter(product_type__in = extra_list1).exists() and AllocationClientSupportProductCategory.objects.filter(product_category_id__in =extra_list2).exists() and AllocationClientSupportProductName.objects.filter(product_name_id__in =extra_list3).exists() and AllocationClientSupportClientType.objects.filter(client_type_id__in =extra_list4).exists() and AllocationClientSupportClientCategory.objects.filter(client_category_id__in = extra_list5).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('clientsupportsupportallocationallocationmatrixlist')
            save_data = AllocationMatrixClientSupport()
            messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
        else:
            allocationsetuid = request.POST['allocationsetuid']
            if AllocationMatrixClientSupport.objects.filter(user_id = request.POST['user'], id =allocationsetuid):
                pass
            else:
                if AllocationMatrixClientSupport.objects.filter(user_id = request.POST['user']):
                    messages.add_message(request, messages.WARNING, "User Already Exists.")
                    return redirect('clientsupportsupportallocationallocationmatrixlist')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != "" ]  if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            if AllocationClientSupportUserCity.objects.filter(~Q(client_support_allocation_id= allocationsetuid), city_id__in = extra_list).exists() and AllocationUserClientSupportProductType.objects.filter(~Q(client_support_allocation_id= allocationsetuid),product_type__in = extra_list1).exists() and AllocationClientSupportProductCategory.objects.filter(~Q(client_support_allocation_id= allocationsetuid),product_category_id__in =extra_list2).exists() and AllocationClientSupportProductName.objects.filter(~Q(client_support_allocation_id= allocationsetuid), product_name_id__in =extra_list3).exists() and AllocationClientSupportClientType.objects.filter(~Q(client_support_allocation_id= allocationsetuid), client_type_id__in =extra_list4).exists() and AllocationClientSupportClientCategory.objects.filter(~Q(client_support_allocation_id= allocationsetuid), client_category_id__in = extra_list5).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('clientsupportsupportallocationallocationmatrixlist')
            save_data = get_object_or_404(AllocationMatrixClientSupport, pk=allocationsetuid)
            messages.add_message(request, messages.SUCCESS, "Record update Successfully.")
        save_data.user_id = request.POST['user']
        
        save_data.save()
        id = save_data.id
        append_city = []
        # Save All Matrix City
        if 'city' in request.POST:
            for data in dict(request.POST)['city']:
                if str(data) != "":
                    try:
                        save_city = AllocationClientSupportUserCity.objects.get(client_support_allocation_id = id, city_id = data)
                        save_city.client_support_allocation_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    except:
                        save_city = AllocationClientSupportUserCity()
                        save_city.client_support_allocation_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationClientSupportUserCity.objects.filter(~Q(city_id__in = append_city) , client_support_allocation_id = id ).delete()
        # Save Product Type
        append_city = []
        if 'product' in request.POST:
            for data in dict(request.POST)['product']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserClientSupportProductType.objects.get(client_support_allocation_id = id, product_type_id = data)
                        save_city.client_support_allocation_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    except:
                        save_city = AllocationUserClientSupportProductType()
                        save_city.client_support_allocation_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserClientSupportProductType.objects.filter(~Q(product_type__in = append_city) , client_support_allocation_id = id).delete()
        
        # Save Product Category
        append_city = []
        if 'product_category' in request.POST:
            for data in dict(request.POST)['product_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationClientSupportProductCategory.objects.get(client_support_allocation_id = id, product_category_id = data)
                        save_city.client_support_allocation_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    except:
                        save_city = AllocationClientSupportProductCategory()
                        save_city.client_support_allocation_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationClientSupportProductCategory.objects.filter(~Q(product_category_id__in = append_city) , client_support_allocation_id = id).delete()
        
        # Save Product Name
        append_city1 = []
        if 'product_name' in request.POST:
            for data in dict(request.POST)['product_name']:
                if str(data) != "":
                    try:
                        save_city = AllocationClientSupportProductName.objects.get(client_support_allocation_id = id, product_name_id = data)
                        save_city.client_support_allocation_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    except:
                        save_city = AllocationClientSupportProductName()
                        save_city.client_support_allocation_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    append_city1.append(data)
            AllocationClientSupportProductName.objects.filter(~Q(product_name_id__in = append_city1) , client_support_allocation_id = id).delete()

        # Client Type 
        append_city = []
        if 'client_type' in request.POST:
            for data in dict(request.POST)['client_type']:
                if str(data) != "":
                    try:
                        save_city = AllocationClientSupportClientType.objects.get(client_support_allocation_id = id, client_type_id = data)
                        save_city.client_support_allocation_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    except:
                        save_city = AllocationClientSupportClientType()
                        save_city.client_support_allocation_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationClientSupportClientType.objects.filter(~Q(client_type_id__in = append_city) , client_support_allocation_id = id).delete()

        # Client Category 
        append_city = []
        if 'client_category' in request.POST:
            for data in dict(request.POST)['client_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationClientSupportClientCategory.objects.get(client_support_allocation_id = id, client_category_id = data)
                        save_city.client_support_allocation_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    except:
                        save_city = AllocationClientSupportClientCategory()
                        save_city.client_support_allocation_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationClientSupportClientCategory.objects.filter(~Q(client_category_id__in = append_city) , client_support_allocation_id = id).delete()

        return redirect('clientsupportsupportallocationallocationmatrixlist')


class CrmAllocationMatrixClientSupportDelete(View):
    def get(self, request, allocationsetuid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationMatrixClientSupport.objects.filter(id = allocationsetuid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('clientsupportsupportallocationallocationmatrixlist')


class CrmAllocationMatrixVendorSupportAllocationList(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/vendor_support_lead_allocation.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AllocationMatrixVendorSupport.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmAddAllocationMatrixVendorSupportAllocation(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/add_vendor_support_allocate_matrix.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, allocationsetuid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_all_mapped_cities = ''
        if allocationsetuid is None:
            data = ''
            allocationsetuid = None
            city = ''
        else:
            data = get_object_or_404(AllocationMatrixVendorSupport, pk=allocationsetuid)
            allocationsetuid = allocationsetuid
            try:
                append_branch_ids = [ data.branch_allocated_id for data in UserMultipleBranch.objects.filter(user_id=data.user.id)] 
                get_all_mapped_cities =[ p.id for p in MapCityBranches.objects.filter(branch_id__in = append_branch_ids)]
            except Exception as e:
                pass
            city = MapCityMultipleWithBranches.objects.filter(city_map__in = get_all_mapped_cities).order_by('-id')
        context = {
            'data': data, 
            'allocationsetuid': allocationsetuid,
            'user_set_up': User.objects.filter(is_active =True, is_superuser=0).order_by('-id'),
            'product_set_up': ManageProductType.objects.filter(is_active =True).order_by('-id'),
            'client_type': ManageClientType.objects.filter(is_active =True).order_by('-id'),
            'client_category': ManageClientCategory.objects.filter(is_active=True).order_by('-id'),
            'product_category': ManageProductCategory.objects.filter(is_active=True).order_by('-id'),
            'product_name': ManageProductName.objects.filter(is_active=True).order_by('-id'),
            'city':   city,
            'get_all_cities': AllocationMatrixVendorSupportUserCity.objects.filter(vendor_support_id= data.id).order_by('-id') if data != "" else "",
            'get_product_type': AllocationMatrixVendorSupportProductType.objects.filter(vendor_support_id= data.id).order_by('-id') if data != "" else "",
            'get_product_category': AllocationMatrixVendorSupportProductCategory.objects.filter(vendor_support_id= data.id).order_by('-id') if data != "" else "",
            'get_product_name': AllocationMatrixVendorSupportProductName.objects.filter(vendor_support_id= data.id).order_by('-id') if data != "" else "",
            'get_client_type': AllocationMatrixVendorSupportClientType.objects.filter(vendor_support_id= data.id).order_by('-id') if data != "" else "",
            'get_client_category': AllocationMatrixVendorSupportClientCategory.objects.filter(vendor_support_id= data.id).order_by('-id') if data != "" else "",
        }
        return render(request, self.template, context)

    def post(self, request, allocationsetuid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['allocationsetuid'] is None or request.POST['allocationsetuid'] == "None":
            if AllocationMatrixVendorSupport.objects.filter(user_id = request.POST['user']):
                messages.add_message(request, messages.WARNING, "User Already Exists.")
                return redirect('crmleadallocationallocationmatrixlist')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != ""]  if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            if AllocationMatrixVendorSupportUserCity.objects.filter(city_id__in = extra_list).exists() and AllocationMatrixVendorSupportUserCity.objects.filter(product_type_id__in = extra_list1).exists() and AllocationMatrixVendorSupportProductCategory.objects.filter(product_category_id__in =extra_list2).exists() and AllocationMatrixVendorSupportProductName.objects.filter(product_name_id__in =extra_list3).exists() and AllocationMatrixVendorSupportClientType.objects.filter(client_type_id__in =extra_list4).exists() and AllocationMatrixVendorSupportClientCategory.objects.filter(client_category_id__in = extra_list5).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('crmleadallocationallocationmatrixlist')
            save_data = AllocationMatrixVendorSupport()
            messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
        else:
            allocationsetuid = request.POST['allocationsetuid']
            if AllocationMatrixVendorSupport.objects.filter(user_id = request.POST['user'], id =allocationsetuid):
                pass
            else:
                if AllocationMatrixVendorSupport.objects.filter(user_id = request.POST['user']):
                    messages.add_message(request, messages.WARNING, "User Already Exists.")
                    return redirect('crmleadallocationallocationmatrixlist')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != "" ]  if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            if AllocationMatrixVendorSupportUserCity.objects.filter(~Q(vendor_support_id= allocationsetuid), city_id__in = extra_list).exists() and AllocationMatrixVendorSupportUserCity.objects.filter(~Q(vendor_support_id= allocationsetuid),product_type_id__in = extra_list1).exists() and AllocationMatrixVendorSupportProductCategory.objects.filter(~Q(vendor_support_id= allocationsetuid),product_category_id__in =extra_list2).exists() and AllocationMatrixVendorSupportProductName.objects.filter(~Q(vendor_support_id= allocationsetuid), product_name_id__in =extra_list3).exists() and AllocationMatrixVendorSupportClientType.objects.filter(~Q(vendor_support_id= allocationsetuid), client_type_id__in =extra_list4).exists() and AllocationMatrixVendorSupportClientCategory.objects.filter(~Q(vendor_support_id= allocationsetuid), client_category_id__in = extra_list5).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('crmleadallocationallocationmatrixlist')
            save_data = get_object_or_404(AllocationMatrixVendorSupport, pk=allocationsetuid)
            messages.add_message(request, messages.SUCCESS, "Record update Successfully.")
        save_data.user_id = request.POST['user']
        save_data.save()
        id = save_data.id
        append_city = []
        # Save All Matrix City
        if 'city' in request.POST:
            for data in dict(request.POST)['city']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixVendorSupportUserCity.objects.get(vendor_support_id = id, city_id = data)
                        save_city.vendor_support_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    except AllocationMatrixVendorSupportUserCity.DoesNotExist:
                        save_city = AllocationMatrixVendorSupportUserCity()
                        save_city.vendor_support_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixVendorSupportUserCity.objects.filter(~Q(city_id__in = append_city) , vendor_support_id = id ).delete()
        # Save Product Type
        append_city = []
        if 'product' in request.POST:
            for data in dict(request.POST)['product']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixVendorSupportProductType.objects.get(vendor_support_id = id, product_type_id = data)
                        save_city.vendor_support_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    except AllocationMatrixVendorSupportProductType.DoesNotExist:
                        save_city = AllocationMatrixVendorSupportProductType()
                        save_city.vendor_support_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixVendorSupportProductType.objects.filter(~Q(product_type_id__in = append_city) , vendor_support_id = id).delete()
        
        # Save Product Category
        append_city = []
        if 'product_category' in request.POST:
            for data in dict(request.POST)['product_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixVendorSupportProductCategory.objects.get(vendor_support_id = id, product_category_id = data)
                        save_city.vendor_support_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    except AllocationMatrixVendorSupportProductCategory.DoesNotExist:
                        save_city = AllocationMatrixVendorSupportProductCategory()
                        save_city.vendor_support_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixVendorSupportProductCategory.objects.filter(~Q(product_category_id__in = append_city) , vendor_support_id = id).delete()
        
        # Save Product Name
        append_city1 = []
        if 'product_name' in request.POST:
            for data in dict(request.POST)['product_name']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixVendorSupportProductName.objects.get(vendor_support_id = id, product_name_id = data)
                        save_city.vendor_support_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    except AllocationMatrixVendorSupportProductName.DoesNotExist:
                        save_city = AllocationMatrixVendorSupportProductName()
                        save_city.vendor_support_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    append_city1.append(data)
            AllocationMatrixVendorSupportProductName.objects.filter(~Q(product_name_id__in = append_city1) , vendor_support_id = id).delete()

        # Client Type 
        append_city = []
        if 'client_type' in request.POST:
            for data in dict(request.POST)['client_type']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixVendorSupportClientType.objects.get(vendor_support_id = id, client_type_id = data)
                        save_city.vendor_support_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    except AllocationMatrixVendorSupportClientType.DoesNotExist:
                        save_city = AllocationMatrixVendorSupportClientType()
                        save_city.vendor_support_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixVendorSupportClientType.objects.filter(~Q(client_type_id__in = append_city) , vendor_support_id = id).delete()

        # Client Category 
        append_city = []
        if 'client_category' in request.POST:
            for data in dict(request.POST)['client_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixVendorSupportClientCategory.objects.get(vendor_support_id = id, client_category_id = data)
                        save_city.vendor_support_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    except AllocationMatrixVendorSupportClientCategory.DoesNotExist:
                        save_city = AllocationMatrixVendorSupportClientCategory()
                        save_city.vendor_support_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixVendorSupportClientCategory.objects.filter(~Q(client_category_id__in = append_city) , vendor_support_id = id).delete()
        return redirect('vendorsupportallocationallocationmatrixlist')


class CrmAllocationMatrixVendorSupportDelete(View):
    def get(self, request, allocationsetuid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationMatrixVendorSupport.objects.filter(id = allocationsetuid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('vendorsupportallocationallocationmatrixlist')


# END
class CrmGetUserDetails(View):
    def post(self, request, *args, **kwargs):
        ServicesHtml = ''
        map_cities = ''
        append_branch_ids = []
        if request.is_ajax:
            try:
                get_user = User.objects.get(id=request.POST['id'])
                branches = UserMultipleBranch.objects.filter(user_id=request.POST['id'])
                if branches:
                    for bran in branches:
                        append_branch_ids.append(bran.branch_allocated_id)
                        ServicesHtml += '<option value="' + \
                                    str(bran.branch_allocated.id) + '">' + bran.branch_allocated.branch_id + '</option>'
                try:
                    get_all_mapped_cities =[ p.id for p in MapCityBranches.objects.filter(branch_id__in = append_branch_ids)]
                    for brnch_cites in MapCityMultipleWithBranches.objects.filter(city_map_id__in = get_all_mapped_cities):
                        map_cities += '<option value="' + \
                                    str(brnch_cites.city.id) + '">' + brnch_cites.city.name + '</option>'
                except Exception as e:
                    pass
                try:
                    lead_client_type = AllocationMatrixdLeadAllocation.objects.get(user_id = request.POST['id'])
                    client_prodcut = lead_client_type.product.product_name
                    client_type = lead_client_type.client_type.client_type
                    client_category = lead_client_type.client_category.client_category
                except Exception as e:
                    client_type = ''
                    client_prodcut = ''
                    client_category = ''
                context = {
                    'user_res': get_user.responsibilities.responsibilities,
                    'user_department':get_user.department.department,
                    'user_deg':get_user.designation.designation,
                    'branches_name': ServicesHtml,
                    'client_type':client_type,
                    'client_prodcut':client_prodcut,
                    'client_category':client_category, 
                    'map_cities':map_cities
                }
                return JsonResponse(context)
            except:
                return JsonResponse({'data': ''})


class CrmCheckUserExists(View):

    def get(self, request):
        if str(request.GET["id"]) == "":
            try:
                User.objects.get(email=request.GET['email_id'])
                response = json.dumps("Email Already Already Exists.")
                return HttpResponse(response)
            except Exception as e:
                response = json.dumps(True)
                return HttpResponse(response)
        else:
            check = User.objects.filter(email=request.GET['email_id'], id=request.GET['id'])
            if check.exists():
                response = json.dumps(True)
                return HttpResponse(response)
            else:
                # email exist check
                check = User.objects.filter(email=request.GET['email'])
                if check.exists():
                    response = json.dumps("Email Already Already Exists.")
                    return HttpResponse(response)
                else:
                    response = json.dumps(True)
                    return HttpResponse(response)


class CrmCheckPhonenumberxists(View):

    def get(self, request):
        if str(request.GET["id"]) == "":
            try:
                User.objects.get(mobile_no=request.GET['mobile_no'])
                response = json.dumps("Mobile Number Already Exists.")
                return HttpResponse(response)
            except Exception as e:
                response = json.dumps(True)
                return HttpResponse(response)
        else:
            check = User.objects.filter(mobile_no=request.GET['mobile_no'], id=request.GET['id'])
            if check.exists():
                response = json.dumps(True)
                return HttpResponse(response)
            else:
                # email exist check
                check = User.objects.filter(mobile_no=request.GET['mobile_no'])
                if check.exists():
                    response = json.dumps("Mobile  Number Already Exists.")
                    return HttpResponse(response)
                else:
                    response = json.dumps(True)
                    return HttpResponse(response)
            

# -------------------- Temaplate Set UP(Client Category) ---------------------------
class CrmTemapleSetUpClientTypeList(View):
    template = 'admin_template/crm_management/template_set_up/template_client_type_set_up_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = TemplateSetupClientType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddTemaplateClientTypeSetUp(request):

    if request.method == 'POST':        
        form = CrmtemplateclienttypeForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            form.save()
            return redirect('crmtemapltesetupclienttypelist')
        else:
            messages.add_message(request, messages.WARNING,'Company with this Company id already exists!!')
    else:
        form = CrmtemplateclienttypeForm()
    return render(request, 'admin_template/crm_management/template_set_up/add_client_type_template_set_up.html',{'form':form})


def CrmEditTemaplateClientTypeSetUp(request, temapalte_id):
    company = get_object_or_404(TemplateSetupClientType, pk=temapalte_id)
    if request.method == "POST":
        form = CrmtemplateclienttypeForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('crmtemapltesetupclienttypelist')
    else:
        form = CrmtemplateclienttypeForm(instance=company)
    return render(request, 'admin_template/crm_management/template_set_up/edit_client_type_template_set_up.html', {'form': form})


class CrmEditTemaplateClientTypeSetUpDelete(View):
    def get(self, request, temapalte_id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TemplateSetupClientType.objects.filter(id = temapalte_id).delete()
        messages.add_message(request, messages.SUCCESS, "Company deleted Successfully.")
        return redirect('crmtemapltesetupclienttypelist')


# -------------------- Temaplate Set UP(Client Category) ---------------------------
class CrmTemapleSetUpClientCategoryList(View):
    template = 'admin_template/crm_management/template_set_up/template_client_category_set_up_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = TemplateSetupClientCategory.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddTemaplateClientCategorySetUp(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmtemplateclientcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmtemapltesetupclientcategorylist')
        else:
            messages.add_message(request, messages.WARNING,'Company with this Company id already exists!!')
    else:
        form = CrmtemplateclientcategoryForm()
    return render(request, 'admin_template/crm_management/template_set_up/add_client_category_template_set_up.html',{'form':form})


def CrmEditTemaplateClientCategorySetUp(request, temapalte_id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(TemplateSetupClientCategory, pk=temapalte_id)
    if request.method == "POST":
        form = CrmtemplateclientcategoryForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmtemapltesetupclientcategorylist')
    else:
        form = CrmtemplateclientcategoryForm(instance=company)
    return render(request, 'admin_template/crm_management/template_set_up/edit_client_category_template_set_up.html', {'form': form})


class CrmEditTemaplateClientCategorySetUpDelete(View):
    def get(self, request, temapalte_id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TemplateSetupClientCategory.objects.filter(id = temapalte_id).delete()
        messages.add_message(request, messages.SUCCESS, "Company deleted Successfully.")
        return redirect('crmtemapltesetupclientcategorylist')




########################################
class CrmCustomizeTemplateList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/customized_template_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = CustomizeTemplate.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmCustomizeTemplateAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/customized_template_add.html'
    def get(self,request):
        form = CrmCustomizeTemplateForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):

        form = CrmCustomizeTemplateForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ') 
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Not Added')
        return redirect('customizetemplatelist')


def CrmCustomizeTemplateEdit(request, id):
    manageproduct = get_object_or_404(CustomizeTemplate, pk=id)
    if request.method == "POST":
        form = CrmCustomizeTemplateForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ') 
            return redirect('customizetemplatelist')
        else:
            messages.add_message(request, messages.WARNING, 'Not Added')
            return redirect('customizetemplatelist')
    else:
        form = CrmCustomizeTemplateForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/customized_template_add.html', {'form': form})


class CrmCustomizeTemplateDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = CustomizeTemplate.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('customizetemplatelist')


# ----------------------------- Currency Set UP -----------------------------------------
class CrmTypeofCurrencyList(View):
    template = 'admin_template/crm_management/currency_set_up/type_of_currency_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = TypeofCurrency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddTypeofCurrency(request):
    if request.method == 'POST':        
        form = TypeofcurrencyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmtypeofcurrencylist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!') 
            return redirect('crmtypeofcurrencylist')
    else:
        form = TypeofcurrencyForm()
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_type_of_currency.html',{'form':form})


def CrmEditTypeofCurrency(request, id):
    company = get_object_or_404(TypeofCurrency, pk=id)
    if request.method == "POST":
        form = TypeofcurrencyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!')
            return redirect('crmtypeofcurrencylist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!') 
            return redirect('crmtypeofcurrencylist')
    else:
        form = TypeofcurrencyForm(instance=company)
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_type_of_currency.html', {'form': form})


class CrmTypeofCurrencyDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TypeofCurrency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crmtypeofcurrencylist')


# --------------------Purpose of currency ================================
class CrmPurposeofCurrencyList(View):
    template = 'admin_template/crm_management/currency_set_up/purpose_of_currency_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = PurposeofCurrency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddPurposeofCurrency(request):
    if request.method == 'POST':        
        form = PurposeofcurrencyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmpurposeofcurrencylist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!')
            return redirect('crmpurposeofcurrencylist')
    else:
        form = PurposeofcurrencyForm()
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_purpose_of_currency.html' ,{'form':form})


def CrmEditPurposeofCurrency(request, id):
    company = get_object_or_404(PurposeofCurrency, pk=id)
    if request.method == "POST":
        form = PurposeofcurrencyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!')
            return redirect('crmpurposeofcurrencylist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!')
            return redirect('crmpurposeofcurrencylist')
    else:
        form = PurposeofcurrencyForm(instance=company)
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_purpose_of_currency.html', {'form': form})


class CrmPurposeofCurrencyDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PurposeofCurrency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crmpurposeofcurrencylist')


# =============================== Currency Set Up =============================
class CrmCurrencySetUpList(View):
    template = 'admin_template/crm_management/currency_set_up/currency_set_up_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = CurrencySetup.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddCurrencySetUp(request):
    if request.method == 'POST':
        form = CrmCurrencySetUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmcurrecncysetuplist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!') 
            return redirect('crmcurrecncysetuplist')
    else:
        form = CrmCurrencySetUpForm()
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_currency_set_up.html' ,{'form':form})


def CrmEditCurrencySetUp(request, id):
    company = get_object_or_404(CurrencySetup, pk=id)
    if request.method == "POST":
        form = CrmCurrencySetUpForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crmcurrecncysetuplist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!') 
            return redirect('crmcurrecncysetuplist')
    else:
        form = CrmCurrencySetUpForm(instance=company)
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_currency_set_up.html', {'form': form})


class CrmCurrencySetUpDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = CurrencySetup.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crmcurrecncysetuplist')




# ----------------------------- Currency Rate -----------------------------------------
class CrmCurrencyRateList(View):
    template = 'admin_template/crm_management/currency_set_up/currency_rate_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = CurrencyRate.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddCurrencyRate(request):

    if request.method == 'POST':        
        form = CurrencyRateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmcurrencyratelist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!') 
            return redirect('crmcurrencyratelist')
    else:
        form = CurrencyRateForm()
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_currency_rate.html',{'form':form})


def CrmEditCurrencyRate(request, id):
    company = get_object_or_404(CurrencyRate, pk=id)
    if request.method == "POST":
        form = CurrencyRateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!')
            return redirect('crmcurrencyratelist')
        else:
            messages.add_message(request, messages.WARNING,'Already Exists!!') 
            return redirect('crmcurrencyratelist')
    else:
        form = CurrencyRateForm(instance=company)
    return render(request, 'admin_template/crm_management/currency_set_up/add_edit_currency_rate.html', {'form': form})


class CrmCurrencyRateDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = CurrencyRate.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crmcurrencyratelist')

#
# ============================  Bulk SMS and Mail Setup  ================================
class CrmBulkSmsList(View):
    template = 'admin_template/crm_management/bulk_mail_set_up/crm_bulk_msg_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = Bulksms.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmMailSmsList(View):
    template = 'admin_template/crm_management/bulk_mail_set_up/crm_mail_msg_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = Mailsms.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


# ==================================== Notification Set Up ====================
class CrmEscalationMatrixDefineLevelsList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/define_level_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = EscalationMatrixDefineLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddEscalationMatrixDefineLevels(request):
    if request.method == 'POST':        
        form = EscalationMatrixDefineLevelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crmescalationmatrixdefinelevelslist')
        else:
            messages.add_message(request, messages.WARNING,'Already Added') 
            return redirect('crmescalationmatrixdefinelevelslist')
    else:
        form = EscalationMatrixDefineLevelForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/add_edit_define_level.html' ,{'form':form})


def CrmEditEscalationMatrixDefineLevels(request, id):
    company = get_object_or_404(EscalationMatrixDefineLevel, pk=id)
    if request.method == "POST":
        form = EscalationMatrixDefineLevelForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crmescalationmatrixdefinelevelslist')
        else:
            messages.add_message(request, messages.WARNING,'Already Added') 
            return redirect('crmescalationmatrixdefinelevelslist')
    else:
        form = EscalationMatrixDefineLevelForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/add_edit_define_level.html', {'form': form})


class CrmEscalationMatrixDefineLevelsDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = EscalationMatrixDefineLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crmescalationmatrixdefinelevelslist')


class CrmEscalationMatrixDefineTurnAroundTimeList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/define_tot_list.html'
    pagesize = 10
    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = EscalationMatrixDefineTurnAroundTime.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddEscalationMatrixDefineTurnAroundTime(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':

        if EscalationMatrixDefineTurnAroundTime.objects.filter(user_id = request.POST['user']):
            messages.add_message(request, messages.WARNING, "User Already Exists.")
            return redirect('crm_escalation_matrix_tot_list')
        extra_list =  [data for data in dict(request.POST)['escalation_level'] if data != ""] if 'escalation_level' in request.POST else []
        extra_list1 = [data for data in dict(request.POST)['escalation_to'] if data != ""] if 'escalation_to' in request.POST else []
        extra_list2 = [data for data in dict(request.POST)['process_name'] if data != ""] if 'EscalationMatrixDefineTurnAroundTimeEscalationName' in request.POST else []
        if EscalationMatrixDefineTurnAroundTimeEscalationName.objects.filter(escalation_name_id__in = extra_list).exists() and EscalationMatrixDefineTurnAroundTimeUser.objects.filter(escalation_user_id__in = extra_list1).exists() and EscalationMatrixDefineTurnAroundTimeProcessName .objects.filter(process_name_level_id__in = extra_list2).exists():
            messages.add_message(request, messages.WARNING, "Already Exists.")
            return redirect('crm_escalation_matrix_tot_list')
        form = CrmNotificationEscalationMatrixDefineTurnAroundTimeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            if 'escalation_level' in request.POST:
                for level in dict(request.POST)['escalation_level']:
                    data_save = EscalationMatrixDefineTurnAroundTimeEscalationName()
                    data_save.turn_around_id = data.id
                    data_save.escalation_name_id = level
                    data_save.save()
            if 'escalation_to' in request.POST:
                for user_id in dict(request.POST)['escalation_to']:
                    data_save1 = EscalationMatrixDefineTurnAroundTimeUser()
                    data_save1.turn_around_id = data.id
                    data_save1.escalation_user_id = user_id
                    data_save1.save()
            if 'process_name' in request.POST:
                for user_id in dict(request.POST)['process_name']:
                    data_save1 = EscalationMatrixDefineTurnAroundTimeProcessName ()
                    data_save1.turn_around_id = data.id
                    data_save1.process_name_level_id = user_id
                    data_save1.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_escalation_matrix_tot_list')
    else:
        form = CrmNotificationEscalationMatrixDefineTurnAroundTimeForm()
    context = {
        'form':form,
        'escalation_level':EscalationMatrixDefineLevel.objects.filter(is_active = True),
        'user_list': User.objects.filter(is_superuser = 0, manual_create_admin = 1, is_active = True),
        'process_name': ApprovalMatrixDefineProcesLevel.objects.filter(is_active = True)
    }
    return render(request, 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/add_edit_define_tot.html', context)


def CrmEditEscalationMatrixDefineTurnAroundTime(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(EscalationMatrixDefineTurnAroundTime, pk=id)
    if request.method == "POST":
        if EscalationMatrixDefineTurnAroundTime.objects.filter(user_id = request.POST['user'], id = id).exists():
            pass
        else:
            if EscalationMatrixDefineTurnAroundTime.objects.filter(user_id = request.POST['user']).exists():
                messages.add_message(request, messages.WARNING, "User Already Exists.")
                return redirect('crm_escalation_matrix_tot_list')
        extra_list =  [data for data in dict(request.POST)['escalation_level'] if data != ""] if 'escalation_level' in request.POST else []
        extra_list1 = [data for data in dict(request.POST)['escalation_to'] if data != ""] if 'escalation_to' in request.POST else []
        extra_list2 = [data for data in dict(request.POST)['process_name'] if data != ""] if 'process_name' in request.POST else []
        if EscalationMatrixDefineTurnAroundTimeEscalationName.objects.filter(~Q(turn_around_id = id), escalation_name_id__in = extra_list).exists() and EscalationMatrixDefineTurnAroundTimeUser.objects.filter(~Q(turn_around_id = id), escalation_user_id__in = extra_list1).exists() and EscalationMatrixDefineTurnAroundTimeProcessName .objects.filter(~Q(turn_around_id = id), process_name_level_id__in = extra_list2).exists():
            messages.add_message(request, messages.WARNING, "Already Exists.")
            return redirect('crm_escalation_matrix_tot_list')
        form = CrmNotificationEscalationMatrixDefineTurnAroundTimeForm(request.POST, instance=company)
        if form.is_valid():
            data = form.save()
            EscalationMatrixDefineTurnAroundTimeEscalationName.objects.filter(turn_around_id = data.id).delete()
            EscalationMatrixDefineTurnAroundTimeUser.objects.filter(turn_around_id = data.id).delete()
            EscalationMatrixDefineTurnAroundTimeProcessName .objects.filter(turn_around_id = data.id).delete()
            if 'escalation_level' in request.POST:
                for level in dict(request.POST)['escalation_level']:
                    data_save = EscalationMatrixDefineTurnAroundTimeEscalationName()
                    data_save.turn_around_id = data.id
                    data_save.escalation_name_id = level
                    data_save.save()
            if 'escalation_to' in request.POST:
                for user_id in dict(request.POST)['escalation_to']:
                    data_save1 = EscalationMatrixDefineTurnAroundTimeUser()
                    data_save1.turn_around_id = data.id
                    data_save1.escalation_user_id = user_id
                    data_save1.save()
            if 'process_name' in request.POST:
                for user_id in dict(request.POST)['process_name']:
                    data_save1 = EscalationMatrixDefineTurnAroundTimeProcessName ()
                    data_save1.turn_around_id = data.id
                    data_save1.process_name_level_id = user_id
                    data_save1.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_escalation_matrix_tot_list')
    else:
        form = CrmNotificationEscalationMatrixDefineTurnAroundTimeForm(instance=company)
    
    context = {
        'form':form,
        'company':company,
        'escalation_level':EscalationMatrixDefineLevel.objects.filter(is_active = True),
        'user_list': User.objects.filter(is_superuser = 0, manual_create_admin = 1, is_active = True),
        'process_name':ApprovalMatrixDefineProcesLevel.objects.filter(is_active = True)
    }
    return render(request, 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/add_edit_define_tot.html', context)


class CrmEscalationMatrixDefineTurnAroundTimeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = EscalationMatrixDefineTurnAroundTime.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_escalation_matrix_tot_list')


# ================================ Set Up SMS Motification ========================
class CrmSmsNotificationSubjectList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notification/subject_list.html'
    pagesize = 10


    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = NotificationSubject.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationSubject(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmNotificationNotificationSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_subject_list')
        else:
            messages.add_message(request, messages.WARNING, 'Data Already Exists.') 
            return redirect('crm_define_notification_subject_list')
    else:
        form = CrmNotificationNotificationSubjectForm()
        return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification/add_edit_subject.html' ,{'form':form})


def CrmEditSmsNotificationSubject(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    company = get_object_or_404(NotificationSubject, pk=id)
    if request.method == "POST":
        form = CrmNotificationNotificationSubjectForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_subject_list')
        else:
            messages.add_message(request, messages.WARNING,'Not added') 
            return redirect('crm_define_notification_subject_list')

    else:
        form = CrmNotificationNotificationSubjectForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification/add_edit_subject.html', {'form': form})


class CrmSmsNotificationSubjectDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = NotificationSubject.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_subject_list')



# =============Notification Action
class DefineSmsNotificationActionList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_notfication_type/action_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = DefineSmsNotificationAction.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {'responselistquery': report_paginate}
        return render(request, self.template, context)


def DefineSmsNotificationActionAdd(request):
    if request.method == 'POST':
        form =  DefineSmsNotificationActionFrom(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()

            messages.add_message(request, messages.SUCCESS,'Successfully added!!')
            return redirect('definesmsnotificationactionlist')
        else:
            messages.add_message(request, messages.WARNING,  'Already exists!!')
            return redirect('definesmsnotificationactionlist')
    else:
        form =  DefineSmsNotificationActionFrom()
        return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/action_edit.html' ,{'form':form})


def DefineSmsNotificationActionEdit(request, id):
    company = get_object_or_404( DefineSmsNotificationAction, pk=id)
    if request.method == "POST":
        form =  DefineSmsNotificationActionFrom(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!')
            return redirect('definesmsnotificationactionlist')
        else:
            messages.add_message(request, messages.WARNING,  'Already exists!!')
            return redirect('definesmsnotificationactionlist')
    else:
        form =  DefineSmsNotificationActionFrom(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/action_edit.html', {'form': form})


class  DefineSmsNotificationActionDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefineSmsNotificationAction.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('definesmsnotificationactionlist') 


# =============Define Notification Type
class CrmSmsNotificationTypeList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_notfication_type/notification_type_list.html'
    pagesize = 10
    def get(self,request):
        responselistquery = SmsNotificationType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationType(request):
    if request.method == 'POST':        
        form = CrmSmsNotificationTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_type_list')
    else:
        form = CrmSmsNotificationTypeForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/add_edit_notification_type.html' ,{'form':form})


def CrmEditSmsNotificationType(request, id):
    company = get_object_or_404(SmsNotificationType, pk=id)
    if request.method == "POST":
        form = CrmSmsNotificationTypeForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_type_list')
    else:
        form = CrmSmsNotificationTypeForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/add_edit_notification_type.html', {'form': form})


class CrmSmsNotificationTypeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = SmsNotificationType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_type_list')


# =============Define Notification Frequency
class CrmSmsNotificationFrequencyList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notification_frequency/frequence_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = SmsNotificationFrequency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationFrequency(request):
    if request.method == 'POST':   
        form = CrmSmsNotificationFrequencyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_frequency_list')
        else:
            messages.add_message(request, messages.ERROR,'Something went wrong.') 
            return redirect('crm_define_notification_frequency_list')
    else:
        form = CrmSmsNotificationFrequencyForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification_frequency/add_edit_fre.html' ,{'form':form})


def CrmEditSmsNotificationFrequency(request, id):
    company = get_object_or_404(SmsNotificationFrequency, pk=id)
    if request.method == "POST":
        form = CrmSmsNotificationFrequencyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_frequency_list')
        else:
            messages.add_message(request, messages.ERROR,'Something went wrong.') 
            return redirect('crm_define_notification_frequency_list')
    else:
        form = CrmSmsNotificationFrequencyForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification_frequency/add_edit_fre.html', {'form': form})


class CrmSmsNotificationFrequencyDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = SmsNotificationFrequency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_frequency_list')


# =============  Define Type Of Message
class CrmSmsNotificationTypeofMessageList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notifica_type_of_message/type_of_message_list.html'
    pagesize = 10
    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = SmsImportanceofNotification.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationTypeofMessage(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmSmsDefineTypeofMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_type_message_list')
    else:
        form = CrmSmsDefineTypeofMessageForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notifica_type_of_message/add_edit_type_of_message.html' ,{'form':form})


def CrmEditSmsNotificationTypeofMessage(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(SmsImportanceofNotification, pk=id)
    if request.method == "POST":
        form = CrmSmsDefineTypeofMessageForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_type_message_list')
    else:
        form = CrmSmsDefineTypeofMessageForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notifica_type_of_message/add_edit_type_of_message.html', {'form': form})


class CrmSmsNotificationTypeofMessageDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = SmsImportanceofNotification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_type_message_list')


# *********************  Define Import Of Message **************
class CrmSmsTargetAudienceMessageList(View):
    template = 'admin_template/crm_management/notification_set_up/target_audience/import_of_message_list.html'
    pagesize = 10

    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = SmsDefineTargetAudience.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmSmsTargetAudienceMessageAddView(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmSmsDefineImportofMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_import_message_list')
    else:
        form = CrmSmsDefineImportofMessageForm()
    return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html' ,{'form':form})


def CrmSmsTargetAudienceMessageEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(SmsDefineTargetAudience, pk=id)
    if request.method == "POST":
        form = CrmSmsDefineImportofMessageForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_import_message_list')
    else:
        form = CrmSmsDefineImportofMessageForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html', {'form': form})


class CrmSmsTargetAudienceMessageeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = SmsDefineTargetAudience.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_import_message_list')



# *********************  Define Template For Notification **************
class CrmDefineTemplateForNotificationList(View):
    template = 'admin_template/crm_management/notification_set_up/template_for_notification/list.html'
    pagesize = 10

    def get(self,request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = DefineTemplateForNotification.objects.filter(notification_type_id = id).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate,
            'id': id

        }
        return render(request, self.template, context)


def CrmDefineTemplateForNotificationAddView(request, id = None):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    if request.method == 'POST':    
        form = CrmDefineTemplateForNotificationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            data.notification_type_id = id
            data.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_template_for_notification_list', id = id)
        else:
            messages.add_message(request, messages.ERROR,'Already added') 
            return redirect('crm_define_template_for_notification_list', id = id)
    else:
        form = CrmDefineTemplateForNotificationForm()
        context = {
            'form':form, 
            'id':id
        }
        return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html', context)


def CrmDefineTemplateForNotificationEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(DefineTemplateForNotification, pk=id)
    if request.method == "POST":
        form = CrmDefineTemplateForNotificationForm(request.POST, instance=company)
        if form.is_valid():
            data = form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_template_for_notification_list', id = company.notification_type_id )
        else:
            messages.add_message(request, messages.ERROR,'Already added') 
            return redirect('crm_define_template_for_notification_list', id = company.notification_type_id)
    else:
        form = CrmDefineTemplateForNotificationForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html', {'form': form})


class CrmDefineTemplateForNotificationDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefineTemplateForNotification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_template_for_notification_list')


# =============  Define Group Of Message ======================
class CrmSmsGroupofMessageList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notifica_group_of_message/group_of_message_list.html'
    pagesize = 10

    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = SmsGroup.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddGroupofMessage(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmSmsDefineGroupofMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_group_message_list')
    else:
        form = CrmSmsDefineGroupofMessageForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notifica_group_of_message/add_edit_group_of_message.html' ,{'form':form})


def CrmEditGroupofMessage(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(SmsGroup, pk=id)
    if request.method == "POST":
        form = CrmSmsDefineGroupofMessageForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_group_message_list')
    else:
        form = CrmSmsDefineGroupofMessageForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notifica_group_of_message/add_edit_group_of_message.html', {'form': form})


class CrmSmsSmsGroupeofMessageeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = SmsGroup.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_group_message_list')


# ================================ Set Up SMS Motification ========================
class CrmSmsNotificationSubjectList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notification/subject_list.html'
    pagesize = 10


    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = NotificationSubject.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationSubject(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmNotificationNotificationSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_define_notification_subject_list')
        else:
            messages.add_message(request, messages.WARNING, 'Data Already Exists.') 
            return redirect('crm_define_notification_subject_list')
    else:
        form = CrmNotificationNotificationSubjectForm()
        return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification/add_edit_subject.html' ,{'form':form})


def CrmEditSmsNotificationSubject(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    company = get_object_or_404(NotificationSubject, pk=id)
    if request.method == "POST":
        form = CrmNotificationNotificationSubjectForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_define_notification_subject_list')
        else:
            messages.add_message(request, messages.WARNING, 'Data Already Exists.') 
            return redirect('crm_define_notification_subject_list')
    else:
        form = CrmNotificationNotificationSubjectForm(instance=company)
        return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification/add_edit_subject.html', {'form': form})


class CrmSmsNotificationSubjectDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = NotificationSubject.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_subject_list')


# =============Define Notification Type
class CrmSmsNotificationTypeList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_notfication_type/notification_type_list.html'
    pagesize = 10
    def get(self,request):
        responselistquery = NotificationType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationType(request):
    if request.method == 'POST':        
        form = CrmSmsNotificationTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING,'Already Exists.') 
        return redirect('crm_define_notification_type_list')
    else:
        form = CrmSmsNotificationTypeForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/add_edit_notification_type.html' ,{'form':form})


def CrmEditSmsNotificationType(request, id):
    company = get_object_or_404(NotificationType, pk=id)
    if request.method == "POST":
        form = CrmSmsNotificationTypeForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists') 
        return redirect('crm_define_notification_type_list')
    else:
        form = CrmSmsNotificationTypeForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/add_edit_notification_type.html', {'form': form})


class CrmSmsNotificationTypeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = NotificationType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_type_list')


# =============Define Notification Frequency
class CrmSmsNotificationFrequencyList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notification_frequency/frequence_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = NotificationFrequency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationFrequency(request):
    if request.method == 'POST':        
        form = CrmSmsNotificationFrequencyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists') 
        return redirect('crm_define_notification_frequency_list')
    else:
        form = CrmSmsNotificationFrequencyForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification_frequency/add_edit_fre.html' ,{'form':form})


def CrmEditSmsNotificationFrequency(request, id):
    company = get_object_or_404(NotificationFrequency, pk=id)
    if request.method == "POST":
        form = CrmSmsNotificationFrequencyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists.') 
        return redirect('crm_define_notification_frequency_list')
    else:
        form = CrmSmsNotificationFrequencyForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notification_frequency/add_edit_fre.html', {'form': form})


class CrmSmsNotificationFrequencyDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = NotificationFrequency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_frequency_list')


# =============  Define Type Of Message
class CrmSmsNotificationTypeofMessageList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_sms_notifica_type_of_message/type_of_message_list.html'
    pagesize = 10
    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = ImportanceofNotification.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddSmsNotificationTypeofMessage(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmSmsDefineTypeofMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists.')
        return redirect('crm_define_notification_type_message_list')
    else:
        form = CrmSmsDefineTypeofMessageForm()
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notifica_type_of_message/add_edit_type_of_message.html' ,{'form':form})


def CrmEditSmsNotificationTypeofMessage(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(ImportanceofNotification, pk=id)
    if request.method == "POST":
        form = CrmSmsDefineTypeofMessageForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists.') 
        return redirect('crm_define_notification_type_message_list')
    else:
        form = CrmSmsDefineTypeofMessageForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_sms_notifica_type_of_message/add_edit_type_of_message.html', {'form': form})


class CrmSmsNotificationTypeofMessageDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ImportanceofNotification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_type_message_list')


# *********************  Define Import Of Message **************
class CrmSmsTargetAudienceMessageList(View):
    template = 'admin_template/crm_management/notification_set_up/target_audience/import_of_message_list.html'
    pagesize = 10

    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = TargetAudience.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmSmsTargetAudienceMessageAddView(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmSmsDefineImportofMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists') 
        return redirect('crm_define_notification_import_message_list')
    else:
        form = CrmSmsDefineImportofMessageForm()
    return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html' ,{'form':form})


def CrmSmsTargetAudienceMessageEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(TargetAudience, pk=id)
    if request.method == "POST":
        form = CrmSmsDefineImportofMessageForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists.')
        return redirect('crm_define_notification_import_message_list')
    else:
        form = CrmSmsDefineImportofMessageForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html', {'form': form})


class CrmSmsTargetAudienceMessageeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TargetAudience.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_notification_import_message_list')


# *********************  Define Template For Notification **************
class CrmDefineTemplateForNotificationList(View):
    template = 'admin_template/crm_management/notification_set_up/template_for_notification/list.html'
    pagesize = 10

    def get(self,request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = TemplateForNotification.objects.filter(notification_type_id = id).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate,
            'id': id
        }
        return render(request, self.template, context)


def CrmDefineTemplateForNotificationAddView(request, id = None):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmDefineTemplateForNotificationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            data.notification_type_id = id
            data.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already added') 
        return redirect('crm_define_template_for_notification_list', id = id)
    else:
        form = CrmDefineTemplateForNotificationForm()
        context = {
            'form':form, 
            'id':id
        }
        return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html', context)


def CrmDefineTemplateForNotificationEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    company = get_object_or_404(TemplateForNotification, pk=id)
    if request.method == "POST":
        form = CrmDefineTemplateForNotificationForm(request.POST, instance=company)
        if form.is_valid():
            data = form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
        else:
            messages.add_message(request, messages.ERROR,'Already added') 
        return redirect('crm_define_template_for_notification_list', id = company.notification_type_id)
    else:
        form = CrmDefineTemplateForNotificationForm(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/target_audience/add_edit_import_of_message.html', {'form': form})


class CrmDefineTemplateForNotificationDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TemplateForNotification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_define_template_for_notification_list')


# =============Notification Action
class DefineSmsNotificationActionList(View):
    template = 'admin_template/crm_management/notification_set_up/setup_notfication_type/action_list.html'
    pagesize = 10


    def get(self,request):
        responselistquery = NotificationAction.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {'responselistquery': report_paginate}
        return render(request, self.template, context)


def DefineSmsNotificationActionAdd(request):
    if request.method == 'POST':
        form =  DefineSmsNotificationActionFrom(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!')
        else:
            messages.add_message(request, messages.WARNING,  'Already exists!!')
        return redirect('definesmsnotificationactionlist')
    else:
        form =  DefineSmsNotificationActionFrom()
        return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/action_edit.html' ,{'form':form})


def DefineSmsNotificationActionEdit(request, id):
    company = get_object_or_404( NotificationAction, pk=id)
    if request.method == "POST":
        form =  DefineSmsNotificationActionFrom(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!')
        else:
            messages.add_message(request, messages.WARNING,  'Already exists!!')
        return redirect('definesmsnotificationactionlist')
    else:
        form =  DefineSmsNotificationActionFrom(instance=company)
    return render(request, 'admin_template/crm_management/notification_set_up/setup_notfication_type/action_edit.html', {'form': form})


class  DefineSmsNotificationActionDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = NotificationAction.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('definesmsnotificationactionlist')


# ================================ Audit Trail Setup ================================================
class CrmAuditTrailSetupList(View):
    template = 'admin_template/crm_management/audit_trail/set_up_audit_trail_list.html'
    pagesize = 10


    def get(self,request):
        return render(request, self.template)


# ================================ Table and Code Setup  ================================================
class CrmTableCodeList(View):
    template = 'admin_template/crm_management/table_code_set_up/table_code_set_up_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        return render(request, self.template)


# ================================ MIS and Reporting Setup  ================================================
class CrmMisReportingManagePerformanceList(View):
    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/define_target_list.html'
    pagesize = 10

    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = MisManagePerformanceDefineTarget.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmMisReportingManagePerformanceAddView(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/add_edit_template.html'
    if request.method == 'POST':        
        form = CrmAddEditMisReportingManagePerformanceDefineTargetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_mis_reporting_manage_performance_list')
        else:
            messages.add_message(request, messages.ERROR, 'Crm mis manage performance define target with this User already exists.') 
            return redirect('crm_mis_reporting_manage_performance_list')
    else:
        form = CrmAddEditMisReportingManagePerformanceDefineTargetForm()
    context = {
        'form':form
    }
    return render(request, template, context)


def CrmMisReportingManagePerformanceEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/add_edit_template.html'
    company = get_object_or_404(MisManagePerformanceDefineTarget, pk=id)
    if request.method == "POST":
        form = CrmAddEditMisReportingManagePerformanceDefineTargetForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_mis_reporting_manage_performance_list')
    else:
        form = CrmAddEditMisReportingManagePerformanceDefineTargetForm(instance=company)
    context = {
        'form':form
    }
    return render(request, template, context)


class CrmMisReportingManagePerformanceDeleteView(View):
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = MisManagePerformanceDefineTarget.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_mis_reporting_manage_performance_list')


class CrmMisReportingForDownloadLocationTrackingUserView(View):

    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        # response content type
        response = HttpResponse(content_type='text/csv')
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="location_tracking.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        #write the headers
        writer.writerow([
            smart_str(u"User Id"),
            smart_str(u"User Name"),
            smart_str(u"Latitude"),
            smart_str(u"Longitude"),
            smart_str(u"Address"),
            smart_str(u"Added"),
        ])
        #get data from database or from text file....
        events = CrmUserGeographicalApi.objects.all()

        for data in events:
            writer.writerow([
                smart_str(data.user.id),
                smart_str(data.user.name),
                smart_str(data.latitude),
                smart_str(data.longitude),
                smart_str(data.address),
                smart_str(data.added),
            ])
        return response


class CrmMisReportingForDownloadAttendenceUserView(View):
    
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        # response content type
        response = HttpResponse(content_type='text/csv')
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="location_tracking.csv"'

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        #write the headers
        writer.writerow([
            smart_str(u"User Id"),
            smart_str(u"User Name"),
            smart_str(u"Login Attendance Type"),
            smart_str(u"Login Address"),
            smart_str(u"Login Latitude"),
            smart_str(u"Login Longitude"),
            smart_str(u"Login Time"),
            smart_str(u"Logout Attendance Type"),
            smart_str(u"Logout Address"),
            smart_str(u"Logout Latitude"),
            smart_str(u"Logout Longitude"),
            smart_str(u"Logout Time"),
            smart_str(u"Added"),
        ])
        #get data from database or from text file....
        events = CrmUserLoginApiLogs.objects.all()
        for data in events:
            writer.writerow([
                smart_str(data.user.id),
                smart_str(data.user.name),
                smart_str(dict(ATTENDENCE_TYPE)[data.attendance_type]) if data.attendance_type != 0 else "",
                smart_str(data.address),
                smart_str(data.latitude),
                smart_str(data.longitude),
                smart_str(data.added),
                smart_str(dict(ATTENDENCE_TYPE)[data.logout_attendance_type]) if data.logout_attendance_type != 0 else "",
                smart_str(data.logout_address),
                smart_str(data.logout_latitude),
                smart_str(data.logout_longitude),
                smart_str(data.logout_time),
                smart_str(data.added)
            ])
            # 
                                         # 
        return response


#  ************ Manage Reporting
class CrmMisReportingManageReportFormatList(View):
    template = 'admin_template/crm_management/mis_reporting_set_up/manage_reporting/report_format_list.html'
    pagesize = 10

    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        responselistquery = MisManageReportingReportFormat.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmMisReportingManageReportFormatAddView(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/add_edit_template.html'
    if request.method == 'POST':        
        form = CrmAddEditManageReportManageReportFormatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_mis_reporting_manage_report_format_list')
        else:
            messages.add_message(request, messages.ERROR, 'Crm mis manage performance define target with this User already exists.') 
            return redirect('crm_mis_reporting_manage_report_format_list')
    else:
        form = CrmAddEditManageReportManageReportFormatForm()
    context = {
        'form':form
    }
    return render(request, template, context)


def CrmMisReportingManageReportFormatEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/add_edit_template.html'
    company = get_object_or_404(MisManageReportingReportFormat, pk=id)
    if request.method == "POST":
        form = CrmAddEditManageReportManageReportFormatForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_mis_reporting_manage_report_format_list')
        else:
            messages.add_message(request, messages.ERROR, 'Crm mis manage performance define target with this User already exists.') 
            return redirect('crm_mis_reporting_manage_report_format_list')
    else:
        form = CrmAddEditManageReportManageReportFormatForm(instance=company)

    context = {
        'form':form
    }
    return render(request, template, context)


class CrmMisReportingManageReportFormatDeleteView(View):

    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = MisManageReportingReportFormat.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_mis_reporting_manage_report_format_list')


#  ************ Manage Report Frequency
class CrmMisReportingManageReportFrequencyList(View):
    template = 'admin_template/crm_management/mis_reporting_set_up/manage_reporting/report_frequency_list.html'
    pagesize = 10

    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        responselistquery = MisManageReportingReportFrequency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
                'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmMisReportingManageReportFrequencyAddView(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/add_edit_template.html'
    if request.method == 'POST':        
        form = CrmMisReportingManageReportFrequencyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_mis_reporting_manage_report_frequency_list')
        else:
            messages.add_message(request, messages.ERROR, 'Crm mis manage performance define target with this User already exists.') 
            return redirect('crm_mis_reporting_manage_report_frequency_list')
    else:
        form = CrmMisReportingManageReportFrequencyForm()
    context = {
        'form':form
    }
    return render(request, template, context)


def CrmMisReportingManageReportFrequencyEditView(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    template = 'admin_template/crm_management/mis_reporting_set_up/manage_performance/add_edit_template.html'
    company = get_object_or_404(MisManageReportingReportFrequency, pk=id)
    if request.method == "POST":
        form = CrmMisReportingManageReportFrequencyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_mis_reporting_manage_report_frequency_list')
        else:
            messages.add_message(request, messages.ERROR, 'Crm mis manage performance define target with this User already exists.') 
            return redirect('crm_mis_reporting_manage_report_frequency_list')
    else:
        form = CrmMisReportingManageReportFrequencyForm(instance=company)

    context = {
        'form':form
    }
    return render(request, template, context)


class CrmMisReportingManageReportFrequencyDeleteView(View):

    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = MisManageReportingReportFrequency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_mis_reporting_manage_report_frequency_list')


#  ************ Manage Report Template *****************
class CrmMisReportingManageReportTemplateList(View):
    template = 'admin_template/crm_management/mis_reporting_set_up/manage_reporting/report_template_list.html'
    pagesize = 10

    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        responselistquery = MisManageReportingReportFrequencyTemplate.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmMisReportingManageReportTemplateEditView(View):
    template = 'admin_template/crm_management/mis_reporting_set_up/manage_reporting/report_template_add_edit.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            data = ''
            id = None
        else:
            data = get_object_or_404(MisManageReportingReportFrequencyTemplate, pk=id)
            id = id
        context = {
            'data': data, 
            'id': id,
            'action_level':ACTION_LEVEL,
            'company_list': CompanySetup.objects.filter(is_active = True).order_by('-id'),
            'head_off_list': ManageHeadOfficeSetup.objects.filter(is_active = True).order_by('-id'),
            'branch_list': ManageBranch.objects.filter(is_active = True).order_by('-id'),
            'user_list': User.objects.filter(is_active = True, is_superuser = False)
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if request.POST['id'] is None or request.POST['id'] == "None":
            for data in dict(request.POST)['action_level']:
                save_data = MisManageReportingReportFrequencyTemplate()
                save_data.activity_level = data
                save_data.periodic_level = request.POST['periodic_level']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()

                get_id = save_data.id
                for data1 in dict(request.POST)['user_id']:
                    data = MisManageReportingReportFrequencyTemplateUser()
                    data.template_id = get_id
                    data.user_id = data1
                    data.save()
                save_com_head_off = MisManageReportingReportFrequencyTemplateCompany()
                save_com_head_off.parent_com_id   = request.POST['parent_company']
                save_com_head_off.head_offce_id   = request.POST['head_offce']
                saved_id = save_com_head_off.save()
                for data in dict(request.POST)['branch_name']:
                    saved_data  = UserMultipleBranchReporting()
                    saved_data.template_id  = get_id
                    saved_data.brach_id  = data
                    saved_data.save()
            messages.add_message(request, messages.SUCCESS, "Record  added Successfully.")
        else:
            MisManageReportingReportFrequencyTemplate().objects.filter(id = id).delete()
            for data in dict(request.POST)['action_level']:
                save_data = MisManageReportingReportFrequencyTemplate()
                save_data.activity_level = data
                save_data.periodic_level = request.POST['periodic_level']
                if 'is_active' in request.POST:
                    save_data.is_active =  True
                else:
                    save_data.is_active =  False
                save_data.save()

                get_id = save_data.id
                for data1 in dict(request.POST)['user_id']:
                    data = MisManageReportingReportFrequencyTemplateUser()
                    data.template_id = get_id
                    data.user_id = data1
                    data.save()
                save_com_head_off = MisManageReportingReportFrequencyTemplateCompany()
                save_com_head_off.parent_com_id   = request.POST['parent_company']
                save_com_head_off.head_offce_id   = request.POST['head_offce']
                saved_id = save_com_head_off.save()
                for data in dict(request.POST)['branch_name']:
                    saved_data  = UserMultipleBranchReporting()
                    saved_data.template_id  = get_id
                    saved_data.brach_id  = data
                    saved_data.save()
            messages.add_message(request, messages.SUCCESS, "Record  Updated Successfully.")
        return redirect('crm_mis_reporting_manage_report_template_list')


class CrmMisReportingManageReportTemplateDeleteView(View):

    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = MisManageReportingReportFrequencyTemplate.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_mis_reporting_manage_report_template_list')


# ================================ Access and Permisson Setup  ================================================
class CrmAccessPermissonList(View):
    template = 'admin_template/crm_management/access_permisson/aceess_permisson_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = DefinePermissionTypes.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddPermissonType(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmDefinePermissionTypesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_access_permisson_list')
    else:
        form = CrmDefinePermissionTypesForm()
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_permission_type.html' ,{'form':form})


def CrmEditPermissonType(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(DefinePermissionTypes, pk=id)
    if request.method == "POST":
        form = CrmDefinePermissionTypesForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_access_permisson_list')
    else:
        form = CrmDefinePermissionTypesForm(instance=company)
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_permission_type.html', {'form': form})


class CrmPermissonTypeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefinePermissionTypes.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_access_permisson_list')


# Provide Access and Permission




class CrmProvideAccessPermisson(View):
    template = 'admin_template/crm_management/access_permisson/provide_access_permisson_view1.html'
    pagesize = 10


    def get(self,request, id ):

        get_bulk_data = UserAccessPermissonModelsPermission.objects.filter(user_id = id)
        context = {
            'user_id': id, 
            'get_bulk_data': get_bulk_data,
            'user_list': User.objects.filter(is_active =True, is_superuser = False).order_by('-id'),
            'department': ManageDepartment.objects.filter(is_active =True).order_by('-id'),
        }


        data = UserAccessPermissonModelsPermission.objects.filter(user_id = id)
        per_list = [ data.process_name.process_name.strip() for data in LeadAllocationProcessName.objects.filter(lead_allocation__user_id = id)]

        context = {
            'user_id': id, 
            'data': data,
            'permission_list': list(set(per_list))
        }
        return render(request, self.template, context)

# ===================== Permission Level =============
class CrmAccessPermissonLevelList(View):
    template = 'admin_template/crm_management/access_permisson/permission_level_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = DefinePermissionLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddPermissonLevelType(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmCrmDefinePermissionLevelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_access_permisson_level_list')
    else:
        form = CrmCrmDefinePermissionLevelForm()
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_permission_level.html' ,{'form':form})


def CrmEditPermissonLevelType(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(DefinePermissionLevel, pk=id)
    if request.method == "POST":
        form = CrmCrmDefinePermissionLevelForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_access_permisson_level_list')
    else:
        form = CrmCrmDefinePermissionLevelForm(instance=company)
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_permission_level.html', {'form': form})


class CrmPermissonTypeLevelDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefinePermissionLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_access_permisson_level_list')


# Define Hierarchy
class CrmAccessPermissonHierarchyList(View):
    template = 'admin_template/crm_management/access_permisson/permisson_hierarchy_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = DefinePermissionHierarchy.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddPermissonHierarchyType(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST': 
        if DefinePermissionHierarchy.objects.filter(user_id = request.POST['user'] ,reporting_type_id = request.POST['reporting_type'], reporting_level_id = request.POST['reporting_level']).exists():
            messages.add_message(request, messages.SUCCESS,'Already permmisson!!') 
            return redirect('crm_access_permisson_hierarchy_list')
        form = CrmDefinePermissionDefineHierarchyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_access_permisson_hierarchy_list')
    else:
        form = CrmDefinePermissionDefineHierarchyForm()
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_permisson_hierarchy_list.html' ,{'form':form})


def CrmEditPermissonHierarchyType(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(DefinePermissionHierarchy, pk=id)
    if request.method == "POST":
        form = CrmDefinePermissionDefineHierarchyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_access_permisson_hierarchy_list')
    else:
        form = CrmDefinePermissionDefineHierarchyForm(instance=company)
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_permisson_hierarchy_list.html', {'form': form})


class CrmPermissonTypeHierarchyDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefinePermissionHierarchy.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_access_permisson_hierarchy_list')


#============================== Reporting Type ================================
class CrmAccessPermissonReprtingTypeList(View):
    template = 'admin_template/crm_management/access_permisson/reporting_type_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = DefinePermissionReportingType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddPermissonReprtingType(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmDefinePermissionReportingTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_access_permisson_reporting_type_list')    
    else:
        form = CrmDefinePermissionReportingTypeForm()
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_reporting_level.html' ,{'form':form})


def CrmEditPermissonReprtingType(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(DefinePermissionReportingType, pk=id)
    if request.method == "POST":
        form = CrmDefinePermissionReportingTypeForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_access_permisson_reporting_type_list')
    else:
        form = CrmDefinePermissionReportingTypeForm(instance=company)
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_reporting_level.html', {'form': form})


class CrmPermissonTypeReprtingTypeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefinePermissionReportingType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_access_permisson_reporting_type_list')


#============================== Reporting Level
class CrmAccessPermissonReprtingLevelList(View):
    template = 'admin_template/crm_management/access_permisson/reporting_level_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = DefinePermissionReportingLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def CrmAddPermissonReprtingLevel(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = CrmDefinePermissionReportingLevelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('crm_access_permisson_reporting_level_list') 
    else:
        form = CrmDefinePermissionReportingLevelForm()
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_reporting_level.html' ,{'form':form})


def CrmEditPermissonReprtingLevel(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(DefinePermissionReportingLevel, pk=id)
    if request.method == "POST":
        form = CrmDefinePermissionReportingLevelForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('crm_access_permisson_reporting_level_list')
    else:
        form = CrmDefinePermissionReportingLevelForm(instance=company)
    return render(request, 'admin_template/crm_management/access_permisson/add_edit_reporting_level.html', {'form': form})


class CrmPermissonTypeReprtingLevelDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefinePermissionReportingLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('crm_access_permisson_reporting_level_list')


class AccessPermissionUserLisView(View):
    template = 'admin_template/crm_management/access_permisson/access_permission_user_list.html'
    pagesize = 10

    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = User.objects.filter(~Q(is_superuser = 1)).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class ProvideAccessAndPermissionView(View):

    def post(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        
        # -------------------
        #   Employee Services
        # -------------------
        if 'employee_services' in request.POST:

            if not 'employee_update_consultnt_all' in request.POST and not 'employee_update_consultnt' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 1).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 1)
            if 'employee_update_consultnt_all' in request.POST or 'employee_update_consultnt' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_update_consultnt_all' in request.POST  and request.POST['employee_update_consultnt_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_update_consultnt']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "consultant"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 1
                user_per.save()
            # ------------------------------
            # Create Requirements
            # ------------------------------
            if not 'employee_create_reqrt_all' in request.POST and not 'employee_create_reqrt_all' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 2).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 2)
            if 'employee_create_reqrt_all' in request.POST or 'employee_create_reqrt' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_create_reqrt_all' in request.POST  and request.POST['employee_create_reqrt_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_create_reqrt']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "create_reqrt"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 2
                user_per.save()


            if not 'employee_requiremetns_status_all' in request.POST and not 'employee_requiremetns_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 1, 3)
            if 'employee_requiremetns_status_all' in request.POST or 'employee_requiremetns_status' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_requiremetns_status_all' in request.POST and request.POST['employee_requiremetns_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_requiremetns_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "requiremetns_status"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 3
                user_per.save()


            if not 'employee_pulish_jobs_all' in request.POST and not 'employee_pulish_jobs' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 4).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 4)
            if 'employee_pulish_jobs_all' in request.POST or 'employee_pulish_jobs' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_pulish_jobs_all' in request.POST and request.POST['employee_pulish_jobs_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_pulish_jobs']:
                        if data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "pulish_jobs"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 4
                user_per.save()

            if not 'employee_resume_receipt_all' in request.POST and not 'employee_resume_receipt' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 1, 5)
            if 'employee_resume_receipt_all' in request.POST or 'employee_resume_receipt' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_resume_receipt_all' in request.POST and request.POST['employee_resume_receipt_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_pulish_jobs']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "resume_receipt"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 5
                user_per.save()

            if not 'employee_candidate_shortlisted_resume_all' in request.POST and not 'employee_candidate_shortlisted_resume' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 6).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 6)
            if 'employee_candidate_shortlisted_resume_all' in request.POST or 'employee_candidate_shortlisted_resume' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_candidate_shortlisted_resume_all' in request.POST and request.POST['employee_candidate_shortlisted_resume_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_candidate_shortlisted_resume']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "candidate_shortlisted_resume"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 6
                user_per.save()

            if not 'employee_interview_status_all' in request.POST and not 'employee_interview_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 7).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 7)
            if 'employee_interview_status_all' in request.POST or 'employee_interview_status' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_interview_status_all' in request.POST and request.POST['employee_interview_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_interview_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "interview_status"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 7
                user_per.save()

            if not 'employee_shortlisted_candidates_all' in request.POST and not 'employee_shortlisted_candidates' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 8).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 8)
            if 'employee_shortlisted_candidates_all' in request.POST or 'employee_shortlisted_candidates' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_shortlisted_candidates_all' in request.POST and request.POST['employee_shortlisted_candidates_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_shortlisted_candidates']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True

                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "shortlisted_candidates"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 8
                user_per.save()

            if not 'employee_offer_status_all' in request.POST and not 'employee_offer_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 9).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 9)
            if 'employee_offer_status_all' in request.POST or 'employee_offer_status' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_offer_status_all' in request.POST and request.POST['employee_offer_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_offer_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "offer_status"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 9
                user_per.save()


            if not 'employee_vacancy_status_all' in request.POST and not 'employee_vacancy_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =1, sub_menu_sequence = 10).delete()
            user_per = UserPermission.AddEditPermission(request, 1, 10)
            if 'employee_vacancy_status_all' in request.POST or 'employee_vacancy_status' in request.POST:
                # user_per = UserAccessPermissonModelsPermission()
                user_per.user_id = request.POST['user_id']
                if 'employee_vacancy_status_all' in request.POST and request.POST['employee_vacancy_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_vacancy_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 1
                user_per.function_level = "employee_services"
                user_per.sub_function_level = "vacancy_status"
                user_per.sequence = 1
                user_per.sub_menu_sequence = 10
                user_per.save()
        # -------------------
        #   On Boarding and Exit Management 
        # -------------------
        if 'boarding_exist_management' in request.POST:
            if not 'employee_update_consultnt_all' in request.POST and not 'employee_update_consultnt' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =2, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 2, 1)
            if 'employee_update_registeration_all' in request.POST or 'employee_update_registeration' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_update_registeration_all' in request.POST  and request.POST['employee_update_registeration_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_update_registeration']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 2
                user_per.function_level = "boarding_exist_management"
                user_per.sub_function_level = "employee_registration"
                user_per.sequence = 2
                user_per.sub_menu_sequence = 1
                user_per.save()
        # -------------------
        #   Key Responsibility Areas & Targets 
        # -------------------
        if 'key_responsibility_areas_targets' in request.POST:

            if not 'area_target_update_kra_targets_all' in request.POST and not 'employee_update_consultnt' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =3, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 3, 1)
            if 'area_target_update_kra_targets_all' in request.POST or 'area_target_update_kra_targets' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'area_target_update_kra_targets_all' in request.POST  and request.POST['area_target_update_kra_targets_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['area_target_update_kra_targets']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 3
                user_per.function_level = "key_responsibility_areas_targets"
                user_per.sub_function_level = "update_kra_targets"
                user_per.sequence = 3
                user_per.sub_menu_sequence = 1
                user_per.save()


            if not 'area_target_update_kra_targets_performance_all' in request.POST and not 'area_target_update_kra_targets_performance' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =3, sub_menu_sequence = 2).delete()
            user_per = UserPermission.AddEditPermission(request, 3, 2)
            if 'area_target_update_kra_targets_performance_all' in request.POST or 'area_target_update_kra_targets_performance' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'area_target_update_kra_targets_performance_all' in request.POST  and request.POST['area_target_update_kra_targets_performance_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['area_target_update_kra_targets_performance']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 3
                user_per.function_level = "key_responsibility_areas_targets"
                user_per.sub_function_level = "kra_targets_performance"
                user_per.sequence = 3
                user_per.sub_menu_sequence = 2
                user_per.save()


            if not 'area_target_update_kra_targets_current_month_all' in request.POST and not 'area_target_update_kra_targets_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =3, sub_menu_sequence = 3).delete()
            user_per = UserPermission.AddEditPermission(request, 3, 3)
            if 'area_target_update_kra_targets_current_month_all' in request.POST or 'area_target_update_kra_targets_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'area_target_update_kra_targets_current_month_all' in request.POST  and request.POST['area_target_update_kra_targets_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['area_target_update_kra_targets_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 3
                user_per.function_level = "key_responsibility_areas_targets"
                user_per.sub_function_level = "kra_targets_current_month"
                user_per.sequence = 3
                user_per.sub_menu_sequence = 3
                user_per.save()

            if not 'area_target_update_kra_targets_previous_month_all' in request.POST and not 'area_target_update_kra_targets_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =3, sub_menu_sequence = 4).delete()
            user_per = UserPermission.AddEditPermission(request, 3, 4)
            if 'area_target_update_kra_targets_previous_month_all' in request.POST or 'area_target_update_kra_targets_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'area_target_update_kra_targets_previous_month_all' in request.POST  and request.POST['area_target_update_kra_targets_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['area_target_update_kra_targets_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 3
                user_per.function_level = "key_responsibility_areas_targets"
                user_per.sub_function_level = "kra_targets_previous_month"
                user_per.sequence = 3
                user_per.sub_menu_sequence = 4
                user_per.save()
        # -------------------
        #   Employee Exit 
        # -------------------
        if 'employee_exit' in request.POST:

            if not 'employee_exit_employee_resignation_all' in request.POST and not 'employee_exit_employee_resignation' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =4, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 4, 1)
            if 'employee_exit_employee_resignation_all' in request.POST or 'employee_exit_employee_resignation' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_exit_employee_resignation_all' in request.POST  and request.POST['employee_exit_employee_resignation_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_exit_employee_resignation']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 4
                user_per.function_level = "employee_exit"
                user_per.sub_function_level = "employee_resignation"
                user_per.sequence = 4
                user_per.sub_menu_sequence = 1
                user_per.save()


            if not 'employee_exit_employee_resignation_status_all' in request.POST and not 'employee_exit_employee_resignation_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =4, sub_menu_sequence = 2).delete()
            user_per = UserPermission.AddEditPermission(request, 4, 2)
            if 'employee_exit_employee_resignation_status_all' in request.POST or 'employee_exit_employee_resignation_status' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_exit_employee_resignation_status_all' in request.POST  and request.POST['employee_exit_employee_resignation_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_exit_employee_resignation_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 4
                user_per.function_level = "employee_exit"
                user_per.sub_function_level = "employee_resignation_status"
                user_per.sequence = 4
                user_per.sub_menu_sequence = 2
                user_per.save()


            if not 'employee_exit_employee_releieving_all' in request.POST and not 'employee_exit_employee_releieving_' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =4, sub_menu_sequence = 3).delete()
            user_per = UserPermission.AddEditPermission(request, 4, 3)
            if 'employee_exit_employee_releieving_all' in request.POST or 'employee_exit_employee_releieving' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_exit_employee_releieving_all' in request.POST  and request.POST['employee_exit_employee_releieving_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_exit_employee_releieving']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 4
                user_per.function_level = "employee_exit"
                user_per.sub_function_level = "employee_releieving"
                user_per.sequence = 4
                user_per.sub_menu_sequence = 3
                user_per.save()

            if not 'employee_exit_full_and_final_settlemet_all' in request.POST and not 'employee_exit_full_and_final_settlemet' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =4, sub_menu_sequence = 4).delete()
            user_per = UserPermission.AddEditPermission(request, 4, 4)
            if 'employee_exit_full_and_final_settlemet_all' in request.POST or 'employee_exit_full_and_final_settlemet' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_exit_full_and_final_settlemet_all' in request.POST  and request.POST['employee_exit_full_and_final_settlemet_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_exit_full_and_final_settlemet']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 4
                user_per.function_level = "employee_exit"
                user_per.sub_function_level = "kra_targets_previous_month"
                user_per.sequence = 4
                user_per.sub_menu_sequence = 4
                user_per.save()
        # -------------------
        #   Update Employee Profile 
        # -------------------
        if 'update_employee_profile' in request.POST:

            if not 'update_employee_profile_list_of_employee_all' in request.POST and not 'update_employee_profile_list_of_employee' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =5, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 5, 1)
            if 'update_employee_profile_list_of_employee_all' in request.POST or 'update_employee_profile_list_of_employee' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'update_employee_profile_list_of_employee_all' in request.POST  and request.POST['update_employee_profile_list_of_employee_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['update_employee_profile_list_of_employee']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 5
                user_per.function_level = "update_employee_profile"
                user_per.sub_function_level = "list_of_employee"
                user_per.sequence = 5
                user_per.sub_menu_sequence = 1
                user_per.save()
        # -------------------
        #   Leave and Holidays Management 
        # -------------------
        if 'leave_holidays_management' in request.POST:

            if not 'leave_and_holidays_management_holidays_all' in request.POST and not 'leave_and_holidays_management_holidays' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 6, 1)
            if 'leave_and_holidays_management_holidays_all' in request.POST or 'leave_and_holidays_management_holidays' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_holidays_all' in request.POST  and request.POST['leave_and_holidays_management_holidays_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_holidays']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "holidays"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 1
                user_per.save()



            if not 'leave_and_holidays_management_leave_update_leave_quota_all' in request.POST and not 'leave_and_holidays_management_leave_update_leave_quota' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 6, 2)
            if 'leave_and_holidays_management_leave_update_leave_quota_all' in request.POST or 'leave_and_holidays_management_leave_update_leave_quota' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_leave_update_leave_quota_all' in request.POST  and request.POST['leave_and_holidays_management_leave_update_leave_quota_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_leave_update_leave_quota']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "leave_quota"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 2
                user_per.save()


            if not 'leave_and_holidays_management_leave_request_all' in request.POST and not 'leave_and_holidays_management_leave_request' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 6, 3)
            if 'leave_and_holidays_management_leave_request_all' in request.POST or 'leave_and_holidays_management_leave_request' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_leave_request_all' in request.POST  and request.POST['leave_and_holidays_management_leave_request_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_leave_request']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "leave_request"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 3
                user_per.save()

            if not 'leave_and_holidays_management_leave_for_approval_all' in request.POST and not 'leave_and_holidays_management_leave_for_approval' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 6, 4)
            if 'leave_and_holidays_management_leave_for_approval_all' in request.POST or 'leave_and_holidays_management_leave_for_approval' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_leave_for_approval_all' in request.POST  and request.POST['leave_and_holidays_management_leave_for_approval_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_leave_for_approval']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "leave_for_approval"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 4
                user_per.save()

            if not 'leave_and_holidays_management_approved_leave_all' in request.POST and not 'leave_and_holidays_management_approved_leave' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 6, 5)
            if 'leave_and_holidays_management_approved_leave_all' in request.POST or 'leave_and_holidays_management_approved_leave' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_approved_leave_all' in request.POST  and request.POST['leave_and_holidays_management_approved_leave_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_approved_leave']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "approved_leave"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 5
                user_per.save()

            if not 'leave_and_holidays_management_leave_reject_all' in request.POST and not 'leave_and_holidays_management_leave_reject' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 6).delete()
            user_per = UserPermission.AddEditPermission(request, 6, 6)
            if 'leave_and_holidays_management_leave_reject_all' in request.POST or 'leave_and_holidays_management_leave_reject' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_leave_reject_all' in request.POST  and request.POST['leave_and_holidays_management_leave_reject_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_leave_reject']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "leave_reject"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 6
                user_per.save()


            if not 'leave_and_holidays_management_my_leave_balance_all' in request.POST and not 'leave_and_holidays_management_my_leave_balance' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =6, sub_menu_sequence = 7).delete()
            user_per = UserPermission.AddEditPermission(request, 6, 7)
            if 'leave_and_holidays_management_my_leave_balance_all' in request.POST or 'leave_and_holidays_management_my_leave_balance' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'leave_and_holidays_management_my_leave_balance_all' in request.POST  and request.POST['leave_and_holidays_management_my_leave_balance_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['leave_and_holidays_management_my_leave_balance']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 6
                user_per.function_level = "leave_holidays_management"
                user_per.sub_function_level = "my_leave_balance"
                user_per.sequence = 6
                user_per.sub_menu_sequence = 7
                user_per.save()
        # -------------------
        #   Attendance & Overtime Management 
        # -------------------
        if 'attendance_overtime_management' in request.POST:

            if not 'attendance_overtime_management_upload_attendance_all' in request.POST and not 'attendance_overtime_management_upload_attendance' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 7, 1)
            if 'attendance_overtime_management_upload_attendance_all' in request.POST or 'attendance_overtime_management_upload_attendance' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_upload_attendance_all' in request.POST  and request.POST['attendance_overtime_management_upload_attendance_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_upload_attendance']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "upload_attendance"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 1
                user_per.save()



            if not 'attendance_overtime_management_update_attendance_all' in request.POST and not 'attendance_overtime_management_update_attendance' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 7, 2)
            if 'attendance_overtime_management_update_attendance_all' in request.POST or 'attendance_overtime_management_update_attendance' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_update_attendance_all' in request.POST  and request.POST['attendance_overtime_management_update_attendance_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_update_attendance']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "update_attendance"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 2
                user_per.save()


            if not 'attendance_overtime_management_attendance_correction_all' in request.POST and not 'attendance_overtime_management_attendance_correction' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 7, 3)
            if 'attendance_overtime_management_attendance_correction_all' in request.POST or 'attendance_overtime_management_attendance_correction' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_attendance_correction_all' in request.POST  and request.POST['attendance_overtime_management_attendance_correction_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_attendance_correction']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "attendance_correction"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 3
                user_per.save()

            if not 'attendance_overtime_management_attendance_status_today_all' in request.POST and not 'attendance_overtime_management_attendance_status_today' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 7, 4)
            if 'attendance_overtime_management_attendance_status_today_all' in request.POST or 'attendance_overtime_management_attendance_status_today' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_attendance_status_today_all' in request.POST  and request.POST['attendance_overtime_management_attendance_status_today_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_attendance_status_today']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "attendance_status_today"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 4
                user_per.save()

            if not 'attendance_overtime_management_attendance_status_current_month_all' in request.POST and not 'attendance_overtime_management_attendance_status_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 7, 5)
            if 'attendance_overtime_management_attendance_status_current_month_all' in request.POST or 'attendance_overtime_management_attendance_status_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_attendance_status_current_month_all' in request.POST  and request.POST['attendance_overtime_management_attendance_status_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_attendance_status_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "status_current_month"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 5
                user_per.save()


            if not 'attendance_overtime_management_attendance_status_previous_month_all' in request.POST and not 'attendance_overtime_management_attendance_status_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 6).delete()
            
            user_per = UserPermission.AddEditPermission(request, 7, 6)
            if 'attendance_overtime_management_attendance_status_previous_month_all' in request.POST or 'attendance_overtime_management_attendance_status_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_attendance_status_previous_month_all' in request.POST  and request.POST['attendance_overtime_management_attendance_status_previous_month'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_attendance_status_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "status_previous_month"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 6
                user_per.save()

            if not 'attendance_overtime_management_over_time_all' in request.POST and not 'attendance_overtime_management_over_time' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 7).delete()
            user_per = UserPermission.AddEditPermission(request, 7, 7)
            if 'attendance_overtime_management_over_time_all' in request.POST or 'attendance_overtime_management_over_time' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_over_time_all' in request.POST  and request.POST['attendance_overtime_management_over_time_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_over_time']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "management_over_time"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 7
                user_per.save()


            if not 'attendance_overtime_management_overtime_status_today_all' in request.POST and not 'attendance_overtime_management_overtime_status_today' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 8).delete()
            user_per = UserPermission.AddEditPermission(request, 7, 8)
            if 'attendance_overtime_management_overtime_status_today_all' in request.POST or 'attendance_overtime_management_overtime_status_today' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_overtime_status_today_all' in request.POST  and request.POST['attendance_overtime_management_overtime_status_today_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_overtime_status_today']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "overtime_status_today"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 8
                user_per.save()


            if not 'attendance_overtime_management_overtime_status_current_month_all' in request.POST and not 'attendance_overtime_management_overtime_status_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 9).delete()
            user_per = UserPermission.AddEditPermission(request, 7, 9)
            if 'attendance_overtime_management_overtime_status_current_month_all' in request.POST or 'attendance_overtime_management_overtime_status_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_overtime_status_current_month_all' in request.POST  and request.POST['attendance_overtime_management_overtime_status_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_overtime_status_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "overtime_status_current_month"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 9
                user_per.save()

            if not 'attendance_overtime_management_overtime_status_previous_month_all' in request.POST and not 'attendance_overtime_management_overtime_status_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =7, sub_menu_sequence = 10).delete()
            user_per = UserPermission.AddEditPermission(request, 7, 10)
            if 'attendance_overtime_management_overtime_status_previous_month_all' in request.POST or 'attendance_overtime_management_overtime_status_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'attendance_overtime_management_overtime_status_previous_month_all' in request.POST  and request.POST['attendance_overtime_management_overtime_status_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['attendance_overtime_management_overtime_status_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 7
                user_per.function_level = "attendance_overtime_management"
                user_per.sub_function_level = "overtime_status_previous_month"
                user_per.sequence = 7
                user_per.sub_menu_sequence = 10
                user_per.save()
        # -------------------
        #   Travel & Claim Management 
        # -------------------
        if 'travel_claim_management' in request.POST:

            if not 'travel_claim_managment_travel_conveyance_travel_request_all' in request.POST and not 'travel_claim_managment_travel_conveyance_travel_request' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =8, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 8, 1)
            if 'travel_claim_managment_travel_conveyance_travel_request_all' in request.POST or 'travel_claim_managment_travel_conveyance_travel_request' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'travel_claim_managment_travel_conveyance_travel_request_all' in request.POST  and request.POST['travel_claim_managment_travel_conveyance_travel_request_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['travel_claim_managment_travel_conveyance_travel_request']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 8
                user_per.function_level = "travel_claim_management"
                user_per.sub_function_level = "travel_request"
                user_per.sequence = 8
                user_per.sub_menu_sequence = 1
                user_per.save()



            if not 'travel_claim_managment_travel_conveyance_travel_request_today_all' in request.POST and not 'travel_claim_managment_travel_conveyance_travel_request_today' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =8, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 8, 2)
            if 'travel_claim_managment_travel_conveyance_travel_request_today_all' in request.POST or 'travel_claim_managment_travel_conveyance_travel_request_today' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'travel_claim_managment_travel_conveyance_travel_request_today_all' in request.POST  and request.POST['travel_claim_managment_travel_conveyance_travel_request_today_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['travel_claim_managment_travel_conveyance_travel_request_today']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 8
                user_per.function_level = "travel_claim_management"
                user_per.sub_function_level = "travel_request_today"
                user_per.sequence = 8
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'travel_claim_managment_travel_conveyance_travel_request_current_month_all' in request.POST and not 'travel_claim_managment_travel_conveyance_travel_request_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =8, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 8, 3)
            if 'travel_claim_managment_travel_conveyance_travel_request_current_month_all' in request.POST or 'travel_claim_managment_travel_conveyance_travel_request_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'travel_claim_managment_travel_conveyance_travel_request_current_month_all' in request.POST  and request.POST['travel_claim_managment_travel_conveyance_travel_request_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['travel_claim_managment_travel_conveyance_travel_request_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 8
                user_per.function_level = "travel_claim_management"
                user_per.sub_function_level = "travel_request_current_month"
                user_per.sequence = 8
                user_per.sub_menu_sequence = 3
                user_per.save()

            if not 'travel_claim_managment_travel_conveyance_travel_request_previous_month_all' in request.POST and not 'travel_claim_managment_travel_conveyance_travel_request_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =8, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 8, 4)
            if 'travel_claim_managment_travel_conveyance_travel_request_previous_month_all' in request.POST or 'travel_claim_managment_travel_conveyance_travel_request_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'travel_claim_managment_travel_conveyance_travel_request_previous_month_all' in request.POST  and request.POST['travel_claim_managment_travel_conveyance_travel_request_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['travel_claim_managment_travel_conveyance_travel_request_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 8
                user_per.function_level = "travel_claim_management"
                user_per.sub_function_level = "travel_request_previous_month"
                user_per.sequence = 8
                user_per.sub_menu_sequence = 4
                user_per.save()
        # -------------------
        #   Claims & Reimbursement 
        # -------------------
        if 'claims_and_reimbursement' in request.POST:

            if not 'claim_reimbursement_submit_claims_all' in request.POST and not 'claim_reimbursement_submit_claims' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 1)
            if 'claim_reimbursement_submit_claims_all' in request.POST or 'claim_reimbursement_submit_claims' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_submit_claims_all' in request.POST  and request.POST['claim_reimbursement_submit_claims_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_submit_claims']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "submit_claims"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 1
                user_per.save()



            if not 'claim_reimbursement_claim_status_all' in request.POST and not 'claim_reimbursement_claim_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 2)
            if 'claim_reimbursement_claim_status_all' in request.POST or 'claim_reimbursement_claim_status' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_claim_status_all' in request.POST  and request.POST['claim_reimbursement_claim_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_claim_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "claim_status"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'claim_reimbursement_claim_processing_all' in request.POST and not 'claim_reimbursement_claim_processing' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 3)
            if 'claim_reimbursement_claim_processing_all' in request.POST or 'claim_reimbursement_claim_processing' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_claim_processing_all' in request.POST  and request.POST['claim_reimbursement_claim_processing_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_claim_processing']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "claim_processing"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 3
                user_per.save()

            if not 'claim_reimbursement_claim_processed_current_month_all' in request.POST and not 'claim_reimbursement_claim_processed_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 4)
            if 'claim_reimbursement_claim_processed_current_month_all' in request.POST or 'claim_reimbursement_claim_processed_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_claim_processed_current_month_all' in request.POST  and request.POST['claim_reimbursement_claim_processed_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_claim_processed_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "claim_processed_current_month"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 4
                user_per.save()

            if not 'claim_reimbursement_claim_processed_previous_month_all' in request.POST and not 'claim_reimbursement_claim_processed_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 5)
            if 'claim_reimbursement_claim_processed_previous_month_all' in request.POST or 'claim_reimbursement_claim_processed_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_claim_processed_previous_month_all' in request.POST  and request.POST['claim_reimbursement_claim_processed_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_claim_processed_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "claim_processed_previous_month"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 5
                user_per.save()


            if not 'claim_reimbursement_submit_reimbursement_all' in request.POST and not 'claim_reimbursement_submit_reimbursement' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 6).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 6)
            if 'claim_reimbursement_submit_reimbursement_all' in request.POST or 'claim_reimbursement_submit_reimbursement' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_submit_reimbursement_all' in request.POST  and request.POST['claim_reimbursement_submit_reimbursement_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_submit_reimbursement']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "submit_reimbursement"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 6
                user_per.save()

            if not 'claim_reimbursement_submit_reimbursement_status_all' in request.POST and not 'claim_reimbursement_submit_reimbursement_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 7).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 7)
            if 'claim_reimbursement_submit_reimbursement_status_all' in request.POST or 'claim_reimbursement_submit_reimbursement_status' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_submit_reimbursement_status_all' in request.POST  and request.POST['claim_reimbursement_submit_reimbursement_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_submit_reimbursement_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "submit_reimbursement_status"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 7
                user_per.save()

            if not 'claim_reimbursement_submit_reimbursement_processing_all' in request.POST and not 'claim_reimbursement_submit_reimbursement_processing' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 8).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 8)
            if 'claim_reimbursement_submit_reimbursement_processing_all' in request.POST or 'claim_reimbursement_submit_reimbursement_processing' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_submit_reimbursement_processing_all' in request.POST  and request.POST['claim_reimbursement_submit_reimbursement_processing_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_submit_reimbursement_processing']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "submit_reimbursement_processing"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 8
                user_per.save()


            if not 'claim_reimbursement_submit_reimbursement_processing_current_month_all' in request.POST and not 'claim_reimbursement_submit_reimbursement_processing_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 9).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 9)
            if 'claim_reimbursement_submit_reimbursement_processing_current_month_all' in request.POST or 'claim_reimbursement_submit_reimbursement_processing_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_submit_reimbursement_processing_current_month_all' in request.POST  and request.POST['claim_reimbursement_submit_reimbursement_processing_current_month'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_submit_reimbursement_processing_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "processing_current_month"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 9
                user_per.save()


            if not 'claim_reimbursement_submit_reimbursement_processing_previous_month_all' in request.POST and not 'claim_reimbursement_submit_reimbursement_processing_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =9, sub_menu_sequence = 10).delete()
            
            user_per = UserPermission.AddEditPermission(request, 9, 10)
            if 'claim_reimbursement_submit_reimbursement_processing_previous_month_all' in request.POST or 'claim_reimbursement_submit_reimbursement_processing_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'claim_reimbursement_submit_reimbursement_processing_previous_month_all' in request.POST  and request.POST['claim_reimbursement_submit_reimbursement_processing_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['claim_reimbursement_submit_reimbursement_processing_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 9
                user_per.function_level = "claims_and_reimbursement"
                user_per.sub_function_level = "processing_previous_month"
                user_per.sequence = 9
                user_per.sub_menu_sequence = 10
                user_per.save()
        # -------------------
        #  Employee Advances
        # -------------------
        if 'employee_advances' in request.POST:

            if not 'employee_advances_submit_advance_request_all' in request.POST and not 'employee_advances_submit_advance_request' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =10, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 10, 1)
            if 'employee_advances_submit_advance_request_all' in request.POST or 'employee_advances_submit_advance_request' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_advances_submit_advance_request_all' in request.POST  and request.POST['employee_advances_submit_advance_request_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_advances_submit_advance_request']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 10
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "submit_advance_request"
                user_per.sequence = 10
                user_per.sub_menu_sequence = 1
                user_per.save()


            if not 'employee_advances_submit_advance_request_status_all' in request.POST and not 'employee_advances_submit_advance_request_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =10, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 10, 2)
            if 'employee_advances_submit_advance_request_status_all' in request.POST or 'employee_advances_submit_advance_request_status' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_advances_submit_advance_request_status_all' in request.POST  and request.POST['employee_advances_submit_advance_request_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_advances_submit_advance_request_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 10
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "submit_advance_request_status"
                user_per.sequence = 10
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'employee_advances_submit_advance_request_processing_all' in request.POST and not 'employee_advances_submit_advance_request_processing' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =10, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 10, 3)
            if 'employee_advances_submit_advance_request_processing_all' in request.POST or 'employee_advances_submit_advance_request_processing' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_advances_submit_advance_request_processing_all' in request.POST  and request.POST['employee_advances_submit_advance_request_processing_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_advances_submit_advance_request_processing']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 10
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "submit_advance_request_processing"
                user_per.sequence = 10
                user_per.sub_menu_sequence = 3
                user_per.save()


            if not 'employee_advances_submit_advance_request_processed_current_month_all' in request.POST and not 'employee_advances_submit_advance_request_processed_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =10, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 10, 4)
            if 'employee_advances_submit_advance_request_processed_current_month_all' in request.POST or 'employee_advances_submit_advance_request_processed_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_advances_submit_advance_request_processed_current_month_all' in request.POST  and request.POST['employee_advances_submit_advance_request_processed_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_advances_submit_advance_request_processed_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 10
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "submit_advance_request_processed_current_month"
                user_per.sequence = 10
                user_per.sub_menu_sequence = 4
                user_per.save()


            if not 'employee_advances_submit_advance_request_processed_previous_month_all' in request.POST and not 'employee_advances_submit_advance_request_processed_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =10, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 10, 5)
            if 'employee_advances_submit_advance_request_processed_previous_month_all' in request.POST or 'employee_advances_submit_advance_request_processed_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'employee_advances_submit_advance_request_processed_previous_month_all' in request.POST  and request.POST['employee_advances_submit_advance_request_processed_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['employee_advances_submit_advance_request_processed_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 10
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "submit_advance_request_processed_previous_month"
                user_per.sequence = 10
                user_per.sub_menu_sequence = 5
                user_per.save()
        # -------------------
        #  Incentive & Bonus 
        # -------------------
        if 'incentive_and_bonus' in request.POST:

            if not 'incentive_bonus_update_incentive_bonus_all' in request.POST and not 'incentive_bonus_update_incentive_bonus' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =11, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 11, 1)
            if 'incentive_bonus_update_incentive_bonus_all' in request.POST or 'incentive_bonus_update_incentive_bonus' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'incentive_bonus_update_incentive_bonus_all' in request.POST  and request.POST['incentive_bonus_update_incentive_bonus_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['incentive_bonus_update_incentive_bonus']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 11
                user_per.function_level = "incentive_and_bonus"
                user_per.sub_function_level = "update_incentive_bonus"
                user_per.sequence = 11
                user_per.sub_menu_sequence = 1
                user_per.save()


            if not 'incentive_bonus_approval_all' in request.POST and not 'incentive_bonus_approval' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =11, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 11, 2)
            if 'incentive_bonus_approval_all' in request.POST or 'incentive_bonus_approval' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'incentive_bonus_approval_all' in request.POST  and request.POST['incentive_bonus_approval_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['incentive_bonus_approval']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 11
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "incentive_bonus_approval"
                user_per.sequence = 11
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'incentive_bonus_processing_all' in request.POST and not 'incentive_bonus_processing' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =11, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 11, 3)
            if 'incentive_bonus_processing_all' in request.POST or 'incentive_bonus_processing' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'incentive_bonus_processing_all' in request.POST  and request.POST['incentive_bonus_processing_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['incentive_bonus_processing']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 11
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "incentive_bonus_processing"
                user_per.sequence = 11
                user_per.sub_menu_sequence = 3
                user_per.save()


            if not 'incentive_bonus_processed_current_month_all' in request.POST and not 'incentive_bonus_processed_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =11, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 11, 4)
            if 'incentive_bonus_processed_current_month_all' in request.POST or 'incentive_bonus_processed_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'incentive_bonus_processed_current_month_all' in request.POST  and request.POST['incentive_bonus_processed_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['incentive_bonus_processed_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 11
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "incentive_bonus_processed_current_month"
                user_per.sequence = 11
                user_per.sub_menu_sequence = 4
                user_per.save()


            if not 'incentive_bonus_processed_previous_month_all' in request.POST and not 'incentive_bonus_processed_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =11, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 11, 5)
            if 'incentive_bonus_processed_previous_month_all' in request.POST or 'incentive_bonus_processed_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'incentive_bonus_processed_previous_month_all' in request.POST  and request.POST['incentive_bonus_processed_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['incentive_bonus_processed_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 11
                user_per.function_level = "employee_advances"
                user_per.sub_function_level = "incentive_bonus_processed_previous_month"
                user_per.sequence = 11
                user_per.sub_menu_sequence = 5
                user_per.save()
        # -------------------
        #  Payroll Process Management @@@@@ 12
        # -------------------
        if 'payroll_process' in request.POST :
            if not 'payroll_process_management_accept_attendance_all' in request.POST and not 'payroll_process_management_accept_attendance' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 1)
            if 'payroll_process_management_accept_attendance_all' in request.POST or 'payroll_process_management_accept_attendance' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_accept_attendance_all' in request.POST  and request.POST['payroll_process_management_accept_attendance_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_accept_attendance']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "accept_attendance"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 1
                user_per.save()

            if not 'payroll_process_management_accept_overtime_all' in request.POST and not 'payroll_process_management_accept_overtime' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 2)
            if 'payroll_process_management_accept_overtime_all' in request.POST or 'payroll_process_management_accept_overtime' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_accept_overtime_all' in request.POST  and request.POST['payroll_process_management_accept_overtime_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_accept_overtime']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "accept_overtime"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'payroll_process_management_update_leaves_all' in request.POST and not 'payroll_process_management_update_leaves' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 3)
            if 'payroll_process_management_update_leaves_all' in request.POST or 'payroll_process_management_update_leaves' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_update_leaves_all' in request.POST  and request.POST['payroll_process_management_update_leaves_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_update_leaves']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "update_leaves"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 3
                user_per.save()


            if not 'payroll_process_management_accept_claims_all' in request.POST and not 'payroll_process_management_accept_claims' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 4)
            if 'payroll_process_management_accept_claims_all' in request.POST or 'payroll_process_management_accept_claims' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_accept_claims_all' in request.POST  and request.POST['payroll_process_management_accept_claims_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_update_leaves']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "update_leaves"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 4
                user_per.save()


            if not 'payroll_process_management_update_reimbursement_all' in request.POST and not 'payroll_process_management_update_reimbursement' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 5)
            if 'payroll_process_management_update_reimbursement_all' in request.POST or 'payroll_process_management_update_reimbursement' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_update_reimbursement_all' in request.POST  and request.POST['payroll_process_management_update_reimbursement_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_update_reimbursement']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "update_reimbursement"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 5
                user_per.save()

            if not 'payroll_process_management_update_recovery_of_advances_all' in request.POST and not 'payroll_process_management_update_recovery_of_advances' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 6).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 6)
            if 'payroll_process_management_update_recovery_of_advances_all' in request.POST or 'payroll_process_management_update_recovery_of_advances' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_update_recovery_of_advances_all' in request.POST  and request.POST['payroll_process_management_update_recovery_of_advances_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_update_recovery_of_advances']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "update_recovery_of_advances"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 6
                user_per.save()


            if not 'payroll_process_management_update_incentives_all' in request.POST and not 'payroll_process_management_update_incentives' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 7).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 7)
            if 'payroll_process_management_update_incentives_all' in request.POST or 'payroll_process_management_update_incentives' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_update_incentives_all' in request.POST  and request.POST['payroll_process_management_update_incentives_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_update_incentives']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "update_incentives"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 7
                user_per.save()


            if not 'payroll_process_management_tax_recovery_all' in request.POST and not 'payroll_process_management_tax_recovery' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 8).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 8)
            if 'payroll_process_management_tax_recovery_all' in request.POST or 'payroll_process_management_tax_recovery' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_tax_recovery_all' in request.POST  and request.POST['payroll_process_management_tax_recovery_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_tax_recovery']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "tax_recovery"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 8
                user_per.save()


            if not 'payroll_process_management_tax_update_other_recoveries_all' in request.POST and not 'payroll_process_management_tax_update_other_recoveries' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 9).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 9)
            if 'payroll_process_management_tax_update_other_recoveries_all' in request.POST or 'payroll_process_management_tax_update_other_recoveries' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_tax_update_other_recoveries_all' in request.POST  and request.POST['payroll_process_management_tax_update_other_recoveries_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_tax_update_other_recoveries']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "update_other_recoveries"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 9
                user_per.save()




            if not 'payroll_process_management_payroll_status_all' in request.POST and not 'payroll_process_management_payroll_status' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 10).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 10)
            if 'payroll_process_management_payroll_status_all' in request.POST or 'payroll_process_management_payroll_status' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_payroll_status_all' in request.POST  and request.POST['payroll_process_management_payroll_status_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_payroll_status']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "payroll_status"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 10
                user_per.save()



            if not 'payroll_process_management_payroll_processed_current_month_all' in request.POST and not 'payroll_process_management_payroll_processed_current_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 11).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 11)
            if 'payroll_process_management_payroll_processed_current_month_all' in request.POST or 'payroll_process_management_payroll_processed_current_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_payroll_processed_current_month_all' in request.POST  and request.POST['payroll_process_management_payroll_processed_current_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_payroll_processed_current_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "payroll_processed_current_month"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 11
                user_per.save()


            if not 'payroll_process_management_payroll_processed_previous_month_all' in request.POST and not 'payroll_process_management_payroll_processed_previous_month' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 12).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 12)
            if 'payroll_process_management_payroll_processed_previous_month_all' in request.POST or 'payroll_process_management_payroll_processed_previous_month' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_payroll_processed_previous_month_all' in request.POST  and request.POST['payroll_process_management_payroll_processed_previous_month_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_payroll_processed_previous_month']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "payroll_processed_previous_month"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 12
                user_per.save()

            if not 'payroll_process_management_salary_disbursements_all' in request.POST and not 'payroll_process_management_salary_disbursement' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 13).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 13)
            if 'payroll_process_management_salary_disbursements_all' in request.POST or 'payroll_process_management_salary_disbursement' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_salary_disbursements_all' in request.POST  and request.POST['payroll_process_management_salary_disbursements_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_salary_disbursement']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "salary_disbursements"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 13
                user_per.save()


            if not 'payroll_process_management_salary_vouchers_all' in request.POST and not 'payroll_process_management_salary_vouchers' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 14).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 14)
            if 'payroll_process_management_salary_vouchers_all' in request.POST or 'payroll_process_management_salary_vouchers' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_salary_vouchers_all' in request.POST  and request.POST['payroll_process_management_salary_vouchers_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_salary_vouchers']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "salary_vouchers"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 14
                user_per.save()



            if not 'payroll_process_management_statutory_deductions_all' in request.POST and not 'payroll_process_management_statutory_deductions' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =12, sub_menu_sequence = 15).delete()
            
            user_per = UserPermission.AddEditPermission(request, 12, 15)
            if 'payroll_process_management_statutory_deductions_all' in request.POST or 'payroll_process_management_statutory_deductions' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'payroll_process_management_statutory_deductions_all' in request.POST  and request.POST['payroll_process_management_statutory_deductions_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['payroll_process_management_statutory_deductions']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 12
                user_per.function_level = "payroll_process"
                user_per.sub_function_level = "statutory_deductions"
                user_per.sequence = 12
                user_per.sub_menu_sequence = 15
                user_per.save()
        # -------------------
        #  Policies & Forms 
        # -------------------
        if 'policies_forms' in request.POST:

            if not 'policies_forms_update_policies_all' in request.POST and not 'policies_forms_update_policies' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =13, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 13, 1)
            if 'policies_forms_update_policies_all' in request.POST or 'policies_forms_update_policies' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'policies_forms_update_policies_all' in request.POST  and request.POST['policies_forms_update_policies_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['policies_forms_update_policies']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 13
                user_per.function_level = "policies_forms"
                user_per.sub_function_level = "update_policies"
                user_per.sequence = 13
                user_per.sub_menu_sequence = 1
                user_per.save()


            if not 'policies_forms_update_forms_all' in request.POST and not 'policies_forms_update_forms' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =13, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 13, 2)
            if 'policies_forms_update_forms_all' in request.POST or 'policies_forms_update_forms' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'policies_forms_update_forms_all' in request.POST  and request.POST['policies_forms_update_forms_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['policies_forms_update_forms']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 13
                user_per.function_level = "policies_forms"
                user_per.sub_function_level = "incentive_bonus_approval"
                user_per.sequence = 13
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'policies_forms_update_circulars_all' in request.POST and not 'policies_forms_update_circulars' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =13, sub_menu_sequence = 3).delete()
            
            user_per = UserPermission.AddEditPermission(request, 13, 3)
            if 'policies_forms_update_circulars_all' in request.POST or 'policies_forms_update_circulars' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'policies_forms_update_circulars_all' in request.POST  and request.POST['policies_forms_update_circulars_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['policies_forms_update_circulars']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 13
                user_per.function_level = "policies_forms"
                user_per.sub_function_level = "update_circulars"
                user_per.sequence = 13
                user_per.sub_menu_sequence = 3
                user_per.save()


            if not 'policies_forms_hr_policies_all' in request.POST and not 'policies_forms_hr_policies' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =13, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 13, 4)
            if 'policies_forms_hr_policies_all' in request.POST or 'policies_forms_hr_policies' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'policies_forms_hr_policies_all' in request.POST  and request.POST['policies_forms_hr_policies_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['policies_forms_hr_policies']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 13
                user_per.function_level = "policies_forms"
                user_per.sub_function_level = "hr_policies"
                user_per.sequence = 13
                user_per.sub_menu_sequence = 4
                user_per.save()


            if not 'policies_forms_circulars_all' in request.POST and not 'policies_forms_circulars' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =13, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 13, 5)
            if 'policies_forms_circulars_all' in request.POST or 'policies_forms_circulars' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'policies_forms_circulars_all' in request.POST  and request.POST['policies_forms_circulars_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['policies_forms_circulars']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 13
                user_per.function_level = "policies_forms"
                user_per.sub_function_level = "circulars"
                user_per.sequence = 13
                user_per.sub_menu_sequence = 5
                user_per.save()

            if not 'policies_forms_forms_all' in request.POST and not 'policies_forms_forms' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =13, sub_menu_sequence = 6).delete()
            
            user_per = UserPermission.AddEditPermission(request, 13, 6)
            if 'policies_forms_forms_all' in request.POST or 'policies_forms_forms' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'policies_forms_forms_all' in request.POST  and request.POST['policies_forms_forms_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['policies_forms_forms']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 13
                user_per.function_level = "policies_forms"
                user_per.sub_function_level = "forms"
                user_per.sequence = 13
                user_per.sub_menu_sequence = 6
                user_per.save()
        # -------------------
        #  Knowledge Sharing & Training
        # -------------------
        if 'knowledge_sharing_training' in request.POST:

            if not 'knowledge_sharing_training_update_documents_all' in request.POST and not 'knowledge_sharing_training_update_documents' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 1).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 1)
            if 'knowledge_sharing_training_update_documents_all' in request.POST or 'knowledge_sharing_training_update_documents' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_update_documents_all' in request.POST  and request.POST['knowledge_sharing_training_update_documents_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_update_documents']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "update_documents"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 1
                user_per.save()


            if not 'knowledge_sharing_training_update_training_all' in request.POST and not 'knowledge_sharing_training_update_training' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 2).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 2)
            if 'knowledge_sharing_training_update_training_all' in request.POST or 'knowledge_sharing_training_update_training' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_update_training_all' in request.POST  and request.POST['knowledge_sharing_training_update_training_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_update_training']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "update_training"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 2
                user_per.save()

            if not 'knowledge_sharing_training_update_promotions_all' in request.POST and not 'knowledge_sharing_training_update_promotions' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 3).delete()
            

            user_per = UserPermission.AddEditPermission(request, 14, 3)
            if 'knowledge_sharing_training_update_promotions_all' in request.POST or 'knowledge_sharing_training_update_promotions' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_update_promotions_all' in request.POST  and request.POST['knowledge_sharing_training_update_promotions_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_update_promotions']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "update_circulars"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 3
                user_per.save()


            if not 'knowledge_sharing_training_knowledge_sharing_all' in request.POST and not 'knowledge_sharing_training_knowledge_sharing' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 4).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 4)
            if 'knowledge_sharing_training_knowledge_sharing_all' in request.POST or 'knowledge_sharing_training_knowledge_sharing' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_knowledge_sharing_all' in request.POST  and request.POST['knowledge_sharing_training_knowledge_sharing_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_knowledge_sharing']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "knowledge_sharing"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 4
                user_per.save()


            if not 'knowledge_sharing_training_upcoming_training_all' in request.POST and not 'knowledge_sharing_training_upcoming_training' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 5).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 5)
            if 'knowledge_sharing_training_upcoming_training_all' in request.POST or 'knowledge_sharing_training_upcoming_training' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_upcoming_training_all' in request.POST  and request.POST['knowledge_sharing_training_upcoming_training_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_upcoming_training']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "upcoming_training"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 5
                user_per.save()

            if not 'knowledge_sharing_training_traning_attend_all' in request.POST and not 'knowledge_sharing_training_traning_attend' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 6).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 6)
            if 'knowledge_sharing_training_traning_attend_all' in request.POST or 'knowledge_sharing_training_traning_attend' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_traning_attend_all' in request.POST  and request.POST['knowledge_sharing_training_traning_attend_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_traning_attend']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "traning_attend"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 6
                user_per.save()

            if not 'knowledge_sharing_training_current_promotions_all' in request.POST and not 'knowledge_sharing_training_current_promotions' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 7).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 7)
            if 'knowledge_sharing_training_current_promotions_all' in request.POST or 'knowledge_sharing_training_current_promotions' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_current_promotions_all' in request.POST  and request.POST['knowledge_sharing_training_current_promotions_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_current_promotions']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "current_promotions"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 7
                user_per.save()

            if not 'knowledge_sharing_training_upcoming_promotions_all' in request.POST and not 'knowledge_sharing_training_upcoming_promotions' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 8).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 8)
            if 'knowledge_sharing_training_upcoming_promotions_all' in request.POST or 'knowledge_sharing_training_upcoming_promotions' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_upcoming_promotions_all' in request.POST  and request.POST['knowledge_sharing_training_upcoming_promotions_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_upcoming_promotions']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "upcoming_promotions"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 8
                user_per.save()

            if not 'knowledge_sharing_training_past_promotions_all' in request.POST and not 'knowledge_sharing_training_past_promotions' in request.POST:
                UserAccessPermissonModelsPermission.objects.filter(main_function =14, sub_menu_sequence = 9).delete()
            
            user_per = UserPermission.AddEditPermission(request, 14, 9)
            if 'knowledge_sharing_training_past_promotions_all' in request.POST or 'knowledge_sharing_training_past_promotions' in request.POST:
                user_per.user_id = request.POST['user_id']
                if 'knowledge_sharing_training_past_promotions_all' in request.POST  and request.POST['knowledge_sharing_training_past_promotions_all'] == "0":
                    user_per.add = True
                    user_per.edit = True
                    user_per.view = True
                    user_per.delete = True
                else:
                    for data in dict(request.POST)['knowledge_sharing_training_past_promotions']:
                        if  data == "1":
                            user_per.add = True 
                        if data == "2":
                            user_per.edit = True
                        if data == "3":
                            user_per.view = True 
                        if data == "4":
                            user_per.delete = True
                user_per.main_function = 14
                user_per.function_level = "knowledge_sharing_training"
                user_per.sub_function_level = "past_promotions"
                user_per.sequence = 14
                user_per.sub_menu_sequence = 9
                user_per.save()

        return redirect("crm_access_user_permission_user_list")


class UploadImage(View):

    def post(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        '''Save images in folder using ckeditor'''
        file = request.FILES['upload']
        filepath = 'media/' + 'template_for_notification/' + \
            str(datetime.now().strftime('%d%m%Y%H%M%S')) + str(file)
        os.path.dirname(filepath)
        img = Image.open(file)
        img.save(filepath)
        url = SiteUrl.site_url(request)
        mainurl = str(url) + '/' + filepath
        return HttpResponse("""
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
            </script>""".format(request.GET['CKEditorFuncNum'], mainurl))


# Approval Matrix >  Define Level
class CrmApprovalMatrixiDefineApprovalLevelList(View):
    template = 'admin_template/crm_management/approval_matrix/approval_matrix_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ApprovalMatrixiDefineApprovalLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmApprovalMatrixiDefineApprovalLevel(View):
    template = 'admin_template/crm_management/approval_matrix/approval_matrix_add_level.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmApprovalMatrixiDefineApprovalLevelForm()
        else:
            data = get_object_or_404(ApprovalMatrixiDefineApprovalLevel, pk=id)
            form = CrmApprovalMatrixiDefineApprovalLevelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmApprovalMatrixiDefineApprovalLevelForm(request.POST)
            if form.is_valid():
                form = form.save()
                form.sequence = form.id
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ApprovalMatrixiDefineApprovalLevel, pk=id)
            form = CrmApprovalMatrixiDefineApprovalLevelForm(request.POST, instance = data)
            if form.is_valid():
                form = form.save()
                form.sequence = form.id
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_approval_matrix_define_approval_level_list')


class CrmApprovalMatrixiDefineApprovalLevelDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ApprovalMatrixiDefineApprovalLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_approval_matrix_define_approval_level_list')


class CrmApprovalMatrixiDefineProcessLevelList(View):
    template = 'admin_template/crm_management/approval_matrix/process_level_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ApprovalMatrixDefineProcesLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmApprovalMatrixiDefineProcessLevel(View):
    template = 'admin_template/crm_management/approval_matrix/add_edit_process_level.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmApprovalMatrixiDefineProcessLevelForm()
        else:
            data = get_object_or_404(ApprovalMatrixDefineProcesLevel, pk=id)
            form = CrmApprovalMatrixiDefineProcessLevelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmApprovalMatrixiDefineProcessLevelForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ApprovalMatrixDefineProcesLevel, pk=id)
            form = CrmApprovalMatrixiDefineProcessLevelForm(request.POST, instance = data)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_approval_matrix_define_process_level_list')


class CrmApprovalMatrixiDefineProcessLevelDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ApprovalMatrixDefineProcesLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_approval_matrix_define_process_level_list')


class CrmApprovalMatrixMapApprovalLevelWithUsersList(View):
    template = 'admin_template/crm_management/approval_matrix/map_with_process_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ApprovalMatrixMapApprovalLevelWithUsers.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate,
        }
        return render(request, self.template, context)


class CrmAddEditCrmApprovalMatrixMapApprovalLevelWithUsers(View):
    template = 'admin_template/crm_management/approval_matrix/add_edit_map_with_process.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmApprovalMatrixMapApprovalLevelWithUsersForm()
        else:
            data = get_object_or_404(ApprovalMatrixMapApprovalLevelWithUsers, pk=id)
            form = CrmApprovalMatrixMapApprovalLevelWithUsersForm(instance=data)
        context = {
            'form': form,
            'location': ManageBranch.objects.filter(is_active = True).order_by('-id'),
            'product_type':ManageProductType.objects.filter(is_active = True).order_by('-id'),
            'product_category': ManageProductCategory.objects.filter(is_active = True).order_by('-id'),
            'product_name': ManageProductName.objects.filter(is_active = True).order_by('-id'),
            'client_type': ManageClientType.objects.filter(is_active = True).order_by('-id'),
            'client_category': ManageClientCategory.objects.filter(is_active = True).order_by('-id'),
            'process_name': ApprovalMatrixDefineProcesLevel.objects.filter(is_active = True).order_by('-id'),
            'approval_level': ApprovalMatrixiDefineApprovalLevel.objects.filter(is_active = True).order_by('-id'),
            'user_location': ApprovalMatrixMapApprovalLevelWithUsersLocation.objects.filter(map_user_id = id).order_by('-id'),
            'user_product_type': MapApprovalMatrixWithUsersProductType.objects.filter(map_user_id = id).order_by('-id'),
            'user_product_category': MapApprovalMatrixWithUsersProductCategory.objects.filter(map_user_id = id).order_by('-id'),
            'user_client_type': ApprovalMatrixMapApprovalLevelWithUsersClientType.objects.filter(map_user_id = id).order_by('-id'),
            'user_client_category': ApprovalMatrixMapApprovalLevelWithUsersClientCategory.objects.filter(map_user_id = id).order_by('-id'),
            'user_process_name': MapApprovalMatrixWithusersProcessName.objects.filter(map_user_id = id).order_by('-id'),
            'user_approval_level': ApprovalMatrixMapApprovalLevelWithUsersProcessLevel.objects.filter(map_user_id = id).order_by('-id'),
            'user_product_name': MapApprovalMatrixWithUsersProductName.objects.filter(map_user_id = id).order_by('-id'),
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            if ApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = request.POST['user']):
                messages.add_message(request, messages.WARNING, "User Already Exists.")
                return redirect('crm_approval_matrix_define_mapwithprocess_list')
            extra_list =  [data for data in dict(request.POST)['location'] if data != ""] if 'location' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product_type'] if data != ""] if 'product_type' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != ""] if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""] if 'client_category' in request.POST else []
            extra_list6 = [data for data in dict(request.POST)['process_name'] if data != ""] if 'process_name' in request.POST else []
            extra_list7 = [data for data in dict(request.POST)['process_level'] if data != ""] if 'process_level' in request.POST else []
            if ApprovalMatrixMapApprovalLevelWithUsersLocation.objects.filter(location_id__in = extra_list).exists() and MapApprovalMatrixWithUsersProductType.objects.filter(product_type_id__in = extra_list1).exists() and MapApprovalMatrixWithUsersProductCategory.objects.filter(product_category_id__in = extra_list2).exists()and MapApprovalMatrixWithUsersProductName.objects.filter(product_name_id__in = extra_list3).exists() and ApprovalMatrixMapApprovalLevelWithUsersClientType.objects.filter(client_type_id__in = extra_list4).exists() and ApprovalMatrixMapApprovalLevelWithUsersClientCategory.objects.filter(client_category_id__in = extra_list5).exists() and MapApprovalMatrixWithusersProcessName.objects.filter(process_id__in = extra_list6).exists() and ApprovalMatrixMapApprovalLevelWithUsersProcessLevel.objects.filter(approval_level_id__in = extra_list7).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('crm_approval_matrix_define_mapwithprocess_list')
            form = CrmApprovalMatrixMapApprovalLevelWithUsersForm(request.POST)
            if form.is_valid():
                data = form.save()
                if 'location' in request.POST:
                    for p in  dict(request.POST)['location']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersLocation()
                        sa_data.map_user_id = data.id
                        sa_data.location_id = p
                        sa_data.save()
                if 'product_type' in request.POST:
                    for p in  dict(request.POST)['product_type']:
                        sa_data = MapApprovalMatrixWithUsersProductType()
                        sa_data.map_user_id = data.id
                        sa_data.product_type_id = p
                        sa_data.save()
                if 'product_category' in request.POST:
                    for p in  dict(request.POST)['product_category']:
                        sa_data = MapApprovalMatrixWithUsersProductCategory()
                        sa_data.map_user_id = data.id
                        sa_data.product_category_id = p
                        sa_data.save()
                if 'product_name' in request.POST:
                    for p in  dict(request.POST)['product_name']:
                        sa_data = MapApprovalMatrixWithUsersProductName()
                        sa_data.map_user_id = data.id
                        sa_data.product_name_id = p
                        sa_data.save()
                if 'client_type' in request.POST:
                    for p in  dict(request.POST)['client_type']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersClientType()
                        sa_data.map_user_id = data.id
                        sa_data.client_type_id = p
                        sa_data.save()
                if 'client_category' in request.POST:
                    for p in  dict(request.POST)['client_category']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersClientCategory()
                        sa_data.map_user_id = data.id
                        sa_data.client_category_id = p
                        sa_data.save()
                if 'process_name' in request.POST:
                    for p in  dict(request.POST)['process_name']:
                        sa_data = MapApprovalMatrixWithusersProcessName()
                        sa_data.map_user_id = data.id
                        sa_data.process_id = p
                        sa_data.save()
                if 'process_level' in request.POST:
                    for p in  dict(request.POST)['process_level']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersProcessLevel()
                        sa_data.map_user_id = data.id
                        sa_data.approval_level_id = p
                        sa_data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            if ApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = request.POST['user'], id = id):
               pass
            else:
                if ApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = request.POST['user']):
                    messages.add_message(request, messages.WARNING, "User Already Exists.")
                    return redirect('crm_approval_matrix_define_mapwithprocess_list')
            extra_list =  [data for data in dict(request.POST)['location'] if data != ""] if 'location' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product_type'] if data != ""] if 'product_type' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != ""] if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""] if 'client_category' in request.POST else []
            extra_list6 = [data for data in dict(request.POST)['process_name'] if data != ""] if 'process_name' in request.POST else []
            extra_list7 = [data for data in dict(request.POST)['process_level'] if data != ""] if 'process_level' in request.POST else []
            if ApprovalMatrixMapApprovalLevelWithUsersLocation.objects.filter(~Q(map_user_id = id), location_id__in = extra_list).exists() and MapApprovalMatrixWithUsersProductType.objects.filter(~Q(map_user_id = id),product_type_id__in = extra_list1).exists() and MapApprovalMatrixWithUsersProductCategory.objects.filter(~Q(map_user_id = id),product_category_id__in = extra_list2).exists()and MapApprovalMatrixWithUsersProductName.objects.filter(~Q(map_user_id = id),product_name_id__in = extra_list3).exists() and ApprovalMatrixMapApprovalLevelWithUsersClientType.objects.filter(~Q(map_user_id = id),client_type_id__in = extra_list4).exists() and ApprovalMatrixMapApprovalLevelWithUsersClientCategory.objects.filter(~Q(map_user_id = id),client_category_id__in = extra_list5).exists() and MapApprovalMatrixWithusersProcessName.objects.filter(~Q(map_user_id = id),process_id__in = extra_list6).exists() and ApprovalMatrixMapApprovalLevelWithUsersProcessLevel.objects.filter(~Q(map_user_id = id),approval_level_id__in = extra_list7).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('crm_approval_matrix_define_mapwithprocess_list')
            
            get_object_or_404(ApprovalMatrixMapApprovalLevelWithUsers, pk=id).delete()
            form = CrmApprovalMatrixMapApprovalLevelWithUsersForm(request.POST)
            if form.is_valid():
                data = form.save()
                if 'location' in request.POST:
                    for p in  dict(request.POST)['location']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersLocation()
                        sa_data.map_user_id = data.id
                        sa_data.location_id = p
                        sa_data.save()
                if 'product_type' in request.POST:
                    for p in  dict(request.POST)['product_type']:
                        sa_data = MapApprovalMatrixWithUsersProductType()
                        sa_data.map_user_id = data.id
                        sa_data.product_type_id = p
                        sa_data.save()
                if 'product_category' in request.POST:
                    for p in  dict(request.POST)['product_category']:
                        sa_data = MapApprovalMatrixWithUsersProductCategory()
                        sa_data.map_user_id = data.id
                        sa_data.product_category_id = p
                        sa_data.save()
                if 'product_name' in request.POST:
                    for p in  dict(request.POST)['product_name']:
                        sa_data = MapApprovalMatrixWithUsersProductName()
                        sa_data.map_user_id = data.id
                        sa_data.product_name_id = p
                        sa_data.save()
                if 'client_type' in request.POST:
                    for p in  dict(request.POST)['client_type']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersClientType()
                        sa_data.map_user_id = data.id
                        sa_data.client_type_id = p
                        sa_data.save()
                if 'client_category' in request.POST:
                    for p in  dict(request.POST)['client_category']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersClientCategory()
                        sa_data.map_user_id = data.id
                        sa_data.client_category_id = p
                        sa_data.save()
                if 'process_name' in request.POST:
                    for p in  dict(request.POST)['process_name']:
                        sa_data = MapApprovalMatrixWithusersProcessName()
                        sa_data.map_user_id = data.id
                        sa_data.process_id = p
                        sa_data.save()
                if 'process_level' in request.POST:
                    for p in  dict(request.POST)['process_level']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersProcessLevel()
                        sa_data.map_user_id = data.id
                        sa_data.approval_level_id = p
                        sa_data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_approval_matrix_define_mapwithprocess_list')


class CrmApprovalMatrixMapApprovalLevelWithUsersDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ApprovalMatrixMapApprovalLevelWithUsers.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_approval_matrix_define_mapwithprocess_list')


# ****************** Product Category **************************
class CrmManageProductCategoryList(View):
    template = 'admin_template/crm_management/product_set_up/product_category_list.html'
    pagesize = 10
   
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageProductCategory.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmManageProductCategoryAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_category_add.html'

    def get(self,request):
        form = ManageProductCategoryForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)           

    def post(self, request, branch_id = None):
        form = ManageProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Data already exists!!')
        return redirect('crm_productcategorylist')


def CrmManageProductCategoryEdit(request, id):
    manageproduct = get_object_or_404(ManageProductCategory, pk=id)
    if request.method == "POST":
        form = ManageProductCategoryForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!')
            return redirect('crm_productcategorylist')
        else:
            messages.add_message(request, messages.SUCCESS, 'Data already exists!!')
            return redirect('crm_productcategorylist')
    else:
        form = ManageProductCategoryForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/product_category_add.html', {'form': form})


class CrmManageProductCategoryDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageProductCategory.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_productcategorylist')


# Display user details for usersetup


class ViewDepartmentList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/view_department.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDepartment.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(department__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)



class ViewDesignationList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/view_Designation.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDesignation.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(designation__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})



class ViewResponsibilityList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/view_responsibility.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageResponsibility.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(responsibilities__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template, {'responselistquery': report_paginate})


class ViewRoleManagementList(View):
    template = 'admin_template/crm_management/company_set_up/view_role_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = RoleMangement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})





class UserTypeList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/user_type_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UserType.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})



class UserTypeAdd(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/user_type_add.html'

    def get(self,request):
        form = UserTypeAddForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        if request.method == 'POST':
            form = UserTypeAddForm(request.POST, request.FILES)
            if form.is_valid():
                 
                messages.add_message(request, messages.SUCCESS,
                                     ('Successfully added!! ')) 
                user_type_form_data = form.save()

                if user_type_form_data.user_type == "Agent":
                    user_type_form_data.is_agent = True


                elif user_type_form_data.user_type == "Sales":
                    user_type_form_data.is_sales = True

                elif user_type_form_data.user_type == "Verification Agency":
                    user_type_form_data.is_sales = True
                user_type_form_data.save()


                return redirect('usertypelist')
            else:
                messages.add_message(request, messages.WARNING,
                                     ('Not Added!'))
        else:
            form = UserTypeAddForm()
        return render(request, 'admin_template/los_management/user_type_add.html', {'form': form})



def UserTypeEdit(request, id):
    manageuser = get_object_or_404(UserType, pk=id)
    form = UserTypeAddForm(request.POST, instance=manageuser)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('usertypelist')
    else:
        form = UserTypeAddForm(instance=manageuser)
    return render(request, 'admin_template/crm_management/company_set_up/user_set_up/manage_responsibility/user_type_add.html', {'form': form})


class UserTypeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UserType.objects.filter(id = id).update(is_agent=1)
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('usertypelist')


#-------------------------------------Define Unit Value -----------------------------------

class ManageUnitValueList(View):
    template = 'admin_template/crm_management/product_set_up/unit_value_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UnitValue.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ManageUnitValueAdd(View):
    template = 'admin_template/crm_management/product_set_up/unit_value_add.html'

    def get(self,request):
        form = UnitValueForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):

        form = UnitValueForm(request.POST, request.FILES)
        if form.is_valid():
             
            messages.add_message(request, messages.SUCCESS,
                                 ('Successfully added!! ')) 
            form.save()

            
        else:
            messages.add_message(request, messages.WARNING,
                                 ('Data already exists!!'))
        return redirect('unitvaluelist')


def ManageUnitValueEdit(request, id):

    manageproduct = get_object_or_404(UnitValue, pk=id)
    if request.method == "POST":
        form = UnitValueForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('unitvaluelist')
    else:
        form = UnitValueForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/unit_value_add.html', {'form': form})


class ManageUnitValueDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UnitValue.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('unitvaluelist')



#################  allocational location Rajesh
# Define Process
#@2
class ManageProcessAllocationList(View):
    # template = 'admin_template/los_management/data-allocation/manage_allocation/define_process_list.html'
    template ='admin_template/crm_management/data_allocation/allocation_matrix/define_process_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = DefineProcessAllocation.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})

class ManageProcessAllocationAdd(View):
    # template = 'admin_template/los_management/data-allocation/manage_allocation/define_process_add.html'
    template ='admin_template/crm_management/data_allocation/allocation_matrix/define_process_add.html'
    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        form = DefineProcessAllocationForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):

        form = DefineProcessAllocationForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,
                                 ('Successfully added!! ')) 
            form.save()
        else:
            messages.add_message(request, messages.WARNING,
                                 ('Data already exists!!'))
        return redirect('defineprocesslist')


def ManageProcessAllocationEdit(request, id):
    manageproduct = get_object_or_404(DefineProcessAllocation, pk=id)
    if request.method == "POST":
        form = DefineProcessAllocationForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('defineprocesslist')
    else:
        form = DefineProcessAllocationForm(instance=manageproduct)
    # return render(request, 'admin_template/los_management/data-allocation/manage_allocation/define_process_add.html', {'form': form})
    return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/define_process_add.html', {'form': form})

class ManageProcessAllocationDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        
        get_report = DefineProcessAllocation.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('defineprocesslist')

# END 1

        

# 2
class AllocationManagementUpdateReallocationCriteriaList(View):
    # template = 'admin_template/los_management/approval_matrix/reallocation_criteria_list.html'
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/reallocation_criteria_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = AllocationManagementUpdateReallocationCriteria.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def AddAllocationManagementUpdateReallocationCriteria(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = AllocationManagementUpdateReallocationCriteriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING,'Already Exists')
        return redirect('approval_matrix_reallocation_criteria_list')

    else:
        form = AllocationManagementUpdateReallocationCriteriaForm()
    # return render(request, 'admin_template/los_management/approval_matrix/reallocation_criteria_add.html' ,{'form':form})
    return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/reallocation_criteria_add.html', {'form': form})

def EditAllocationManagementUpdateReallocationCriteria(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(AllocationManagementUpdateReallocationCriteria, pk=id)
    if request.method == "POST":
        form = AllocationManagementUpdateReallocationCriteriaForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING,'Already Exists')
        return redirect('approval_matrix_reallocation_criteria_list')
    else:
        form = AllocationManagementUpdateReallocationCriteriaForm(instance=company)
    # return render(request, 'admin_template/los_management/approval_matrix/reallocation_criteria_add.html', {'form': form})
    return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/reallocation_criteria_add.html', {'form': form})


class EditAllocationManagementUpdateReallocationCriteriaDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationManagementUpdateReallocationCriteria.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('approval_matrix_reallocation_criteria_list')

#2
# ---------------------------------------------------------------------------
#@1
class AllocationManagementManageReallocationList(View):
    # template = 'admin_template/los_management/approval_matrix/manage_reallocation_list.html'
    template ='admin_template/crm_management/data_allocation/allocation_matrix/manage_reallocation_list.html'
    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        
        responselistquery = AllocationManagementManageReallocation.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)

# ##11
# def AddAllocationManagementManageReallocation(request):
#     # import pdb;pdb.set_trace()
#     if not request.user.is_superuser:
#         return redirect('adminlogin')
#     if request.method == 'POST':        
#         form = AllocationManagementManageReallocationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form = form.save()
#             if 'process_name' in request.POST:
#                 for p in  dict(request.POST).get('process_name'):
#                     data = AllocationProcessMultipleReallocation()
#                     data.allocation_reallocation_id = form.id
#                     data.process_name_id = p
#                     data.save()
#             messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
#         else:
#             messages.add_message(request, messages.WARNING,'Already Exists')
#         return redirect('approval_matrix_manage_reallocation_list')

#     else:
#         form = AllocationManagementManageReallocationForm()
#     # return render(request, 'admin_template/los_management/approval_matrix/manage_reallocation_add.html', {'form':form})
#     return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/manage_reallocation_add.html', {'form':form})

def AddAllocationManagementManageReallocation(request):
    if request.method == 'POST':        
        form = AllocationManagementManageReallocationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            # if 'process_name' in request.POST:
            #     for p in  dict(request.POST).get('process_name'):
            #         data = AllocationProcessMultipleReallocation()
            #         data.allocation_reallocation_id = form.id
            #         data.process_name_id = p
            #         data.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING,'Already Exists')
        return redirect('approval_matrix_manage_reallocation_list')

    else:
        form = AllocationManagementManageReallocationForm()
    return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/manage_reallocation_add.html', {'form':form})



def EditAllocationManagementManageReallocation(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(AllocationManagementManageReallocation, pk=id)
    if request.method == "POST":
        form = AllocationManagementManageReallocationForm(request.POST, instance=company)
        if form.is_valid():
            form = form.save()
            process_id = []
            if 'process_name' in request.POST:
                for p in  dict(request.POST).get('process_name'):
                    try:
                        data = AllocationProcessMultipleReallocation.objects.get(process_name_id = p, allocation_reallocation_id = form.id)
                    except Exception as e:
                        data = AllocationProcessMultipleReallocation()
                        data.allocation_reallocation_id = form.id
                        data.process_name_id = p
                        data.save()
                    process_id.append(p)
            AllocationProcessMultipleReallocation.objects.filter(~Q(process_name_id__in = process_id), allocation_reallocation_id = id).delete()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING,'Already Exists')
        return redirect('approval_matrix_manage_reallocation_list')
    else:
        form = AllocationManagementManageReallocationForm(instance=company)
        get_process_name = AllocationMatrixLeadAllocation.objects.get(id = company.existing_user_id)
        context = {
            'form': form,
            'get_user_lead_allocation': get_process_name.leadallocationprocessname_set.all(),
            'details': company
        }
        # return render(request, 'admin_template/los_management/approval_matrix/manage_reallocation_edit.html',context)
        return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/manage_reallocation_edit.html',context)

class EditAllocationManagementManageReallocationDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationManagementManageReallocation.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('approval_matrix_manage_reallocation_list')
##3
# Allocation Matrix Lead Allocation

#4
class AllocationMatrixLeadAllocationList(View):
    #template = 'admin_template/los_management/data_allocation/allow_set_up_matrix_lead_allocation_list.html'
    template ='admin_template/crm_management/data_allocation/allocation_matrix/allow_set_up_matrix_lead_allocation_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)

    def get(self, request):
        # import pdb;pdb.set_trace()
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AllocationMatrixLeadAllocation.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddAllocationMatrixLeadAllocation(View):

    template   = 'admin_template/crm_management/data_allocation/allocation_matrix/add_allow_set_up_matrix_lead_allocation.html'
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, allocationsetuid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_all_mapped_cities = ''
        if allocationsetuid is None:
            data = ''
            allocationsetuid = None
            city = ''
        else:
            data = get_object_or_404(AllocationMatrixLeadAllocation, pk=allocationsetuid)
            allocationsetuid = allocationsetuid
            map_cities = []
#123
            append_branch_ids = [ data.branch_allocated_id for data in UserMultipleBranch.objects.filter(user=data.user.id)] 
            get_all_mapped_cities =[ p.id for p in MapCityBranches.objects.filter(branch_id__in = append_branch_ids)]
            city = MapCityMultipleWithBranches.objects.filter(city_map__in = get_all_mapped_cities).order_by('-id')
        context = {
            'data': data, 
            'allocationsetuid': allocationsetuid,
            'user_set_up': User.objects.filter(is_active =True, is_superuser=0,is_client=0,is_agent=0,is_verification_agency=0,is_legal_team=0,is_technical_team=0,is_valuation_team=0,is_fraud_investigation_team=0,is_document_verification_team=0).order_by('-id'),
            'product_set_up': DefineProductType.objects.filter(is_active =True).order_by('-id'),
            'client_type': ManageClientType.objects.filter(is_active =True).order_by('-id'),
            'client_category': ManageClientCategory.objects.filter(is_active=True).order_by('-id'),
            'product_category': ManageProductCategory.objects.filter(is_active=True).order_by('-id'),
            'product_name': ManageProductName.objects.filter(is_active=True).order_by('-id'),
            'process_name': DefineProcessAllocation.objects.values('process_name').annotate(Count('process_name')).filter(is_active = True),
            'city':   city,
            'get_all_cities': AllocationMatrixLeadUserCity.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_product_type': AllocationUserDefineProductType.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_product_category': AllocationUserProductCategory.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_product_name': AllocationUserProductName.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_client_type': AllocationUserClientType.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_client_category': AllocationUserClientCategory.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_process_name': LeadAllocationProcessName.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
        }
        return render(request, self.template, context)

    def post(self, request, allocationsetuid = None):
        
        if request.POST['allocationsetuid'] is None or request.POST['allocationsetuid'] == "None":
            if AllocationMatrixLeadAllocation.objects.filter(user_id = request.POST['user']):
                messages.add_message(request, messages.WARNING, "User Already Exists.")
                return redirect('leadallocationallocationmatrixlist')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != ""]  if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            extra_list6 = [data for data in dict(request.POST)['process_name'] if data != ""]  if 'process_name' in request.POST else []
            if LeadAllocationProcessName.objects.filter(process_name_id__in = extra_list6).exists() and AllocationMatrixLeadUserCity.objects.filter(city_id__in = extra_list).exists() and AllocationUserDefineProductType.objects.filter(product_type_id__in = extra_list1).exists() and AllocationUserProductCategory.objects.filter(product_category_id__in =extra_list2).exists() and AllocationUserProductName.objects.filter(product_name_id__in =extra_list3).exists() and AllocationUserClientType.objects.filter(client_type_id__in =extra_list4).exists() and AllocationUserClientCategory.objects.filter(client_category_id__in = extra_list5).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('leadallocationallocationmatrixlist')
            save_data = AllocationMatrixLeadAllocation()
            messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
        else:
            allocationsetuid = request.POST['allocationsetuid']
            if AllocationMatrixLeadAllocation.objects.filter(user_id = request.POST['user'], id =allocationsetuid):
                pass
            else:
                if AllocationMatrixLeadAllocation.objects.filter(user_id = request.POST['user']):
                    messages.add_message(request, messages.WARNING, "User Already Exists.")
                    return redirect('leadallocationallocationmatrixlist')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            extra_list4 = [data for data in dict(request.POST)['client_type'] if data != "" ]  if 'client_type' in request.POST else []
            extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            extra_list6 = [data for data in dict(request.POST)['process_name'] if data != ""]  if 'process_name' in request.POST else []
            if LeadAllocationProcessName.objects.filter(~Q(lead_allocation_id= allocationsetuid), process_name__in = extra_list6).exists() and AllocationMatrixLeadUserCity.objects.filter(~Q(lead_allocation_id= allocationsetuid), city_id__in = extra_list).exists() and LeadAllocationProductType.objects.filter(~Q(lead_allocation_id= allocationsetuid),product_type_id__in = extra_list1).exists() and LeadAllocationProductCategory.objects.filter(~Q(lead_allocation_id= allocationsetuid),product_category_id__in =extra_list2).exists() and LeadAllocationProductName.objects.filter(~Q(lead_allocation_id= allocationsetuid), product_name_id__in =extra_list3).exists() and LeadAllocationClientType.objects.filter(~Q(lead_allocation_id= allocationsetuid), client_type_id__in =extra_list4).exists() and LeadAllocationClientCategory.objects.filter(~Q(lead_allocation_id= allocationsetuid), client_category_id__in = extra_list5).exists():
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('leadallocationallocationmatrixlist')
            save_data = get_object_or_404(AllocationMatrixLeadAllocation, pk=allocationsetuid)
            messages.add_message(request, messages.SUCCESS, "Record update Successfully.")
        save_data.user_id = request.POST['user']
        
        save_data.save()
        id = save_data.id
        append_city = []
        # Save All Matrix City
        if 'city' in request.POST:
            for data in dict(request.POST)['city']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixLeadUserCity.objects.get(lead_allocation_id = id, city_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    except AllocationMatrixLeadUserCity.DoesNotExist:
                        save_city = AllocationMatrixLeadUserCity()
                        save_city.lead_allocation_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixLeadUserCity.objects.filter(~Q(city_id__in = append_city) , lead_allocation_id = id ).delete()
        # Save Product Type
        append_city = []
        if 'product' in request.POST:
            for data in dict(request.POST)['product']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserDefineProductType.objects.get(lead_allocation_id = id, product_type_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    except AllocationUserDefineProductType.DoesNotExist:
                        save_city = AllocationUserDefineProductType()
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserDefineProductType.objects.filter(~Q(product_type_id__in = append_city) , lead_allocation_id = id).delete()
        
        # Save Product Category
        append_city = []
        if 'product_category' in request.POST:
            for data in dict(request.POST)['product_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserProductCategory.objects.get(lead_allocation_id = id, product_category_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    except AllocationUserProductCategory.DoesNotExist:
                        save_city = AllocationUserProductCategory()
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserProductCategory.objects.filter(~Q(product_category_id__in = append_city) , lead_allocation_id = id).delete()
        
        # Save Product Name
        append_city1 = []
        if 'product_name' in request.POST:
            for data in dict(request.POST)['product_name']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserProductName.objects.get(lead_allocation_id = id, product_name_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    except AllocationUserProductName.DoesNotExist:
                        save_city = AllocationUserProductName()
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    append_city1.append(data)
            AllocationUserProductName.objects.filter(~Q(product_name_id__in = append_city1) , lead_allocation_id = id).delete()

        # Client Type 
        append_city = []
        if 'client_type' in request.POST:
            for data in dict(request.POST)['client_type']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserClientType.objects.get(lead_allocation_id = id, client_type_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    except AllocationUserClientType.DoesNotExist:
                        save_city = AllocationUserClientType()
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserClientType.objects.filter(~Q(client_type_id__in = append_city) , lead_allocation_id = id).delete()

        # Client Category 
        append_city = []
        if 'client_category' in request.POST:
            for data in dict(request.POST)['client_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserClientCategory.objects.get(lead_allocation_id = id, client_category_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    except AllocationUserClientCategory.DoesNotExist:
                        save_city = AllocationUserClientCategory()
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserClientCategory.objects.filter(~Q(client_category_id__in = append_city) , lead_allocation_id = id).delete()
        process_name = []
        if 'process_name' in request.POST:
            for data in dict(request.POST)['process_name']:
                if str(data) != "":
                    try:
                        save_city = LeadAllocationProcessName.objects.get(lead_allocation_id = id, process_name_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.process_name_id = data
                        save_city.save()
                    except LeadAllocationProcessName.DoesNotExist:
                        save_city = LeadAllocationProcessName()
                        save_city.lead_allocation_id = save_data.id
                        save_city.process_name_id = data
                        save_city.save()
                    process_name.append(data)
            LeadAllocationProcessName.objects.filter(~Q(process_name_id__in = process_name) , lead_allocation_id = id).delete()



        return redirect('leadallocationallocationmatrixlist')


class AllocationMatrixLeadDelete(View):
    def get(self, request, allocationsetuid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        
        get_report = AllocationMatrixLeadAllocation.objects.filter(id = allocationsetuid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('leadallocationallocationmatrixlist')


#@!!
# Map Joint Approval Process

class MapApprovallevelWithJointUserList(View):
    
    template   = 'admin_template/crm_management/data_allocation/allocation_matrix/map_approval_level_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = MapApprovalLevelWithJointApproval.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


####@!!
class AddEditMapApprovallevelWithJointUser(View):
   
    template   = 'admin_template/crm_management/data_allocation/allocation_matrix/map_approval_level_add.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = MapApprovalLevelWithJointApprovalForm()
        else:
            data = get_object_or_404(MapApprovalLevelWithJointApproval, pk=id)
            form = MapApprovalLevelWithJointApprovalForm(instance=data)
        context = {
            'form': form,
            'process_name': DefineProcessAllocation.objects.values('process_name').annotate(Count('process_name')).filter(is_active = True),
            'approval_level':ApprovalMatrixiDefineApprovalLevel.objects.filter(is_active = True).order_by('-id'),
            'user_process_name':MapApprovalMatrixWithusersProcessName.objects.filter(map_user_id=id),
            'user_approval_level':ApprovalMatrixMapApprovalLevelWithUsersProcessLevel.objects.filter(map_user_id= id),
            
            'user' : User.objects.filter(manual_create_admin = 1, is_active =True, is_superuser=0,is_client=0,is_agent=0,is_verification_agency=0,is_legal_team=0,is_technical_team=0,is_valuation_team=0,is_fraud_investigation_team=0,is_document_verification_team=0),
            'user_joint_applicant': MapApprovalLevelWithJointApprovalUsers.objects.filter(map_joint_user_id= id),    #ok
            }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:

            form = MapApprovalLevelWithJointApprovalForm(request.POST)
            if form.is_valid():
                data=form.save()
                if 'process_name' in request.POST:
                    for p in  dict(request.POST)['process_name']:
                        sa_data = MapApprovalMatrixWithusersProcessName()
                        sa_data.map_joint_user_id = data.id
                        sa_data.process_name_id = p
                        sa_data.save()

                if 'process_level' in request.POST:
                    for p in  dict(request.POST)['process_level']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersProcessLevel()
                        sa_data.map_joint_user_id = data.id
                        sa_data.approval_level_id = p
                        sa_data.save()
                
                if 'user_name' in request.POST:
                    for p in dict(request.POST)['user_name']:
                        data_save1 = MapApprovalLevelWithJointApprovalUsers()
                        data_save1.map_joint_user_id = data.id
                        data_save1.users_id = p
                        data_save1.save()

                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data Already Exists.")
        else:
            data = get_object_or_404(MapApprovalLevelWithJointApproval, pk=id)
            form = MapApprovalLevelWithJointApprovalForm(request.POST, instance = data)
            if form.is_valid():
                data=form.save()
                MapApprovalMatrixWithusersProcessName.objects.filter(map_joint_user_id=data.id).delete()
                ApprovalMatrixMapApprovalLevelWithUsersProcessLevel.objects.filter(map_joint_user_id=data.id).delete()
                MapApprovalLevelWithJointApprovalUsers.objects.filter(map_joint_user_id=data.id).delete()
                if 'process_name' in request.POST:
                    for p in  dict(request.POST)['process_name']:
                        sa_data = MapApprovalMatrixWithusersProcessName()
                        sa_data.map_joint_user_id = data.id
                        sa_data.process_name_id = p
                        sa_data.save()

                if 'process_level' in request.POST:
                    for p in  dict(request.POST)['process_level']:
                        sa_data = ApprovalMatrixMapApprovalLevelWithUsersProcessLevel()
                        sa_data.map_joint_user_id = data.id
                        sa_data.approval_level_id = p
                        sa_data.save()
                if 'user_name' in request.POST:
                    for p in dict(request.POST)['user_name']:
                        data_save1 = MapApprovalLevelWithJointApprovalUsers()
                        data_save1.map_joint_user_id = data.id
                        data_save1.users_id = p
                        data_save1.save()

                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('mapapprovaluser_list')


class MapApprovallevelWithJointUserDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = MapApprovalLevelWithJointApproval.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('mapapprovaluser_list')

#@!!

#@11
class EscalationManagementManageEscalationList(View):
    # template = 'admin_template/los_management/notification_set_up/setup_escalation_matrix/manage_escalation_list.html'
    template = 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/manage_escalation_list.html'

    pagesize = 10


    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = EscalationManagementManageEscalation.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)

def AddEscalationManagementManageEscalation(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':        
        form = EscalationManagementManageEscalationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            # if  'process_name' in request.POST:
            #     for p in dict(request.POST)['process_name']:
            #         dat = ManageEscalationProcessName()
            #         dat.escalation_id = form.id
            #         dat.process_name_id = p
            #         dat.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
        else:
            messages.add_message(request, messages.WARNING,'Already Exists')
        return redirect('escalation_manage_escalation_list')

    else:
        form = EscalationManagementManageEscalationForm()
        context = {
            'form':form
        }
    return render(request, 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/manage_escalation_add.html', context)


def EditEscalationManagementManageEscalation(request, id):
    company = get_object_or_404(EscalationManagementManageEscalation, pk=id)
    if request.method == "POST":
        form = EscalationManagementManageEscalationForm(request.POST, instance=company)
        if form.is_valid():
            form = form.save()
            data = []
            if  'process_name' in request.POST:
                for p in dict(request.POST)['process_name']:
                    try:
                        dat = ManageEscalationProcessName.objects.get(escalation_id = form.id, process_name_id = p)
                        dat.escalation_id = form.id
                        dat.process_name_id = p
                        dat.save()
                    except ManageEscalationProcessName.DoesNotExist:
                        dat = ManageEscalationProcessName()
                        dat.escalation_id = form.id
                        dat.process_name_id = p
                        dat.save()
                    data.append(p)
                ManageEscalationProcessName.objects.filter(~Q(process_name_id__in = data), escalation_id = form.id).delete()
            messages.add_message(request, messages.SUCCESS, 'Successfully updated!!') 
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists')
        return redirect('escalation_manage_escalation_list')
    else:
        form = EscalationManagementManageEscalationForm(instance=company)
        get_process_name = AllocationMatrixLeadAllocation.objects.get(id = company.user_id)
        context = {
            'form': form,
            'id': id,
            'company': company,
            'get_user_allocattion_process' : get_process_name.leadallocationprocessname_set.all()
        }
    return render(request, 'admin_template/crm_management/notification_set_up/setup_escalation_matrix/manage_escalation_add.html', context)

class EditEscalationManagementManageEscalationDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = EscalationManagementManageEscalation.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('escalation_manage_escalation_list')

#@1



class ManageMonthEndProcessList(View):

    # template = 'admin_template/los_management/month-end/manage_process_list.html'
    template = 'admin_template/crm_management/month-end/manage_process_list.html'
    pagesize = 10
    def get(self,request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        responselistquery = ManageMonthEndProcess.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, responselistquery, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


def ManageMonthEndProcessAdd(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    if request.method == 'POST':
        extra_list2 = [data for data in dict(request.POST)['process_name'] if data != ""] if 'process_name' in request.POST else []
        form = ManageMonthEndProcessForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()    
            if 'process_name' in request.POST:
                for user_id in dict(request.POST)['process_name']:
                    data_save1 = ManageMonthEndProcessName()
                    data_save1.names_id = data.id
                    data_save1.process_name_level_id = user_id
                    data_save1.save()
            messages.add_message(request, messages.SUCCESS,'Successfully added!!') 
            return redirect('managemonthendprocesslist')
    else:
        form = ManageMonthEndProcessForm()
    context = {
        'form':form,
        # 'process_name':ApprovalMatrixDefineProcesLevel.objects.values('process_name').annotate(Count('process_name')).filter(is_active = True)
    }
    return render(request, 'admin_template/crm_management/month-end/manage_process_add.html', context)


def ManageMonthEndProcessEdit(request, id):
    if not request.user.is_superuser:
        return redirect('adminlogin')
    company = get_object_or_404(ManageMonthEndProcess, pk=id)
    if request.method == "POST":
        extra_list2 = [data for data in dict(request.POST)['process_name'] if data != ""] if 'process_name' in request.POST else []
        form = ManageMonthEndProcessForm(request.POST, instance=company)
        if form.is_valid():
            data = form.save()
            ManageMonthEndProcessName.objects.filter(names_id = data.id).delete()            
            if 'process_name' in request.POST:
                for user_id in dict(request.POST)['process_name']:
                    data_save1 = ManageMonthEndProcessName()
                    data_save1.names_id = data.id
                    data_save1.process_name_level_id = user_id
                    data_save1.save()
            messages.add_message(request, messages.SUCCESS,'Successfully updated!!') 
            return redirect('managemonthendprocesslist')
    else:
        form = ManageMonthEndProcessForm(instance=company)
    
    context = {
        'form':form,
        'company':company,
        'escalation_process_name': ManageMonthEndProcessName .objects.filter(names_id = id),
        'process_name':ApprovalMatrixDefineProcesLevel.objects.values('process_name').annotate(Count('process_name')).filter(is_active = False)
    }
    return render(request, 'admin_template/crm_management/month-end/manage_process_add.html', context)

class ManageMonthEndProcessDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageMonthEndProcess.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted Successfully.")
        return redirect('managemonthendprocesslist')



############# Update Tax Rates 
class CrmUpdateTaxRatesList(View):
    template = 'admin_template/crm_management/product_set_up/product_setup_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageUpdateTaxRates.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmUpdateTaxRatesAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_setup_add.html'

    def get(self,request):
        form = ManageUpdateTaxRatesForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            


    def post(self, request):
        
        form = ManageUpdateTaxRatesForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            return redirect('crmupdatetaxlist')
        else:
            messages.add_message(request, messages.WARNING, 'Data already exists!!')
        return redirect('crmupdatetaxlist')


def CrmUpdateTaxRatesEdit(request, id):
    manageproduct = get_object_or_404(ManageUpdateTaxRates, pk=id)
    if request.method == "POST":
        form = ManageUpdateTaxRatesForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Updated!! ')
            return redirect('crmupdatetaxlist')
        else:
            messages.add_message(request, messages.WARNING, 'Already Exists.')
            return redirect('crmupdatetaxlist')
    else:
        form = ManageUpdateTaxRatesForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/edit_product.html', {'form': form})


class CrmUpdateTaxRatesDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageUpdateTaxRates.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crmupdatetaxlist')



###########  Manage Pricing 


class ManagePricinglist(View):
    template = 'admin_template/crm_management/product_set_up/product_facility_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePricing.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ManagePricingAdd(View):
    template = 'admin_template/crm_management/product_set_up/product_facility_add.html'

    def get(self,request):
        form = ManagePricingForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):

        form = ManagePricingForm(request.POST, request.FILES)
        if form.is_valid():
             
            messages.add_message(request, messages.SUCCESS,
                                 ('Successfully added!! ')) 
            form.save()

            
        else:
            messages.add_message(request, messages.WARNING,
                                 ('Data already exists!!'))
        return redirect('managepricinglist')


def ManagePricingEdit(request, id):

    manageproduct = get_object_or_404(ManagePricing, pk=id)
    if request.method == "POST":
        form = ManagePricingForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('managepricinglist')
    else:
        form = ManagePricingForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/product_set_up/product_facility_add.html', {'form': form})


class ManagePricingDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePricing.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('managepricinglist')
###############

# UpdateEmploymentType
class CrmUpdateEmploymentTypeList(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/update_employee_type/emptype_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageUpdateEmploymentType.objects.all().order_by('-id')
        if request.GET.get('search') != None and str(request.GET.get('search')) != "":
            get_report = get_report.filter(department__icontains = request.GET.get('search'))
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmUpdateEmploymentTypeAdd(View):
    template = 'admin_template/crm_management/company_set_up/user_set_up/update_employee_type/emptype_add.html'
    def get(self,request):
        form = ManageUpdateEmploymentTypeForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = ManageUpdateEmploymentTypeForm(request.POST)
        if form.is_valid(): 
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ')
            form.save()
        else:
            messages.add_message(request, messages.WARNING, 'Department already exists!!')
        return redirect('crmupdateemploymentypelist')


def CrmUpdateEmploymentTypeEdit(request, delete):
    company = get_object_or_404(ManageUpdateEmploymentType, pk=delete)
    if request.method == "POST":
        form = ManageUpdateEmploymentTypeForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added!! ') 
            return redirect('crmupdateemploymentypelist')
        else:
            messages.add_message(request, messages.WARNING, 'Department already exists!!')
            return redirect('crmupdateemploymentypelist')
    else:
        form = ManageUpdateEmploymentTypeForm(instance=company)
    return render(request, 'admin_template/crm_management/company_set_up/user_set_up/depart_designation_master/department_add.html', {'form': form})


class CrmUpdateEmploymentTypedelete(View):
    def get(self, request, delete):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageUpdateEmploymentType.objects.filter(id = delete).delete()
        messages.add_message(request, messages.SUCCESS, "Data Deleted Successfully.")
        return redirect('crmupdateemploymentypelist')


#### Manage Country
class ManageCountryList(View):
    template = 'admin_template/crm_management/country/country_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = Country.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ManageCountryAdd(View):
    template = 'admin_template/crm_management/country/country_add.html'

    def get(self,request):
        form = CountryForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('countrylist')


def ManageCountryEdit(request, id):

    manageproduct = get_object_or_404(Country, pk=id)
    if request.method == "POST":
        form = CountryForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('countrylist')
    else:
        form = CountryForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/country/country_add.html', {'form': form})


class ManageCountryDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = Country.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('countrylist')

#########State


class ManageStateList(View):
    template = 'admin_template/crm_management/company_set_up/state/state_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = State.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ManageStateAdd(View):
    template = 'admin_template/crm_management/company_set_up/state/state_add.html'

    def get(self,request):
        form = StateForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = StateForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('statelist')


def ManageStateEdit(request, id):

    manageproduct = get_object_or_404(State, pk=id)
    if request.method == "POST":
        form = StateForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('statelist')
    else:
        form = StateForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/company_set_up/state/state_add.html', {'form': form})


class ManageStateDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = State.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('statelist')


################
#
class UpdateTemplateTypeList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatetemplatetype_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateTemplateType.objects.all().order_by("-id")
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class UpdateTemplateTypeAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatetemplatetypelist_add.html'

    def get(self,request):
        form = UpdateTemplateTypeForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        
        if request.method=='POST':
            form = UpdateTemplateTypeForm(request.POST, request.FILES)
            if form.is_valid():             
                messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
                form.save()   
            else:
                messages.add_message(request, messages.WARNING,('Data already exists!!'))
            return redirect('updatetemplatetypelist')


def UpdateTemplateTypeEdit(request, id):

    manageproduct = get_object_or_404(UpdateTemplateType, pk=id)
    if request.method == "POST":
        form = UpdateTemplateTypeForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('updatetemplatetypelist')
    else:
        form = UpdateTemplateTypeForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/updatetemplatetypelist_add.html', {'form': form})


class UpdateTemplateTypeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateTemplateType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('updatetemplatetypelist')
#######UpdatePurposeofTemplate



class UpdatePurposeofTemplateList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatepurposeoftemplatelist_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdatePurposeofTemplate.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class UpdatePurposeofTemplateAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatepurposeoftemplatelist_add.html'

    def get(self,request):
        form = UpdatePurposeofTemplateForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = UpdatePurposeofTemplateForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('updatepurposeoftemplatelist')


def UpdatePurposeofTemplateEdit(request, id):

    manageproduct = get_object_or_404(UpdatePurposeofTemplate, pk=id)
    if request.method == "POST":
        form = UpdatePurposeofTemplateForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('updatepurposeoftemplatelist')
    else:
        form = UpdatePurposeofTemplateForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/updatepurposeoftemplatelist_add.html', {'form': form})


class UpdatePurposeofTemplateDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdatePurposeofTemplate.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('updatepurposeoftemplatelist')
############UpdateTemplateRequirementList



class UpdateTemplateRequirementList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatetemplaterequirementlist_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateTemplateRequirement.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class UpdateTemplateRequirementAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatetemplaterequirementlist_add.html'

    def get(self,request):
        form = UpdateTemplateRequirementForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = UpdateTemplateRequirementForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('updatetemplaterequirementlist')


def UpdateTemplateRequirementEdit(request, id):

    manageproduct = get_object_or_404(UpdateTemplateRequirement, pk=id)
    if request.method == "POST":
        form = UpdateTemplateRequirementForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('updatetemplaterequirementlist')
    else:
        form = UpdatePurposeofTemplateForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/updatetemplaterequirementlist_add.html', {'form': form})


class UpdateTemplateRequirementDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateTemplateRequirement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('updatetemplaterequirementlist')


#
#UpdateFieldMastersList


class UpdateFieldMastersList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatefieldmasterslist_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TemplateCreateFields.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class UpdateFieldMastersAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/updatefieldmasterslist_add.html'

    def get(self,request):
        form = TemplateCreateFieldsForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = TemplateCreateFieldsForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('updatefieldmasterslist')


def UpdateFieldMastersEdit(request, id):

    manageproduct = get_object_or_404(TemplateCreateFields, pk=id)
    if request.method == "POST":
        form = TemplateCreateFieldsForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('updatefieldmasterslist')
    else:
        form = TemplateCreateFieldsForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/updatefieldmasterslist_add.html', {'form': form})


class UpdateFieldMastersDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TemplateCreateFields.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('updatefieldmasterslist')

##  AdditionalTemplate


class AdditionalTemplateList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/additionaltemplate_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AdditionalTemplate.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AdditionalTemplateAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/additionaltemplate_add.html'

    def get(self,request):
        form = AdditionalTemplateForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = AdditionalTemplateForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('additionaltemplatelist')

def AdditionalTemplateEdit(request, id):

    manageproduct = get_object_or_404(AdditionalTemplate, pk=id)
    if request.method == "POST":
        form = AdditionalTemplateForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('additionaltemplatelist')
    else:
        form = AdditionalTemplateForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/additionaltemplate_add.html', {'form': form})


class AdditionalTemplateDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AdditionalTemplateAdditionalTemplate.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('additionaltemplatelist')
###ApplicationFormList



class ApplicationFormList(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/applicationform_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ApplicationForm.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class ApplicationFormAdd(View):
    template = 'admin_template/crm_management/template_set_up/customize_template/applicationform_add.html'

    def get(self,request):
        form = ApplicationFormForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = ApplicationFormForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('applicationformlist')

def ApplicationFormEdit(request, id):

    manageproduct = get_object_or_404(ApplicationForm, pk=id)
    if request.method == "POST":
        form = ApplicationFormForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('applicationformlist')
    else:
        form = ApplicationFormForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/template_set_up/customize_template/applicationform_add.html', {'form': form})


class ApplicationFormDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ApplicationForm.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('applicationformlist')

######




class CrmAllocationMatrixClientSupportList(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/list_client_support_allocate_matrix.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationMatrixsClientSupport.objects.all()
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class CrmAddAllocationMatrixClientSupport(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/add_edit_client_support_allocate_matrix.html'
    
    def get(self,request):
        form = AllocationMatrixsClientSupportForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = AllocationMatrixsClientSupportForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('clientsupportsupportallocationallocationmatrixlist1')

def CrmAddEditAllocationMatrixClientSupport(request, id):

    manageproduct = get_object_or_404(AllocationMatrixsClientSupport, pk=id)
    if request.method == "POST":
        form = AllocationMatrixsClientSupportForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('clientsupportsupportallocationallocationmatrixlist1')
    else:
        form = AllocationMatrixsClientSupportForm(instance=manageproduct)
    return render(request, 'admin_template/crm_management/data_allocation/allocation_matrix/add_edit_client_support_allocate_matrix.html', {'form': form})


class CrmAllocationMatrixClientSupportsDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationMatrixsClientSupport.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('clientsupportsupportallocationallocationmatrixlist1')

###############

#1
class AllocationMatrixsLeadAllocationList(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/list_client_support_allocate_matrix1.html'
    # template = 'admin_template/los_management/data_allocation/allow_set_up_matrix_lead_allocation_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        
        get_data = AllocationMatrixLeadAllocation.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddAllocationMatrixsLeadAllocation(View):
    template = 'admin_template/crm_management/data_allocation/allocation_matrix/add_edit_client_support_allocate_matrix1.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, allocationsetuid = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_all_mapped_cities = ''
        if allocationsetuid is None:
            data = ''
            allocationsetuid = None
            city = ''
        else:
            data = get_object_or_404(AllocationMatrixLeadAllocation, pk=allocationsetuid)
            allocationsetuid = allocationsetuid
            map_cities = []
    #123
            append_branch_ids = [ data.branch_allocated_id for data in UserMultipleBranch.objects.filter(user=data.user.id)] 
            get_all_mapped_cities =[ p.id for p in MapCityBranches.objects.filter(branch_id__in = append_branch_ids)]
            city = MapCityMultipleWithBranches.objects.filter(city_map__in = get_all_mapped_cities).order_by('-id')
        context = {
            'data': data, 
            'allocationsetuid': allocationsetuid,
            'user_set_up': User.objects.filter(is_active =True, is_superuser=0,is_client=0,is_agent=0,is_verification_agency=0,is_legal_team=0,is_technical_team=0,is_valuation_team=0,is_fraud_investigation_team=0,is_document_verification_team=0).order_by('-id'),
            # 'product_set_up': DefineProductType.objects.filter(is_active =True).order_by('-id'),
            # 'client_type': DefineClientType.objects.filter(is_active =True).order_by('-id'),
            # 'client_category': ManageClientCategory.objects.filter(is_active=True).order_by('-id'),
            # 'product_category': ManageProductCategory.objects.filter(is_active=True).order_by('-id'),
            # 'product_name': ManageProductName.objects.filter(is_active=True).order_by('-id'),
            'process_name': DefineProcessAllocation.objects.values('process_name').annotate(Count('process_name')).filter(is_active = True),
            'city':   city,
            'get_all_cities': AllocationMatrixLeadUserCity.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            # 'get_product_type': AllocationUserDefineProductType.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            # 'get_product_category': AllocationUserProductCategory.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            # 'get_product_name': AllocationUserProductName.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            # 'get_client_type': AllocationUserClientType.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            # 'get_client_category': AllocationUserClientCategory.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
            'get_process_name': LeadAllocationProcessName.objects.filter(lead_allocation_id= data.id).order_by('-id') if data != "" else "",
        }
        return render(request, self.template, context)

    def post(self, request, allocationsetuid = None):
        
        if request.POST['allocationsetuid'] is None or request.POST['allocationsetuid'] == "None":
            if AllocationMatrixLeadAllocation.objects.filter(user_id = request.POST['user']):
                messages.add_message(request, messages.WARNING, "User Already Exists.")
                return redirect('leadallocationallocationmatrixslist1')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            # extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            # extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            # extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            # extra_list4 = [data for data in dict(request.POST)['client_type'] if data != ""]  if 'client_type' in request.POST else []
            # extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            extra_list6 = [data for data in dict(request.POST)['process_name'] if data != ""]  if 'process_name' in request.POST else []
            # if LeadAllocationProcessName.objects.filter(process_name_id__in = extra_list6).exists() and AllocationMatrixLeadUserCity.objects.filter(city_id__in = extra_list).exists() and AllocationUserDefineProductType.objects.filter(product_type_id__in = extra_list1).exists() and AllocationUserProductCategory.objects.filter(product_category_id__in =extra_list2).exists() and AllocationUserProductName.objects.filter(product_name_id__in =extra_list3).exists() and AllocationUserClientType.objects.filter(client_type_id__in =extra_list4).exists() and AllocationUserClientCategory.objects.filter(client_category_id__in = extra_list5).exists():
            if LeadAllocationProcessName.objects.filter(process_name_id__in = extra_list6).exists() and AllocationMatrixLeadUserCity.objects.filter(city_id__in = extra_list).exists():
            
                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('leadallocationallocationmatrixslist1')
            save_data = AllocationMatrixLeadAllocation()
            messages.add_message(request, messages.SUCCESS, "Record added Successfully.")
        else:
            allocationsetuid = request.POST['allocationsetuid']
            if AllocationMatrixLeadAllocation.objects.filter(user_id = request.POST['user'], id =allocationsetuid):
                pass
            else:
                if AllocationMatrixLeadAllocation.objects.filter(user_id = request.POST['user']):
                    messages.add_message(request, messages.WARNING, "User Already Exists.")
                    return redirect('leadallocationallocationmatrixslist1')
            extra_list =  [data for data in dict(request.POST)['city'] if data != ""] if 'city' in request.POST else []
            # extra_list1 = [data for data in dict(request.POST)['product'] if data != ""] if 'product' in request.POST else []
            # extra_list2 = [data for data in dict(request.POST)['product_category'] if data != ""] if 'product_category' in request.POST else []
            # extra_list3 = [data for data in dict(request.POST)['product_name'] if data != ""] if 'product_name' in request.POST else []
            # extra_list4 = [data for data in dict(request.POST)['client_type'] if data != "" ]  if 'client_type' in request.POST else []
            # extra_list5 = [data for data in dict(request.POST)['client_category'] if data != ""]  if 'client_category' in request.POST else []
            extra_list6 = [data for data in dict(request.POST)['process_name'] if data != ""]  if 'process_name' in request.POST else []
            # if LeadAllocationProcessName.objects.filter(~Q(lead_allocation_id= allocationsetuid), process_name__in = extra_list6).exists() and AllocationMatrixLeadUserCity.objects.filter(~Q(lead_allocation_id= allocationsetuid), city_id__in = extra_list).exists() and LeadAllocationProductType.objects.filter(~Q(lead_allocation_id= allocationsetuid),product_type_id__in = extra_list1).exists() and LeadAllocationProductCategory.objects.filter(~Q(lead_allocation_id= allocationsetuid),product_category_id__in =extra_list2).exists() and LeadAllocationProductName.objects.filter(~Q(lead_allocation_id= allocationsetuid), product_name_id__in =extra_list3).exists() and LeadAllocationClientType.objects.filter(~Q(lead_allocation_id= allocationsetuid), client_type_id__in =extra_list4).exists() and LeadAllocationClientCategory.objects.filter(~Q(lead_allocation_id= allocationsetuid), client_category_id__in = extra_list5).exists():
            
            if LeadAllocationProcessName.objects.filter(~Q(lead_allocation_id= allocationsetuid), process_name__in = extra_list6).exists() and AllocationMatrixLeadUserCity.objects.filter(~Q(lead_allocation_id= allocationsetuid), city_id__in = extra_list).exists():

                messages.add_message(request, messages.WARNING, "Already Exists.")
                return redirect('leadallocationallocationmatrixslist1')
            save_data = get_object_or_404(AllocationMatrixLeadAllocation, pk=allocationsetuid)
            messages.add_message(request, messages.SUCCESS, "Record update Successfully.")
        save_data.user_id = request.POST['user']
        
        save_data.save()
        id = save_data.id
        append_city = []
        # Save All Matrix City
        if 'city' in request.POST:
            for data in dict(request.POST)['city']:
                if str(data) != "":
                    try:
                        save_city = AllocationMatrixLeadUserCity.objects.get(lead_allocation_id = id, city_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    except AllocationMatrixLeadUserCity.DoesNotExist:
                        save_city = AllocationMatrixLeadUserCity()
                        save_city.lead_allocation_id = save_data.id
                        save_city.city_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationMatrixLeadUserCity.objects.filter(~Q(city_id__in = append_city) , lead_allocation_id = id ).delete()
        # Save Product Type
        append_city = []
        if 'product' in request.POST:
            for data in dict(request.POST)['product']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserDefineProductType.objects.get(lead_allocation_id = id, product_type_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    except AllocationUserDefineProductType.DoesNotExist:
                        save_city = AllocationUserDefineProductType()
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserDefineProductType.objects.filter(~Q(product_type_id__in = append_city) , lead_allocation_id = id).delete()
        
        # Save Product Category
        append_city = []
        if 'product_category' in request.POST:
            for data in dict(request.POST)['product_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserProductCategory.objects.get(lead_allocation_id = id, product_category_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    except AllocationUserProductCategory.DoesNotExist:
                        save_city = AllocationUserProductCategory()
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserProductCategory.objects.filter(~Q(product_category_id__in = append_city) , lead_allocation_id = id).delete()
        
        # Save Product Name
        append_city1 = []
        if 'product_name' in request.POST:
            for data in dict(request.POST)['product_name']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserProductName.objects.get(lead_allocation_id = id, product_name_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    except AllocationUserProductName.DoesNotExist:
                        save_city = AllocationUserProductName()
                        save_city.lead_allocation_id = save_data.id
                        save_city.product_name_id = data
                        save_city.save()
                    append_city1.append(data)
            AllocationUserProductName.objects.filter(~Q(product_name_id__in = append_city1) , lead_allocation_id = id).delete()

        # Client Type 
        append_city = []
        if 'client_type' in request.POST:
            for data in dict(request.POST)['client_type']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserClientType.objects.get(lead_allocation_id = id, client_type_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    except AllocationUserClientType.DoesNotExist:
                        save_city = AllocationUserClientType()
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_type_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserClientType.objects.filter(~Q(client_type_id__in = append_city) , lead_allocation_id = id).delete()

        # Client Category 
        append_city = []
        if 'client_category' in request.POST:
            for data in dict(request.POST)['client_category']:
                if str(data) != "":
                    try:
                        save_city = AllocationUserClientCategory.objects.get(lead_allocation_id = id, client_category_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    except AllocationUserClientCategory.DoesNotExist:
                        save_city = AllocationUserClientCategory()
                        save_city.lead_allocation_id = save_data.id
                        save_city.client_category_id = data
                        save_city.save()
                    append_city.append(data)
            AllocationUserClientCategory.objects.filter(~Q(client_category_id__in = append_city) , lead_allocation_id = id).delete()
        process_name = []
        if 'process_name' in request.POST:
            for data in dict(request.POST)['process_name']:
                if str(data) != "":
                    try:
                        save_city = LeadAllocationProcessName.objects.get(lead_allocation_id = id, process_name_id = data)
                        save_city.lead_allocation_id = save_data.id
                        save_city.process_name_id = data
                        save_city.save()
                    except LeadAllocationProcessName.DoesNotExist:
                        save_city = LeadAllocationProcessName()
                        save_city.lead_allocation_id = save_data.id
                        save_city.process_name_id = data
                        save_city.save()
                    process_name.append(data)
            LeadAllocationProcessName.objects.filter(~Q(process_name_id__in = process_name) , lead_allocation_id = id).delete()



        return redirect('leadallocationallocationmatrixslist1')


class AllocationMatrixsLeadDelete(View):
    def get(self, request, allocationsetuid):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AllocationMatrixLeadAllocation.objects.filter(id = allocationsetuid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('leadallocationallocationmatrixslist1')
# END
#rajesh




class ProvideAccessPermisson(View):
    template = 'admin_template/crm_management/access_permisson/provide_access_permisson_view.html'
    pagesize = 10


    def get(self,request, id ):

        data = UserAccessPermissonModelsPermission.objects.filter(user_id = id)
        per_list = [ data.process_name.process_name.strip() for data in LeadAllocationProcessName.objects.filter(lead_allocation__user_id = id)]

        context = {
            'user_id': id, 
            'data': data,
            'permission_list': list(set(per_list))
        }
        return render(request, self.template,context)





##
class HrmProvideAccessAndPermissionView(View):

    def post(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if 'applcation_management' in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], function_level = "completeapp", main_function = "1", sub_function_level = "reciptofapplication").delete()
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], function_level = "incompleteapp", main_function = "1", sub_function_level = "reciptofapplication").delete()
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], function_level = "completeapp", main_function = "1", sub_function_level = "reciptofapplication").delete()
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], function_level = "incompleteapp", main_function = "1", sub_function_level = "reciptofapplication").delete()
            
            if 'datamanagement1' in request.POST and 'completeapp' in request.POST['datamanagement1']:

                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']

                if '1_application_management_completeapp_0' in dict(request.POST)['datamanagement1']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"

                else:
                    for data in dict(request.POST)['datamanagement1']:
                        if '1_application_management_completeapp_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_application_management_completeapp_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_application_management_completeapp_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_application_management_completeapp_4' in data:
                            save_sub_permission.permission_view = "4"

                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "completeapp"
                save_sub_permission.sub_function_level = "reciptofapplication"
                save_sub_permission.sequence = "1"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "allocationofapplication").delete()
            if 'data_managment1_1' in request.POST and 'allocationofapplication' in request.POST['data_managment1_1']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_1_allocationofapplication_0' in dict(request.POST)['data_managment1_1']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_1']:
                        if '1_1_allocationofapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_1_allocationofapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_1_allocationofapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_1_allocationofapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "allocationofapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "3"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "allocationofincompleteapplication").delete()
            if 'data_managment1_2' in request.POST and 'allocationofincompleteapplication' in request.POST['data_managment1_2']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_2_allocationofincompleteapplication_0' in dict(request.POST)['data_managment1_2']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_2']:
                        if '1_2_allocationofincompleteapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_2_allocationofincompleteapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_2_allocationofincompleteapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_2_allocationofincompleteapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "allocationofincompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "4"
                save_sub_permission.save()




            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "allocatedcompleteapplication").delete()
            if 'data_managment1_3' in request.POST and 'allocatedcompleteapplication' in request.POST['data_managment1_3']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_3_allocatedcompleteapplication_0' in dict(request.POST)['data_managment1_3']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_3']:
                        if '1_3_allocatedcompleteapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_3_allocatedcompleteapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_3_allocatedcompleteapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_3_allocatedcompleteapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "allocatedcompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "5"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "allocatedincompleteapplication").delete()
            if 'data_managment1_4' in request.POST and 'allocatedincompleteapplication' in request.POST['data_managment1_4']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_4_allocatedincompleteapplication_0' in dict(request.POST)['data_managment1_4']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_4']:
                        if '1_4_allocatedincompleteapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_4_allocatedincompleteapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_4_allocatedincompleteapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_4_allocatedincompleteapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "allocatedincompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "6"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "unallocatedcompleteapplication").delete()
            if 'data_managment1_5' in request.POST and 'unallocatedcompleteapplication' in request.POST['data_managment1_5']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_5_unallocatedcompleteapplication_0' in dict(request.POST)['data_managment1_5']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_5']:
                        if '1_5_unallocatedcompleteapplication_0_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_5_unallocatedcompleteapplication_0_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_5_unallocatedcompleteapplication_0_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_5_unallocatedcompleteapplication_0_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "unallocatedcompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "7"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "unallocatedincompleteapplication").delete()
            if 'data_managment1_6' in request.POST and 'unallocatedincompleteapplication' in request.POST['data_managment1_6']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_6_unallocatedincompleteapplication_0' in dict(request.POST)['data_managment1_6']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_6']:
                        if '1_6_unallocatedincompleteapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_6_unallocatedincompleteapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_6_unallocatedincompleteapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_6_unallocatedincompleteapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "unallocatedincompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "8"
                save_sub_permission.save()



            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "reallocatedcompleteapplication").delete()
            if 'data_managment1_7' in request.POST and 'reallocatedcompleteapplication' in request.POST['data_managment1_7']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_7_reallocatedincompleteapplication_0' in dict(request.POST)['data_managment1_7']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_7']:
                        if '1_7_reallocatedcompleteapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_7_reallocatedcompleteapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_7_reallocatedcompleteapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_7_reallocatedcompleteapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "reallocatedcompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "9"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "reallocatedincompleteapplication").delete()
            if 'data_managment1_8' in request.POST and 'reallocatedincompleteapplication' in request.POST['data_managment1_8']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_8_reallocatedincompleteapplication_0' in dict(request.POST)['data_managment1_8']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment1_8']:
                        if '1_8_reallocatedincompleteapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_8_reallocatedincompleteapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_8_reallocatedincompleteapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_8_reallocatedincompleteapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "reallocatedincompleteapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "10"
                save_sub_permission.save()

            if 'datamanagement2' in request.POST and 'incompleteapp' in request.POST['datamanagement2']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']

                if '1_application_management_incompleteapp_0' in dict(request.POST)['datamanagement2']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"

                else:
                    for data in dict(request.POST)['datamanagement2']:
                        if '1_application_management_incompleteapp_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_application_management_incompleteapp_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_application_management_incompleteapp_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_application_management_incompleteapp_4' in data:
                            save_sub_permission.permission_view = "4"

                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "incompleteapp"
                save_sub_permission.sub_function_level = "reciptofapplication" 
                save_sub_permission.sequence = "2"
                save_sub_permission.save()


            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "completeescalatedapplication").delete()
            if 'data_managment3' in request.POST and 'completeescalatedapplication' in request.POST['data_managment3']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '3_completeescalatedapplication_0' in dict(request.POST)['data_managment3']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment3']:
                        if '3_completeescalatedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '3_completeescalatedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '3_completeescalatedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '3_completeescalatedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "completeescalatedapplication"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.sequence = "11"
                save_sub_permission.save()

            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "escalatedapplication", main_function = "1", function_level = "incompleteescalatedapplication").delete()
            if 'data_managment4' in request.POST and 'incompleteescalatedapplication' in  request.POST['data_managment4']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '4_incompleteescalatedapplication_0' in dict(request.POST)['data_managment4']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment4']:
                        if '4_incompleteescalatedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '4_incompleteescalatedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '4_incompleteescalatedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '4_incompleteescalatedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "escalatedapplication"
                save_sub_permission.function_level = "incompleteescalatedapplication"
                save_sub_permission.sequence = "12"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "expiredapplication", main_function = "1", function_level = "completeexpiredapplication").delete()
            if 'data_managment5' in request.POST and 'completeexpiredapplication' in request.POST['data_managment5']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '5_completeexpiredapplication_0' in dict(request.POST)['data_managment5']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment5']:
                        if '5_completeexpiredapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '5_completeexpiredapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '5_completeexpiredapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '5_completeexpiredapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "completeexpiredapplication"
                save_sub_permission.sub_function_level = "expiredapplication"
                save_sub_permission.sequence = "13"
                save_sub_permission.save()

            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "expiredapplication", main_function = "1", function_level = "incompleteexpiredapplication").delete()
            if 'data_managment6' in request.POST and 'incompleteexpiredapplication' in  request.POST['data_managment6']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '6_incompleteexpiredapplication_0' in dict(request.POST)['data_managment6']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment6']:
                        if '6_incompleteexpiredapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '6_incompleteexpiredapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '6_incompleteexpiredapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '6_incompleteexpiredapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "expiredapplication"
                save_sub_permission.function_level = "incompleteexpiredapplication"
                save_sub_permission.sequence = "14"
                save_sub_permission.save()
        

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "rejectedapplication", main_function = "1", function_level = "completerejectedapplication").delete()
            if 'data_managment7' in request.POST and 'completerejectedapplication' in request.POST['data_managment7']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '7_completerejectedapplication_0' in dict(request.POST)['data_managment7']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment7']:
                        if '7_completerejectedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '7_completerejectedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '7_completerejectedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '7_completerejectedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "completerejectedapplication"
                save_sub_permission.sub_function_level = "rejectedapplication"
                save_sub_permission.sequence = "15"
                save_sub_permission.save()

            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "rejectedapplication", main_function = "1", function_level = "incompleterejectedapplication").delete()
            if 'data_managment8' in request.POST and 'incompleterejectedapplication' in  request.POST['data_managment8']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '8_incompleterejectedapplication_0' in dict(request.POST)['data_managment8']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment8']:
                        if '8_incompleterejectedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '8_incompleterejectedapplication_1' in data:
                            save_sub_permission.permission_edit = "2"
                        if '8_incompleterejectedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '8_incompleterejectedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "rejectedapplication"
                save_sub_permission.function_level = "incompleterejectedapplication"
                save_sub_permission.sequence = "16"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "deletedapplication", main_function = "1", function_level = "completedeletedapplication").delete()
            if 'data_managment9' in request.POST and 'completedeletedapplication' in request.POST['data_managment9']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '9_completedeletedapplication_0' in dict(request.POST)['data_managment9']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment9']:
                        if '9_completedeletedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '9_completedeletedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '9_completedeletedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '9_completedeletedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "completedeletedapplication"
                save_sub_permission.sub_function_level = "deletedapplication"
                save_sub_permission.sequence = "17"
                save_sub_permission.save()

            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "deletedapplication", main_function = "1", function_level = "incompletedeletedapplication").delete()
            if 'data_managment10' in request.POST and 'incompletedeletedapplication' in  request.POST['data_managment10']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '10_incompletedeletedapplication_0' in dict(request.POST)['data_managment10']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment10']:
                        if '10_incompletedeletedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '10_incompletedeletedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '10_incompletedeletedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '10_incompletedeletedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "deletedapplication"
                save_sub_permission.function_level = "incompletedeletedapplication"
                save_sub_permission.sequence = "18"
                save_sub_permission.save()
            

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "allapplication", main_function = "1", function_level = "completeallapplication").delete()
            if 'data_managment11' in request.POST and 'completeallapplication' in request.POST['data_managment11']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '11_completeallapplication_0' in dict(request.POST)['data_managment11']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment11']:
                        if '11_completeallapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '11_completeallapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '11_completeallapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '11_completeallapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.function_level = "completeallapplication"
                save_sub_permission.sub_function_level = "allapplication"
                save_sub_permission.sequence = "19"
                save_sub_permission.save()

            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "allapplication", main_function = "1", function_level = "incompleteallapplication").delete()
            if 'data_managment12' in request.POST and 'incompleteallapplication' in  request.POST['data_managment12']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '12_incompleteallapplication_0' in dict(request.POST)['data_managment12']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment12']:
                        if '12_incompleteallapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '12_incompleteallapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '12_incompleteallapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '12_incompleteallapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "allapplication"
                save_sub_permission.function_level = "incompleteallapplication"
                save_sub_permission.sequence = "20"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "applicationforverification").delete()
            if 'data_managment13' in request.POST and 'applicationforverification' in  request.POST['data_managment13']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '13_applicationforverification_0' in dict(request.POST)['data_managment13']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment13']:
                        if '13_applicationforverification_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '13_applicationforverification_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '13_applicationforverification_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '13_applicationforverification_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "applicationforverification"
                save_sub_permission.sequence = "21"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "verifiedapplication").delete()
            if 'data_managment14' in request.POST and 'verifiedapplication' in  request.POST['data_managment14']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '14_verifiedapplication_0' in dict(request.POST)['data_managment14']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment14']:
                        if '14_verifiedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '14_verifiedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '14_verifiedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '14_verifiedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "verifiedapplication"
                save_sub_permission.sequence = "22"
                save_sub_permission.save()



            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "unverifiedapplication").delete()
            if 'data_managment15' in request.POST and 'unverifiedapplication' in  request.POST['data_managment15']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '15_unverifiedapplication_0' in dict(request.POST)['data_managment15']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment15']:
                        if '15_unverifiedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '15_unverifiedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '15_unverifiedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '15_unverifiedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "unverifiedapplication"
                save_sub_permission.sequence = "23"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "rejectedapplication").delete()
            if 'data_managment16' in request.POST and 'rejectedapplication' in  request.POST['data_managment16']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '16_rejectedapplication_0' in dict(request.POST)['data_managment16']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment16']:
                        if '16_rejectedapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '16_rejectedapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '16_rejectedapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '16_rejectedapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "rejectedapplication"
                save_sub_permission.sequence = "24"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "expiredapplication").delete()
            if 'data_managment17' in request.POST and 'expiredapplication' in  request.POST['data_managment17']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '17_expiredapplication_0' in dict(request.POST)['data_managment17']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment17']:
                        if '17_expiredapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '17_expiredapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '17_expiredapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '17_expiredapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "expiredapplication"
                save_sub_permission.sequence = "25"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "allapplication").delete()
            if 'data_managment18' in request.POST and 'allapplication' in  request.POST['data_managment18']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_allapplication_0' in dict(request.POST)['data_managment18']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment18']:
                        if '18_allapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '18_allapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '18_allapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '18_allapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "allapplication"
                save_sub_permission.sequence = "26"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "oblisationnewapplication").delete()
            if 'data_managment18_1' in request.POST and 'oblisationnewapplication' in  request.POST['data_managment18_1']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_1_oblisationnewapplication_0' in dict(request.POST)['data_managment18_1']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment18_1']:
                        if '18_1_oblisationnewapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '18_1_oblisationnewapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '18_1_oblisationnewapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '18_1_oblisationnewapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "oblisationnewapplication"
                save_sub_permission.sequence = "27"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "oblisationupdate").delete()
            if 'data_managment18_2' in request.POST and 'oblisationupdate' in  request.POST['data_managment18_2']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_2_oblisationupdate_0' in dict(request.POST)['data_managment18_2']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment18_2']:
                        if '18_2_oblisationupdate_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '18_2_oblisationupdate_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '18_2_oblisationupdate_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '18_2_oblisationupdate_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "oblisationupdate"
                save_sub_permission.sequence = "28"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "pendingforoblisationupdate").delete()
            if 'data_managment18_3' in request.POST and 'pendingforoblisationupdate' in  request.POST['data_managment18_3']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_3_pendingforoblisationupdate_0' in dict(request.POST)['data_managment18_3']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment18_3']:
                        if '18_3_pendingforoblisationupdate_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '18_3_pendingforoblisationupdate_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '18_3_pendingforoblisationupdate_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '18_3_pendingforoblisationupdate_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "pendingforoblisationupdate"
                save_sub_permission.sequence = "29"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "oblisationrejectedapp").delete()
            if 'data_managment18_4' in request.POST and 'oblisationrejectedapp' in  request.POST['data_managment18_4']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_4_oblisationrejectedapp_0' in dict(request.POST)['data_managment18_4']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment18_4']:
                        if '18_4_oblisationrejectedapp_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '18_4_oblisationrejectedapp_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '18_4_oblisationrejectedapp_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '18_4_oblisationrejectedapp_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "oblisationrejectedapp"
                save_sub_permission.sequence = "30"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationofapplication", main_function = "1", function_level = "oblisationallapp").delete()
            if 'data_managment18_5' in request.POST and 'oblisationallapp' in  request.POST['data_managment18_5']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_5_oblisationallapp_0' in dict(request.POST)['data_managment18_5']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment18_5']:
                        if '18_5_oblisationallapp_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '18_5_oblisationallapp_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '18_5_oblisationallapp_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '18_5_oblisationallapp_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "1"
                save_sub_permission.sub_function_level = "verificationofapplication"
                save_sub_permission.function_level = "oblisationallapp"
                save_sub_permission.sequence = "31"
                save_sub_permission.save()





        elif 'agent_report_button'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "newrequest").delete()
            if 'data_managment19' in request.POST and 'newrequest' in  request.POST['data_managment19']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '19_newrequest_0' in dict(request.POST)['data_managment19']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment19']:
                        if '19_newrequest_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '19_newrequest_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '19_newrequest_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '19_newrequest_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "newrequest"
                save_sub_permission.sequence = "32"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "requestsent").delete()
            if 'data_managment20' in request.POST and 'requestsent' in  request.POST['data_managment20']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '20_requestsent_0' in dict(request.POST)['data_managment20']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment20']:
                        if '20_requestsent_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '20_requestsent_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '20_requestsent_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '20_requestsent_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "requestsent"
                save_sub_permission.sequence = "33"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "pendingforrequest").delete()
            if 'data_managment21' in request.POST and 'pendingforrequest' in  request.POST['data_managment21']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '21_pendingforrequest_0' in dict(request.POST)['data_managment21']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment21']:
                        if '21_pendingforrequest_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '21_pendingforrequest_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '21_pendingforrequest_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '21_pendingforrequest_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "pendingforrequest"
                save_sub_permission.sequence = "34"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "revisitrequired").delete()
            if 'data_managment22' in request.POST and 'revisitrequired' in  request.POST['data_managment22']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '22_revisitrequired_0' in dict(request.POST)['data_managment22']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment22']:
                        if '22_revisitrequired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '22_revisitrequired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '22_revisitrequired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '22_revisitrequired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "revisitrequired"
                save_sub_permission.sequence = "35"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "requestexpired").delete()
            if 'data_managment23' in request.POST and 'requestexpired' in  request.POST['data_managment23']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '23_requestexpired_0' in dict(request.POST)['data_managment23']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment23']:
                        if '23_requestexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '23_requestexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '23_requestexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '23_requestexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "requestexpired"
                save_sub_permission.sequence = "36"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "applicationrejected").delete()
            if 'data_managment24' in request.POST and 'applicationrejected' in  request.POST['data_managment24']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '24_applicationrejected_0' in dict(request.POST)['data_managment24']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment24']:
                        if '24_applicationrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '24_applicationrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '24_applicationrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '24_applicationrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "applicationrejected"
                save_sub_permission.sequence = "37"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "allrequest").delete()
            if 'data_managment25' in request.POST and 'allrequest' in  request.POST['data_managment25']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '25_allrequest_0' in dict(request.POST)['data_managment25']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment25']:
                        if '25_allrequest_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '25_allrequest_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '25_allrequest_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '25_allrequest_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "allrequest"
                save_sub_permission.sequence = "38"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "reportreceived").delete()
            if 'data_managment26' in request.POST and 'reportreceived' in  request.POST['data_managment26']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '26_verificationreport_0' in dict(request.POST)['data_managment26']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment26']:
                        if '26_verificationreport_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '26_verificationreport_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '26_verificationreport_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '26_verificationreport_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "reportreceived"
                save_sub_permission.sequence = "39"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "reportaccepted").delete()
            if 'data_managment27' in request.POST and 'reportaccepted' in  request.POST['data_managment27']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '27_reportaccepted_0' in dict(request.POST)['data_managment27']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment27']:
                        if '27_reportaccepted_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '27_reportaccepted_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '27_reportaccepted_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '27_reportaccepted_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "reportaccepted"
                save_sub_permission.sequence = "40"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "reportrejected").delete()
            if 'data_managment28' in request.POST and 'reportrejected' in  request.POST['data_managment28']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '28_reportrejected_0' in dict(request.POST)['data_managment28']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment28']:
                        if '28_reportrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '28_reportrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '28_reportrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '28_reportrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "reportrejected"
                save_sub_permission.sequence = "41"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "reportexpired").delete()
            if 'data_managment29' in request.POST and 'reportexpired' in  request.POST['data_managment29']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '29_reportexpired_0' in dict(request.POST)['data_managment29']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment29']:
                        if '29_reportexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '29_reportexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '29_reportexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '29_reportexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "reportexpired"
                save_sub_permission.sequence = "42"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "reportrequiredrevisit").delete()
            if 'data_managment30' in request.POST and 'reportrequiredrevisit' in  request.POST['data_managment30']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '30_reportrequiredrevisit_0' in dict(request.POST)['data_managment30']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment30']:
                        if '30_reportrequiredrevisit_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '30_reportrequiredrevisit_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '30_reportrequiredrevisit_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '30_reportrequiredrevisit_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "reportrequiredrevisit"
                save_sub_permission.sequence = "43"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "verificationrequest", main_function = "2", function_level = "allreports").delete()
            if 'data_managment31' in request.POST and 'allreports' in  request.POST['data_managment31']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '31_allreports_0' in dict(request.POST)['data_managment31']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment31']:
                        if '31_allreports_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '31_allreports_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '31_allreports_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '31_allreports_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "2"
                save_sub_permission.sub_function_level = "verificationrequest"
                save_sub_permission.function_level = "allreports"
                save_sub_permission.sequence = "44"
                save_sub_permission.save()


        elif 'eligibilitystatement'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "incomedetails").delete()
            if 'data_managment32' in request.POST and 'incomedetails' in  request.POST['data_managment32']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '32_incomedetails_0' in dict(request.POST)['data_managment32']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment32']:
                        if '32_incomedetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '32_incomedetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '32_incomedetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '32_incomedetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "incomedetails"
                save_sub_permission.sequence = "45"
                save_sub_permission.save()
            
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "bankingdetails").delete()
            if 'data_managment33' in request.POST and 'bankingdetails' in  request.POST['data_managment33']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '33_bankingdetails_0' in dict(request.POST)['data_managment33']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment33']:
                        if '33_bankingdetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '33_bankingdetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '33_bankingdetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '33_bankingdetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "bankingdetails"
                save_sub_permission.sequence = "46"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "liquidincomedetail").delete()
            if 'data_managment34' in request.POST and 'liquidincomedetail' in  request.POST['data_managment34']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '34_liquidincomedetail_0' in dict(request.POST)['data_managment34']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment34']:
                        if '34_liquidincomedetail_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '34_liquidincomedetail_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '34_liquidincomedetail_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '34_liquidincomedetail_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "liquidincomedetail"
                save_sub_permission.sequence = "47"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "existingoblisation").delete()
            if 'data_managment35' in request.POST and 'existingoblisation' in  request.POST['data_managment35']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '35_existingoblisation_0' in dict(request.POST)['data_managment35']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment35']:
                        if '35_existingoblisation_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '35_existingoblisation_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '35_existingoblisation_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '35_existingoblisation_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "existingoblisation"
                save_sub_permission.sequence = "48"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "collateraldetails").delete()
            if 'data_managment36' in request.POST and 'collateraldetails' in  request.POST['data_managment36']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '36_collateraldetails_0' in dict(request.POST)['data_managment36']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment36']:
                        if '36_collateraldetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '36_collateraldetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '36_collateraldetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '36_collateraldetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "collateraldetails"
                save_sub_permission.sequence = "49"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "statementperiod").delete()
            if 'data_managment37' in request.POST and 'statementperiod' in  request.POST['data_managment37']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '37_statementperiod_0' in dict(request.POST)['data_managment37']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment37']:
                        if '37_statementperiod_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '37_statementperiod_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '37_statementperiod_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '37_statementperiod_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "statementperiod"
                save_sub_permission.sequence = "50"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "pendingincomedetails").delete()
            if 'data_managment38' in request.POST and 'pendingincomedetails' in  request.POST['data_managment38']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '38_pendingincomedetails_0' in dict(request.POST)['data_managment38']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment38']:
                        if '38_pendingincomedetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '38_pendingincomedetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '38_pendingincomedetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '38_pendingincomedetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "pendingincomedetails"
                save_sub_permission.sequence = "51"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "bankingdetails").delete()
            if 'data_managment39' in request.POST and 'bankingdetails' in  request.POST['data_managment39']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '39_bankingdetails_0' in dict(request.POST)['data_managment39']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment39']:
                        if '39_bankingdetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '39_bankingdetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '39_bankingdetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '39_bankingdetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "bankingdetails"
                save_sub_permission.sequence = "52"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "liquidincomedetails").delete()
            if 'data_managment40' in request.POST and 'liquidincomedetails' in  request.POST['data_managment40']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '40_liquidincomedetails_0' in dict(request.POST)['data_managment40']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment40']:
                        if '40_liquidincomedetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '40_liquidincomedetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '40_liquidincomedetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '40_liquidincomedetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "liquidincomedetails"
                save_sub_permission.sequence = "53"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "pendingobligations").delete()
            if 'data_managment41' in request.POST and 'pendingobligations' in  request.POST['data_managment41']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '41_pendingobligations_0' in dict(request.POST)['data_managment41']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment41']:
                        if '41_pendingobligations_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '41_pendingobligations_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '41_pendingobligations_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '41_pendingobligations_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "pendingobligations"
                save_sub_permission.sequence = "51"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "collateraldetails").delete()
            if 'data_managment42' in request.POST and 'collateraldetails' in  request.POST['data_managment42']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '42_collateraldetails_0' in dict(request.POST)['data_managment42']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment42']:
                        if '42_collateraldetails_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '42_collateraldetails_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '42_collateraldetails_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '42_collateraldetails_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "collateraldetails"
                save_sub_permission.sequence = "55"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "applicationexpired").delete()
            if 'data_managment43' in request.POST and 'applicationexpired' in  request.POST['data_managment43']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '43_applicationexpired_0' in dict(request.POST)['data_managment43']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment43']:
                        if '43_applicationexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '43_applicationexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '43_applicationexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '43_applicationexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "applicationexpired"
                save_sub_permission.sequence = "56"
                save_sub_permission.save()



            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "applicationrejected").delete()
            if 'data_managment44' in request.POST and 'applicationrejected' in  request.POST['data_managment44']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '44_applicationrejected_0' in dict(request.POST)['data_managment44']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment44']:
                        if '44_applicationrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '44_applicationrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '44_applicationrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '44_applicationrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "applicationrejected"
                save_sub_permission.sequence = "57"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "eligibilitystat", main_function = "3", function_level = "allapplicationeligibility").delete()
            if 'data_managment45' in request.POST and 'allapplicationeligibility' in  request.POST['data_managment45']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '45_allapplicationeligibility_0' in dict(request.POST)['data_managment45']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment45']:
                        if '45_allapplicationeligibility_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '45_allapplicationeligibility_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '45_allapplicationeligibility_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '45_allapplicationeligibility_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "3"
                save_sub_permission.sub_function_level = "eligibilitystat"
                save_sub_permission.function_level = "allapplicationeligibility"
                save_sub_permission.sequence = "58"
                save_sub_permission.save()

        elif 'creditscoremanagement'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "creditscorenewapplication").delete()
            if 'data_managment46' in request.POST and 'creditscorenewapplication' in  request.POST['data_managment46']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '46_creditscorenewapplication_0' in dict(request.POST)['data_managment46']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment46']:
                        if '46_creditscorenewapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '46_creditscorenewapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '46_creditscorenewapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '46_creditscorenewapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "creditscorenewapplication"
                save_sub_permission.sequence = "59"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "scoregenrated").delete()
            if 'data_managment47' in request.POST and 'scoregenrated' in  request.POST['data_managment47']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '47_scoregenrated_0' in dict(request.POST)['data_managment47']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment47']:
                        if '47_scoregenrated_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '47_scoregenrated_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '47_scoregenrated_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '47_scoregenrated_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "scoregenrated"
                save_sub_permission.sequence = "60"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "pendingforcreditscore").delete()
            if 'data_managment48' in request.POST and 'pendingforcreditscore' in  request.POST['data_managment48']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '48_pendingforcreditscore_0' in dict(request.POST)['data_managment48']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment48']:
                        if '48_pendingforcreditscore_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '48_pendingforcreditscore_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '48_pendingforcreditscore_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '48_pendingforcreditscore_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "pendingforcreditscore"
                save_sub_permission.sequence = "61"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "applicationexpire").delete()
            if 'data_managment49' in request.POST and 'applicationexpire' in  request.POST['data_managment49']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '49_applicationexpire_0' in dict(request.POST)['data_managment49']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment49']:
                        if '49_applicationexpire_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '49_applicationexpire_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '49_applicationexpire_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '49_applicationexpire_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "applicationexpire"
                save_sub_permission.sequence = "62"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "applicationreject").delete()
            if 'data_managment50' in request.POST and 'applicationreject' in  request.POST['data_managment50']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '50_applicationreject_0' in dict(request.POST)['data_managment50']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment50']:
                        if '50_applicationreject_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '50_applicationreject_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '50_applicationreject_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '50_applicationreject_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "applicationreject"
                save_sub_permission.sequence = "63"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "applicationreview").delete()
            if 'data_managment51' in request.POST and 'applicationreview' in  request.POST['data_managment51']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '51_applicationreview_0' in dict(request.POST)['data_managment51']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment51']:
                        if '51_applicationreview_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '51_applicationreview_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '51_applicationreview_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '51_applicationreview_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "applicationreview"
                save_sub_permission.sequence = "64"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditscore", main_function = "4", function_level = "allappcredit").delete()
            if 'data_managment52' in request.POST and 'allappcredit' in  request.POST['data_managment52']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '52_allappcredit_0' in dict(request.POST)['data_managment52']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment52']:
                        if '52_allappcredit_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '52_allappcredit_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '52_allappcredit_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '52_allappcredit_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "4"
                save_sub_permission.sub_function_level = "creditscore"
                save_sub_permission.function_level = "allappcredit"
                save_sub_permission.sequence = "65"
                save_sub_permission.save()

        elif 'creditnotes'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "televerification").delete()
            if 'data_managment53' in request.POST and 'televerification' in  request.POST['data_managment53']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '53_televerification_0' in dict(request.POST)['data_managment53']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment53']:
                        if '53_televerification_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '53_televerification_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '53_televerification_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '53_televerification_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "televerification"
                save_sub_permission.sequence = "66"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "personalmeeting").delete()
            if 'data_managment54' in request.POST and 'personalmeeting' in  request.POST['data_managment54']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '54_personalmeeting_0' in dict(request.POST)['data_managment54']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment54']:
                        if '54_personalmeeting_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '54_personalmeeting_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '54_personalmeeting_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '54_personalmeeting_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "personalmeeting"
                save_sub_permission.sequence = "67"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "verificationagencyreport").delete()
            if 'data_managment55' in request.POST and 'verificationagencyreport' in  request.POST['data_managment55']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '55_verificationagencyreport_0' in dict(request.POST)['data_managment55']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment55']:
                        if '55_verificationagencyreport_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '55_verificationagencyreport_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '55_verificationagencyreport_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '55_verificationagencyreport_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "verificationagencyreport"
                save_sub_permission.sequence = "68"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "riskandmitigationplan").delete()
            if 'data_managment56' in request.POST and 'riskandmitigationplan' in  request.POST['data_managment56']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '56_riskandmitigationplan_0' in dict(request.POST)['data_managment56']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment56']:
                        if '56_riskandmitigationplan_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '56_riskandmitigationplan_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '56_riskandmitigationplan_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '56_riskandmitigationplan_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "riskandmitigationplan"
                save_sub_permission.sequence = "69"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "emieligibility").delete()
            if 'data_managment57' in request.POST and 'emieligibility' in  request.POST['data_managment57']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '57_emieligibility_0' in dict(request.POST)['data_managment57']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment57']:
                        if '57_emieligibility_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '57_emieligibility_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '57_emieligibility_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '57_emieligibility_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "emieligibility"
                save_sub_permission.sequence = "70"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "productrequirement").delete()
            if 'data_managment58' in request.POST and 'productrequirement' in  request.POST['data_managment58']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '58_productrequirement_0' in dict(request.POST)['data_managment58']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment58']:
                        if '58_productrequirement_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '58_productrequirement_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '58_productrequirement_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '58_productrequirement_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "productrequirement"
                save_sub_permission.sequence = "71"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "productoffered").delete()
            if 'data_managment59' in request.POST and 'productoffered' in  request.POST['data_managment59']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '59_productoffered_0' in dict(request.POST)['data_managment59']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment59']:
                        if '59_productoffered_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '59_productoffered_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '59_productoffered_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '59_productoffered_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "productoffered"
                save_sub_permission.sequence = "72"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "creditnoteprepared").delete()
            if 'data_managment60' in request.POST and 'creditnoteprepared' in  request.POST['data_managment60']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '60_creditnoteprepared_0' in dict(request.POST)['data_managment60']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment60']:
                        if '60_creditnoteprepared_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '60_creditnoteprepared_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '60_creditnoteprepared_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '60_creditnoteprepared_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "creditnoteprepared"
                save_sub_permission.sequence = "73"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "pendingforcreditnote").delete()
            if 'data_managment61' in request.POST and 'pendingforcreditnote' in  request.POST['data_managment61']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '61_pendingforcreditnote_0' in dict(request.POST)['data_managment61']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment61']:
                        if '61_pendingforcreditnote_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '61_pendingforcreditnote_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '61_pendingforcreditnote_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '61_pendingforcreditnote_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "pendingforcreditnote"
                save_sub_permission.sequence = "74"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "creditnoteapplicationexpired").delete()
            if 'data_managment62' in request.POST and 'creditnoteapplicationexpired' in  request.POST['data_managment62']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '62_creditnoteapplicationexpired_0' in dict(request.POST)['data_managment62']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment62']:
                        if '62_creditnoteapplicationexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '62_creditnoteapplicationexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '62_creditnoteapplicationexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '62_creditnoteapplicationexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "creditnoteapplicationexpired"
                save_sub_permission.sequence = "75"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "applicationforreview").delete()
            if 'data_managment63' in request.POST and 'applicationforreview' in  request.POST['data_managment63']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '63_applicationforreview_0' in dict(request.POST)['data_managment63']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment63']:
                        if '63_applicationforreview_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '63_applicationforreview_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '63_applicationforreview_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '63_applicationforreview_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "applicationforreview"
                save_sub_permission.sequence = "76"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "creditscoreapplicationrejected").delete()
            if 'data_managment64' in request.POST and 'creditscoreapplicationrejected' in  request.POST['data_managment64']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '64_creditscoreapplicationrejected_0' in dict(request.POST)['data_managment64']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment64']:
                        if '64_creditscoreapplicationrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '64_creditscoreapplicationrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '64_creditscoreapplicationrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '64_creditscoreapplicationrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "creditscoreapplicationrejected"
                save_sub_permission.sequence = "77"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "creditnotesdetails", main_function = "5", function_level = "creditscoreallapplication").delete()
            if 'data_managment65' in request.POST and 'creditscoreallapplication' in  request.POST['data_managment65']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '65_creditscoreallapplication_0' in dict(request.POST)['data_managment65']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment65']:
                        if '65_creditscoreallapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '65_creditscoreallapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '65_creditscoreallapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '65_creditscoreallapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "5"
                save_sub_permission.sub_function_level = "creditnotesdetails"
                save_sub_permission.function_level = "creditscoreallapplication"
                save_sub_permission.sequence = "78"
                save_sub_permission.save()


        elif 'appraisalnotes'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "appraisalnotesnewapplication").delete()
            if 'data_managment66' in request.POST and 'appraisalnotesnewapplication' in  request.POST['data_managment66']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '66_appraisalnotesnewapplication_0' in dict(request.POST)['data_managment66']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment66']:
                        if '66_appraisalnotesnewapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '66_appraisalnotesnewapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '66_appraisalnotesnewapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '66_appraisalnotesnewapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "appraisalnotesnewapplication"
                save_sub_permission.sequence = "79"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "appraisalnoteprepared").delete()
            if 'data_managment67' in request.POST and 'appraisalnoteprepared' in  request.POST['data_managment67']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '67_appraisalnoteprepared_0' in dict(request.POST)['data_managment67']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment67']:
                        if '67_appraisalnoteprepared_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '67_appraisalnoteprepared_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '67_appraisalnoteprepared_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '67_appraisalnoteprepared_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "appraisalnoteprepared"
                save_sub_permission.sequence = "80"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "pendingforappraisal").delete()
            if 'data_managment68' in request.POST and 'pendingforappraisal' in  request.POST['data_managment68']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '68_pendingforappraisal_0' in dict(request.POST)['data_managment68']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment68']:
                        if '68_pendingforappraisal_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '68_pendingforappraisal_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '68_pendingforappraisal_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '68_pendingforappraisal_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "pendingforappraisal"
                save_sub_permission.sequence = "81"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "applicationexpired").delete()
            if 'data_managment69' in request.POST and 'applicationexpired' in  request.POST['data_managment69']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '69_applicationexpired_0' in dict(request.POST)['data_managment69']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment69']:
                        if '69_applicationexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '69_applicationexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '69_applicationexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '69_applicationexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "applicationexpired"
                save_sub_permission.sequence = "82"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "applicationrejected").delete()
            if 'data_managment70' in request.POST and 'applicationrejected' in  request.POST['data_managment70']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '70_applicationrejected_0' in dict(request.POST)['data_managment70']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment70']:
                        if '70_applicationrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '70_applicationrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '70_applicationrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '70_applicationrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "applicationrejected"
                save_sub_permission.sequence = "83"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "appraisalapplicationforreview").delete()
            if 'data_managment71' in request.POST and 'appraisalapplicationforreview' in  request.POST['data_managment71']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '71_appraisalapplicationforreview_0' in dict(request.POST)['data_managment71']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment71']:
                        if '71_appraisalapplicationforreview_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '71_appraisalapplicationforreview_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '71_appraisalapplicationforreview_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '71_appraisalapplicationforreview_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "appraisalapplicationforreview"
                save_sub_permission.sequence = "84"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "appraisalnotes", main_function = "6", function_level = "appraisalallapplication").delete()
            if 'data_managment72' in request.POST and 'appraisalallapplication' in  request.POST['data_managment72']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '72_appraisalallapplication_0' in dict(request.POST)['data_managment72']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment72']:
                        if '72_appraisalallapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '72_appraisalallapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '72_appraisalallapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '72_appraisalallapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "6"
                save_sub_permission.sub_function_level = "appraisalnotes"
                save_sub_permission.function_level = "appraisalallapplication"
                save_sub_permission.sequence = "85"
                save_sub_permission.save()


        elif 'recommendations'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "recommendationnewapplication").delete()
            if 'data_managment73' in request.POST and 'recommendationnewapplication' in  request.POST['data_managment73']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '73_recommendationnewapplication_0' in dict(request.POST)['data_managment73']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment73']:
                        if '73_recommendationnewapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '73_recommendationnewapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '73_recommendationnewapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '73_recommendationnewapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "recommendationnewapplication"
                save_sub_permission.sequence = "86"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "recommendations").delete()
            if 'data_managment74' in request.POST and 'recommendations' in  request.POST['data_managment74']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '74_recommendations_0' in dict(request.POST)['data_managment74']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment74']:
                        if '74_recommendations_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '74_recommendations_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '74_recommendations_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '74_recommendations_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "recommendations"
                save_sub_permission.sequence = "87"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "pendingforrecommendations").delete()
            if 'data_managment75' in request.POST and 'pendingforrecommendations' in  request.POST['data_managment75']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '75_pendingforrecommendations_0' in dict(request.POST)['data_managment75']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment75']:
                        if '75_pendingforrecommendations_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '75_pendingforrecommendations_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '75_pendingforrecommendations_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '75_pendingforrecommendations_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "pendingforrecommendations"
                save_sub_permission.sequence = "88"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "recommendedapplicationexpired").delete()
            if 'data_managment76' in request.POST and 'recommendedapplicationexpired' in  request.POST['data_managment76']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '76_recommendedapplicationexpired_0' in dict(request.POST)['data_managment76']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment76']:
                        if '76_recommendedapplicationexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '76_recommendedapplicationexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '76_recommendedapplicationexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '76_recommendedapplicationexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "recommendedapplicationexpired"
                save_sub_permission.sequence = "89"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "recommendedapplicationrejected").delete()
            if 'data_managment77' in request.POST and 'recommendedapplicationrejected' in  request.POST['data_managment77']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '77_recommendedapplicationrejected_0' in dict(request.POST)['data_managment77']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment77']:
                        if '77_recommendedapplicationrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '77_recommendedapplicationrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '77_recommendedapplicationrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '77_recommendedapplicationrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "recommendedapplicationrejected"
                save_sub_permission.sequence = "90"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "recommendedapplicationforreview").delete()
            if 'data_managment78' in request.POST and 'recommendedapplicationforreview' in  request.POST['data_managment78']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '78_recommendedapplicationforreview_0' in dict(request.POST)['data_managment78']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment78']:
                        if '78_recommendedapplicationforreview_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '78_recommendedapplicationforreview_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '78_recommendedapplicationforreview_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '78_recommendedapplicationforreview_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "recommendedapplicationforreview"
                save_sub_permission.sequence = "91"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "recommendation", main_function = "7", function_level = "recommendedallapplications").delete()
            if 'data_managment79' in request.POST and 'recommendedallapplications' in  request.POST['data_managment79']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '79_recommendedallapplications_0' in dict(request.POST)['data_managment79']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment79']:
                        if '79_recommendedallapplications_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '79_recommendedallapplications_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '79_recommendedallapplications_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '79_recommendedallapplications_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "7"
                save_sub_permission.sub_function_level = "recommendation"
                save_sub_permission.function_level = "recommendedallapplications"
                save_sub_permission.sequence = "92"
                save_sub_permission.save()

        elif 'approval'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "approvalnewapplication").delete()
            if 'data_managment80' in request.POST and 'approvalnewapplication' in  request.POST['data_managment80']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '80_approvalnewapplication_0' in dict(request.POST)['data_managment80']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment80']:
                        if '80_approvalnewapplication_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '80_approvalnewapplication_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '80_approvalnewapplication_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '80_approvalnewapplication_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "approvalnewapplication"
                save_sub_permission.sequence = "93"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "approvalapproved").delete()
            if 'data_managment81' in request.POST and 'approvalapproved' in  request.POST['data_managment81']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '81_approvalapproved_0' in dict(request.POST)['data_managment81']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment81']:
                        if '81_approvalapproved_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '81_approvalapproved_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '81_approvalapproved_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '81_approvalapproved_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "approvalapproved"
                save_sub_permission.sequence = "94"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "pendingforapproval").delete()
            if 'data_managment82' in request.POST and 'pendingforapproval' in  request.POST['data_managment82']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '82_pendingforapproval_0' in dict(request.POST)['data_managment82']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment82']:
                        if '82_pendingforapproval_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '82_pendingforapproval_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '82_pendingforapproval_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '82_pendingforapproval_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "pendingforapproval"
                save_sub_permission.sequence = "95"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "approvalapplicationexpires").delete()
            if 'data_managment83' in request.POST and 'approvalapplicationexpires' in  request.POST['data_managment83']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '83_approvalapplicationexpires_0' in dict(request.POST)['data_managment83']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment83']:
                        if '83_approvalapplicationexpires_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '83_approvalapplicationexpires_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '83_approvalapplicationexpires_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '83_approvalapplicationexpires_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "approvalapplicationexpires"
                save_sub_permission.sequence = "96"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "approvalapplicationrejected").delete()
            if 'data_managment84' in request.POST and 'approvalapplicationrejected' in  request.POST['data_managment84']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '84_approvalapplicationrejected_0' in dict(request.POST)['data_managment84']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment84']:
                        if '84_approvalapplicationrejected_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '84_approvalapplicationrejected_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '84_approvalapplicationrejected_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '84_approvalapplicationrejected_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "approvalapplicationrejected"
                save_sub_permission.sequence = "97"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "approvalapplicationforreview").delete()
            if 'data_managment85' in request.POST and 'approvalapplicationforreview' in  request.POST['data_managment85']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '85_approvalapplicationforreview_0' in dict(request.POST)['data_managment85']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment85']:
                        if '85_approvalapplicationforreview_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '85_approvalapplicationforreview_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '85_approvalapplicationforreview_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '85_approvalapplicationforreview_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "approvalapplicationforreview"
                save_sub_permission.sequence = "98"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "approval", main_function = "8", function_level = "approvalallapplications").delete()
            if 'data_managment86' in request.POST and 'approvalallapplications' in  request.POST['data_managment86']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '86_approvalallapplications_0' in dict(request.POST)['data_managment86']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment86']:
                        if '86_approvalallapplications_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '86_approvalallapplications_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '86_approvalallapplications_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '86_approvalallapplications_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "8"
                save_sub_permission.sub_function_level = "approval"
                save_sub_permission.function_level = "approvalallapplications"
                save_sub_permission.sequence = "99"
                save_sub_permission.save()


        elif 'loansanctioned'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "newapplicationsanctioned").delete()
            if 'data_managment87' in request.POST and 'newapplicationsanctioned' in  request.POST['data_managment87']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '87_newapplicationsanctioned_0' in dict(request.POST)['data_managment87']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment87']:
                        if '87_newapplicationsanctioned_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '87_newapplicationsanctioned_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '87_newapplicationsanctioned_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '87_newapplicationsanctioned_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "newapplicationsanctioned"
                save_sub_permission.sequence = "100"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "sanctionletterissue").delete()
            if 'data_managment88' in request.POST and 'sanctionletterissue' in  request.POST['data_managment88']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '88_sanctionletterissue_0' in dict(request.POST)['data_managment88']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment88']:
                        if '88_sanctionletterissue_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '88_sanctionletterissue_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '88_sanctionletterissue_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '88_sanctionletterissue_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "sanctionletterissue"
                save_sub_permission.sequence = "101"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "pendingforsanctionletter").delete()
            if 'data_managment89' in request.POST and 'pendingforsanctionletter' in  request.POST['data_managment89']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '89_pendingforsanctionletter_0' in dict(request.POST)['data_managment89']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment89']:
                        if '89_pendingforsanctionletter_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '89_pendingforsanctionletter_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '89_pendingforsanctionletter_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '89_pendingforsanctionletter_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "pendingforsanctionletter"
                save_sub_permission.sequence = "102"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "sanctionletterexpired").delete()
            if 'data_managment90' in request.POST and 'sanctionletterexpired' in  request.POST['data_managment90']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '90_sanctionletterexpired_0' in dict(request.POST)['data_managment90']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment90']:
                        if '90_sanctionletterexpired_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '90_sanctionletterexpired_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '90_sanctionletterexpired_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '90_sanctionletterexpired_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "sanctionletterexpired"
                save_sub_permission.sequence = "103"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "validsanctionletter").delete()
            if 'data_managment91' in request.POST and 'validsanctionletter' in  request.POST['data_managment91']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '91_validsanctionletter_0' in dict(request.POST)['data_managment91']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment91']:
                        if '91_validsanctionletter_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '91_validsanctionletter_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '91_validsanctionletter_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '91_validsanctionletter_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "validsanctionletter"
                save_sub_permission.sequence = "104"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "sanctionletteracceptbyclient").delete()
            if 'data_managment92' in request.POST and 'sanctionletteracceptbyclient' in  request.POST['data_managment92']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '92_sanctionletteracceptbyclient_0' in dict(request.POST)['data_managment92']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment92']:
                        if '92_sanctionletteracceptbyclient_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '92_sanctionletteracceptbyclient_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '92_sanctionletteracceptbyclient_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '92_sanctionletteracceptbyclient_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "sanctionletteracceptbyclient"
                save_sub_permission.sequence = "105"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "sanctionletterrejectbyclient").delete()
            if 'data_managment93' in request.POST and 'sanctionletterrejectbyclient' in  request.POST['data_managment93']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '93_sanctionletterrejectbyclient_0' in dict(request.POST)['data_managment93']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment93']:
                        if '93_sanctionletterrejectbyclient_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '93_sanctionletterrejectbyclient_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '93_sanctionletterrejectbyclient_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '93_sanctionletterrejectbyclient_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "sanctionletterrejectbyclient"
                save_sub_permission.sequence = "106"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "loansanctioned", main_function = "9", function_level = "sanctionletterrejectbycompany").delete()
            if 'data_managment94' in request.POST and 'sanctionletterrejectbycompany' in  request.POST['data_managment94']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '94_sanctionletterrejectbycompany_0' in dict(request.POST)['data_managment94']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['data_managment94']:
                        if '94_sanctionletterrejectbycompany_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '94_sanctionletterrejectbycompany_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '94_sanctionletterrejectbycompany_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '94_sanctionletterrejectbycompany_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "9"
                save_sub_permission.sub_function_level = "loansanctioned"
                save_sub_permission.function_level = "sanctionletterrejectbycompany"
                save_sub_permission.sequence = "107"
                save_sub_permission.save()


        elif 'clientdashboard'  in request.POST:
            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "applyfornewloan").delete()
            if 'dashboard_managment_1' in request.POST and 'applyfornewloan' in  request.POST['dashboard_managment_1']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '1_applyfornewloan_0' in dict(request.POST)['dashboard_managment_1']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_1']:
                        if '1_applyfornewloan_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '1_applyfornewloan_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '1_applyfornewloan_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '1_applyfornewloan_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "applyfornewloan"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "applicationstatus").delete()
            if 'dashboard_managment_2' in request.POST and 'applicationstatus' in  request.POST['dashboard_managment_2']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '2_applicationstatus_0' in dict(request.POST)['dashboard_managment_2']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_2']:
                        if '2_applicationstatus_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '2_applicationstatus_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '2_applicationstatus_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '2_applicationstatus_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "applicationstatus"
                save_sub_permission.save()



            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "myscorecard").delete()
            if 'dashboard_managment_3' in request.POST and 'myscorecard' in  request.POST['dashboard_managment_3']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '3_myscorecard_0' in dict(request.POST)['dashboard_managment_3']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_3']:
                        if '3_myscorecard_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '3_myscorecard_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '3_myscorecard_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '3_myscorecard_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "myscorecard"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "loanhistory").delete()
            if 'dashboard_managment_4' in request.POST and 'loanhistory' in  request.POST['dashboard_managment_4']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '4_loanhistory_0' in dict(request.POST)['dashboard_managment_4']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_4']:
                        if '4_loanhistory_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '4_loanhistory_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '4_loanhistory_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '4_loanhistory_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "loanhistory"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboarddisbursement").delete()
            if 'dashboard_managment_5' in request.POST and 'clientdashboarddisbursement' in  request.POST['dashboard_managment_5']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '5_clientdashboarddisbursement_0' in dict(request.POST)['dashboard_managment_5']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_5']:
                        if '5_clientdashboarddisbursement_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '5_clientdashboarddisbursement_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '5_clientdashboarddisbursement_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '5_clientdashboarddisbursement_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboarddisbursement"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardprepayment").delete()
            if 'dashboard_managment_6' in request.POST and 'clientdashboardprepayment' in  request.POST['dashboard_managment_6']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '6_clientdashboardprepayment_0' in dict(request.POST)['dashboard_managment_6']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_6']:
                        if '6_clientdashboardprepayment_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '6_clientdashboardprepayment_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '6_clientdashboardprepayment_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '6_clientdashboardprepayment_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardprepayment"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardemipayment").delete()
            if 'dashboard_managment_7' in request.POST and 'clientdashboardemipayment' in  request.POST['dashboard_managment_7']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '7_clientdashboardemipayment_0' in dict(request.POST)['dashboard_managment_7']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_7']:
                        if '7_clientdashboardemipayment_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '7_clientdashboardemipayment_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '7_clientdashboardemipayment_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '7_clientdashboardemipayment_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardemipayment"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardtopup").delete()
            if 'dashboard_managment_8' in request.POST and 'clientdashboardtopup' in  request.POST['dashboard_managment_8']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '8_clientdashboardtopup_0' in dict(request.POST)['dashboard_managment_8']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_8']:
                        if '8_clientdashboardtopup_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '8_clientdashboardtopup_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '8_clientdashboardtopup_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '8_clientdashboardtopup_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardtopup"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardnewloan").delete()
            if 'dashboard_managment_9' in request.POST and 'clientdashboardnewloan' in  request.POST['dashboard_managment_9']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '9_clientdashboardnewloan_0' in dict(request.POST)['dashboard_managment_9']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_9']:
                        if '9_clientdashboardnewloan_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '9_clientdashboardnewloan_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '9_clientdashboardnewloan_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '9_clientdashboardnewloan_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardnewloan"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardloanclosure").delete()
            if 'dashboard_managment_10' in request.POST and 'clientdashboardloanclosure' in  request.POST['dashboard_managment_10']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '10_clientdashboardloanclosure_0' in dict(request.POST)['dashboard_managment_10']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_10']:
                        if '10_clientdashboardloanclosure_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '10_clientdashboardloanclosure_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '10_clientdashboardloanclosure_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '10_clientdashboardloanclosure_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardloanclosure"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardrepaymentdue").delete()
            if 'dashboard_managment_11' in request.POST and 'clientdashboardrepaymentdue' in  request.POST['dashboard_managment_11']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '11_clientdashboardrepaymentdue_0' in dict(request.POST)['dashboard_managment_11']:
                    save_sub_permission.permission_add = "1"
                    save_sub_permission.permission_edit = "2"
                    save_sub_permission.permission_delete = "3"
                    save_sub_permission.permission_view = "4"
                else:
                    for data in dict(request.POST)['dashboard_managment_11']:
                        if '11_clientdashboardrepaymentdue_1' in data:
                            save_sub_permission.permission_add = "1"
                        if '11_clientdashboardrepaymentdue_2' in data:
                            save_sub_permission.permission_edit = "2"
                        if '11_clientdashboardrepaymentdue_3' in data:
                            save_sub_permission.permission_delete = "3"
                        if '11_clientdashboardrepaymentdue_4' in data:
                            save_sub_permission.permission_view = "4"
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardrepaymentdue"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardpastrepayments").delete()
            if 'dashboard_managment_12' in request.POST and 'clientdashboardpastrepayments' in  request.POST['dashboard_managment_12']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '12_clientdashboardpastrepayments_0' in dict(request.POST)['dashboard_managment_12']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_12']:
                        if '12_clientdashboardpastrepayments_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '12_clientdashboardpastrepayments_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardpastrepayments"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardsanctionletter").delete()
            if 'dashboard_managment_13' in request.POST and 'clientdashboardsanctionletter' in  request.POST['dashboard_managment_13']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '13_clientdashboardsanctionletter_0' in dict(request.POST)['dashboard_managment_13']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_13']:
                        if '13_clientdashboardsanctionletter_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '13_clientdashboardsanctionletter_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardsanctionletter"
                save_sub_permission.save()



            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardagreements").delete()
            if 'dashboard_managment_14' in request.POST and 'clientdashboardagreements' in  request.POST['dashboard_managment_14']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '14_clientdashboardagreements_0' in dict(request.POST)['dashboard_managment_14']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_14']:
                        if '14_clientdashboardagreements_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '14_clientdashboardagreements_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardagreements"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardlistofdocuments").delete()
            if 'dashboard_managment_15' in request.POST and 'clientdashboardlistofdocuments' in  request.POST['dashboard_managment_15']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '15_clientdashboardlistofdocuments_0' in dict(request.POST)['dashboard_managment_15']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_15']:
                        if '15_clientdashboardlistofdocuments_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '15_clientdashboardlistofdocuments_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardlistofdocuments"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardstatements").delete()
            if 'dashboard_managment_16' in request.POST and 'clientdashboardstatements' in  request.POST['dashboard_managment_16']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '16_clientdashboardstatements_0' in dict(request.POST)['dashboard_managment_16']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_16']:
                        if '16_clientdashboardstatements_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '16_clientdashboardstatements_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardstatements"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboarrecipts").delete()
            if 'dashboard_managment_17' in request.POST and 'clientdashboarrecipts' in  request.POST['dashboard_managment_17']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '17_clientdashboarrecipts_0' in dict(request.POST)['dashboard_managment_17']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_17']:
                        if '17_clientdashboarrecipts_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '17_clientdashboarrecipts_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboarrecipts"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardinvoices").delete()
            if 'dashboard_managment_18' in request.POST and 'clientdashboardinvoices' in  request.POST['dashboard_managment_18']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '18_clientdashboardinvoices_0' in dict(request.POST)['dashboard_managment_18']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_18']:
                        if '18_clientdashboardinvoices_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '18_clientdashboardinvoices_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardinvoices"
                save_sub_permission.save()



            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardcommunicationreceived").delete()
            if 'dashboard_managment_19' in request.POST and 'clientdashboardcommunicationreceived' in  request.POST['dashboard_managment_19']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '19_clientdashboardcommunicationreceived_0' in dict(request.POST)['dashboard_managment_19']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_19']:
                        if '19_clientdashboardcommunicationreceived_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '19_clientdashboardcommunicationreceived_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardcommunicationreceived"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardcommunicationmade").delete()
            if 'dashboard_managment_20' in request.POST and 'clientdashboardcommunicationmade' in  request.POST['dashboard_managment_20']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '20_clientdashboardcommunicationmade_0' in dict(request.POST)['dashboard_managment_20']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_20']:
                        if '20_clientdashboardcommunicationmade_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '20_clientdashboardcommunicationmade_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardcommunicationmade"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardhelp").delete()
            if 'dashboard_managment_21' in request.POST and 'clientdashboardhelp' in  request.POST['dashboard_managment_21']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '21_clientdashboardhelp_0' in dict(request.POST)['dashboard_managment_21']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_21']:
                        if '21_clientdashboardhelp_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '21_clientdashboardhelp_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardhelp"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardmyprofile").delete()
            if 'dashboard_managment_22' in request.POST and 'clientdashboardmyprofile' in  request.POST['dashboard_managment_22']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '22_clientdashboardmyprofile_0' in dict(request.POST)['dashboard_managment_22']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_22']:
                        if '22_clientdashboardmyprofile_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '22_clientdashboardmyprofile_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardmyprofile"
                save_sub_permission.save()

            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardmychangepassword").delete()
            if 'dashboard_managment_23' in request.POST and 'clientdashboardmychangepassword' in  request.POST['dashboard_managment_23']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '23_clientdashboardmychangepassword_0' in dict(request.POST)['dashboard_managment_23']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_23']:
                        if '23_clientdashboardmychangepassword_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '23_clientdashboardmychangepassword_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardmychangepassword"
                save_sub_permission.save()


            UserAccessPermissonModelsPermission.objects.filter(user_id = request.POST['user_id'], sub_function_level = "clientdashboard", main_function = "10", function_level = "clientdashboardlogout").delete()
            if 'dashboard_managment_24' in request.POST and 'clientdashboardlogout' in  request.POST['dashboard_managment_24']:
                save_sub_permission = UserAccessPermissonModelsPermission()
                save_sub_permission.user_id = request.POST['user_id']
                if '24_clientdashboardlogout_0' in dict(request.POST)['dashboard_managment_24']:
                    save_sub_permission.permission_show = "1"
                    save_sub_permission.permission_hide = "2"
                    
                else:
                    for data in dict(request.POST)['dashboard_managment_24']:
                        if '24_clientdashboardlogout_1' in data:
                            save_sub_permission.permission_show = "1"
                        if '24_clientdashboardlogout_2' in data:
                            save_sub_permission.permission_hide = "2"
                        
                save_sub_permission.main_function = "10"
                save_sub_permission.sub_function_level = "clientdashboard"
                save_sub_permission.function_level = "clientdashboardlogout"
                save_sub_permission.save()

        return redirect("crm_provide_permission_access_permission")
