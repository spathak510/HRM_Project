from __future__ import unicode_literals
import csv
import json
import random
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
from django.db.models import Q
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
from aditshsoft.common import CommonPagination
from aditshsoft.common import Getmonthlist, SiteUrl
from aditshsoft.common import Getyearlist, time_slots, Getyearlist1
from hrms_management.models import *
from admin_main.models import *
from hrms_management.forms import *
from hrms_employees.forms import *





# Define Reporting Structure
class DefineReportingStructureList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageEmployeeReportingStructure.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineReportingStructure(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/define_reporting_structure_add_edit.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = EmployeeServiceEmployeeReportingStructureForm()
        else:
            data = get_object_or_404(ManageEmployeeReportingStructure, pk=id)
            form = EmployeeServiceEmployeeReportingStructureForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):

        if id is None:
            form = EmployeeServiceEmployeeReportingStructureForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageEmployeeReportingStructure, pk=id)
            form = EmployeeServiceEmployeeReportingStructureForm(request.POST, instance = data)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_reportingstructure_list')


class DefineReportingStructureDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageEmployeeReportingStructure.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_reportingstructure_list')

# Define Employee ID
class DefineEmployeeIDList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/define_employees_id_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageEmployeeId.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineEmployeeID(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/define_employees_id_add_edit.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = EmployeeIDForm()
        else:
            data = get_object_or_404(ManageEmployeeId, pk=id)
            form = EmployeeIDForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = EmployeeIDForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = ''.join(random.choice(string.digits) for i in range(5))
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManageEmployeeId, pk=id)
            form = EmployeeIDForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = ''.join(random.choice(string.digits) for i in range(5))
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_employeeid_list')


class DefineEmployeeIDDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageEmployeeId.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_employeeid_list')


# Manage Grade 
class ManageGradeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/manage_grade_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageGrade.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManageGrade(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_grade.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageGradeForm()
        else:
            data = get_object_or_404(ManageGrade, pk=id)
            form = ManageGradeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageGradeForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageGrade, pk=id)
            form = ManageGradeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_managegrade_list')


class ManageGradeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageGrade.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_managegrade_list')


# Manage Salary Range
class ManageSalaryRangeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/manage_salary_range_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageSalaryRange.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManageSalaryRange(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_salary_range.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageSalaryRangeForm()
        else:
            data = get_object_or_404(ManageSalaryRange, pk=id)
            form = ManageSalaryRangeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageSalaryRangeForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageSalaryRange, pk=id)
            form = ManageSalaryRangeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_managesalaryrange_list')


class ManageSalaryRangeDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageSalaryRange.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_managesalaryrange_list')


# Define Salary
class DefineSalaryList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/define_salary_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageSalary.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineSalary(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_define_salary.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = DefineSalaryForm()
        else:
            data = get_object_or_404(ManageSalary, pk=id)
            form = DefineSalaryForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = DefineSalaryForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageSalary, pk=id)
            form = DefineSalaryForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_definesalary_list')


class DefineSalaryDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageSalary.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_definesalary_list')

# Define Deduction
class DefineDeductionsStuctureList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/define_deductions_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageDeductionsStructure.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template, {'responselistquery': report_paginate})


class AddEditDefineDeductionsStucture(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_define_deductions.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = DefineDeductionsModelForm()
        else:
            data = get_object_or_404(ManageDeductionsStructure, pk=id)
            form = DefineDeductionsModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = DefineDeductionsModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageDeductionsStructure, pk=id)
            form = DefineDeductionsModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_define_deductions_list')


class DefineDeductionsStuctureDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageDeductionsStructure.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_define_deductions_list')


# Define Other Income
class DefineOtherIncomeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/define_other_Income_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageOtherIncome.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineOtherIncome(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_define_other_Income.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = DefineOtherIncomeForm()
        else:
            data = get_object_or_404(ManageOtherIncome, pk=id)
            form = DefineOtherIncomeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = DefineOtherIncomeForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageOtherIncome, pk=id)
            form = DefineOtherIncomeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_otherincome_list')


class DefineOtherIncomeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageOtherIncome.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_otherincome_list')


# Define Other Income
class ManageLanguageList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/manage_language_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageLanguage.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManageLanguage(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_language.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageLanguageForm()
        else:
            data = get_object_or_404(ManageLanguage, pk=id)
            form = ManageLanguageForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageLanguageForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageLanguage, pk=id)
            form = ManageLanguageForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_language_list')


class ManageLanguageDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageLanguage.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_language_list')


# Define Manage Qualification
class ManageQualificationList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/manage_qualification_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_data = ManageQualification.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManageQualification(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_qualification.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageQualificationForm()
        else:
            data = get_object_or_404(ManageQualification, pk=id)
            form = ManageQualificationForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageQualificationForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageQualification, pk=id)
            form = ManageQualificationForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_qualification_list')


class ManageQualificationDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageQualification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_qualification_list')


# Define Manage Expereince 
class ManageExpereinceList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/manage_expereince_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageExpereince.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManageExpereince(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_expereince.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageExpereinceForm()
        else:
            data = get_object_or_404(ManageExpereince, pk=id)
            form = ManageExpereinceForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageExpereinceForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManageExpereince, pk=id)
            form = ManageExpereinceForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_expereince_list')


class ManageExpereinceDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageExpereince.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_expereince_list')


# Define Manage Expereince 
class ManageFamilyList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/manage_family_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageFamily.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManageFamily(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_family.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageFamilyForm()
        else:
            data = get_object_or_404(ManageFamily, pk=id)
            form = ManageFamilyForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageFamilyForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManageFamily, pk=id)
            form = ManageFamilyForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_family_list')


class ManageFamilyDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageFamily.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_family_list')


# PayRoll
class DefineTaxStructureList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/tax_structure_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagePayRollTaxStructure.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineTaxStructure(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_define_tax_structure.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagePayRollDefineTaxStructureModelForm()
        else:
            data = get_object_or_404(ManagePayRollTaxStructure, pk=id)
            form = ManagePayRollDefineTaxStructureModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagePayRollDefineTaxStructureModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManagePayRollTaxStructure, pk=id)
            form = ManagePayRollDefineTaxStructureModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_taxstructure_list')


class DefineTaxStructureDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePayRollTaxStructure.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_taxstructure_list')

# ///
class DefineReimbursementList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/define_reimbursement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagePayRollReimbursement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditDefineReimbursement(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_define_reimbursement.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagePayRollDefineReimbursementModelForm()
        else:
            data = get_object_or_404(ManagePayRollReimbursement, pk=id)
            form = ManagePayRollDefineReimbursementModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagePayRollDefineReimbursementModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManagePayRollReimbursement, pk=id)
            form = ManagePayRollDefineReimbursementModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_reimbursement_list')


class DefineReimbursementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePayRollReimbursement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_reimbursement_list')

# ****
class DefineExemptedIncomeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/define_exempted_Income_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagePayRollExemptedIncome.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineExemptedIncome(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_define_exempted_Income.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagePayRollDefineExemptedIncomeModelForm()
        else:
            data = get_object_or_404(ManagePayRollExemptedIncome, pk=id)
            form = ManagePayRollDefineExemptedIncomeModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None): 
       
        if id is None:
            form = ManagePayRollDefineExemptedIncomeModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManagePayRollExemptedIncome, pk=id)
            form = ManagePayRollDefineExemptedIncomeModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_exemptedincome_list')


class DefineExemptedIncomeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePayRollExemptedIncome.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_exemptedincome_list')

# ---------------

class DefineStatutoryDeductionsList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/define_statutory_deductions_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagePayRollDefineStatutoryDeductions.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineStatutoryDeductions(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_define_statutory_deductions.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagePayRollDefineStatutoryDeductionsModelForm()
        else:
            data = get_object_or_404(ManagePayRollDefineStatutoryDeductions, pk=id)
            form = ManagePayRollDefineStatutoryDeductionsModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagePayRollDefineStatutoryDeductionsModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManagePayRollDefineStatutoryDeductions, pk=id)
            form = ManagePayRollDefineStatutoryDeductionsModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')


class DefineStatutoryDeductionsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePayRollDefineStatutoryDeductions.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')


# ++++++

class DefineAdvancesList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/define_advances_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagePayRollDefineAdvances.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineAdvances(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_define_advances.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagePayRollDefineAdvancesModelForm()
        else:
            data = get_object_or_404(ManagePayRollDefineAdvances, pk=id)
            form = ManagePayRollDefineAdvancesModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagePayRollDefineAdvancesModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManagePayRollDefineAdvances, pk=id)
            form = ManagePayRollDefineAdvancesModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                data.unique_id = str(data.id).zfill(5)
                data.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_advances_list')


class DefineAdvancesDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePayRollDefineAdvances.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_advances_list')


class DefineDeductionsList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/define_deductions_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagePayRollDeductions.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditDefineDeductions(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_define_deductions.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagePayRollDefineDeductionsModelForm()
        else:
            data = get_object_or_404(ManagePayRollDeductions, pk=id)
            form = ManagePayRollDefineDeductionsModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagePayRollDefineDeductionsModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(ManagePayRollDeductions, pk=id)
            form = ManagePayRollDefineDeductionsModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_deductions_list')


class DefineDeductionsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagePayRollDeductions.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_deductions_list')

# Holidays and Leaves

class HolidaysandLeavesDefineLeaveTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/holidays_and_leaves/define_leave_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = HolidaysandLeavesLeaveType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditHolidaysandLeavesDefineLeaveTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/holidays_and_leaves/add_edit_define_leave_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = HolidaysandLeavesDefineLeaveTypeModelForm()
        else:
            data = get_object_or_404(HolidaysandLeavesLeaveType, pk=id)
            form = HolidaysandLeavesDefineLeaveTypeModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = HolidaysandLeavesDefineLeaveTypeModelForm(request.POST)
            if form.is_valid():
                data = form.save()

                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(HolidaysandLeavesLeaveType, pk=id)
            form = HolidaysandLeavesDefineLeaveTypeModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_holidaysandleaves_defineleavetype_list')


class HolidaysandLeavesDefineLeaveTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = HolidaysandLeavesLeaveType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_holidaysandleaves_defineleavetype_list')


class HolidaysandLeavesManageLeaveQoutaList(View):
    template = 'admin_template/crm_employees/emplyees_services/holidays_and_leaves/manage_leave_qouta_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = HolidaysandLeavesManageLeaveQouta.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditHolidaysandLeavesManageLeaveQoutaList(View):
    template = 'admin_template/crm_employees/emplyees_services/holidays_and_leaves/add_edit_manage_leave_qouta.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = HolidaysandLeavesManageLeaveQoutaModelForm()
        else:
            data = get_object_or_404(HolidaysandLeavesManageLeaveQouta, pk=id)
            form = HolidaysandLeavesManageLeaveQoutaModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = HolidaysandLeavesManageLeaveQoutaModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(HolidaysandLeavesManageLeaveQouta, pk=id)
            form = HolidaysandLeavesManageLeaveQoutaModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_holidaysandleaves_manageleaveqouta_list')


class HolidaysandLeavesManageLeaveQoutaDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = HolidaysandLeavesManageLeaveQouta.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_holidaysandleaves_manageleaveqouta_list')


# Manage Claims
class ManageClaimsDefineClaimTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/define_claim_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageClaimType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmManageClaimsDefineClaimType(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_define_claim_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageClaimsDefineClaimTypeModelForm()
        else:
            data = get_object_or_404(ManageClaimType, pk=id)
            form = ManageClaimsDefineClaimTypeModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageClaimsDefineClaimTypeModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManageClaimType, pk=id)
            form = ManageClaimsDefineClaimTypeModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageclaims_claimtype_list')


class ManageClaimsDefineClaimTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageClaimType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageclaims_claimtype_list')



class ManageClaimsClaimEntitlementList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/claim_entitlement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageClaimsClaimEntitlement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmManageClaimsClaimEntitlement(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_claim_entitlement.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageClaimsDefineClaimEntitlementModelForm()
        else:
            data = get_object_or_404(ManageClaimsClaimEntitlement, pk=id)
            form = ManageClaimsDefineClaimEntitlementModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageClaimsDefineClaimEntitlementModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManageClaimsClaimEntitlement, pk=id)
            form = ManageClaimsDefineClaimEntitlementModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageclaims_claimentitlement_list')


class ManageClaimsClaimEntitlementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageClaimsClaimEntitlement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageclaims_claimentitlement_list')


#Travel 
class TravelandClaimTravelManagementDefineModeofTravelList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/define_mode_of_travel_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = TravelandClaimTravelManagementModeofTravel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditTravelandClaimTravelManagementDefineModeofTravel(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_define_mode_of_travel.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = TravelandClaimTravelManagementDefineModeofTravelForm()
        else:
            data = get_object_or_404(TravelandClaimTravelManagementModeofTravel, pk=id)
            form = TravelandClaimTravelManagementDefineModeofTravelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = TravelandClaimTravelManagementDefineModeofTravelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(TravelandClaimTravelManagementModeofTravel, pk=id)
            form = TravelandClaimTravelManagementDefineModeofTravelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_manageclaims_modeoftravel_list')


class TravelandClaimTravelManagementDefineModeofTravelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TravelandClaimTravelManagementModeofTravel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageclaims_modeoftravel_list')


class TravelandClaimTravelManagementDefineTravelTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/travel_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = TravelandClaimTravelManagementTravelType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditTravelandClaimTravelManagementDefineTravelType(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_travel_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = TravelandClaimTravelManagementDefineTravelTypeForm()
        else:
            data = get_object_or_404(TravelandClaimTravelManagementTravelType, pk=id)
            form = TravelandClaimTravelManagementDefineTravelTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = TravelandClaimTravelManagementDefineTravelTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(TravelandClaimTravelManagementTravelType, pk=id)
            form = TravelandClaimTravelManagementDefineTravelTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('crm_crmemployee_manageclaims_traveltype_list')


class TravelandClaimTravelManagementDefineTravelTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TravelandClaimTravelManagementTravelType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageclaims_traveltype_list')


# 
class TravelandClaimTravelManagementDefineTravelPolicyList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/travel_policy_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = TravelandClaimTravelManagementTravelPolicy.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditTravelandClaimTravelManagementDefineTravelPolicy(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_travel_policy.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = TravelandClaimTravelManagementDefineTravelPolicyForm()
        else:
            data = get_object_or_404(TravelandClaimTravelManagementTravelPolicy, pk=id)
            form = TravelandClaimTravelManagementDefineTravelPolicyForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = TravelandClaimTravelManagementDefineTravelPolicyForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(TravelandClaimTravelManagementTravelPolicy, pk=id)
            form = TravelandClaimTravelManagementDefineTravelPolicyForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('crm_crmemployee_manageclaims_travelpolicy_list')


class TravelandClaimTravelManagementDefineTravelPolicyDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TravelandClaimTravelManagementTravelPolicy.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageclaims_travelpolicy_list')


#
class TravelandClaimTravelManagementManageTravelList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/manage_travel_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = TravelandClaimTravelManagementManageTravel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditTravelandClaimTravelManagementManageTravel(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_manage_travel.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = TravelandClaimTravelManagementManageTravelForm()
        else:
            data = get_object_or_404(TravelandClaimTravelManagementManageTravel, pk=id)
            form = TravelandClaimTravelManagementManageTravelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = TravelandClaimTravelManagementManageTravelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(TravelandClaimTravelManagementManageTravel, pk=id)
            form = TravelandClaimTravelManagementManageTravelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('crm_crmemployee_manageclaims_managetravel_list')


class TravelandClaimTravelManagementManageTravelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = TravelandClaimTravelManagementManageTravel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageclaims_managetravel_list') 


# Manage Reimbursement 
class ManageReimbursementDefineReimbursementList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_reimbursement/define_reimbursement_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageReimbursement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmManageReimbursementDefineReimbursement(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_reimbursement/add_edit_define_reimbursement_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageReimbursementDefineReimbursementModelForm()
        else:
            data = get_object_or_404(ManageReimbursement, pk=id)
            form = ManageReimbursementDefineReimbursementModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageReimbursementDefineReimbursementModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageReimbursement, pk=id)
            form = ManageReimbursementDefineReimbursementModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_managereimbursement_reimbursementtype_list')


class ManageReimbursementDefineReimbursementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageReimbursement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_managereimbursement_reimbursementtype_list')


class ManageReimbursementReimbursementEntitilementList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_reimbursement/define_reimbursement_entitilement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageReimbursementReimbursementEntitilement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmManageReimbursementReimbursementEntitilement(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_reimbursement/add_edit_define_reimbursement_entitilement.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageReimbursementReimbursementEntitilementModelForm()
        else:
            data = get_object_or_404(ManageReimbursementReimbursementEntitilement, pk=id)
            form = ManageReimbursementReimbursementEntitilementModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManageReimbursementReimbursementEntitilementModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageReimbursementReimbursementEntitilement, pk=id)
            form = ManageReimbursementReimbursementEntitilementModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_managereimbursement_claimentitlement_list')


class ManageReimbursementReimbursementEntitilementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageReimbursementReimbursementEntitilement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_managereimbursement_claimentitlement_list')

# Recruitement Policies  ------------------
# 1 
class RecruitementPoliciesDefineEmployeeStrengthList(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/define_employee_strength_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitementPoliciesDefineEmployeeStrength.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmRecruitementPoliciesDefineEmployeeStrength(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/add_edit_define_employee_strength.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitementPoliciesDefineEmployeeStrengthModelForm()
        else:
            data = get_object_or_404(RecruitementPoliciesDefineEmployeeStrength, pk=id)
            form = RecruitementPoliciesDefineEmployeeStrengthModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitementPoliciesDefineEmployeeStrengthModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitementPoliciesDefineEmployeeStrength, pk=id)
            form = RecruitementPoliciesDefineEmployeeStrengthModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_recruitementpolicies_employeestrength_list')


class RecruitementPoliciesDefineEmployeeStrengthDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitementPoliciesDefineEmployeeStrength.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitementpolicies_employeestrength_list')

# 2
class RecruitementPoliciesDefineQualificationModelList(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/define_qualification_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitementPoliciesDefineQualification.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmRecruitementPoliciesDefineQualificationModel(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/add_edit_define_qualification.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitementPoliciesDefineQualificationModelForm()
        else:
            data = get_object_or_404(RecruitementPoliciesDefineQualification, pk=id)
            form = RecruitementPoliciesDefineQualificationModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitementPoliciesDefineQualificationModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitementPoliciesDefineQualification, pk=id)
            form = RecruitementPoliciesDefineQualificationModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_recruitementpolicies_qualification_list')


class RecruitementPoliciesDefineQualificationModelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitementPoliciesDefineQualification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitementpolicies_qualification_list')

# 3
class RecruitementPoliciesDefineExperienceModelList(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/define_experience_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitementPoliciesDefineExperience.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmRecruitementPoliciesDefineExperienceModel(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/add_edit_define_experience.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitementPoliciesDefineExperienceModelForm()
        else:
            data = get_object_or_404(RecruitementPoliciesDefineExperience, pk=id)
            form = RecruitementPoliciesDefineExperienceModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitementPoliciesDefineExperienceModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitementPoliciesDefineExperience, pk=id)
            form = RecruitementPoliciesDefineExperienceModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_recruitementpolicies_experience_list')


class RecruitementPoliciesDefineExperienceModelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitementPoliciesDefineExperience.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitementpolicies_experience_list')

# 4
class RecruitementPoliciesManageRecruitmentRulesModelList(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/manage_recruitment_rules_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitementPoliciesManageRecruitmentRules.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmRecruitementPoliciesManageRecruitmentRulesModel(View):
    template = 'admin_template/crm_employees/emplyees_services/recruitement_policies/add_edit_manage_recruitment_rules.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitementPoliciesManageRecruitmentRulesModelForm()
        else:
            data = get_object_or_404(RecruitementPoliciesManageRecruitmentRules, pk=id)
            form = RecruitementPoliciesManageRecruitmentRulesModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitementPoliciesManageRecruitmentRulesModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitementPoliciesManageRecruitmentRules, pk=id)
            form = RecruitementPoliciesManageRecruitmentRulesModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_recruitementpolicies_recruitmentrules_list')


class RecruitementPoliciesManageRecruitmentRulesModelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitementPoliciesManageRecruitmentRules.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitementpolicies_recruitmentrules_list')


# HR Policies
class HRPoliciesDefinePolicyTypeModelList(View):
    template = 'admin_template/crm_employees/emplyees_services/hr_policies/define_policy_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = HRPoliciesPolicyType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditCrmHRPoliciesDefinePolicyTypeModel(View):
    template = 'admin_template/crm_employees/emplyees_services/hr_policies/add_edit_define_policy_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = HRPoliciesPolicyTypeForm()
        else:
            data = get_object_or_404(HRPoliciesPolicyType, pk=id)
            form = HRPoliciesPolicyTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = HRPoliciesPolicyTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(HRPoliciesPolicyType, pk=id)
            form = HRPoliciesPolicyTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_hrpolicies_policytype_list')


class HRPoliciesDefinePolicyTypeModelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = HRPoliciesPolicyType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_hrpolicies_policytype_list')


# Form
class PoliciesandFormsManagementHRPoliciesFormList(View):
    template = 'admin_template/crm_employees/emplyees_services/hr_policies/form_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PoliciesandFormsManagementHRPolicies.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditPoliciesandFormsManagementHRPoliciesForm(View):
    template = 'admin_template/crm_employees/emplyees_services/hr_policies/add_edit_form.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PoliciesandFormsManagementHRPoliciesFormModelForm()
        else:
            data = get_object_or_404(PoliciesandFormsManagementHRPolicies, pk=id)
            form = PoliciesandFormsManagementHRPoliciesFormModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = PoliciesandFormsManagementHRPoliciesFormModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(PoliciesandFormsManagementHRPolicies, pk=id)
            form = PoliciesandFormsManagementHRPoliciesFormModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crm_employee_hrpolicies_form_list')


class PoliciesandFormsManagementHRPoliciesFormDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PoliciesandFormsManagementHRPolicies.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crm_employee_hrpolicies_form_list')


# Recruite Management
class RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthList(View):
    template = 'admin_template/crm_employees/recruitment_management/employee_strength_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementRecruitmentPlanningEmployeeStrength.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditRecruitmentManagementRecruitmentPlanningDefineEmployeeStrength(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_employee_strength.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthForm()
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningEmployeeStrength, pk=id)
            form = RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningEmployeeStrength, pk=id)
            form = RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_employeestrength_list')


class RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitmentManagementRecruitmentPlanningEmployeeStrength.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_employeestrength_list')


class RecruitmentManagementRecruitmentPlanningDefineQualificationList(View):
    template = 'admin_template/crm_employees/recruitment_management/qualification_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementRecruitmentPlanningQualification.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditRecruitmentManagementRecruitmentPlanningDefineQualification(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_qualification.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningDefineQualificationForm()
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningQualification, pk=id)
            form = RecruitmentManagementRecruitmentPlanningDefineQualificationForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningDefineQualificationForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningQualification, pk=id)
            form = RecruitmentManagementRecruitmentPlanningDefineQualificationForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_recruitmentmanagement_qualification_list')


class RecruitmentManagementRecruitmentPlanningDefineQualificationDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitmentManagementRecruitmentPlanningQualification.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_qualification_list')


class RecruitmentManagementRecruitmentPlanningDefineExperienceList(View):
    template = 'admin_template/crm_employees/recruitment_management/define_experience_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementRecruitmentPlanningExperience.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditRecruitmentManagementRecruitmentPlanningDefineExperience(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_experience_list.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningDefineExperienceForm()
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningExperience, pk=id)
            form = RecruitmentManagementRecruitmentPlanningDefineExperienceForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningDefineExperienceForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningExperience, pk=id)
            form = RecruitmentManagementRecruitmentPlanningDefineExperienceForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_recruitmentmanagement_experience_list')


class RecruitmentManagementRecruitmentPlanningDefineExperienceDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RecruitmentManagementRecruitmentPlanningExperience.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_experience_list')


class RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesList(View):
    template = 'admin_template/crm_employees/recruitment_management/recruitment_rules_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementRecruitmentPlanningManageRecruitmentRules.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditRecruitmentManagementRecruitmentPlanningManageRecruitmentRules(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_recruitment_rules.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesForm()
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningManageRecruitmentRules, pk=id)
            form = RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(RecruitmentManagementRecruitmentPlanningManageRecruitmentRules, pk=id)
            form = RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('crm_crmemployee_recruitmentmanagement_recruitmentrules_list')


class RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementRecruitmentPlanningManageRecruitmentRules.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_recruitmentrules_list')

# 
class RecruitmentManagementCandidateSourcingManageJobPublishmentList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_job_publishment_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementCandidateSourcingManageJobPublishment.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementCandidateSourcingManageJobPublishment(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_manage_job_publishment.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementCandidateSourcingManageJobPublishmentForm()
        else:
            data = get_object_or_404(RecruitmentManagementCandidateSourcingManageJobPublishment, pk=id)
            form = RecruitmentManagementCandidateSourcingManageJobPublishmentForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementCandidateSourcingManageJobPublishmentForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementCandidateSourcingManageJobPublishment, pk=id)
            form = RecruitmentManagementCandidateSourcingManageJobPublishmentForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_candidatesourcing_list')


class RecruitmentManagementCandidateSourcingManageJobPublishmentDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementCandidateSourcingManageJobPublishment.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_candidatesourcing_list')


# 4
class RecruitmentManagementCandidateSourcingManageReceiptofResumeList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_receipt_of_resume_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementCandidateSourcingManageReceiptofResume.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementCandidateSourcingManageReceiptofResume(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_manage_receipt_of_resume.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementCandidateSourcingManageReceiptofResumeForm()
        else:
            data = get_object_or_404(RecruitmentManagementCandidateSourcingManageReceiptofResume, pk=id)
            form = RecruitmentManagementCandidateSourcingManageReceiptofResumeForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementCandidateSourcingManageReceiptofResumeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementCandidateSourcingManageReceiptofResume, pk=id)
            form = RecruitmentManagementCandidateSourcingManageReceiptofResumeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_managereceiptofresume_list')


class RecruitmentManagementCandidateSourcingManageReceiptofResumeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementCandidateSourcingManageReceiptofResume.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_managereceiptofresume_list')


# 111
class RecruitmentManagementInterveiwProcessDefineScreeningLevelList(View):
    template = 'admin_template/crm_employees/recruitment_management/screening_level_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementInterveiwProcessScreeningLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementInterveiwProcessDefineScreeningLevel(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_screening_level.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementInterveiwProcessDefineScreeningLevelForm()
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwProcessScreeningLevel, pk=id)
            form = RecruitmentManagementInterveiwProcessDefineScreeningLevelForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementInterveiwProcessDefineScreeningLevelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwProcessScreeningLevel, pk=id)
            form = RecruitmentManagementInterveiwProcessDefineScreeningLevelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_interveiwprocess_list')


class RecruitmentManagementInterveiwProcessDefineScreeningLevelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementInterveiwProcessScreeningLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_interveiwprocess_list')


# 66
class RecruitmentManagementInterveiwProcessManageInterviewProcessList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_interview_process_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementInterveiwProcessManageInterviewProcess.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementInterveiwProcessManageInterviewProcess(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_manage_interview_process.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementInterveiwProcessManageInterviewProcessForm()
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwProcessManageInterviewProcess, pk=id)
            form = RecruitmentManagementInterveiwProcessManageInterviewProcessForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementInterveiwProcessManageInterviewProcessForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwProcessManageInterviewProcess, pk=id)
            form = RecruitmentManagementInterveiwProcessManageInterviewProcessForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_manageinterviewprocess_list')


class RecruitmentManagementInterveiwProcessManageInterviewProcessDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementInterveiwProcessManageInterviewProcess.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_manageinterviewprocess_list')

# 7
class RecruitmentManagementInterveiwProcessDefineScorecardList(View):
    template = 'admin_template/crm_employees/recruitment_management/define_scorecard_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementInterveiwProcessScorecard.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementInterveiwProcessDefineScorecard(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_define_scorecard.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementInterveiwProcessDefineScorecardForm()
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwProcessScorecard, pk=id)
            form = RecruitmentManagementInterveiwProcessDefineScorecardForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementInterveiwProcessDefineScorecardForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwProcessScorecard, pk=id)
            form = RecruitmentManagementInterveiwProcessDefineScorecardForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_scorecard_list')


class RecruitmentManagementInterveiwProcessDefineScorecardDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementInterveiwProcessScorecard.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_scorecard_list')


# 8
class RecruitmentManagementInterveiwManageCandidateShortlistingAuthorityList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_candidate_shortlisting_authority_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = Recruitmentapprovingauthority.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementInterveiwManageCandidateShortlistingAuthority(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_manage_candidate_shortlisting_authority.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentRecruitmentapprovingauthorityForm()
        else:
            data = get_object_or_404(Recruitmentapprovingauthority, pk=id)
            form = RecruitmentRecruitmentapprovingauthorityForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentRecruitmentapprovingauthorityForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(Recruitmentapprovingauthority, pk=id)
            form = RecruitmentRecruitmentapprovingauthorityForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_managecandidateshortlistingauthority_list')


class RecruitmentManagementInterveiwManageCandidateShortlistingAuthorityDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = Recruitmentapprovingauthority.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_managecandidateshortlistingauthority_list')


# 9

class RecruitmentManagementInterveiwManageSelectionProcessList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_selection_process_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagementInterveiwManageSelectionProcess.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagementInterveiwManageSelectionProcess(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_manage_selection_process.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagementInterveiwManageSelectionProcessForm()
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwManageSelectionProcess, pk=id)
            form = RecruitmentManagementInterveiwManageSelectionProcessForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagementInterveiwManageSelectionProcessForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagementInterveiwManageSelectionProcess, pk=id)
            form = RecruitmentManagementInterveiwManageSelectionProcessForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_manageselectionprocess_list')


class RecruitmentManagementInterveiwManageSelectionProcessDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagementInterveiwManageSelectionProcess.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_manageselectionprocess_list')

# Attendance & Overtime  Management 
class AttendanceOvertimeManagementOvertimeListView(View):
    template = 'admin_template/crm_employees/employee_attendanceovertimemanagement_overtime_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageOverTime.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})

class LeaveHolidaysManagementHolidaysListView(View):
    template = 'admin_template/crm_employees/leave_holidays_management_holidays_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_financial_year = ManageHolidays.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})

# Type of Job
class ManagementEmployeeTypeofJobList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/type_of_job_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagementEmployeeTypeofJob.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManagementEmployeeTypeofJob(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_family.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagementEmployeeTypeofJobForm()
        else:
            data = get_object_or_404(ManagementEmployeeTypeofJob, pk=id)
            form = ManagementEmployeeTypeofJobForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagementEmployeeTypeofJobForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManagementEmployeeTypeofJob, pk=id)
            form = ManagementEmployeeTypeofJobForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('employee_emplyeesservices_typeofjob_list')


class ManagementEmployeeTypeofJobDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagementEmployeeTypeofJob.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('employee_emplyeesservices_typeofjob_list')


# Payroll of
class ManagementEmployeePayrollofJobList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/payroll_job_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManagementEmployeePayrollofJob.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditManagementEmployeePayrollofJob(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_employee_setup/add_edit_manage_family.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManagementEmployeePayrollofJobForm()
        else:
            data = get_object_or_404(ManagementEmployeePayrollofJob, pk=id)
            form = ManagementEmployeePayrollofJobForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ManagementEmployeePayrollofJobForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(ManagementEmployeePayrollofJob, pk=id)
            form = ManagementEmployeePayrollofJobForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('employee_emplyeesservices_payrollof_list')


class ManagementEmployeePayrollofJobDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManagementEmployeePayrollofJob.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('employee_emplyeesservices_payrollof_list')


# On boarding & Exit Management Master
class OnboardingExitRemunerationManagementList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/remuneration_management_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = OnboardingExitRemunerationManagement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)



class AddEditOnboardingExitRemunerationManagement(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_remuneration_management.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = OnboardingExitRemunerationManagementForm()
            form1 = OnboardingExitRemunerationManagementGrossSalaryForm()
            form2 = OnboardingExitRemunerationManagementDeductionsForm()
        else:
            data = get_object_or_404(OnboardingExitRemunerationManagement, pk=id)
            form = OnboardingExitRemunerationManagementForm(instance=data)
            form1 = OnboardingExitRemunerationManagementGrossSalaryForm(instance=data)
            form2 = OnboardingExitRemunerationManagementDeductionsForm(instance=data)
        context = {
            'form': form,
            'form1': form1,
            'form2': form2,
            'id':id
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = OnboardingExitRemunerationManagementForm(request.POST)
            if form.is_valid():
                data = form.save()
                data1 = get_object_or_404(OnboardingExitRemunerationManagement, pk=data.id)
                form1 = OnboardingExitRemunerationManagementGrossSalaryForm(request.POST, instance=data1)
                form1.save()
                form2 = OnboardingExitRemunerationManagementDeductionsForm(request.POST,instance=data1)
                form2.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        else:
            data = get_object_or_404(OnboardingExitRemunerationManagement, pk=id)
            form = OnboardingExitRemunerationManagementForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                form1 = OnboardingExitRemunerationManagementGrossSalaryForm(request.POST, instance=data)
                form1.save()
                form2 = OnboardingExitRemunerationManagementDeductionsForm(request.POST, instance=data)
                form2.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Something went wrong.")
        return redirect('onbboardingexitmanagement_remuneration_list')


class OnboardingExitRemunerationManagementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = OnboardingExitRemunerationManagement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('onbboardingexitmanagement_remuneration_list')


# Registration Management  > Define Employment Type
class RegistrationManagementDefineEmploymentTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/define_employment_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RegistrationManagementEmploymentType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)



class AddEditRegistrationManagementDefineEmploymentType(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_define_employment_type.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RegistrationManagementDefineEmploymentTypeForm()
        else:
            data = get_object_or_404(RegistrationManagementEmploymentType, pk=id)
            form = RegistrationManagementDefineEmploymentTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RegistrationManagementDefineEmploymentTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(RegistrationManagementEmploymentType, pk=id)
            form = RegistrationManagementDefineEmploymentTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('registrationmanagment_employmenttype_list')


class RegistrationManagementDefineEmploymentTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RegistrationManagementEmploymentType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('registrationmanagment_employmenttype_list')



# Registration Management  > Define Payroll Type
class RegistrationManagementDefinePayrollTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/define_payroll_type_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RegistrationManagementPayrollType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRegistrationManagementDefinePayrollType(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_define_payroll_type.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = RegistrationManagementDefinePayrollTypeForm()
        else:
            data = get_object_or_404(RegistrationManagementPayrollType, pk=id)
            form = RegistrationManagementDefinePayrollTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RegistrationManagementDefinePayrollTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(RegistrationManagementPayrollType, pk=id)
            form = RegistrationManagementDefinePayrollTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('registrationmanagment_payrolltype_list')


class RegistrationManagementDefinePayrollTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RegistrationManagementPayrollType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('registrationmanagment_payrolltype_list')


# Registration Management  >  Payroll Roll Agency
class RegistrationManagementDefinePayrollAgencyList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/define_payroll_agency_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RegistrationManagementPayrollAgency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRegistrationManagementDefinePayrollAgency(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_define_payroll_agency.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RegistrationManagementDefinePayrollAgencyForm()
        else:
            data = get_object_or_404(RegistrationManagementPayrollAgency, pk=id)
            form = RegistrationManagementDefinePayrollAgencyForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RegistrationManagementDefinePayrollAgencyForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(RegistrationManagementPayrollAgency, pk=id)
            form = RegistrationManagementDefinePayrollAgencyForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('registrationmanagment_payrollagency_list')


class RegistrationManagementDefinePayrollAgencyDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RegistrationManagementPayrollAgency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('registrationmanagment_payrollagency_list')


# Registration Management  >  Define Key Responsibility Areas  
class RegistrationManagementDefineKeyResponsibilityAreasList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/registrationmanagment_keyresponsibilityareas_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RegistrationManagementKeyResponsibilityAreas.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRegistrationManagementDefineKeyResponsibilityAreas(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_registrationmanagment_keyresponsibilityareas_list.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RegistrationManagementDefineKeyResponsibilityAreasForm()
        else:
            data = get_object_or_404(RegistrationManagementKeyResponsibilityAreas, pk=id)
            form = RegistrationManagementDefineKeyResponsibilityAreasForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RegistrationManagementDefineKeyResponsibilityAreasForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(RegistrationManagementKeyResponsibilityAreas, pk=id)
            form = RegistrationManagementDefineKeyResponsibilityAreasForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('registrationmanagment_keyresponsibilityareas_list')


class RegistrationManagementDefineKeyResponsibilityAreasDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = RegistrationManagementKeyResponsibilityAreas.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('registrationmanagment_keyresponsibilityareas_list')


# Exit Management > Exit Type
class ExitManagementDefineExitTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/exitmanagement_exittype_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ExitManagementExitType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditExitManagementDefineExitType(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_exitmanagement_exittype.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = ExitManagementDefineExitTypeForm()
        else:
            data = get_object_or_404(ExitManagementExitType, pk=id)
            form = ExitManagementDefineExitTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ExitManagementDefineExitTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ExitManagementExitType, pk=id)
            form = ExitManagementDefineExitTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('exitmanagement_exittype_list')


class ExitManagementDefineExitTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ExitManagementExitType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('exitmanagement_exittype_list')


# Exit Management > Define Notice Period
class ExitManagementDefineNoticePeriodList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/exitmanagement_noticeperiod_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ExitManagementNoticePeriod.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditExitManagementDefineNoticePeriod(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_exitmanagement_noticeperiod.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = ExitManagementDefineNoticePeriodeForm()
        else:
            data = get_object_or_404(ExitManagementNoticePeriod, pk=id)
            form = ExitManagementDefineNoticePeriodeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = ExitManagementDefineNoticePeriodeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ExitManagementNoticePeriod, pk=id)
            form = ExitManagementDefineNoticePeriodeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('exitmanagement_noticeperiod_list')


class ExitManagementDefineNoticePeriodDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ExitManagementNoticePeriod.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('exitmanagement_noticeperiod_list')


# Exit Management > Define Final Settlement
class ExitManagementDefineFinalSettlementList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/exitmanagement_finaldsettlement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ExitManagementFinalSettlement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditExitManagementDefineFinalSettlement(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_exitmanagement_finaldsettlement.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = ExitManagementDefineFinalSettlementForm()
        else:
            data = get_object_or_404(ExitManagementFinalSettlement, pk=id)
            form = ExitManagementDefineFinalSettlementForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = ExitManagementDefineFinalSettlementForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ExitManagementFinalSettlement, pk=id)
            form = ExitManagementDefineFinalSettlementForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('exitmanagement_finaldsettlement_list')


class ExitManagementDefineFinalSettlementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ExitManagementFinalSettlement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('exitmanagement_finaldsettlement_list')


# Exit Management > Define Exit Interview 
class ExitManagementDefineExitInterviewList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/exitmanagement_exitinterview_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ExitManagementExitInterview.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditExitManagementDefineExitInterview(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_exitmanagement_exitinterview.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = ExitManagementDefineExitInterviewForm()
        else:
            data = get_object_or_404(ExitManagementExitInterview, pk=id)
            form = ExitManagementDefineExitInterviewForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = ExitManagementDefineExitInterviewForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ExitManagementExitInterview, pk=id)
            form = ExitManagementDefineExitInterviewForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('exitmanagement_exitinterview_list')


class ExitManagementDefineExitInterviewDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ExitManagementExitInterview.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('exitmanagement_exitinterview_list')


# Asset Management  > Define Assets Type
class AssetManagementDefineAssetsTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/assetmanagement_assettype_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AssetManagementAssetsType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditAssetManagementDefineAssetsType(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_assetmanagement_assettype.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = AssetManagementDefineAssetsTypeForm()
        else:
            data = get_object_or_404(AssetManagementAssetsType, pk=id)
            form = AssetManagementDefineAssetsTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = AssetManagementDefineAssetsTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(AssetManagementAssetsType, pk=id)
            form = AssetManagementDefineAssetsTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('assetmanagement_assettype_list')


class AssetManagementDefineAssetsTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AssetManagementAssetsType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('assetmanagement_assettype_list')


# Asset Management  > Manage Assets
class AssetManagementManageAssetsList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/assetmanagement_manageasset_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AssetManagementManageAssets.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditAssetManagementManageAssets(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_assetmanagement_manageasset.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = AssetManagementManageAssetsForm()
        else:
            data = get_object_or_404(AssetManagementManageAssets, pk=id)
            form = AssetManagementManageAssetsForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = AssetManagementManageAssetsForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(AssetManagementManageAssets, pk=id)
            form = AssetManagementManageAssetsForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('assetmanagement_manageasset_list')


class AssetManagementManageAssetsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AssetManagementManageAssets.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('assetmanagement_manageasset_list')



# Asset Management  > Define Allocation Policy
class AssetManagementDefineAllocationPolicyList(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/assetmanagement_allocationpolicy_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AssetManagementAllocationPolicy.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditAssetManagementDefineAllocationPolicy(View):
    template = 'admin_template/crm_employees/emplyees_services/on_boarding_exit_management/add_edit_assetmanagement_allocationpolicy.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = AssetManagementDefineAllocationPolicyForm()
        else:
            data = get_object_or_404(AssetManagementAllocationPolicy, pk=id)
            form = AssetManagementDefineAllocationPolicyForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = AssetManagementDefineAllocationPolicyForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(AssetManagementAllocationPolicy, pk=id)
            form = AssetManagementDefineAllocationPolicyForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('assetmanagement_allocationpolicy_list')


class AssetManagementDefineAllocationPolicyDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AssetManagementAllocationPolicy.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('assetmanagement_allocationpolicy_list')


# Performance & Appraisal Management > Performance Management > Define Targets
class PerformanceAppraisalManagementPerformanceManagementDefineTargetsList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performance_management_define_target_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalPerformanceManagementTargets.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalManagementPerformanceManagementDefineTargets(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performance_management_define_target.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalManagementPerformanceManagementDefineTargetsForm()
        else:
            data = get_object_or_404(PerformanceAppraisalPerformanceManagementTargets, pk=id)
            form = PerformanceAppraisalManagementPerformanceManagementDefineTargetsForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalManagementPerformanceManagementDefineTargetsForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalPerformanceManagementTargets, pk=id)
            form = PerformanceAppraisalManagementPerformanceManagementDefineTargetsForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_performancemanagementtarget_list')


class PerformanceAppraisalManagementPerformanceManagementDefineTargetsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalPerformanceManagementTargets.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_performancemanagementtarget_list')


# Performance & Appraisal Management > Performance Management > Define Incentive
class PerformanceAppraisalManagementPerformanceManagementDefineIncentiveList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_performancemanagementincentive_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalPerformanceManagementIncentive.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalManagementPerformanceManagementDefineIncentive(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_performancemanagementincentive.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalManagementPerformanceManagementDefineIncentiveForm()
        else:
            data = get_object_or_404(PerformanceAppraisalPerformanceManagementIncentive, pk=id)
            form = PerformanceAppraisalManagementPerformanceManagementDefineIncentiveForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalManagementPerformanceManagementDefineIncentiveForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalPerformanceManagementIncentive, pk=id)
            form = PerformanceAppraisalManagementPerformanceManagementDefineIncentiveForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_performancemanagementincentive_list')


class PerformanceAppraisalManagementPerformanceManagementDefineIncentiveDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalPerformanceManagementIncentive.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_performancemanagementincentive_list')



# Performance & Appraisal Management > Performance Management > Manage Performance Incentive 
class PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/manage_performance_incentive_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalManagePerformanceIncentive.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentive(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_manage_performance_incentive.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveForm()
        else:
            data = get_object_or_404(PerformanceAppraisalManagePerformanceIncentive, pk=id)
            form = PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalManagePerformanceIncentive, pk=id)
            form = PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_manageperformanceincentive_list')


class PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalManagePerformanceIncentive.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_manageperformanceincentive_list')


# Performance & Appraisal Management > Performance Management > Manage Performance Incentive 
class PerformanceAppraisalManagementDefineAppraisalFrequencyList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalManagementAppraisalFrequency.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalManagementDefineAppraisalFrequency(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalManagementDefineAppraisalFrequencyForm()
        else:
            data = get_object_or_404(PerformanceAppraisalManagementAppraisalFrequency, pk=id)
            form = PerformanceAppraisalManagementDefineAppraisalFrequencyForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalManagementDefineAppraisalFrequencyForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalManagementAppraisalFrequency, pk=id)
            form = PerformanceAppraisalManagementDefineAppraisalFrequencyForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_list')


class PerformanceAppraisalManagementDefineAppraisalFrequencyDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalManagementAppraisalFrequency.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_list')



# Performance & Appraisal Management > Performance Management > Define Cross Department 
class PerformanceAppraisalManagementDefineCrossDepartmentList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_appraisalmanagementcrossdepartment_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalManagementCrossDepartment.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalManagementDefineCrossDepartment(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_appraisalmanagementcrossdepartment.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalManagementDefineCrossDepartmentForm()
        else:
            data = get_object_or_404(PerformanceAppraisalManagementCrossDepartment, pk=id)
            form = PerformanceAppraisalManagementDefineCrossDepartmentForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalManagementDefineCrossDepartmentForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalManagementCrossDepartment, pk=id)
            form = PerformanceAppraisalManagementDefineCrossDepartmentForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_appraisalmanagementcrossdepartment_list')


class PerformanceAppraisalManagementDefineCrossDepartmentDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalManagementCrossDepartment.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_appraisalmanagementcrossdepartment_list')



# Performance & Appraisal Management > Define Appraisal  Rating > Define Weightage
class PerformanceAppraisalDefineAppraisalRatingDefineWeightageList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_appraisalratingdefineweightage_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalRatingWeightage.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalDefineAppraisalRatingDefineWeightage(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_appraisalratingdefineweightage.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalDefineAppraisalRatingDefineWeightageForm()
        else:
            data = get_object_or_404(PerformanceAppraisalRatingWeightage, pk=id)
            form = PerformanceAppraisalDefineAppraisalRatingDefineWeightageForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalDefineAppraisalRatingDefineWeightageForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalRatingWeightage, pk=id)
            form = PerformanceAppraisalDefineAppraisalRatingDefineWeightageForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_appraisalratingdefineweightage_list')


class PerformanceAppraisalDefineAppraisalRatingDefineWeightageDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalRatingWeightage.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_appraisalratingdefineweightage_list')


# Performance & Appraisal Management > Define Appraisal  Rating > Manage Rating 
class PerformanceAppraisalDefineAppraisalRatingManageRatingList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_appraisalratingmanagerating_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalRatingManageRating.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalDefineAppraisalRatingManageRating(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_appraisalratingmanagerating.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalDefineAppraisalRatingManageRatingForm()
        else:
            data = get_object_or_404(PerformanceAppraisalRatingManageRating, pk=id)
            form = PerformanceAppraisalDefineAppraisalRatingManageRatingForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalDefineAppraisalRatingManageRatingForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalRatingManageRating, pk=id)
            form = PerformanceAppraisalDefineAppraisalRatingManageRatingForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_appraisalratingmanagerating_list')


class PerformanceAppraisalDefineAppraisalRatingManageRatingDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalRatingManageRating.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_appraisalratingmanagerating_list')


# Performance & Appraisal Management > Define Appraisal Committee
class PerformanceAppraisalDefineAppraisalCommitteeList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_defineappraisalcommittee_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalAppraisalCommittee.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalDefineAppraisalCommittee(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_defineappraisalcommittee.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalDefineAppraisalCommitteeForm()
        else:
            data = get_object_or_404(PerformanceAppraisalAppraisalCommittee, pk=id)
            form = PerformanceAppraisalDefineAppraisalCommitteeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalDefineAppraisalCommitteeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalAppraisalCommittee, pk=id)
            form = PerformanceAppraisalDefineAppraisalCommitteeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_defineappraisalcommittee_list')


class PerformanceAppraisalDefineAppraisalCommitteeDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalAppraisalCommittee.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_defineappraisalcommittee_list')



# Performance & Appraisal Management > Define Appraisal Benefits > Define Change in Grade
class PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_definechangeingrade_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalAppraisalBenefitsDefineChangeinGrade.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGrade(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_definechangeingrade.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeForm()
        else:
            data = get_object_or_404(PerformanceAppraisalAppraisalBenefitsDefineChangeinGrade, pk=id)
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalAppraisalBenefitsDefineChangeinGrade, pk=id)
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_definechangeingrade_list')


class PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalAppraisalBenefitsDefineChangeinGrade.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_definechangeingrade_list')




# Performance & Appraisal Management > Define Appraisal Benefits > Define Increment
class PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_defineincrement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalBenefitsDefineIncrement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineIncrement(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_defineincrement.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementForm()
        else:
            data = get_object_or_404(PerformanceAppraisalBenefitsDefineIncrement, pk=id)
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalBenefitsDefineIncrement, pk=id)
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_defineincrement_list')


class PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalBenefitsDefineIncrement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_defineincrement_list')


# Performance & Appraisal Management > Define Appraisal Benefits > Define Increment
class PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_defineappraisalincentive_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalBenefitsAppraisalIncentive.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentive(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_defineappraisalincentivet.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveForm()
        else:
            data = get_object_or_404(PerformanceAppraisalBenefitsAppraisalIncentive, pk=id)
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalBenefitsAppraisalIncentive, pk=id)
            form = PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_defineappraisalincentive_list')


class PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalBenefitsAppraisalIncentive.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_defineappraisalincentive_list')

#############
#anagepsychometrictest




class RecruitmentManagePsychometricTestList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_psychometrictestlist.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManagePsychometricTest.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManagePsychometricTest(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_managepsychometrictest.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManagePsychometricTestForm()
        else:
            data = get_object_or_404(RecruitmentManagePsychometricTest, pk=id)
            form = RecruitmentManagePsychometricTestForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManagePsychometricTestForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManagePsychometricTest, pk=id)
            form = RecruitmentManagePsychometricTestForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_recruitmentmanagement_managepsychometrictest_list')


class RecruitmentManagePsychometricTestDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManagePsychometricTest.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_recruitmentmanagement_managepsychometrictest_list')


############ Manage Test Result
 
class RecruitmentManageTestResultList(View):
    template = 'admin_template/crm_employees/recruitment_management/manage_managetestresultlist.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = RecruitmentManageTestResult.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditRecruitmentManageTestResult(View):
    template = 'admin_template/crm_employees/recruitment_management/add_edit_managetestresult.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = RecruitmentManageTestResultForm()
        else:
            data = get_object_or_404(RecruitmentManageTestResult, pk=id)
            form = RecruitmentManageTestResultForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = RecruitmentManageTestResultForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(RecruitmentManageTestResult, pk=id)
            form = RecruitmentManageTestResultForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_managetestresult_list')


class RecruitmentManageTestResultDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = RecruitmentManageTestResult.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_managetestresult_list')


################


class UpdateAdvanceTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/updateadvancetype_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = Updateadvancetype.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditUpdateAdvanceType(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_updateadvancetype_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = UpdateadvancetypeForm()
        else:
            data = get_object_or_404(Updateadvancetype, pk=id)
            form = UpdateadvancetypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = UpdateadvancetypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(Updateadvancetype, pk=id)
            form = UpdateadvancetypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('updateadvancetype_list')


class UpdateAdvanceTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = Updateadvancetype.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('updateadvancetype_list')

##############dvance entitlement



class AdvanceEntitlementList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/dvanceentitlement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = AdvanceEntitlement.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditAdvanceEntitlement(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_claims/add_edit_dvanceentitlement.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = AdvanceEntitlementForm()
        else:
            data = get_object_or_404(AdvanceEntitlement, pk=id)
            form = AdvanceEntitlementForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = AdvanceEntitlementForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(AdvanceEntitlement, pk=id)
            form = AdvanceEntitlementForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('dvanceentitlement_list')


class AdvanceEntitlementDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = AdvanceEntitlement.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('dvanceentitlement_list')


######## UpdateOtherDeductions

class UpdateOtherDeductionsList(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/updateotherdeductions_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = UpdateOtherDeductions.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEditUpdateOtherDeductions(View):
    template = 'admin_template/crm_employees/emplyees_services/manage_pay_roll/add_edit_updateotherdeductions.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = UpdateOtherDeductionsForm()
        else:
            data = get_object_or_404(UpdateOtherDeductions, pk=id)
            form = UpdateOtherDeductionsForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = UpdateOtherDeductionsForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(UpdateOtherDeductions, pk=id)
            form = UpdateOtherDeductionsForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_crmemployee_manageemployee_updateotherdeductions_list')

class UpdateOtherDeductionsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateOtherDeductions.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_updateotherdeductions_list')


#UpdateIncentiveTypeList
class UpdateIncentiveTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/performance_management_updateincentivetype_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalUpdateIncentiveType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditUpdateIncentiveType(View):
    template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/add_edit_performance_management_updateincentivetype.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalUpdateIncentiveTypeForm()
        else:
            data = get_object_or_404(PerformanceAppraisalUpdateIncentiveType, pk=id)
            form = PerformanceAppraisalUpdateIncentiveTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalUpdateIncentiveTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalUpdateIncentiveType, pk=id)
            form = PerformanceAppraisalUpdateIncentiveTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_updateincentivetype_list')


class UpdateIncentiveTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalUpdateIncentiveType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_updateincentivetype_list')

 # UpdateBonus 


class UpdateBonusList(View):
    template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/performanceappraisalmanagement_updatebonus_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalUpdateBonus.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditUpdateBonus(View):
    template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/add_edit_performanceappraisalmanagement_updatebonus.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalUpdateBonusForm()
        else:
            data = get_object_or_404(PerformanceAppraisalUpdateBonus, pk=id)
            form = PerformanceAppraisalUpdateBonusForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalUpdateBonusForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalUpdateBonus, pk=id)
            form = PerformanceAppraisalUpdateBonusForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_updatebonus_list')


class UpdateBonusDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalUpdateBonus.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_updatebonus_list')
##### ManageBonusList


class ManageBonusList(View):
    template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/p_updatebonus_list.html'
    # template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/p_managebonus_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = PerformanceAppraisalManageBonus.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditManageBonus(View):
    template = 'admin_template/crm_employees/emplyees_services/updateincentivetype/add_edit_performanceappraisalmanagement_managebonus.html'


    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = PerformanceAppraisalManageBonusForm()
        else:
            data = get_object_or_404(PerformanceAppraisalManageBonus, pk=id)
            form = PerformanceAppraisalManageBonusForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = PerformanceAppraisalManageBonusForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(PerformanceAppraisalManageBonus, pk=id)
            form = PerformanceAppraisalManageBonusForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('p_managebonus_list')


class ManageBonusDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = PerformanceAppraisalManageBonus.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('p_managebonus_list')


# 8
class ExitApprovalAuthoritylistingAuthorityList(View):
    template = 'admin_template/crm_employees/exit_approval_authority_/manage_crm_exitapprovalauthority_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = UpdateExitApprovalAuthority.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditExitApprovalAuthority(View):
    template = 'admin_template/crm_employees/exit_approval_authority_/add_edit_crm_exitapprovalauthority.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        if id is None:
            form = UpdateExitApprovalAuthorityForm()
        else:
            data = get_object_or_404(UpdateExitApprovalAuthority, pk=id)
            form = UpdateExitApprovalAuthorityForm(instance=data)
        
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = UpdateExitApprovalAuthorityForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        else:
            data = get_object_or_404(UpdateExitApprovalAuthority, pk=id)
            form = UpdateExitApprovalAuthorityForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Data already exists.")
        return redirect('crm_exitapprovalauthority_list')


class ExitApprovalAuthorityDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')

        get_report = UpdateExitApprovalAuthority.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_exitapprovalauthority_list')


# Update Appraisal Process Type
class UpdateAppraisalProcessTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_updateappraisalprocesstype_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = UpdateAppraisalProcessType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditUpdateAppraisalProcessType(View):
    
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_updateappraisalprocesstype.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = UpdateAppraisalProcessTypeForm()
        else:
            data = get_object_or_404(UpdateAppraisalProcessType, pk=id)
            form = UpdateAppraisalProcessTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = UpdateAppraisalProcessTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(UpdateAppraisalProcessType, pk=id)
            form = UpdateAppraisalProcessTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_updateappraisalprocesstype_list')


class UpdateAppraisalProcessTypelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateAppraisalProcessType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_updateappraisalprocesstype_list')

##UpdatePyschometricTest
class UpdatePyschometricTestList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_updatepyschometricest_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = UpdatePyschometricTest.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditUpdatePyschometricTest(View):
    
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_updatepyschometricest.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = UpdatePyschometricTestForm()
        else:
            data = get_object_or_404(UpdatePyschometricTest, pk=id)
            form = UpdatePyschometricTestForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = UpdatePyschometricTestForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(UpdatePyschometricTest, pk=id)
            form = UpdatePyschometricTestForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_updatepyschometricest_list')


class UpdatePyschometricTestdelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdatePyschometricTest.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_updatepyschometricest_list')

#############UpdateAppraisalBenefitTypeList

class UpdateAppraisalBenefitTypeList(View):
    template = 'admin_template/crm_employees/emplyees_services/appraisalbenefittype/updateappraisalbenefittype_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = UpdateAppraisalBenefitType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditUpdateAppraisalBenefitType(View):
    template = 'admin_template/crm_employees/emplyees_services/appraisalbenefittype/add_edit_updateappraisalbenefittype.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = UpdateAppraisalBenefitTypeForm()
        else:
            data = get_object_or_404(UpdateAppraisalBenefitType, pk=id)
            form = UpdateAppraisalBenefitTypeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = UpdateAppraisalBenefitTypeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(UpdateAppraisalBenefitType, pk=id)
            form = UpdateAppraisalBenefitTypeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_updateappraisalbenefittype_list')


class UpdateAppraisalBenefitTypeDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = UpdateAppraisalBenefitType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_updateappraisalbenefittype_list')


#############Manage Grade Change

class ManageGradeChangeList(View):
    template = 'admin_template/crm_employees/emplyees_services/appraisalbenefittype/managegradechange_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageGradeChange.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditManageGradeChange(View):
    template = 'admin_template/crm_employees/emplyees_services/appraisalbenefittype/add_edit_managegradechange.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageGradeChangeForm()
        else:
            data = get_object_or_404(ManageGradeChange, pk=id)
            form = ManageGradeChangeForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = ManageGradeChangeForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ManageGradeChange, pk=id)
            form = ManageGradeChangeForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_managegradechange_list')


class ManageGradeChangeDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageGradeChange.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_managegradechange_list')


# ManageIncrementsList
class ManageIncrementsList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/performanceappraisalmanagement_manageincrements_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageIncrements.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditManageIncrements(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_performanceappraisalmanagement_manageincrements.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageIncrementsForm()
        else:
            data = get_object_or_404(ManageIncrements, pk=id)
            form = ManageIncrementsForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = ManageIncrementsForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ManageIncrements, pk=id)
            form = ManageIncrementsForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_manageincrements_list1')


class ManageIncrementsDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageIncrements.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_manageincrements_list1')

###################ManageAppraisalIncentive

class ManageAppraisalIncentiveList(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/ManageAppraisalIncentiveList_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_data = ManageAppraisalIncentive.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class AddEditManageAppraisalIncentive(View):
    template = 'admin_template/crm_employees/emplyees_services/performanceappraisalmanagement/add_edit_ManageAppraisalIncentive.html'

    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = ManageAppraisalIncentiveForm()
        else:
            data = get_object_or_404(ManageAppraisalIncentive, pk=id)
            form = ManageAppraisalIncentiveForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)


    def post(self, request, id = None):
        if id is None:
            form = ManageAppraisalIncentiveForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        else:
            data = get_object_or_404(ManageAppraisalIncentive, pk=id)
            form = ManageAppraisalIncentiveForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.WARNING, "Already exists.")
        return redirect('performanceappraisalmanagement_manageappraisalincentive_list')


class ManageAppraisalIncentiveDelete(View):

    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageAppraisalIncentive.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('performanceappraisalmanagement_manageappraisalincentive_list')

################
def ManageSaalry(request):

    return render(request,'admin_template/crm_employees/slip/salary_slip.html')