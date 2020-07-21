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
from aditshsoft.common import CommonPagination, SaveCsvSheet
from aditshsoft.common import Getmonthlist, SiteUrl, SendSmsEmailAndNotification
from aditshsoft.common import Getyearlist, time_slots, Getyearlist1, GetAndManageHierarchyOfEmployee
from employee_website.models import *
from admin_main.models import *
from hrms_employees.models import *
from employee_website.forms import *
from knowleage_tranning.forms import *
from datetime import date, datetime
from django.db.models import Q


class EmployeeServicesRecruitementUpdateConsultantsList(View):
	template = 'employee_website/employee_services/recruitement/update_consultants_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		# get_report_p = EmployeeServicesRecruitementUpdateConsultantsDetails.objects.all().order_by('-id')
		get_report = EmployeeServicesRecruitementUpdateConsultants.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			# 'get_report_p':get_report_p,
		}
		return render(request, self.template, context)

##123
class AddEditCrmEmployeeServicesRecruitementUpdateConsultants(View):
	template = 'employee_website/employee_services/recruitement/add_edit_update_consultants.html'
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		# form1 = EmployeeServicesRecruitementUpdateConsultantsmodelForm()
		form_address = EmployeeServicesRecruitementUpdateConsultantsAddressForm()
		location_list=  ManageBranch.objects.all()
		
		context = {
			# "form":form1 ,
			"form_address":form_address,
			'location_list':location_list,
		}
		return render(request, self.template, context)

	def post(self,request,id= None):
	
		try:
			if not request.user.is_authenticated:
				return redirect('index')
			if request.method=="POST":
				form = EmployeeServicesRecruitementUpdateConsultantsmodelForm(request.POST)
				if form.is_valid():
					form.save()
				try:	
					form1 = EmployeeServicesRecruitementUpdateConsultantsAddressForm(request.POST)
					
					if form1.is_valid():
						form1.save()
					messages.add_message(request, messages.SUCCESS, "Data is Save SuccessFully.")
					return redirect('crm_website_employeeservices_recruitement_updateconsultants_list')
				except Exception as ee:
					messages.add_message(request, messages.ERROR, "pan card already registered.")
					return redirect('crm_website_employeeservices_recruitement_updateconsultants_list')

		except Exception as ee:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
			return redirect('crm_website_employeeservices_recruitement_updateconsultants_list')


def EditCrmEmployeeServicesRecruitementUpdateConsultants(request, id):

    manageproduct = get_object_or_404(EmployeeServicesRecruitementUpdateConsultants, pk=id)
    if request.method == "POST":
        form =EmployeeServicesRecruitementUpdateConsultantsAddressForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('crm_website_employeeservices_recruitement_updateconsultants_list')
    else:
        form = EmployeeServicesRecruitementUpdateConsultantsAddressForm(instance=manageproduct)
    return render(request, 'employee_website/employee_services/recruitement/edit_update_consultants.html', {'form': form})


			

	


class EmployeeServicesRecruitementUpdateConsultantsDelete(View):
	def get(self, request, id):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementUpdateConsultants.objects.filter(id = id).delete()
		messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
		return redirect('crm_website_employeeservices_recruitement_updateconsultants_list')


# 2
class EmployeeServicesRecruitementCreateRequirementList(View):
	template = 'employee_website/employee_services/recruitement/create_requirement_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementCreateRequirement.objects.all().order_by('-id')
		
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class AddEditCrmEmployeeServicesRecruitementCreateRequirement(View):
	template = 'employee_website/employee_services/recruitement/add_edit_create_requirement.html'
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		if id is None:
			form = EmployeeServicesRecruitementCreateRequirementmodelForm1()
		else:
			data = get_object_or_404(EmployeeServicesRecruitementCreateRequirement, pk=id)
			form = EmployeeServicesRecruitementCreateRequirementmodelForm1(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if id is None:
			form = EmployeeServicesRecruitementCreateRequirementmodelForm1(request.POST)
			if form.is_valid():
				data = form.save()
				data.user_id = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:
			data = get_object_or_404(EmployeeServicesRecruitementCreateRequirement, pk=id)
			form = EmployeeServicesRecruitementCreateRequirementmodelForm1(request.POST, instance = data)
			if form.is_valid():
				data = form.save()
				data.user_id = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_createrequirement_list')


class EmployeeServicesRecruitementCreateRequirementDelete(View):
	
	def get(self, request, id):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementCreateRequirement.objects.filter(id = id).delete()
		messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
		return redirect('crm_website_employeeservices_recruitement_createrequirement_list')


# 3
class EmployeeServicesRecruitementApproveVacanciesList(View):
	template = 'employee_website/employee_services/recruitement/approved_vacancies_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		# get_report = EmployeeServicesRecruitementCreateRequirement.objects.filter(~Q(approval_level_id = 5)).order_by('-id')
		
		get_report = EmployeeServicesRecruitementCreateRequirement.objects.filter(~Q(approval_level_id = 5)).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)
#
#
#EmployeeServicesRecruitementCreateRequirementmodelUpdateForm

class AddEditCrmEmployeeServicesRecruitementApproveVacancies(View):
	template = 'employee_website/employee_services/recruitement/add_edit_create_requirement.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(EmployeeServicesRecruitementCreateRequirement, pk=id)
		# form = EmployeeServicesRecruitementApproveVacanciesUpdateForm(instance=data)
		form =EmployeeServicesRecruitementCreateRequirementmodelForm2(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(EmployeeServicesRecruitementCreateRequirement, pk=id)
		# form = EmployeeServicesRecruitementApproveVacanciesUpdateForm(request.POST, instance = data)
		form = EmployeeServicesRecruitementCreateRequirementmodelForm2(request.POST, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_approvevacancies_list')


# 4
class EmployeeServicesRecruitementPublishVacanciesList(View):
	template = 'employee_website/employee_services/recruitement/publish_vacancies_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		
		get_report = EmployeeServicesRecruitementCreateRequirement.objects.filter(action_required = 'Approved').order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class AddEditCrmEmployeeServicesRecruitementPublishVacancies(View):
	template = 'employee_website/employee_services/recruitement/add_edit_create_requirement.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(EmployeeServicesRecruitementCreateRequirement, pk=id)
		form = EmployeeServicesRecruitementCreateRequirementmodelUpdateForm1(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(EmployeeServicesRecruitementCreateRequirement, pk=id)
		form = EmployeeServicesRecruitementCreateRequirementmodelUpdateForm1(request.POST, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_publishvacancies_list')


# 5
class EmployeeServicesRecruitementInviteResumeList(View):
	template = 'employee_website/employee_services/recruitement/invite_resume_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		# get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 1).order_by('-id')
		get_report = EmployeeServicesRecruitementInviteResume.objects.all().order_by('-id')

		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class AddEditCrmEmployeeServicesRecruitementInviteResume(View):
	template = 'employee_website/employee_services/recruitement/add_edit_invite_resume.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
	
		if id is None:
			form = EmployeeServicesRecruitementInviteResumeAddForm()
		else:
			data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
			form = EmployeeServicesRecruitementInviteResumeUpdateForm(instance=data)
		context = {
			'form': form,
			
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		if id is None:
			form = EmployeeServicesRecruitementInviteResumeAddForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
				return redirect('crm_website_employeeservices_recruitement_inviteresume_add1')
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
				return redirect('crm_website_employeeservices_recruitement_inviteresume_add1')
		else:
			data = get_object_or_404(EmployeeServicesRecruitementInviteResume,  pk=id)
			form = EmployeeServicesRecruitementInviteResumeUpdateForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_inviteresume_list')

def AddEmployeeServicesRecruitementResume(request,id=None):
	get_report = EmployeeServicesRecruitementCreateRequirement.objects.filter(action_required = 'Approved').order_by('-id')
	return render(request,'employee_website/employee_services/recruitement/add_invite_resume.html',{'responselistquery':get_report})
###
def AddUpdateEmployeeServicesRecruitementResumeView(request,id=None):
	form =AddUpdateEmployeeServicesRecruitementResume()
	if request.method=="POST":
		form = AddUpdateEmployeeServicesRecruitementResume(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			return redirect('crm_website_employeeservices_recruitement_inviteresume_list')
	return render(request,'employee_website/employee_services/recruitement/add_edit_invite_resume.html',{'form':form})

###############

class AddEditCrmEmployeeServicesRecruitementResume(View):
	template = 'employee_website/employee_services/recruitement/add_edit_invite_resume.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		if id is None:
			form = EmployeeServicesRecruitementesumeAddForm1()
		else:
			data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
			form = EmployeeServicesRecruitementInviteResumeUpdateForm(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		if id is None:
			form = EmployeeServicesRecruitementesumeAddForm1(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:
			data = get_object_or_404(EmployeeServicesRecruitementInviteResume,  pk=id)
			form = EmployeeServicesRecruitementInviteResumeUpdateForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_inviteresume_list')


################

class EmployeeServicesRecruitementInviteResumeDelete(View):
	
	def get(self, request, id):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementInviteResume.objects.filter(id = id).delete()
		messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
		return redirect('crm_website_employeeservices_recruitement_inviteresume_list')
#######psychometrictest

class EmployeeServicesRecruitementPsychometricTestList(View):
	template = 'employee_website/employee_services/recruitement/psychometrictest_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		# get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 1).order_by('-id')
		get_report = EmployeeServicesRecruitementPsychometricTest.objects.all().order_by('-id')

		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class AddEditCrmEmployeeServicesRecruitementPsychometricTest(View):
	template = 'employee_website/employee_services/recruitement/add_edit_psychometrictest.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		if id is None:
			form = EmployeeServicesRecruitementPsychometricTestAddForm()
		else:
			data = get_object_or_404(EmployeeServicesRecruitementPsychometricTest, pk=id)
			form = EmployeeServicesRecruitementPsychometricTestUpdateForm(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if id is None:
			form = EmployeeServicesRecruitementPsychometricTestAddForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:
			data = get_object_or_404(EmployeeServicesRecruitementPsychometricTest,  pk=id)
			form = EmployeeServicesRecruitementPsychometricTestUpdateForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_psychometrictest_list')


class EmployeeServicesRecruitementPsychometricTestDelete(View):
	
	def get(self, request, id):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementPsychometricTest.objects.filter(id = id).delete()
		messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
		return redirect('crm_website_employeeservices_recruitement_psychometrictest_list')

#######

# 6
class EmployeeServicesRecruitementResumeShortlistedList(View):
	template = 'employee_website/employee_services/recruitement/resume_shortlisted_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')      
		# get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 2).order_by('-id')
		get_report = EmployeeServicesRecruitementInviteResume.objects.filter(interview_status = 1).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class AddEditCrmEmployeeServicesRecruitementCandidatesShortlisted(View):
	template = 'employee_website/employee_services/recruitement/add_edit_create_requirement.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementCandidatesShortlistedUpdateForm(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementCandidatesShortlistedUpdateForm(request.POST, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_candidateshortlisted_list')


class EmployeeServicesRecruitementOfferStatusList(View):
	template = 'employee_website/employee_services/recruitement/offer_status_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 4, interview_status = 1).order_by('-id')
		
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)

###
class EmployeeServicesRecruitementDocumentList(View):
	template = 'employee_website/employee_services/recruitement/document_list.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 4).order_by('-id')
		context = {
			'responselistquery': get_report,
		}
		return render(request, self.template, context)
class EmployeeServicesRecruitementDocumentadd(View):
	template = 'employee_website/employee_services/recruitement/document_add_edit.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementDocumentForm(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementDocumentForm(request.POST, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
			return redirect('crm_website_employeeservices_recruitement_document_list')
		return redirect('crm_website_employeeservices_recruitement_document_list')

####

class AddEditCrmEmployeeServicesRecruitementCandidatesOfferStatus(View):
	template = 'employee_website/employee_services/recruitement/update_candidates_joined.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm1(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm1(request.POST, request.FILES, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_offer_status_list')


class AddEditCrmEmployeeServicesRecruitementCandidatesOfferUpdateStatus(View):
	template = 'employee_website/employee_services/recruitement/update_candidates_joined.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementOfferStatusUpdateForm(instance=data)
		context = {
			'form': form,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		form = EmployeeServicesRecruitementOfferStatusUpdateForm(request.POST, request.FILES, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_offer_status_list')


class EmployeeServicesRecruitementVacancyStatusList(View):
	template = 'employee_website/employee_services/recruitement/vacancy_status_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementCreateRequirement.objects.filter(approval_level = 2).order_by('-id')
	
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeServicesRecruitementCandidatesInterViewStatusList(View):
	template = 'employee_website/employee_services/recruitement/interview_status.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeServicesRecruitementInviteResume.objects.filter(Q(interview_status = 1) | Q(interview_status = 2)).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class AddEditCrmEmployeeServicesInterViewStatus(View):
	template = 'employee_website/employee_services/recruitement/add_edit_interview_status.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		# form = EmployeeServicesRecruitementInterViewStatusForm(instance=data)
		short_listed_candidated = EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm(instance=data)
		context = {
			# 'form': form,
			'short_listed_candidated': short_listed_candidated,
			'data': data
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		data = get_object_or_404(EmployeeServicesRecruitementInviteResume, pk=id)
		# form = EmployeeServicesRecruitementInterViewStatusForm(request.POST, instance = data)
		form = EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm(request.POST, instance = data)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			# if request.POST['status'] == '3':
			# 	if form1.is_valid():
			# 		form1.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_website_employeeservices_recruitement_interviewstatus_list')


class EmployeeServicesRecruitementCandidateShortlistedList(View):
	template = 'employee_website/employee_services/recruitement/candidate_short_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		
		# get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 3, interview_status = 1).order_by('-id')
		# get_report = EmployeeServicesRecruitementInviteResume.objects.filter(interview_of_status='Attended').order_by('-id')
		get_report = EmployeeServicesRecruitementInviteResume.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


# 7
class EmployeeServicesEmployeeRegistrationUpdateRegistrationsList(View):
	template = 'employee_website/employee_services/employee_registration/update_registrations_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
			#
			####
		get_report = EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)

##1
##2

class EmployeeServicesEmployeeOfferLatter(View):
	template = 'employee_website/employee_services/employee_registration/employee_offer_latter_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
			#
			####
		get_report = EmployeeServicesRecruitementInviteResume.objects.filter(status = 4, interview_status = 1).order_by('-id')
	
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)

class AddEmployeeServicesEmployeeRegistrationUpdateRegistrations(View):
	template = 'employee_website/employee_services/employee_registration/add_edit_update_registrations.html'
	template1 = 'employee_website/employee_services/employee_registration/employee_registertion_verification_report.html'
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'personal_details': EmployeeEmployeeRegistrationUpdateRegistrationPersonalDetailsmodelForm,
			'family_detail_mother': EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelMotherForm,
			'family_detail_father': EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelFatherForm,
			'family_detail_spouse': EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelSpouseForm,
			'family_detail_children': EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelChildrenForm,
			'other_family_relationship': EmployeeEmployeeRegistrationUpdateRegistrationFamilityOtherRelationshipForm,
			'medical_history': EmployeeEmployeeRegistrationUpdateRegistrationMedicalHistorymodelForm,
			'correspondence_address': EmployeeEmployeeRegistrationCorrespondenceAddressForm,
			'permanent_address': EmployeeEmployeeRegistrationPermanentAddressForm,
			'joining_detail': EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetailsmodelForm,
			'qualification': EmployeeEmployeeRegistrationUpdateEducationalQualificationmodelForm,
			'professional_journey': EmployeeEmployeeRegistrationUpdateProfessionalJourneymodelForm,
			'salary_structutre': EmployeeEmployeeRegistrationUpdateSalaryStructutremodelForm,
			'bank_detail': EmployeeEmployeeRegistrationUpdateBankDetailsmodelForm,
			'verification_report': EmployeeEmployeeRegistrationVerificationReportmodelForm,
			'deduction_perquisites': EmployeeEmployeeRegistrationDeductionAndPerquisitesForm,
			'deduction': EmployeeEmployeeRegistrationDeductionForm,
			'asset_allocated': EmployeeEmployeeAssetAllocatedForm,
			'access_control': EmployeeEmployeeAccessControlsForm,
			'references': EmployeeEmployeeRegistrationReferencesmodelForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		if request.POST['one_form'] == "one_form":
			if User.objects.filter(email = request.POST['email']):
				messages.add_message(request, messages.WARNING, "Email already exists.")
				return redirect('crm_website_employeeservices_employeeregistration_updateregistrations_add')
			
			save_user = User()
			save_user.email = request.POST['email']
			save_user.username = request.POST['email']
			save_user.mobile_no = request.POST['mobile_no']
			save_user.name = request.POST['first_name']
			save_user.department_id = request.POST['joining_department']
			save_user.designation_id = request.POST['joining_designation']
			save_user.responsibilities_id = request.POST['joining_responsibilities']
			save_user.user_role_id = request.POST['joining_role']
			save_user.reporting_to_id = request.POST['joining_reporting_to']
			save_user.is_sub_staff = True
			save_user.is_staff = False
			save_user.save()

			form = EmployeeEmployeeRegistrationUpdateRegistrationPersonalDetailsmodelForm(request.POST)
			if form.is_valid():
				data = form.save()
				data.user_id = save_user.id
				data.employee_created_by_id = request.user.id
				data.save()
				get_id = data.id
			save_obj = EmployeeRegistrationUpdateRegistrationFamilityDetails()
			if str(request.POST.get('mother_name'))  and str(request.POST.get('mother_dob')) and str(request.POST.get('mother_occupation')):
				save_obj.mother_name = str(request.POST.get('mother_name'))
				save_obj.mother_dob = str(request.POST.get('mother_dob'))
				save_obj.mother_occupation = str(request.POST.get('mother_occupation'))
				save_obj.mother_contact_number = str(request.POST.get('mother_contact_number'))
				save_obj.user_employee_id= get_id
				save_obj.save()
			if str(request.POST.get('father_name'))  and str(request.POST.get('father_dob')) and str(request.POST.get('father_occupation')):
				save_obj.father_name = str(request.POST.get('father_name'))
				save_obj.father_dob = str(request.POST.get('father_dob'))
				save_obj.father_occupation = str(request.POST.get('father_occupation'))
				save_obj.father_contact_number = str(request.POST.get('father_contact_number'))
				save_obj.user_employee_id= get_id
				save_obj.save()
			if str(request.POST.get('spouse_name'))  and str(request.POST.get('spouse_dob')) and str(request.POST.get('spouse_occupation')):
				save_obj.spouse_name = str(request.POST.get('spouse_name'))
				save_obj.spouse_dob = str(request.POST.get('spouse_dob'))
				save_obj.spouse_occupation = str(request.POST.get('spouse_occupation'))
				save_obj.spouse_contact_number = str(request.POST.get('spouse_contact_number'))
				save_obj.user_employee_id= get_id
				save_obj.save()
			children_data = [int(p.split('_')[2]) for p in request.POST if 'children_name_' in p]
			children_data.sort()
			for cer in children_data:
				children = EmployeeRegistrationUpdateRegistrationFamilityChildren()
				children.children_name_1 = request.POST.get('children_name_' + str(cer)).strip()
				children.children_dob_1 = request.POST.get('children_dob_' + str(cer)).strip()
				children.children_occupation_1 = request.POST.get('children_occupation_' + str(cer)).strip()
				children.children_contact_number_1 = request.POST.get('children_contact_number_' + str(cer)).strip()
				children.user_employee_id = get_id
				children.save()

			other_relation = [int(p.split('_')[2]) for p in request.POST if 'other_name_' in p]
			other_relation.sort()
			for cer in other_relation:
				other_rela = EmployeeRegistrationUpdateRegistrationFamiliyOtherDetails()
				other_rela.other_name_1 = request.POST.get('other_name_' + str(cer)).strip()
				other_rela.other_dob_1 = request.POST.get('other_dob_' + str(cer)).strip()
				other_rela.other_occupation_1 = request.POST.get('other_occupation_' + str(cer)).strip()
				other_rela.other_contact_number_1 = request.POST.get('other_contact_number_' + str(cer)).strip()
				other_rela.user_employee_id = get_id
				other_rela.save()


			# Save Medical History
			medical_history_id = [int(p.split('_')[2]) for p in request.POST if 'blood_group_' in p]
			medical_history_id.sort()
			for cer in medical_history_id:
				medical_history = EmployeeRegistrationUpdateRegistrationMedicalHistory()
				medical_history.blood_group_1 = request.POST.get('blood_group_' + str(cer)).strip()
				medical_history.type_of_illness_1 = request.POST.get('type_of_illness_' + str(cer)).strip()
				medical_history.result_1 = request.POST.get('result_' + str(cer)).strip()
				medical_history.user_employee_id = get_id
				medical_history.save()

			form2 = EmployeeEmployeeRegistrationCorrespondenceAddressForm(request.POST)
			if form2.is_valid():
				data = form2.save()
				data.user_employee_id = get_id
				data.save()

			form3 = EmployeeEmployeeRegistrationPermanentAddressForm(request.POST)
			if form3.is_valid():
				data = form3.save()
				data.user_employee_id = get_id
				data.save()
			form4 = EmployeeEmployeeRegistrationDeductionForm(request.POST)
			if form4.is_valid():
				data = form4.save()
				data.user_employee_id = get_id
				data.save()

			joining_detail = EmployeeRegistrationUpdateRegistrationJoiningDetails()
			joining_detail.joining_location_id= request.POST.get('joining_location')
			joining_detail.joining_date_of_joining = request.POST.get('joining_date_of_joining')
			joining_detail.joining_time= request.POST.get('joining_time')
			joining_detail.joining_grade_offered= request.POST.get('joining_grade_offered')
			joining_detail.joining_next_date_of_increment= request.POST.get('joining_next_date_of_increment')
			joining_detail.joining_department_id= request.POST.get('joining_department')
			joining_detail.joining_designation_id= request.POST.get('joining_designation')
			joining_detail.joining_responsibilities_id = request.POST.get('joining_responsibilities')
			joining_detail.joining_role_id = request.POST.get('joining_role')
			joining_detail.joining_reporting_to_id = request.POST.get('joining_reporting_to')
			joining_detail.joining_probation_period = request.POST.get('joining_probation_period')
			joining_detail.contract_valid_up_to = request.POST.get('contract_valid_up_to')
			joining_detail.user_employee_id = get_id
			joining_detail.save()

			# Save Joining Detail History
			joining_history = EmployeeRegistrationUpdateRegistrationJoiningDetailsHistory()
			joining_history.new_designation_id = request.POST.get('joining_designation')
			joining_history.new_department_id = request.POST.get('joining_department')
			joining_history.new_reporting_id = request.POST.get('joining_reporting_to')
			joining_history.new_responsibilities_id = request.POST.get('joining_responsibilities')
			joining_history.new_location_id =  request.POST.get('joining_location')
			joining_history.joining_role_id = request.POST.get('joining_role')
			joining_history.user_employee_id = get_id
			joining_history.save()

			qualification_id = [int(p.split('_')[3]) for p in request.POST if 'educational_qualificationcourse_name_' in p]
			qualification_id.sort()
			for cer in qualification_id:
				qualification = EmployeeRegistrationUpdateEducationalQualification()
				qualification.educational_qualificationcourse_name_1= request.POST.get('educational_qualificationcourse_name_' + str(cer)).strip()
				qualification.educational_qualificationstart_date_1 = request.POST.get('educational_qualificationstart_date_' + str(cer)).strip()
				qualification.educational_qualificationend_date_1 = request.POST.get('educational_qualificationend_date_' + str(cer)).strip()
				qualification.educational_qualificationmarks_division_1 = request.POST.get('educational_qualificationmarks_division_' + str(cer)).strip()
				qualification.educational_qualificationroll_number_1= request.POST.get('educational_qualificationroll_number_' + str(cer)).strip()
				qualification.educational_qualificationuniversity_institution_1= request.POST.get('educational_qualificationuniversity_institution_' + str(cer)).strip()
				qualification.user_employee_id = get_id
				qualification.save()

			professional_journey_id = [int(p.split('_')[2]) for p in request.POST if 'professional_journeycompany_' in p]
			professional_journey_id.sort()
			for cer in professional_journey_id:
				professional_journey = EmployeeRegistrationUpdateProfessionalJourney()
				professional_journey.professional_journeycompany_1= request.POST.get('professional_journeycompany_' + str(cer)).strip()
				professional_journey.professional_journeystart_date_1 = request.POST.get('professional_journeystart_date_' + str(cer)).strip()
				professional_journey.professional_journeyend_date_1 = request.POST.get('professional_journeyend_date_' + str(cer)).strip()
				professional_journey.professional_journeylast_desgination_1_id = request.POST.get('professional_journeylast_desgination_' + str(cer)).strip()
				professional_journey.professional_journeynature_of_duties_1 = request.POST.get('professional_journeynature_of_duties_' + str(cer)).strip()
				professional_journey.professional_journeylast_drawn_dalary_1 = request.POST.get('professional_journeylast_drawn_dalary_' + str(cer)).strip()
				professional_journey.reason_for_leaving_1 = request.POST.get('reason_for_leaving_' + str(cer)).strip()
				professional_journey.user_employee_id = get_id
				professional_journey.save()


			salary_struct_id = [int(p.split('_')[4]) for p in request.POST if 'salary_structut_salary_code_' in p]
			salary_struct_id.sort()
			for cer in salary_struct_id:
				salary_struct = EmployeeRegistrationUpdateSalaryStructutre()
				salary_struct.salary_structut_salary_code_1_id = request.POST.get('salary_structut_salary_code_' + str(cer)).strip()
				salary_struct.salary_structut_salary_name_1 = request.POST.get('salary_structut_salary_name_' + str(cer)).strip()
				salary_struct.salary_structut_salary_frequency_1 = request.POST.get('salary_structut_salary_frequency_' + str(cer)).strip()
				salary_struct.salary_structut_amount_offered_1= request.POST.get('salary_structut_amount_offered_' + str(cer)).strip()
				salary_struct.salary_structut_percentage_value_flag_1= request.POST.get('salary_structut_percentage_value_flag_' + str(cer)).strip()
				salary_struct.salary_structut_taxability_1 = request.POST.get('salary_structut_taxability_' + str(cer)).strip()
				salary_struct.user_employee_id = get_id
				salary_struct.save()

			deduc = [int(p.split('_')[1]) for p in request.POST if 'appicablitity_' in p]
			deduc.sort()
			for cer in deduc:
				salary_struct = EmployeeRegistrationDeductionAndPerquisites()
				if str(request.POST.get('appicablitity_'+str(cer))) == "2":
					salary_struct.appicablitity_1  = str(request.POST.get('appicablitity_'+str(cer)))
					salary_struct.save()
				else:
					salary_struct.appicablitity_1  = str(request.POST.get('appicablitity_'+str(cer)))
					salary_struct.perquisitec_category_1  = str(request.POST.get('perquisitec_category_'+str(cer)))
					salary_struct.perquisitec_name_1  = str(request.POST.get('perquisitec_name_'+str(cer)))
					salary_struct.perquisite_frequency_1  = str(request.POST.get('perquisite_frequency_'+str(cer)))
					salary_struct.percentage_value_flag_1  = str(request.POST.get('percentage_value_flag_'+str(cer)))
					salary_struct.perquisite_amount_1  = str(request.POST.get('perquisite_amount_'+str(cer)))
					salary_struct.save()

			save_bank_detail = EmployeeRegistrationUpdateBankDetails()
			save_bank_detail.account_type = request.POST.get('account_type')
			save_bank_detail.bank_account_number = request.POST.get('bank_account_number')
			save_bank_detail.bank_name = request.POST.get('bank_name')
			save_bank_detail.branch = request.POST.get('branch')
			save_bank_detail.ifscc_code = request.POST.get('ifscc_code')
			save_bank_detail.micr = request.POST.get('micr')
			save_bank_detail.user_employee_id = get_id 
			save_bank_detail.save()

			reference_id = [int(p.split('_')[1]) for p in request.POST if 'referencename_' in p]
			reference_id.sort()
			for cer in reference_id:
				reference = EmployeeRegistrationReferences()
				reference.referencename_1= request.POST.get('referencename_' + str(cer)).strip()
				reference.referencerelationship_1 = request.POST.get('referencerelationship_' + str(cer)).strip()
				reference.referencecontact_number_1 = request.POST.get('referencecontact_number_' + str(cer)).strip()
				reference.referenceemail_id_1 = request.POST.get('referenceemail_id_' + str(cer)).strip()
				reference.referenceaddress_1= request.POST.get('referenceaddress_' + str(cer)).strip()
				reference.referenceknown_since_1= request.POST.get('referenceknown_since_' + str(cer)).strip()
				reference.user_employee_id = get_id
				reference.save()

			asset_allocated = [int(p.split('_')[2]) for p in request.POST if 'asset_code_' in p]
			asset_allocated.sort()
			for cer in asset_allocated:
				asset_alloca= EmployeeAssetAllocated()
				asset_alloca.asset_code_1= request.POST.get('asset_code_' + str(cer)).strip()
				asset_alloca.asset_serial_number_1 = request.POST.get('asset_serial_number_' + str(cer)).strip()
				asset_alloca.asset_name_1 = request.POST.get('asset_name_' + str(cer)).strip()
				asset_alloca.asset_condition_1 = request.POST.get('asset_condition_' + str(cer)).strip()
				asset_alloca.asset_location_1= request.POST.get('asset_location_' + str(cer)).strip()
				asset_alloca.user_employee_id = get_id
				asset_alloca.save()

			form4 = EmployeeEmployeeAccessControlsForm(request.POST)
			if form4.is_valid():
				data = form4.save()
				data.user_employee_id = get_id
				data.save()
			messages.add_message(request, messages.SUCCESS, "Employee Created successfully.")
			return redirect('crm_website_employeeservices_employeeregistration_verficationreport_add', id = get_id)


class AddEmployeeServicesEmployeeRegistrationVerficationReport(View):
	template = 'employee_website/employee_services/employee_registration/employee_registertion_verification_report.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'verification_report': EmployeeEmployeeRegistrationVerificationReportmodelForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return render(request, self.template1, context)
		verification_report = [int(p.split('_')[2]) for p in request.POST if 'verification_agency_' in p]
		verification_report.sort()
		for cer in verification_report:
			verificationreport = EmployeeRegistrationVerificationReport()
			verificationreport.verification_agency = request.POST.get('verification_agency_' + str(cer))
			verificationreport.finding = request.POST.get('finding_' + str(cer))
			verificationreport.upload_report = request.FILES.get('upload_report_' + str(cer))
			verificationreport.user_employee_id = id
			verificationreport.save()
		return redirect('crm_website_employeeservices_employeeregistration_document_add', id = id)


class AddEmployeeServicesEmployeeRegistrationDocument(View):
	template = 'employee_website/employee_services/employee_registration/employee_registered_document.html'
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'documents': CrmEmployeeEmployeeRegistrationDocumentsmodelForm
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return render(request, self.template1, context)
		document_id = [int(p.split('_')[3]) for p in request.POST if 'name_of_documents_' in p]
		document_id.sort()
		for cer in document_id:
			document = EmployeeRegistrationDocuments()
			document.name_of_documents_1 = request.POST.get('name_of_documents_' + str(cer)).strip()
			document.upload_1 = request.FILES.get('upload_' + str(cer))
			document.user_employee_id = id
			document.save()
		messages.add_message(request, messages.SUCCESS, "Employee Registeration Successfully.")
		return redirect('crm_website_employeeservices_employeeregistration_employee_list')


class EditEmployeeServicesEmployeeRegistrationUpdateRegistrations(View):
	template = 'employee_website/employee_services/employee_registration/edit_employee.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.get(id = id)
		context = {
			'personal_details': EmployeeRegistrationUpdateRegistrationPersonalDetailsmodelForm(instance=data),
			'family_detail_mother': EmployeeRegistrationUpdateRegistrationFamilityDetailsmodelMotherForm(instance = EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetails.objects.get(user_employee_id = data.id)),
			'family_detail_father': EmployeeRegistrationUpdateRegistrationFamilityDetailsmodelFatherForm(instance = EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetails.objects.get(user_employee_id = data.id)),
			'family_detail_spouse': EmployeeRegistrationUpdateRegistrationFamilityDetailsmodelSpouseForm(instance = EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetails.objects.get(user_employee_id = data.id)),
			'family_detail_children': EmployeeRegistrationUpdateRegistrationFamilityDetailsmodelChildrenForm(instance = EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetails.objects.get(user_employee_id = data.id)),
			'medical_history': EmployeeEmployeeRegistrationUpdateRegistrationMedicalHistory.objects.filter(user_employee_id = data.id),
			'joining_detail': EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetailsmodelForm(instance = EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetails.objects.get(user_employee_id = data.id)),
			'qualification': EmployeeEmployeeRegistrationUpdateEducationalQualification.objects.filter(user_employee_id = data.id),
			'professional_journey': EmployeeEmployeeRegistrationUpdateProfessionalJourney.objects.filter(user_employee_id = data.id),
			'salary_structutre': EmployeeEmployeeRegistrationUpdateSalaryStructutre.objects.filter(user_employee_id = data.id),
			'bank_detail': EmployeeEmployeeRegistrationUpdateBankDetailsmodelForm(instance = EmployeeEmployeeRegistrationUpdateBankDetails.objects.get(user_employee_id = data.id)),
			'verification_report': EmployeeEmployeeRegistrationVerificationReportmodelForm(instance = EmployeeEmployeeRegistrationVerificationReport.objects.get(user_employee_id = data.id)),
			'references': EmployeeEmployeeRegistrationReferences.objects.filter(user_employee_id = data.id),
			'documents': EmployeeEmployeeRegistrationDocuments.objects.filter(user_employee_id = data.id),
			'deduction_perquisites': EmployeeEmployeeRegistrationDeductionAndPerquisitesForm(instance=EmployeeEmployeeRegistrationDeductionAndPerquisites.objects.get(user_employee_id = data.id)),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.get(id = id).delete()
		personal_details = EmployeeRegistrationUpdateRegistrationPersonalDetailssmodel()
		personal_details.employee_id_id = request.POST.get('employee_id')
		personal_details.user_id = request.POST.get('user')
		personal_details.salute= request.POST.get('salute')
		personal_details.first_name= request.POST.get('first_name')
		personal_details.middle_name= request.POST.get('middle_name')
		personal_details.last_name= request.POST.get('last_name')
		personal_details.date_of_birth= request.POST.get('date_of_birth')
		personal_details.caste= request.POST.get('caste')
		personal_details.religion= request.POST.get('religion')
		personal_details.marital_status= request.POST.get('marital_status')
		personal_details.mobile_number= request.POST.get('mobile_number')
		personal_details.email_id= request.POST.get('email_id')
		personal_details.landline_number= request.POST.get('landline_number')
		personal_details.emergency_number= request.POST.get('emergency_number')
		personal_details.name= request.POST.get('name')
		personal_details.pan_card= request.POST.get('pan_card')
		personal_details.adhar_card= request.POST.get('adhar_card')
		personal_details.driving_license= request.POST.get('driving_license')
		personal_details.language_known= request.POST.get('language_known')
		personal_details.relationship= request.POST.get('relationship')
		personal_details.photo = request.FILES.get('photo')
		personal_details.user_id = request.user.id
		get_id = personal_details.save()
		save_obj = EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetails()
		if str(request.POST.get('mother_name'))  and str(request.POST.get('mother_dob')) and str(request.POST.get('mother_occupation')):
			save_obj.mother_name = str(request.POST.get('mother_name'))
			save_obj.mother_dob = str(request.POST.get('mother_dob'))
			save_obj.mother_occupation = str(request.POST.get('mother_occupation'))
			save_obj.user_employee_id= personal_details.id
			save_obj.save()
		if str(request.POST.get('father_name'))  and str(request.POST.get('father_dob')) and str(request.POST.get('father_occupation')):
			save_obj.father_name = str(request.POST.get('father_name'))
			save_obj.father_dob = str(request.POST.get('father_dob'))
			save_obj.father_occupation = str(request.POST.get('father_occupation'))
			save_obj.user_employee_id= personal_details.id
			save_obj.save()
		if str(request.POST.get('spouse_name'))  and str(request.POST.get('spouse_dob')) and str(request.POST.get('spouse_occupation')):
			save_obj.spouse_name = str(request.POST.get('spouse_name'))
			save_obj.spouse_dob = str(request.POST.get('spouse_dob'))
			save_obj.spouse_occupation = str(request.POST.get('spouse_occupation'))
			save_obj.user_employee_id= personal_details.id
			save_obj.save()
		if str(request.POST.get('children_name'))  and str(request.POST.get('children_dob')) and str(request.POST.get('children_occupation')):
			save_obj.children_name = str(request.POST.get('children_name'))
			save_obj.children_dob = str(request.POST.get('children_dob'))
			save_obj.children_occupation = str(request.POST.get('children_occupation'))
			save_obj.user_employee_id= personal_details.id
			save_obj.save()

		joining_detail = EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetails()
		joining_detail.joining_location= request.POST.get('joining_location')
		joining_detail.joining_date_of_joining = request.POST.get('joining_date_of_joining')
		joining_detail.joining_time= request.POST.get('joining_time')
		joining_detail.joining_grade_offered= request.POST.get('joining_grade_offered')
		joining_detail.joining_next_date_of_increment= request.POST.get('joining_next_date_of_increment')
		joining_detail.joining_department_id= request.POST.get('joining_department')
		joining_detail.joining_designation_id= request.POST.get('joining_designation')
		joining_detail.joining_responsibilities_id = request.POST.get('joining_responsibilities')
		joining_detail.joining_reporting_to_id = request.POST.get('joining_reporting_to')
		joining_detail.joining_probation_period = request.POST.get('joining_probation_period')
		joining_detail.user_employee_id = personal_details.id
		joining_detail.save()

		# Save Medical History
		medical_history_id = [int(p.split('_')[2]) for p in request.POST if 'blood_group_' in p]
		medical_history_id.sort()
		for cer in medical_history_id:
			medical_history = EmployeeEmployeeRegistrationUpdateRegistrationMedicalHistory()
			medical_history.blood_group_1 = request.POST.get('blood_group_' + str(cer)).strip()
			medical_history.type_of_illness_1 = request.POST.get('type_of_illness_' + str(cer)).strip()
			medical_history.result_1 = request.POST.get('result_' + str(cer)).strip()
			medical_history.user_employee_id = personal_details.id
			medical_history.save()

		qualification_id = [int(p.split('_')[3]) for p in request.POST if 'educational_qualificationcourse_name_' in p]
		qualification_id.sort()
		for cer in qualification_id:
			qualification = EmployeeEmployeeRegistrationUpdateEducationalQualification()
			qualification.educational_qualificationcourse_name_1= request.POST.get('educational_qualificationcourse_name_' + str(cer)).strip()
			qualification.educational_qualificationstart_date_1 = request.POST.get('educational_qualificationstart_date_' + str(cer)).strip()
			qualification.educational_qualificationend_date_1 = request.POST.get('educational_qualificationend_date_' + str(cer)).strip()
			qualification.educational_qualificationmarks_division_1 = request.POST.get('educational_qualificationmarks_division_' + str(cer)).strip()
			qualification.educational_qualificationroll_number_1= request.POST.get('educational_qualificationroll_number_' + str(cer)).strip()
			qualification.educational_qualificationuniversity_institution_1= request.POST.get('educational_qualificationuniversity_institution_' + str(cer)).strip()
			qualification.user_employee_id = personal_details.id
			qualification.save()

		professional_journey_id = [int(p.split('_')[2]) for p in request.POST if 'professional_journeycompany_' in p]
		professional_journey_id.sort()
		for cer in professional_journey_id:
			professional_journey = EmployeeEmployeeRegistrationUpdateProfessionalJourney()
			professional_journey.professional_journeycompany_1= request.POST.get('professional_journeycompany_' + str(cer)).strip()
			professional_journey.professional_journeystart_date_1 = request.POST.get('professional_journeystart_date_' + str(cer)).strip()
			professional_journey.professional_journeyend_date_1 = request.POST.get('professional_journeyend_date_' + str(cer)).strip()
			professional_journey.professional_journeylast_desgination_1_id = request.POST.get('professional_journeylast_desgination_' + str(cer)).strip()
			professional_journey.professional_journeynature_of_duties_1= request.POST.get('professional_journeynature_of_duties_' + str(cer)).strip()
			professional_journey.professional_journeylast_drawn_dalary_1= request.POST.get('professional_journeylast_drawn_dalary_' + str(cer)).strip()
			professional_journey.user_employee_id = personal_details.id
			professional_journey.save()

		salary_struct_id = [int(p.split('_')[4]) for p in request.POST if 'salary_structut_salary_code_' in p]
		salary_struct_id.sort()
		for cer in salary_struct_id:
			salary_struct = EmployeeEmployeeRegistrationUpdateSalaryStructutre()
			salary_struct.salary_structut_salary_code_1= request.POST.get('salary_structut_salary_code_' + str(cer)).strip()
			salary_struct.salary_structut_salary_name_1 = request.POST.get('salary_structut_salary_name_' + str(cer)).strip()
			salary_struct.professional_journeyend_date_1 = request.POST.get('professional_journeyend_date_' + str(cer)).strip()
			salary_struct.salary_structut_salary_frequency_1 = request.POST.get('salary_structut_salary_frequency_' + str(cer)).strip()
			salary_struct.salary_structut_amount_offered_1= request.POST.get('salary_structut_amount_offered_' + str(cer)).strip()
			salary_struct.salary_structut_percentage_value_flag_1= request.POST.get('salary_structut_percentage_value_flag_' + str(cer)).strip()
			salary_struct.salary_structut_taxability_1 = request.POST.get('salary_structut_taxability_' + str(cer)).strip()
			salary_struct.user_employee_id = personal_details.id
			salary_struct.save()

		save_bank_detail = EmployeeEmployeeRegistrationUpdateBankDetails()
		save_bank_detail.account_type = request.POST.get('account_type')
		save_bank_detail.bank_account_number = request.POST.get('bank_account_number')
		save_bank_detail.bank_name = request.POST.get('bank_name')
		save_bank_detail.branch = request.POST.get('branch')
		save_bank_detail.ifscc_code = request.POST.get('ifscc_code')
		save_bank_detail.micr = request.POST.get('micr')
		save_bank_detail.user_employee_id = personal_details.id
		save_bank_detail.save()

		reference_id = [int(p.split('_')[1]) for p in request.POST if 'referencename_' in p]
		reference_id.sort()
		for cer in reference_id:
			reference = EmployeeEmployeeRegistrationReferences()
			reference.referencename_1= request.POST.get('referencename_' + str(cer)).strip()
			reference.referencerelationship_1 = request.POST.get('referencerelationship_' + str(cer)).strip()
			reference.referencecontact_number_1 = request.POST.get('referencecontact_number_' + str(cer)).strip()
			reference.referenceemail_id_1 = request.POST.get('referenceemail_id_' + str(cer)).strip()
			reference.referenceaddress_1= request.POST.get('referenceaddress_' + str(cer)).strip()
			reference.referenceknown_since_1= request.POST.get('referenceknown_since_' + str(cer)).strip()
			reference.user_employee_id = personal_details.id
			reference.save()

		verificationreport = EmployeeEmployeeRegistrationVerificationReport()
		verificationreport.verification_agency = request.POST.get('verification_agency')
		verificationreport.finding = request.POST.get('finding')
		verificationreport.upload_report = request.FILES.get('upload_report')
		verificationreport.user_employee_id = personal_details.id
		verificationreport.save()

		verificationreport = EmployeeEmployeeRegistrationDeductionAndPerquisites()
		verificationreport.user_employee_id = personal_details.id
		verificationreport.perquisitec_category = request.POST.get('perquisitec_category')
		verificationreport.perquisitec_type = request.POST.get('perquisitec_type')
		verificationreport.perquisitec_name = request.POST.get('perquisitec_name')
		verificationreport.perquisite_frequency = request.POST.get('perquisite_frequency')
		verificationreport.perquisite_amount = request.POST.get('perquisite_amount')
		verificationreport.save()

		document_id = [int(p.split('_')[3]) for p in request.POST if 'name_of_documents_' in p]
		document_id.sort()
		for cer in document_id:
			document = EmployeeEmployeeRegistrationDocuments()
			document.name_of_documents_1 = request.POST.get('name_of_documents_' + str(cer)).strip()
			document.upload_1 = request.FILES.get('upload_' + str(cer))
			document.user_employee_id = personal_details.id
			document.save()
		messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		return redirect('crm_website_employeeservices_employeeregistration_updateregistrations_list')


class EmployeeServicesEmployeeRegistrationUpdateRegistrationsDelete(View):
	
	def get(self, request, id):
		if not request.user.is_authenticated:
		   return redirect('index')
		get_report = EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.filter(id = id).delete()
		messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
		return redirect('crm_website_employeeservices_employeeregistration_updateregistrations_list')


class AddEditCrmEmployeeEmployeeRegistrationUpdateDepartment(View):
	template = 'employee_website/employee_services/employee_registration/update_department.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeEmployeeRegistrationUpdateDepartmentForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		form = EmployeeEmployeeRegistrationUpdateDepartmentForm(request.POST)
		if form.is_valid():
			data = form.save()
			joining_detail = EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetails.objects.get(user_employee_id = request.POST['employee_id'])
			joining_detail.joining_location= request.POST.get('new_location')
			joining_detail.joining_department_id= request.POST.get('new_department')
			joining_detail.joining_designation_id= request.POST.get('new_designation')
			joining_detail.joining_responsibilities_id = request.POST.get('new_responsibilities')
			joining_detail.joining_reporting_to_id = request.POST.get('new_reporting_to')
			joining_detail.save()
		messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		return redirect('crm_website_employeeservices_employeeregistration_updatedeaprtment_update')


class AddEditCrmEmployeeEmployeeRegistrationUpdateDepartmentJsonEmployee(View):
	def post(self, request, *args, **kwargs):
		ServicesHtml = ''
		if request.is_ajax:
			get_info = EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetails.objects.get(user_employee_id = request.POST['id'])
			data = {
				'employee_name':get_info.user_employee.first_name,
				'department':get_info.joining_department.department,
				'designation':get_info.joining_designation.designation,
				'responsibilites':get_info.joining_responsibilities.responsibilities,
				'reporting_to':get_info.joining_reporting_to.name,
				'location':get_info.joining_location,
				'current_sal':'n/a',
			}
			return JsonResponse({'data': data})


class EmployeeServicesEmployeeRegistrationEmployeeListList(View):
	template = 'employee_website/employee_services/employee_registration/update_registrations_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = EmployeeRegistrationUpdateRegistrationJoiningDetails.objects.filter(user_employee__employee_created_by_id__in  = get_users).order_by('-id')
		get_report = EmployeeRegistrationUpdateRegistrationJoiningDetails.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)

#### update 
class EmployeeServicesEmployeeRegistrationEmployeeUpdate(View):
	template = 'employee_website/employee_services/employee_registration/update_registrations_update.html'
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		instance = get_object_or_404(EmployeeRegistrationUpdateRegistrationJoiningDetails, pk=id)
		context = {
			'form':EmployeeRegistrationUpdateRegistrationJoiningDetailsFormUpdate(instance = instance),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		instance = get_object_or_404(EmployeeRegistrationUpdateRegistrationJoiningDetails, pk=id)
		form = EmployeeRegistrationUpdateRegistrationJoiningDetailsFormUpdate(request.POST,  instance = instance)
		if form.is_valid():
			form.save()
		messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		return redirect('crm_website_employeeservices_employeeregistration_employee_list')

####
class LeavesUpdateLeaveQuotaOfEmployesListView(View):
	template = 'employee_website/employee_services/leaves/update_employees_leave_quota_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = LeaveandHolidaysManagementUpdateLeavesQuota.objects.filter(user_id__in = get_users).order_by('-id')
		get_report = LeaveandHolidaysManagementUpdateLeavesQuota.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class LeavesUpdateLeaveQuotaOfEmployesAddView(View):
	template = 'employee_website/employee_services/leaves/update_employees_leave_quota.html'


	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': LeaveandHolidaysManagementLeavesForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
		form = LeaveandHolidaysManagementLeavesForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('crm_website_employeeservices_employees_leavequota_list')


class LeavesUpdateLeaveQuotaOfEmployesUpdateView(View):
	template = 'employee_website/employee_services/leaves/update_employees_leave_quota.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = LeaveandHolidaysManagementUpdateLeavesQuota.objects.get(id = id )
		context = {
			'form': LeaveandHolidaysManagementLeavesForm(instance = data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
	
		data = LeaveandHolidaysManagementUpdateLeavesQuota.objects.get(id = id )
		form = LeaveandHolidaysManagementLeavesForm(request.POST, instance = data)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('crm_website_employeeservices_employees_leavequota_list')


class LeavesUpdateLeaveQuotaOfEmployesUpdateViewDelete(View):
	
	def get(self, request, id):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = LeaveandHolidaysManagementUpdateLeavesQuota.objects.filter(id = id).delete()
		messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
		return redirect('crm_website_employeeservices_employees_leavequota_list')


class EmployeeLeavesLeaveRequestPostLeave(View):
	template = 'employee_website/employee_services/leaves/apply_leave.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeLeavesLeaveRequestForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		if request.method=='POST':
			form =EmployeeLeavesLeaveRequestForm(request.POST)
			if form.is_valid():
				form.save()
		# save_user = EmployeeLeavesLeaveRequest()
		# save_user.employee_id_id = request.user.id
		# save_user.type_of_leave_id = request.POST.get('type_of_leave')
		# save_user.leave_available = request.POST.get('leave_available')
		# save_user.start_date = request.POST.get('start_date')
		# save_user.end_date = request.POST.get('end_date')
		# save_user.total_leave = request.POST.get('total_leave')
		# save_user.explaination = request.POST.get('explaination')
		# save_user.save()
		messages.add_message(request, messages.SUCCESS, "Leave apply Successfully.")
		return redirect('crm_website_employeeservices_leave_pendingforapproval_list')


class LeavesUpdateLeaveQuotaOfEmployesUpdateViewCancel(View):
	
	def get(self, request, id):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeLeavesLeaveRequest.objects.filter(id = id).update(status = 4)
		messages.add_message(request, messages.SUCCESS, "Leave cancel Successfully.")
		return redirect('crm_website_employeeservices_employees_leavequota_list')


class EmployeeLeavesLeaveRequestPendingforApprovalList(View):
	template = 'employee_website/employee_services/leaves/pending_for_approval_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = EmployeeLeavesLeaveRequest.objects.filter(employee_id_id__in = get_users).order_by('-id')
		get_report = EmployeeLeavesLeaveRequest.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeLeavesLeaveRequestPostLeaveUpdate(View):
	template = 'employee_website/employee_services/leaves/update_status.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		instance = get_object_or_404(EmployeeLeavesLeaveRequest, pk=id)
		context = {
			'form': EmployeeLeavesLeaveRequestUpdateStatusForm(instance = instance),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		instance = get_object_or_404(EmployeeLeavesLeaveRequest, pk=id)
		form = EmployeeLeavesLeaveRequestUpdateStatusForm(request.POST,  instance = instance)
		if form.is_valid():
			form.save()
		messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		return redirect('crm_website_employeeservices_leave_pendingforapproval_list')


class EmployeeLeavesLeaveRequestPostLeaveJsonData(View):
	def post(self, request, *args, **kwargs):
		if request.is_ajax:
			get_info = LeaveandHolidaysManagementUpdateLeavesQuota.objects.filter(user_id = request.POST['user_id'] , leave_type_id = request.POST['id'])
			if get_info:
				data = {
					'employee_quota':get_info[0].leave_balance,
				}
			else:
				data = {
					'employee_quota': 0
				}
			return JsonResponse({'data': data})


class EmployeeLeavesLeaveRequestApprovedLeaveList(View):
	template = 'employee_website/employee_services/leaves/approved_leave_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = EmployeeLeavesLeaveRequest.objects.filter(employee_id_id__in = get_users, status = 2).order_by('-id')
		get_report = EmployeeLeavesLeaveRequest.objects.filter( status = 2).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeLeavesLeaveRequestRejectedLeaveList(View):
	template = 'employee_website/employee_services/leaves/rejected_leave_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = EmployeeLeavesLeaveRequest.objects.filter(employee_id_id__in = get_users, status = 3).order_by('-id')
		get_report = EmployeeLeavesLeaveRequest.objects.filter( status = 3).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeLeavesLeaveRequestMyBalanceLeaveList(View):
	template = 'employee_website/employee_services/leaves/my_balance_leave.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = LeaveandHolidaysManagementUpdateLeavesQuota.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


# Leaves
class EmployeeAttendanceUploadAttendanceUpdate(View):
	template = 'employee_website/employee_services/attendance/upload_attendance.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': UserAttendenceSerializersForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		try:
			
			if 'upload_attendance' not in request.POST:
				today_date = date.today()
				# if CrmUserLoginApiLogs.objects.filter(added__date=today_date, login_true = True, user_id = request.user.id):
				# 	messages.add_message(request, messages.ERROR, "Login attendance already marked.")
				# 	return redirect('crm_website_employeeservices_leave_pendingforapproval_list')
				data  = UserLoginApiLogs()
				data.attendance_type =  request.POST.get('attendance_type')
				data.address =  request.POST.get('address')
				data.logout_address =  request.POST.get('logout_address')
				data.login_time =  str(request.POST['date_field'])+'-01'+' '+ request.POST['login_time']
				data.logout_time =  str(request.POST['date_field'])+'-01'+' '+ request.POST['logout_time']
				data.login_true =  True
				data.logout_true =  True
				data.employee_id =  request.POST.get('employee_id')
				data.save()
				messages.add_message(request, messages.SUCCESS, "Attendance added Successfully.")
		
			else:
				excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
				SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
				with open(excel_name_sheet,'r')as f:
					data = csv.reader(f)
					count = 0
					for row in data:
						if count !=0:
							data  = UserLoginApiLogs()
							data.user_id = row[0]
							data.login_time =  str(row[1])+'-01'+' '+ str(row[3])
							data.attendance_type =  row[2]
							data.address =  row[4]
							data.logout_time =  str(row[1])+'-01'+' '+ str(row[5])
							data.logout_address =  row[6]
							data.login_true =  True
							data.logout_true =  True
							data.save()
						count += 1
				messages.add_message(request, messages.SUCCESS, "Attendance uploaded Successfully.")
			return redirect('crm_employee_services_attendance_update_list')
		except: 
			messages.add_message(request, messages.ERROR, "Timing format is invalid try again .")
			return redirect('crm_employee_services_attendance_update_list')

class EmployeeAttendanceUpdateAttendanceList(View):
    template = 'employee_website/employee_services/attendance/update_attendance.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_authenticated:
            return redirect('index')
        today = date.today()
        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = UserLoginApiLogs.objects.filter( added__date = today).order_by('-id')
        user_name = request.GET.get('user_name')
        search_date = request.GET.get('date')
        if  user_name != None and str(user_name) != "":
            get_data = get_data.filter(user__name__icontains=str(user_name).strip())
        if search_date != None and str(search_date) != "":
            get_data = get_data.filter(added__date =str(search_date).strip())
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)       
        context ={
            'responselistquery': report_paginate,
        }
        return render(request, self.template, context)


class EmployeeAttendanceUpdateAttendanceUpdate(View):
	template = 'employee_website/employee_services/attendance/update_attendance_today.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(UserLoginApiLogs, pk = id)
		context = {
			'form': UserAttendenceSerializersUpdateForm(instance = data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		today_date = date.today()
		data = get_object_or_404(UserLoginApiLogs, pk = id)
		form = UserAttendenceSerializersUpdateForm(request.POST, instance = data)
		if form.is_valid():
			data  =form.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_employee_services_attendance_update_list')


class EmployeeAttendanceAttendanceStatusList(View):
    template = 'employee_website/employee_services/attendance/attendance_status.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_authenticated:
            return redirect('index')

        today = date.today()
        filter_type = request.GET.get('type')
        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = UserLoginApiLogs.objects.filter( added__date = today).order_by('-id')
        if filter_type is not None:
        	if str(filter_type) == "1":
        		today = date.today()
        		get_data = UserLoginApiLogs.objects.filter(added__date = today).order_by('-id')
        	elif str(filter_type) == "2":
        		current_month = datetime.now().month
        		get_data = UserLoginApiLogs.objects.filter(added__month = current_month).order_by('-id')
        	elif str(filter_type) == "3":
        		previous_month = datetime.now().month - 1
        		get_data = UserLoginApiLogs.objects.filter(added__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)       
        context ={
            'responselistquery': report_paginate,
        }
        return render(request, self.template, context)

###
class EmployeeAttendanceAttendanceStatusUpdate(View):
	template = 'employee_website/employee_services/attendance/update_attendance_today.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		data = get_object_or_404(UserLoginApiLogs, pk = id)
		context = {
			'form': UserLoginApiLogsForm(instance = data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
		today_date = date.today()
		data = get_object_or_404(UserLoginApiLogs, pk = id)
		form = UserLoginApiLogsForm(request.POST, instance = data)
		print(form.errors)
		if form.is_valid():
			
			data  =form.save()
			messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_employee_services_attendance_status')




# HR Policies  > Update Policy
class EmployeeHRPoliciesUpdatePolicy(View):
	template = 'employee_website/employee_services/hr_policies/update_policies_upload.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		if id is None:
			context = {
				'form': EmployeeHRPoliciesUpdatePoliciesmodelForm,
			}
		else:
			data = get_object_or_404(EmployeeHRPoliciesUpdatePolicies,  pk=id)
			context = {
				'form': EmployeeHRPoliciesUpdatePoliciesmodelForm(instance = data),
			}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if id is None:
			form = EmployeeHRPoliciesUpdatePoliciesmodelForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				data.user_id  = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:
			data = get_object_or_404(EmployeeHRPoliciesUpdatePolicies,  pk=id)
			form = EmployeeHRPoliciesUpdatePoliciesmodelForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_employee_services_hrpolicies_upload_update_policies_list')	


class EmployeeHRPoliciesUpdateForms(View):
	template = 'employee_website/employee_services/hr_policies/update_forms_upload.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		if id is None:
			context = {
				'form': EmployeeHRPoliciesUpdateFormmodelForm,
			}
		else:
			data = get_object_or_404(EmployeeHRPoliciesUpdateForm,  pk=id)
			context = {
				'form': EmployeeHRPoliciesUpdateFormmodelForm(instance = data),
			}

		return render(request, self.template, context)

	def post(self, request, id = None):

		if id is None:
			form = EmployeeHRPoliciesUpdateFormmodelForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				data.user_id  = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:                                                                                        
			data = get_object_or_404(EmployeeHRPoliciesUpdateForm,  pk=id)
			form = EmployeeHRPoliciesUpdateFormmodelForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_employee_services_hrpolicies_upload_update_forms_list')


class EmployeeHRUpdateCircularsForms(View):
	template = 'employee_website/employee_services/hr_policies/update_circularal.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		if id is None:
			context = {
				'form': EmployeeHRPoliciesUpdateCircularsForm,
			}
		else:
			data = get_object_or_404(EmployeeHrPoliciesUpdateCirculars,  pk=id)
			context = {
				'form': EmployeeHRPoliciesUpdateCircularsForm(instance = data),
			}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if id is None:
			form = EmployeeHRPoliciesUpdateCircularsForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				data.user_id  = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:
			data = get_object_or_404(EmployeeHrPoliciesUpdateCirculars,  pk=id)
			form = EmployeeHRPoliciesUpdateCircularsForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_employee_services_hrpolicies_upload_update_circulars_list')


class EmployeeHRPoliciesUpdatePolicyList(View):
	template = 'employee_website/employee_services/hr_policies/update_policies_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = EmployeeHRPoliciesUpdatePolicies.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)

		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeHRPoliciesUpdateFormmodelList(View):
	template = 'employee_website/employee_services/hr_policies/update_forms_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = EmployeeHRPoliciesUpdateForm.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeHRPoliciesUpdateCircularsmodelList(View):
	template = 'employee_website/employee_services/hr_policies/update_circulars_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = EmployeeHrPoliciesUpdateCirculars.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


# Claim and Reimbursement
class EmployeeClaimandReimbursementSubmitClaimsFormView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/submit_claim.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitClaimsForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		if request.method=='POST':
			
			form = EmployeeClaimandReimbursementSubmitClaimsForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
			messages.add_message(request, messages.SUCCESS, "Claim submited Successfully.")
			return redirect('crm_employee_services_claimandreimbursement_submitclaims')
		


class EmployeeClaimandReimbursementSubmitClaimsApprovedView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/approved_claim.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitClaimsApprovedForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		try:
			EmployeeClaimandReimbursementSubmitClaimsUpdateStatus.objects.get(user_id = request.user.id, submit_claim_id= id)
			messages.add_message(request, messages.WARNING, "Already submited.")
			return redirect('crm_employee_services_claimandreimbursement_submitclaims_list')
		except:
			save_data = EmployeeClaimandReimbursementSubmitClaimsUpdateStatus()
			save_data.user_id = request.user.id
			save_data.submit_claim_id = id
			save_data.approved_amount = request.POST.get('approved_amount_1')
			save_data.save()
			messages.add_message(request, messages.SUCCESS, "Amount offered Successfully.")
			return redirect('crm_employee_services_claimandreimbursement_submitclaims_list')


class EmployeeClaimandReimbursementSubmitClaimsListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/submit_claim_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeClaimandReimbursementSubmitClaims.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeClaimandReimbursementSubmitClaimsApprovedListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/submit_claim_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_report = EmployeeClaimandReimbursementSubmitClaims.objects.filter(status = 'Approved').order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeClaimandReimbursementSubmitReimbursementFormView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/submit_reimbursement.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitReimbursementForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		get_all_id = [int(p.split('_')[2]) for p in request.POST if 'reimbursement_month_' in p]
		get_all_id.sort()
		for data in get_all_id:
			save_submit_claim = EmployeeClaimandReimbursementSubmitReimbursement()
			save_submit_claim.user_id = request.user.id
			save_submit_claim.reimbursement_month_1 = request.POST.get('reimbursement_month_'+str(data))
			save_submit_claim.reimbursement_type_1_id = request.POST.get('reimbursement_type_'+str(data))
			save_submit_claim.reimbursement_period_1 = request.POST.get('reimbursement_period_'+str(data))
			save_submit_claim.details_1 = request.POST.get('details_'+str(data))
			save_submit_claim.amount_1 = request.POST.get('amount_'+str(data))
			save_submit_claim.maximum_limit_1 = request.POST.get('maximum_limit_'+str(data))
			save_submit_claim.comment_1 =  request.POST.get('comment_'+str(data))
			save_submit_claim.upload_1 = request.FILES.get('upload_'+str(data))
			save_submit_claim.save()
		messages.add_message(request, messages.SUCCESS, "Claim submited Successfully.")
		return redirect('crm_employee_services_claimandreimbursement_submitreimbursement')


class EmployeeClaimandReimbursementSubmitReimbursementApprovedView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/approved_reimbursement.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitReimbursementFormApprovedForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		try:
			save_data = EmployeeClaimandReimbursementSubmitClaimsUpdateStatus.objects.get(user_id = request.user.id, submit_claim_id = id)
		except:
			save_data = EmployeeClaimandReimbursementSubmitClaimsUpdateStatus()
			save_data.user_id = request.user.id
			save_data.submit_claim_id = id
			save_data.approved_amount = request.POST['approved_amount_1']
			save_data.save()
		messages.add_message(request, messages.SUCCESS, "Amount offered Successfully.")
		return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_list')


class EmployeeClaimandReimbursementSubmitReimbursementApprovedListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/submit_reimbursement_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeClaimandReimbursementSubmitReimbursement.objects.filter(status = 2).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


# Approved Claim To Process
class EmployeeClaimandReimbursementSubmitReimbursementApprovedClaimToProcessView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/claim_processing.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = EmployeeClaimandReimbursementSubmitClaimsUpdateStatus.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeClaimandReimbursementApprovedDateOfProcessingView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/approved_reimbursement.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitAmountApprovedProcessingForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		get_data = get_object_or_404(EmployeeClaimandReimbursementSubmitClaimsUpdateStatus, pk = id)
		instance = get_object_or_404(EmployeeClaimandReimbursementSubmitClaims, pk = get_data.submit_claim_id)
		form = EmployeeClaimandReimbursementSubmitAmountApprovedProcessingForm(request.POST, instance = instance)
		if form.is_valid():
			data = form.save()
			if request.POST.get('status') == "2":
				data.approved_by_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Amount offered Successfully.")
		else:
			messages.add_message(request, messages.ERROR, "Someting went Wrong.")
		return redirect('crm_employee_services_claimandreimbursement_claimprocessing_list')


class EmployeeClaimandReimbursementSubmitReimbursementApprovedClaimToProcessListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/reimbursement_processing.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = EmployeeClaimandReimbursementSubmitReimbursement.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeClaimandReimbursementClaimClaimProcessedListView(View):
    template = 'employee_website/employee_services/claim_and_reimbursement/claim_processed_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
           return redirect('index')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        # get_data = EmployeeClaimandReimbursementSubmitClaims.objects.filter( status = 'Pending').order_by('-id')
        get_data = EmployeeClaimandReimbursementSubmitClaims.objects.all().order_by('-id')
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(updated__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(date_of_processing__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(date_of_processing__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)

#########
class EmployeeClaimandReimbursementClaimClaimProcessedUpdatesView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/approved_reimbursement.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitClaimsUpdatesForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		manageproduct = get_object_or_404(EmployeeClaimandReimbursementSubmitClaims, pk=id)
		if request.method == "POST":
			form =EmployeeClaimandReimbursementSubmitClaimsUpdatesForm(request.POST, instance=manageproduct)
			if form.is_valid():
				form.save()
				return redirect('crm_employee_services_claimandreimbursement_claim_claimprocessed_list')
		else:
			form = EmployeeClaimandReimbursementSubmitClaimsUpdatesForm(instance=manageproduct)
		return redirect('crm_employee_services_claimandreimbursement_claim_claimprocessed_list')



class EmployeeClaimandReimbursementReimbursementRejectedListView(View):
    template = 'employee_website/employee_services/claim_and_reimbursement/submit_reimbursement_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
           return redirect('index')

       	get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = EmployeeClaimandReimbursementSubmitReimbursement.objects.all().order_by('-id')
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(updated__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(date_of_processing__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(date_of_processing__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        
        context = {
           'responselistquery': report_paginate
        }
        return render(request, self.template, context)
###############
class EmployeeClaimandReimbursementReimbursementRejectedUpdateView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/submit_reimbursement_add.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitReimbursementSubmitUpdateForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		manageproduct = get_object_or_404(EmployeeClaimandReimbursementSubmitReimbursement, pk=id)
		if request.method == "POST":
			form =EmployeeClaimandReimbursementSubmitReimbursementSubmitUpdateForm(request.POST, instance=manageproduct)
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, "Data Add Successfully.")
				return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_reimbursementprocessed_list')
		else:
			form = EmployeeClaimandReimbursementSubmitReimbursementSubmitUpdateForm(instance=manageproduct)
			messages.add_message(request, messages.SUCCESS, "Data Add Fail.")

		return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_reimbursementprocessed_list')




# All Claim and Reimbursement
class EmployeeClaimandReimbursementClaimStatusListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/claim_status_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = EmployeeClaimandReimbursementSubmitClaims.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeClaimandReimbursementSubmitReimbursementListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/approved_reimbursement.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeClaimandReimbursementSubmitClaimsApprovedForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		manageproduct = get_object_or_404(EmployeeClaimandReimbursementSubmitReimbursement, pk=id)
		if request.method == "POST":
			form =EmployeeClaimandReimbursementSubmitClaimsApprovedForm(request.POST, instance=manageproduct)
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, "Data Add Successfully.")
				return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_status_list')
		else:
			form = EmployeeClaimandReimbursementSubmitClaimsApprovedForm(instance=manageproduct)
			messages.add_message(request, messages.SUCCESS, "Data Add Fail.")

		return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_status_list')



		# try:
		# 	save_data = EmployeeClaimandReimbursementSubmitReimbursementUpdateStatus.objects.get(user_id = request.user.id, submit_claim_id = id)
		# except:
		# 	save_data = EmployeeClaimandReimbursementSubmitReimbursementUpdateStatus()
		# 	save_data.user_id = request.user.id
		# 	save_data.submit_claim_id = id
		# 	save_data.approved_amount = request.POST['approved_amount']
		# 	save_data.save()
		# messages.add_message(request, messages.SUCCESS, "Amount offered Successfully.")
		# return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_status_list')


class EmployeeClaimandReimbursementRembursementStatusListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/rembursement_status_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = EmployeeClaimandReimbursementSubmitReimbursement.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class EmployeeClaimandReimbursementSubmitReimbursementApprovedDateOfProcessingView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/approved_reimbursement.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeReimbursementSubmitAmountApprovedProcessingForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):


		manageproduct = get_object_or_404(EmployeeClaimandReimbursementSubmitReimbursement, pk=id)
		if request.method == "POST":
			form =EmployeeClaimandReimbursementSubmitAmountApprovedProcessingForm(request.POST, instance=manageproduct)
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, "Data Add Successfully.")
				return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursementprocessing_list')
		else:
			form = EmployeeClaimandReimbursementSubmitAmountApprovedProcessingForm(instance=manageproduct)
			messages.add_message(request, messages.ERROR, "Someting went Wrong.")

		return redirect('crm_employee_services_claimandreimbursement_submitreimbursement_reimbursementprocessing_list')


class EmployeePayrollProcessingAcceptAttendanceListView(View):
	template = 'employee_website/employee_services/payroll/accept_attendance.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_current_month = date.today().month
		get_all_user_ids = UserLoginApiLogs.objects.filter(attendance_status=2).order_by("-id")
		
		get_all_data  = ManageWorkingDays.objects.all().order_by('-id')
		get_financial_year = ManageHolidays.objects.all().order_by('-id')
	
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'get_all_data':get_all_data,
			'get_financial_year':get_financial_year,
			'stauts': ATTENDENCE_STATUS,
			# 'get_monthly_holidays_days':get_monthly_holidays_days,
		}
		return render(request, self.template, context)

	def post(self, request):
		get_current_month = date.today().month
		accept_reject = UserLoginApiLogs.objects.filter(user_id__in = [data  for data in request.POST['bul_data'].split(',')], added__month = get_current_month).update(attendance_status = request.POST['status'])
		messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		return redirect('crm_employee_services_payroll_accept_attendance_list')
#1
class UserAcceptAttendanceUpdateFormView(View):
	template = 'employee_website/employee_services/payroll/accept_attendance_update.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': UserAcceptAttendanceUpdateForm(),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		manageproduct = get_object_or_404(UserLoginApiLogs, pk=id)
		if request.method == "POST":
			form =UserAcceptAttendanceUpdateForm(request.POST, instance=manageproduct)
			if form.is_valid():
				form.save()
				return redirect('crm_employee_services_payroll_accept_attendance_list')
		else:
			form = UserAcceptAttendanceUpdateForm(instance=manageproduct)
		return redirect('crm_employee_services_payroll_accept_attendance_list')




class EmployeePayrollProcessingAcceptOverTimeListView(View):
	template = 'employee_website/employee_services/payroll/accept_overtime_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_current_month = date.today().month
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_all_user_ids =[p['user_id'] for p in OvertimeManagementUpdateOvertime.objects.values('user_id').filter(user_id__in = get_users, added__month = get_current_month, user_id = request.user.id).distinct()] 
		get_all_user_ids = OvertimeManagementUpdateOvertime.objects.all().order_by("-id")
		# get_report = User.objects.filter(id__in = get_all_user_ids)
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'stauts': ATTENDENCE_STATUS
		}
		return render(request, self.template, context)

	def post(self, request):
		get_current_month = date.today().month
		accept_reject = UserLoginApiLogs.objects.filter(user_id__in = [data  for data in request.POST['bul_data'].split(',')], added__month = get_current_month).update(attendance_status = request.POST['status'])
		messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		return redirect('crm_employee_services_payroll_accept_attendance_list')


class EmployeePayrollUpdateLeavesListView(View):
	template = 'employee_website/employee_services/payroll/update_leaves_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_current_month = date.today().month
		get_all_user_ids = EmployeeLeavesLeaveRequest.objects.filter(added__month = get_current_month).order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'leave_status':LEAVE_STATUS
		}
		return render(request, self.template, context)

	def post(self, request):
		data1 = [data  for data in request.POST['bul_data'].split(',')]
		accept_reject = EmployeeLeavesLeaveRequest.objects.filter(id__in = data1).update(status = request.POST['status'])
		messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		return redirect('crm_employee_services_payroll_update_leave_list')


class EmployeePayrollAcceptClaimsView(View):
	template = 'employee_website/employee_services/payroll/accept_claims_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_current_month = date.today().month
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_all_user_ids = EmployeeClaimandReimbursementSubmitClaims.objects.filter(user_id__in = get_users, added__month = get_current_month, user_id = request.user.id, status = 2)
		get_all_user_ids = EmployeeClaimandReimbursementSubmitClaims.objects.filter(status='Approved').order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status':CLAIM_STATUS
		}
		return render(request, self.template, context)

	def post(self, request):
		data1 = [data  for data in request.POST['bul_data'].split(',')]
		accept_reject = EmployeeClaimandReimbursementSubmitClaims.objects.filter(id__in = data1).update(status = request.POST['status'])
		messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		return redirect('crm_employee_services_payroll_claim_update_list')


class EmployeePayrollUpdateReimbursementView(View):
	template = 'employee_website/employee_services/payroll/update_reimbursement_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_current_month = date.today().month
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_all_user_ids = EmployeeClaimandReimbursementSubmitReimbursement.objects.filter(added__month = get_current_month, status = 'Approved')
		print(get_all_user_ids)
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status':CLAIM_STATUS
		}
		return render(request, self.template, context)

	def post(self, request):
		data1 = [data  for data in request.POST['bul_data'].split(',')]
		accept_reject = EmployeeClaimandReimbursementSubmitReimbursement.objects.filter(id__in = data1).update(status = request.POST['status'])
		messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		return redirect('crm_employee_services_payroll_reimbursement_update_list')


class EmployeePayrollUpdateAdvancesView(View):
	template = 'employee_website/employee_services/payroll/update_advances_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_all_user_ids = EmployeePayrollProcessingUpdateAdvances.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		if 'upload_bulk_data' in request.FILES:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet,'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = EmployeePayrollProcessingUpdateAdvances()
							save_data.location = row[0]
							save_data.department = row[1]
							save_data.month_and_year = row[2]
							save_data.user_id = row[3]
							save_data.recovery_period = row[4]
							save_data.advance_amount = row[5]
							save_data.interest_rate = row[6]
							save_data.total_amount = row[7]
							save_data.recovery_amount = row[8]
							save_data.recovery_start_date = row[9]
							save_data.save()
						except EmployeePayrollProcessingUpdateAdvances.DoesNotExist:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_employee_services_payroll_update_advances_list')

					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_employee_services_payroll_update_advances_list')
		else:
			data1 = [data  for data in request.POST['bul_data'].split(',')]
			accept_reject = EmployeePayrollProcessingUpdateAdvances.objects.filter(id__in = data1).update(status = request.POST['status'])
			messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
			return redirect('crm_employee_services_payroll_update_advances_list')


class EmployeePayrollIncentivesView(View):
	template = 'employee_website/employee_services/payroll/update_incentives.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_current_month = date.today().month
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_all_user_ids = EmployeeAdvancesSubmitIncentiveBonus.objects.filter(user_id__in = get_users, added__month = get_current_month, user_id = request.user.id, status = 3)
		get_all_user_ids = EmployeeAdvancesSubmitIncentiveBonus.objects.filter( status = "Processed").order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		if 'upload_bulk_data' in request.FILES:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet,'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = EmployeePayrollProcessingUpdateIncentives()
							save_data.location = row[0]
							save_data.department = row[1]
							save_data.month_and_year = row[2]
							save_data.user_id = row[3]
							save_data.incentive_type = row[4]
							save_data.incentive_period = row[5]
							save_data.incentive_amount = row[6]
							save_data.save()
						except:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_employee_services_payroll_update_incentive_list')

					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_employee_services_payroll_update_incentive_list')
		else:
			data1 = [data  for data in request.POST['bul_data'].split(',')]
			accept_reject = EmployeePayrollProcessingUpdateIncentives.objects.filter(id__in = data1).update(status = request.POST['status'])
			messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
			return redirect('crm_employee_services_payroll_update_incentive_list')


class EmployeeUpdateTaxDeclarationView(View):
	template = 'employee_website/employee_services/payroll/update_tax_declaration.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		
		form = EmployeePayrollProcessingUpdateTaxDeclarationForm()
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_all_user_ids = EmployeePayrollProcessingUpdateTaxDeclaration.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS,
			'form':form
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		                                             
		if 'upload_bulk_data' not in request.FILES:

			form = EmployeePayrollProcessingUpdateTaxDeclarationForm(request.POST)
			
			if form.is_valid():
				form.save()
			return redirect('crm_employee_services_payroll_tax_declaration_list')
			
		else:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet, 'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = EmployeePayrollProcessingUpdateTaxDeclaration()
							save_data.location = row[0]
							save_data.departments = row[1]
							save_data.assessment_year = row[2]
							save_data.employee_id = row[3]
							save_data.employee_names= row[4]
							save_data.tax_declaration_type = row[5]
							save_data.tax_rule = row[6]
							save_data.exemption_claimed = row[7]
							save_data.exemption_approved = row[8]
							save_data.maximum_limit = row[9]
							save_data.save()
							messages.add_message(request, messages.SUCCESS, "Data upload Sucessfully.")
							return redirect('crm_employee_services_payroll_tax_declaration_list')
						except Exception as e:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_employee_services_payroll_tax_declaration_list')
					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_employee_services_payroll_tax_declaration_list')
		
###

def EmployeeUpdateTaxDeclarationUpdateView(request, id = None):
	form = EmployeePayrollProcessingUpdateTaxDeclarationForm()
	manageproduct = get_object_or_404(EmployeePayrollProcessingUpdateTaxDeclaration, pk=id)
	if request.method == "POST":
		form =EmployeePayrollProcessingUpdateTaxDeclarationForm(request.POST, instance=manageproduct)
		if form.is_valid():
			form.save()
			return redirect('crm_employee_services_payroll_tax_declaration_list')
	else:
		form = EmployeePayrollProcessingUpdateTaxDeclarationForm(instance=manageproduct)
	return render(request,'employee_website/employee_services/payroll/update_tax_declaration_edit.html',{'form':form})
########

class EmployeeUpdateTaxRecoveryView(View):
	template = 'employee_website/employee_services/payroll/update_tax_recovery.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		form = EmployeePayrollProcessingUpdateTaxRecoveryForm()
		
		get_all_user_ids = EmployeePayrollProcessingUpdateTaxRecovery.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'form':form
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		if 'upload_bulk_data' not in request.FILES:
			form = EmployeePayrollProcessingUpdateTaxRecoveryForm(request.POST)
			if form.is_valid():
				form.save()
			return redirect('crm_employee_services_payroll_tax_recovery_list')
			
		else:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet, 'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							
							save_data = EmployeePayrollProcessingUpdateTaxRecovery()
							save_data.location = row[0]
							save_data.departments = row[1]
							save_data.assessment_year = row[2]
							save_data.employee_id = row[3]
							save_data.employee_names= row[4]
							save_data.year_to_date_salary = row[5]
							save_data.annual_salary = row[6]
							save_data.total_tax_payable = row[7]
							save_data.tax_already_recovered = row[8]
							save_data.recovery_during_current_month = row[9]
							save_data.total_tax_recovered = row[10]
							save_data.balance_tax_payable = row[11]
							save_data.save()
							messages.add_message(request, messages.SUCCESS, "Data upload Sucessfully.")
							return redirect('crm_employee_services_payroll_tax_recovery_list')
						except Exception as e:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_employee_services_payroll_tax_recovery_list')
					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_employee_services_payroll_tax_recovery_list')
		
###

def EmployeeUpdateTaxRecoveryUpdateView(request, id = None):
	form = EmployeePayrollProcessingUpdateTaxRecoveryForm()
	manageproduct = get_object_or_404(EmployeePayrollProcessingUpdateTaxRecovery, pk=id)
	if request.method == "POST":
		form =EmployeePayrollProcessingUpdateTaxRecoveryForm(request.POST, instance=manageproduct)
		if form.is_valid():
			form.save()
			return redirect('crm_employee_services_payroll_tax_recovery_list')
	else:
		form = EmployeePayrollProcessingUpdateTaxRecoveryForm(instance=manageproduct)
	return render(request,'employee_website/employee_services/payroll/update_tax_recovery_edit.html',{'form':form})


#######end 

class EmployeeSalaryDeductionsListAddView(View):
	template = 'employee_website/employee_services/payroll/statutory_deductions_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		form = PayrollStatutoryDeductionsForm()
		get_all_user_ids = PayrollStatutoryDeductions.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS,
			'form':form,
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
	
		if 'upload_bulk_from_btn' not in request.FILES:
			
			if request.method=="POST":
				form = PayrollStatutoryDeductionsForm(request.POST)
				
				if form.is_valid():
					form.save()
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')

		else:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet, 'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = PayrollStatutoryDeductions()
							save_data.user_id = row[0]
							data_time = datetime.strptime(str(row[1]), "%d/%m/%Y") 
							save_data.month_and_year = data_time.strftime("%Y-%m-%d")
							save_data.deduction_type_id = row[2]
							save_data.employer_contribution = row[3]
							save_data.employee_contribution = row[4]
							save_data.others = row[5]
							save_data.total_deduction = row[6]
							save_data.save()
							messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
							return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')
						except Exception as e:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')
					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')


def PayrollStatutoryDeductionsUpdateView(request, id = None):
	form = PayrollStatutoryDeductionsUpdateForm()
	manageproduct = get_object_or_404(PayrollStatutoryDeductions, pk=id)
	if request.method == "POST":
		form =PayrollStatutoryDeductionsUpdateForm(request.POST, instance=manageproduct)
		if form.is_valid():
			form.save()
			return redirect('crm_crmemployee_manageemployee_statutorydeductions_list')
	else:
		form = PayrollStatutoryDeductionsUpdateForm(instance=manageproduct)
	return render(request,'employee_website/employee_services/payroll/statutory_deductions_update.html',{'form':form})


class PayrollSalaryVoucherListAddView(View):
	template = 'employee_website/employee_services/payroll/payroll_salary_voucher_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		form = PayrollSalaryVoucherForm()
		get_all_user_ids = PayrollSalaryVoucher.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS,
			'form':form
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		
		if 'upload_bulk_data' not in request.FILES:
			if request.method =="POST":
				form =PayrollSalaryVoucherForm(request.POST)
				if form.is_valid():
					form.save()
					messages.add_message(request, messages.SUCCESS, 'Data Is Save SuceessFully.')
					return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')
				messages.add_message(request, messages.SUCCESS, 'Invalid Data.')
				return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')
		else:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet,'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = PayrollSalaryVoucher()
							save_data.month_and_year =row[0]
							save_data.gl_code = row[1]
							save_data.particulars = row[2]
							save_data.debit_amount = row[3]
							save_data.credit_amount = row[4]
							save_data.save()
							messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
							return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')
						except Exception as e:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')
					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')
		# else:
		# 	data1 = [data  for data in request.POST['bul_data'].split(',')]
		# 	accept_reject = PayrollSalaryVoucher.objects.filter(id__in = data1).update(status = request.POST['status'])
		# 	messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		# 	return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')

###


def PayrollSalaryVoucherListUpdateView(request, id = None):
	
	form = PayrollSalaryVoucherUpdateForm()
	manageproduct = get_object_or_404(PayrollSalaryVoucher, pk=id)
	if request.method == "POST":
		form =PayrollSalaryVoucherUpdateForm(request.POST, instance=manageproduct)
		if form.is_valid():
			form.save()
			return redirect('crm_crmemployee_manageemployee_salaryvoucher_list')
	else:
		form = PayrollSalaryVoucherUpdateForm(instance=manageproduct)
	return render(request,'employee_website/employee_services/payroll/payroll_salary_voucher_update.html',{'form':form})




class PayrollSalaryDisbursementListAddView(View):
	template = 'employee_website/employee_services/payroll/salary_disbursement_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_all_user_ids = PayrollSalaryDisbursement.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		
		excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
		SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
		with open(excel_name_sheet,'r')as f:
			data = csv.reader(f)
			count = 0
			for row in data:
				if count !=0:
					try:
						
						save_data = PayrollSalaryDisbursement()
						# data_time = datetime.strptime(str(row[0]), "%d/%m/%Y") 
						# save_data.month_and_year = data_time.strftime("%Y-%m-%d")
						save_data.month_and_year = row[0]
						save_data.employee_id = row[1]
						save_data.employee_names =row[2]
						save_data.bank_name = row[3]
						save_data.ifsc_code = row[4]
						save_data.account_number = row[5]
						save_data.amount = row[6]
						save_data.mode_of_payment = row[7]
						save_data.date_of_payment = row[8]
						# date_payment = datetime.strptime(str(row[8]), "%d/%m/%Y") 
						# save_data.date_of_payment = date_payment.strftime("%Y-%m-%d")
						save_data.save()
						messages.add_message(request, messages.SUCCESS, "Data Save SuccessFully.")
						return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
					except Exception as e:
						messages.add_message(request, messages.ERROR, "Something went wrong.")
						return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
				count += 1
			messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
####
### upload data to form 
def PayrollSalaryDisbursementListAddFormView(request):
	form = PayrollSalaryDisbursementAddForm()
	if request.method=="POST":
		form = PayrollSalaryDisbursementAddForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
	return render(request,'employee_website/employee_services/payroll/salary_disbursement_addedit.html',{'form':form})
		
####
def PayrollSalaryDisbursementListUpdate(request,id=None):
	manageEmp = get_object_or_404(PayrollSalaryDisbursement,pk=id)
	form = PayrollSalaryDisbursementAddForm(instance=manageEmp)
	
	if request.method=='POST':
		form = PayrollSalaryDisbursementAddForm(request.POST,instance=manageEmp)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
	return render(request,'employee_website/employee_services/payroll/salary_disbursement_addedit.html',{'form':form})



class EmployeePayrollProcessingTaxCalculationView(View):
	template = 'employee_website/employee_services/payroll/tax_calculation.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		form = EmployeePayrollProcessingTaxCalculationForm()
		get_all_user_ids = EmployeePayrollProcessingTaxCalculation.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS,
			'form':form
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		if 'upload_bulk_data' not in request.FILES:
		
			form = EmployeePayrollProcessingTaxCalculationForm(request.POST)
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
			return redirect('crm_employee_services_payroll_tax_calculation_list')
		
		else:
			
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet,'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = EmployeePayrollProcessingTaxCalculation()
							save_data.location = row[0]
							save_data.departments = row[1]
							save_data.assessment_year = row[2]
							save_data.year_to_date_salary = row[3]
							save_data.annual_salary = row[4]
							save_data.other_income = row[5]
							save_data.total_income = row[6]
							save_data.exemption = row[7]
							save_data.deduction = row[9]
							save_data.taxable_income = row[10]
							save_data.tax = row[11]
							save_data.cess = row[12]
							save_data.total_tax_payable = row[13]
							save_data.tax_deducted = row[14]
							save_data.tax_paid = row[15]
							# save_data.balance_tax_payable = row[16]
							save_data.save()
					
							messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
							return redirect('crm_employee_services_payroll_tax_calculation_list')
						except Exception as e:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_employee_services_payroll_tax_calculation_list')
					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_employee_services_payroll_tax_calculation_list')
		# else:
		# 	data1 = [data  for data in request.POST['bul_data'].split(',')]
		# 	accept_reject = EmployeePayrollProcessingTaxCalculation.objects.filter(id__in = data1).update(status = request.POST['status'])
		# 	messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
		# 	return redirect('crm_employee_services_payroll_tax_calculation_list')

#########
def EmployeePayrollProcessingTaxCalculationUpdateView(request,id=None):
	manage_data = get_object_or_404(EmployeePayrollProcessingTaxCalculation,pk=id)
	form = EmployeePayrollProcessingTaxCalculationForm(instance=manage_data)
	if request.method=="POST":
		form = EmployeePayrollProcessingTaxCalculationForm(request.POST,instance=manage_data)
		if form.is_valid():
			form.save()
			messages.add_message(request,messages.SUCCESS, "Data Update Successfully.")
			return redirect('crm_employee_services_payroll_tax_calculation_list')
		else:
			messages.add_message(request,messages.ERROR, "Something went wrong.")
			return redirect('crm_employee_services_payroll_tax_calculation_list')
	return render(request, 'employee_website/employee_services/payroll/tax_calculation_update.html' ,{'form':form})

class EmployeePayrollProcessingUpdateRecoveriesView(View):
	template = 'employee_website/employee_services/payroll/update_recoveries_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_all_user_ids = EmployeePayrollProcessingUpdateRecoveries.objects.all().order_by("-id")
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'status': CLAIM_STATUS
		}
		return render(request, self.template, context)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		if 'upload_bulk_data' in request.FILES:
			excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
			SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
			with open(excel_name_sheet,'r')as f:
				data = csv.reader(f)
				count = 0
				for row in data:
					if count !=0:
						try:
							save_data = EmployeePayrollProcessingUpdateRecoveries()
							save_data.location = row[0]
							save_data.departments = row[1]
							save_data.month_and_year = row[2]
							save_data.employee_id = row[3]
							save_data.employee_names = row[4]
							save_data.recovery_period = row[5]
							save_data.recovery_type = row[6]
							save_data.recovery_amount = row[7]
							save_data.save()
						except Exception as e:
							messages.add_message(request, messages.ERROR, "Something went wrong.")
							return redirect('crm_employee_services_payroll_update_recovery_list')
					count += 1
				messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
				return redirect('crm_employee_services_payroll_update_recovery_list')
		else:
			data1 = [data  for data in request.POST['bul_data'].split(',')]
			accept_reject = EmployeePayrollProcessingUpdateRecoveries.objects.filter(id__in = data1).update(status = request.POST['status'])
			messages.add_message(request, messages.SUCCESS, "Status Change Successfully..")
			return redirect('crm_employee_services_payroll_update_recovery_list')


### upload data to form 
def EmployeePayrollProcessingUpdateRecoveriesAdd(request):
	form = EmployeePayrollProcessingUpdateRecoveriesAddForm()
	if request.method=="POST":
		form = EmployeePayrollProcessingUpdateRecoveriesAddForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
			return redirect('crm_employee_services_payroll_update_recovery_list')
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
			return redirect('crm_employee_services_payroll_update_recovery_list')
	return render(request,'employee_website/employee_services/payroll/update_recoveries_editadd.html',{'form':form})
		
####
def EmployeePayrollProcessingUpdateRecoveriesUpdate(request,id=None):

	manageEmp = get_object_or_404(EmployeePayrollProcessingUpdateRecoveries,pk=id)
	form = EmployeePayrollProcessingUpdateRecoveriesAddForm(instance=manageEmp)
	
	if request.method=='POST':
		form = EmployeePayrollProcessingUpdateRecoveriesAddForm(request.POST,instance=manageEmp)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data uploaded Successfully.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
		else:
			messages.add_message(request, messages.ERROR, "Something went wrong.")
			return redirect('crm_crmemployee_manageemployee_salarydisbursement_list')
	return render(request,'employee_website/employee_services/payroll/update_recoveries_editadd.html',{'form':form})

	
	
#1
# Key Responsibility Areas & Targets
class AddEditKeyResponsibilityAreasUpdateTargetsKRATargetsView(View):
	template = 'employee_website/employee_services/kra_responsibility_areas_target/add_edit_update_kra_targets.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': KeyResponsibilityAreasTargetsUpdateKRATargetsForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		
		form = KeyResponsibilityAreasTargetsUpdateKRATargetsForm(request.POST)
		if form.is_valid():
			form = form.save()
			form.user_id = request.user.id
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('crm_employee_services_payroll_keyresponsibilityareas_update_kra')


class KeyResponsibilityAreasTargetsKRATargetsPerformanceListView(View):
	template = 'employee_website/employee_services/kra_responsibility_areas_target/kra_targets_performance_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# data_list = KeyResponsibilityAreasTargetsUpdateKRATargets.objects.filter(user_id__in = get_users)
	
		
		data_list = KeyResponsibilityAreasTargetsUpdateKRATargets.objects.all()

		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class KeyResponsibilityAreasTargetsKRATargetsPerformanceUpdateView(View):
	template = 'employee_website/employee_services/kra_responsibility_areas_target/add_edit_update_kra_targets.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': KeyResponsibilityAreasTargetsUpdateKRATargetsUpdateForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		data = get_object_or_404(KeyResponsibilityAreasTargetsUpdateKRATargets, pk = id)
		data.status = request.POST.get('status')
		data.kra_fulfilment = request.POST.get('kra_fulfilment')
		data.save()
		messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		return redirect('crm_employee_services_payroll_kra_target_performance_list')


class KeyResponsibilityAreasTargetsKRATargetsReviewListView(View):
	template = 'employee_website/employee_services/kra_responsibility_areas_target/kra_target_review_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		current_month = datetime.now().month
		# data_list = KeyResponsibilityAreasTargetsUpdateKRATargets.objects.filter(user_id__in = get_users)
		data_list = KeyResponsibilityAreasTargetsUpdateKRATargets.objects.all().order_by('-id')

		if str(request.GET.get('filter_type')) == "1":
			data_list = data_list.filter(month_and_year__month = current_month)
		elif str(request.GET.get('filter_type')) == "2":
			data_list = data_list.filter(month_and_year__month = current_month - 1)
	
		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class EmployeeExitEmployeeResignationLetterView(View):
	template = 'employee_website/employee_services/employee_exit/add_employee_resignation.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeExitEmployeeResignationForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		form = EmployeeExitEmployeeResignationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('employee_services_employee_resignation')


class EmployeeExitEmployeeResignationLetterListView(View):
	template = 'employee_website/employee_services/employee_exit/resignation_status_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# data_list = EmployeeExitEmployeeResignation.objects.filter(user_id__in = get_users)
		
		
		data_list = EmployeeExitEmployeeResignation.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class EmployeeExitEmployeeResignationLetterResignationStatusView(View):
	template = 'employee_website/employee_services/employee_exit/add_employee_resignation.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_data = get_object_or_404(EmployeeExitEmployeeResignation, pk = id)
		context = {
			'form': EmployeeExitEmployeeResignationUpdateStatusForm(instance = get_data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		get_data = get_object_or_404(EmployeeExitEmployeeResignation, pk = id)
		form = EmployeeExitEmployeeResignationUpdateStatusForm(request.POST, instance = get_data)
		if form.is_valid():
			data = form.save()
			if request.POST['status'] == '2':
				data.approved_date = datetime.now()
				data.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('employee_services_employee_resignation_list')


class EmployeeExitEmployeeEmployeeRelievingView(View):
	template = 'employee_website/employee_services/employee_exit/employee_relieving.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# data_list = EmployeeExitEmployeeResignation.objects.filter(user_id__in = get_users, status = 2)
		data_list = EmployeeExitEmployeeResignation.objects.filter( status = 5)

		

		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class EmployeeExitEmployeeResignationRelievingStatusView(View):
	template = 'employee_website/employee_services/employee_exit/add_employee_resignation.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_data = get_object_or_404(EmployeeExitEmployeeResignation, pk = id)
		context = {
			'form': EmployeeExitEmployeeRelievingUpdateStatusForm(instance = get_data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		get_data = get_object_or_404(EmployeeExitEmployeeResignation, pk = id)
		form = EmployeeExitEmployeeRelievingUpdateStatusForm(request.POST, instance = get_data)
		if form.is_valid():
			data = form.save()
			if request.POST['status'] == '2':
				data.approved_date = datetime.now()
				data.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('employee_services_employee_relieving_list')	


class EmployeeExitEmployeeFullandFinalSettlementListView(View):
	template = 'employee_website/employee_services/employee_exit/full_and_final_settlement_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# data_list = EmployeeExitEmployeeResignation.objects.filter(Q(status = 3) | Q(status = 5), user_id__in =get_users, )
		data_list = EmployeeExitEmployeeResignation.objects.filter( status = 3).order_by('-id')

		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class EmployeeExitEmployeeFullandFinalSettlementUpdateStatusView(View):
	template = 'employee_website/employee_services/employee_exit/add_employee_resignation.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_data = get_object_or_404(EmployeeExitEmployeeResignation, pk = id)
		context = {
			'form': EmployeeExitEmployeeFullandFinalSettlementUpdateStatusseForm(instance = get_data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		get_data = get_object_or_404(EmployeeExitEmployeeResignation, pk = id)
		form = EmployeeExitEmployeeFullandFinalSettlementUpdateStatusseForm(request.POST, instance = get_data)
		if form.is_valid():
			data = form.save()
			data.approved_date = datetime.now()
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('employee_services_employee_fullandfinalsettlement_list')


class WebsiteHolidaysListView(View):
    template = 'employee_website/employee_services/leaves/manage_manage_holidays_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('adminlogin')
        get_financial_year = ManageHolidays.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_financial_year, self.pagesize)
        context = {
        	'responselistquery': report_paginate
    	}
        return render(request, self.template, context)


class WebsiteAddUpdateHoliDaysView(View):
    template = 'employee_website/employee_services/leaves/add_manage_holidays.html'

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, holidaysdaysid = None):
        if not request.user.is_authenticated:
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
            'impace_on_salary':YESNO,
            'parent_company': CompanySetup.objects.filter(is_active = True).order_by('-id'),
            'head_offce': ManageHeadOfficeSetup.objects.filter(is_active = True).order_by('-id'),
            'branches': ManageBranch.objects.filter(is_active = True).order_by('-id'),
            'month_list' : Getmonthlist.month_list(),
            'year_list':Getyearlist.year_list()
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
        save_fina_year.year =  str(request.POST['holiday_year'])
        save_fina_year.month =  str(request.POST['holiday_month'])
        save_fina_year.company_id =  request.POST['parent_company']
        save_fina_year.head_office_id =  request.POST['head_offce']
        save_fina_year.date =  request.POST['holidays_date']
        save_fina_year.implact_on_salry =  request.POST['implact_on_salry']
        if 'is_active' in request.POST:
            save_fina_year.is_active =  True
        else:
            save_fina_year.is_active =  False
        save_fina_year.save()
        append_data = []
        if 'branches' in request.POST:
            for p in  dict(request.POST)['branches']:
            	if str(p) != "":
	                append_data.append(p)
	                try:
	                    saved_data = ManageHolidaysBranches.objects.get(holiday_id = save_fina_year.id, branch_id = p)
	                except ManageHolidaysBranches.DoesNotExist:
	                    saved_data = ManageHolidaysBranches()
	                    saved_data.holiday_id = save_fina_year.id
	                    saved_data.branch_id = p
	                    saved_data.save()
        ManageHolidaysBranches.objects.filter(~Q(branch_id__in = append_data), holiday_id = save_fina_year.id).delete()
        return redirect('website_list_holi_days_add')


class WebsiteHolidaysDeletView(View):
    def get(self, request, holidaysdaysid):
        if not request.user.is_authenticated:
            return redirect('adminlogin')
        get_report = ManageHolidays.objects.filter(id = holidaysdaysid).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('website_list_holi_days_add')


# Overtime
class OvertimeManagementUpdateOvertimeListView(View):
    template = 'employee_website/employee_services/over_time/update_over_time_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('adminlogin')
        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = OvertimeManagementUpdateOvertime.objects.filter( status = 1).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        	'responselistquery': report_paginate
    	}
        return render(request, self.template, context)

    def post(self, request):
        excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
        SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
        with open(excel_name_sheet,'r')as f:
            data = csv.reader(f)
            count = 0
            for row in data:
                if count !=0:
                    save_data = OvertimeManagementUpdateOvertime()
                    data_time = datetime.strptime(str(row[1]), "%d/%m/%y") 
                    save_data.user_id = row[0]
                    save_data.month_and_year_date = data_time.strftime("%Y-%m-%d")
                    save_data.overtime_start = row[2]
                    save_data.overtime_end = row[3]
                    save_data.total_hours = row[4]
                    save_data.reason = row[5]
                    save_data.save()
                count += 1
        messages.add_message(request, messages.SUCCESS, "Overtime uploaded successfully.")
        return redirect('website_edit_update_over_time_list')


###
class OvertimeManagementUpdateOvertimeAddView(View):
	template = 'employee_website/employee_services/over_time/update_over_time_add.html'
	def get(self,request):
		if not request.user.is_authenticated:
			return redirect('index')
		form = OvertimeManagementUpdateOvertimeForm()
		context={
			'form':form
		}
		return render(request,self.template,context)
	def post(self,request):
		if not request.user.is_authenticated:
			return redirect('index')
		if request.method=="POST":
			form = OvertimeManagementUpdateOvertimeForm(request.POST)
			if form.is_valid():
				form.save()
				
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('website_edit_update_over_time_list')

		

class OvertimeManagementUpdateOvertimeDeletView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('adminlogin')
        get_report = OvertimeManagementUpdateOvertime.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('website_edit_update_over_time_list')


class OvertimeManagementUpdateOvertimeStatusListView(View):
    template = 'employee_website/employee_services/over_time/update_over_time_status_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('adminlogin')
        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = OvertimeManagementUpdateOvertime.objects.all().order_by('-id')
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(added__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(month_and_year_date__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(month_and_year_date__month = previous_month).order_by('-id')
        
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        	'responselistquery': report_paginate
    	}
        return render(request, self.template, context)


class OvertimeManagementUpdateOvertimeStatusListViewUpdateStatusView(View):
	template = 'employee_website/employee_services/employee_exit/add_employee_resignation.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_data = get_object_or_404(OvertimeManagementUpdateOvertime, pk = id)
		context = {
			'form': OvertimeManagementUpdateOvertimeStatusListViewUpdateStatusViewForm(instance = get_data),
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		get_data = get_object_or_404(OvertimeManagementUpdateOvertime, pk = id)
		form = OvertimeManagementUpdateOvertimeStatusListViewUpdateStatusViewForm(request.POST, instance = get_data)
		if form.is_valid():
			data = form.save()
			
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('website_edit_update_over_time_list')


class TravelClaimManagementTravelConveyanceTravelRequestListView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/travel_request_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_data = TravelClaimManagementTravelConveyanceTravelRequest.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class TravelClaimManagementTravelConveyanceTravelRequestAddView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/add_travel_request.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		form = TravelClaimManagementTravelConveyanceTravelRequestForm
		context = {
			'form': form
		}
		return render(request, self.template, context)

	def post(self, request):
		if request.method=="POST":
			form = TravelClaimManagementTravelConveyanceTravelRequestForm(request.POST)
			if form.is_valid():
				data = form.save()
				# data.user_id = request.user.id
				# data.save()
				messages.add_message(request, messages.SUCCESS, "Data added successfully.")
			else:
				messages.add_message(request, messages.WARNING, "Data already exists.")
			return redirect('website_travel_request_list')
###

###
class TravelClaimManagementTravelConveyanceTravelRequestStatusView(View):
    template = 'employee_website/employee_services/claim_and_reimbursement/travel_request_status_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('adminlogin')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = TravelClaimManagementTravelConveyanceTravelRequest.objects.filter(status='Pending').order_by('-id')
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(added__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(added__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(added__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        	'responselistquery': report_paginate
    	}
        return render(request, self.template, context)
#1
###
class TravelClaimManagementTravelConveyanceTravelRequestStatusApprovedView(View):
    template = 'employee_website/employee_services/claim_and_reimbursement/travel_request_status_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('adminlogin')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = TravelClaimManagementTravelConveyanceTravelRequest.objects.filter(status='Approved').order_by('-id')
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(added__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(added__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(added__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        	'responselistquery': report_paginate
    	}
        return render(request, self.template, context)

#11
###
class TravelClaimManagementTravelConveyanceTravelRequestStatusRejectedView(View):
    template = 'employee_website/employee_services/claim_and_reimbursement/travel_request_status_list.html'
    pagesize = 10
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('adminlogin')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = TravelClaimManagementTravelConveyanceTravelRequest.objects.filter(status='Rejected').order_by('-id')
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(added__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(added__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(added__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        	'responselistquery': report_paginate
    	}
        return render(request, self.template, context)








class TravelClaimManagementTravelConveyanceTravelRequestUpdateStatusView(View):
	template = 'employee_website/employee_services/claim_and_reimbursement/add_travel_request.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		instance = get_object_or_404(TravelClaimManagementTravelConveyanceTravelRequest, pk = id)
		form = TravelClaimManagementTravelConveyanceTravelRequestUpdateForm(instance = instance)
		context = {
			'form': form
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		instance = get_object_or_404(TravelClaimManagementTravelConveyanceTravelRequest, pk = id)
		form = TravelClaimManagementTravelConveyanceTravelRequestUpdateForm(request.POST, instance = instance)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
		return redirect('website_travel_request_list')


# Employee Advances 
class EmployeeAdvancesSubmitAdvanceRequestView(View):
	template = 'employee_website/employee_services/employee_advances/add_update_form.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': EmployeeAdvancesSubmitAdvanceRequestForm,
			'frm': True
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if request.method=='POST':
			form = EmployeeAdvancesSubmitAdvanceRequestForm(request.POST,request.FILES)
			if form.is_valid():
				form.save()
			messages.add_message(request, messages.SUCCESS, "Data added successfully.")
			return redirect('website_travel_advance_request_submit_request')
			
		else:
			messages.add_message(request, messages.WARNING, "Data already exists.")
			return redirect('website_travel_advance_request_submit_request')


		# ids = [int(p.split('_')[2]) for p in request.POST if 'advance_type_' in p]
		# ids.sort()
		# for data in ids:
		# 	save_data = EmployeeAdvancesSubmitAdvanceRequest()
		# 	save_data.advance_type_1_id = request.POST.get('advance_type_'+str(data))
		# 	save_data.advance_amount_1 = request.POST.get('advance_amount_'+str(data))
		# 	save_data.recovery_start_from_1 = request.POST.get('recovery_start_from_'+str(data))
		# 	save_data.justification_1 = request.POST.get('justification_'+str(data))
		# 	save_data.recovery_period_1 = request.POST.get('recovery_period_'+str(data))
		# 	save_data.advance_approved_1 = request.POST.get('advance_approved_'+str(data))
		# 	save_data.user_id = request.user.id
		# 	save_data.save()
		return redirect('website_travel_advance_request_submit_request')


class EmployeeAdvancesSubmitAdvanceRequestListView(View):
	template = 'employee_website/employee_services/employee_advances/list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		data_list = EmployeeAdvancesSubmitAdvanceRequest.objects.all().order_by("-id")
		# data_list = EmployeeAdvancesSubmitAdvanceRequest.objects.filter(status='Processed').order_by("-id")
		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class EmployeeAdvancesSubmitAdvanceRequestUpdateView(View):
	template = 'employee_website/employee_services/employee_advances/add_update_form.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
		form=EmployeeAdvancesSubmitAdvanceRequestUpdateStatusForm()
		return render(request, self.template, {"form":form})

	def post(self, request, id = None):
		
	
		if request.method=="POST":
			data = ''
			instance = get_object_or_404(EmployeeAdvancesSubmitAdvanceRequest, pk = id)
			form = EmployeeAdvancesSubmitAdvanceRequestUpdateStatusForm(request.POST, instance = instance)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data added successfully.")
			else:
				messages.add_message(request, messages.WARNING, "Data already exists.")
			if data.status == "Processing":
				return redirect('website_travel_advance_request_status_list')
			elif data.status == "Processed":
				return redirect('website_travel_advance_request_processed_list')
			else:
				return redirect('website_travel_advance_request_processing_list')


class EmployeeAdvancesSubmitAdvanceRequestProcessingListView(View):
	template = 'employee_website/employee_services/employee_advances/list_processing_list.html'
	pagesize = 10

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		data_list = EmployeeAdvancesSubmitAdvanceRequest.objects.filter( status ="Processing")
		report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
		context = {
			'responselistquery': report_paginate,
		}
		return render(request, self.template, context)


class EmployeeAdvancesSubmitAdvanceRequestProcessedListView(View):
    template = 'employee_website/employee_services/employee_advances/request_processed_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_authenticated:
            return redirect('index')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = EmployeeAdvancesSubmitAdvanceRequest.objects.filter( status ="Processed")
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(added__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(added__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(added__month = previous_month).order_by('-id')

        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        'responselistquery': report_paginate,
        }
        return render(request, self.template, context)

##11
# # Incentive &  Bonus
class IncentiveBonusUpdateIncentiveBonusAddView(View):
	template = 'employee_website/employee_services/incentive_bonus/update_incentive_bonus.html'
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		form = EmployeeAdvanceSubmitIncentiveBonusForm()
		return render(request, self.template,{'form':form})
	def post(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		try:
			if 'upload_bulk_data' not in request.POST:
		
				form =EmployeeAdvanceSubmitIncentiveBonusForm(request.POST,request.FILES)
				if form.is_valid():
					form.save()
				messages.add_message(request, messages.SUCCESS, "Incentive bonus updated successfully.")
				return redirect('website_travel_incentive_bonus_add')
					
			else:
				excel_name_sheet = settings.MEDIA_URL+'upload_csv_file/'+ str(request.FILES['upload_bulk_data'])
				SaveCsvSheet.save_file(request, request.FILES['upload_bulk_data'], settings.MEDIA_URL + 'upload_csv_file')
				with open(excel_name_sexcel_name_sfilterheetfilterheet, 'r')as f:
					data = csv.reader(f)
					count = 0
					for row in data:
						if count !=0:
							try:
								save_data = EmployeeAdvancesSubmitIncentiveBonus()
								save_data.employee_id_id = row[0]
								save_data.incentive_type = row[1]
								save_data.incentive_period = row[2]
								save_data.incentive_amount = row[3]
								save_data.save()
							except:
								messages.add_message(request, messages.ERROR, "Something went wrong.")
								return redirect('crm_employee_services_payroll_update_advances_list')
						count +=1
			messages.add_message(request, messages.SUCCESS, "Incentive bonus updated successfully.")
			return redirect('website_travel_incentive_bonus_add')

		except:
			messages.add_message(request, messages.ERROR, " invalid data try again .")
			return redirect('website_travel_incentive_bonus_add')






class IncentiveBonusUpdateIncentiveBonusIncentiveBonusApprovalListView(View):
    template = 'employee_website/employee_services/incentive_bonus/incentive_bonus_approval_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_authenticated:
            return redirect('index')
        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        data_list = EmployeeAdvancesSubmitIncentiveBonus.objects.filter( status = "Pending").order_by("-id")
        report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
        context = {
            'responselistquery': report_paginate,
        }
        return render(request, self.template, context)

#11
class IncentiveBonusUpdateIncentiveBonusIncentiveBonusApprovalUpdateView(View):
	template = 'employee_website/employee_services/employee_advances/add_update_form.html'
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		instance = get_object_or_404(EmployeeAdvancesSubmitIncentiveBonus, pk = id)
		context = {
            'form': EmployeeAdvancesSubmitIncentiveBonusUpdateStatusForm(instance = instance),
        }
		return render(request, self.template, context)
	def post(self, request, id = None):
		data = ''
		
		instance =get_object_or_404(EmployeeAdvancesSubmitIncentiveBonus, pk=id)
		form = EmployeeAdvancesSubmitIncentiveBonusUpdateStatusForm(request.POST, instance = instance)
		if form.is_valid():
			form.save()
			messages.add_message(request,messages.SUCCESS,"Data added successfully")
			return redirect('website_travel_incentive_bonus_status_list')
		else:
			messages.add_message(request,messages.WARNING, "Data already exists")
		if data.status=="Pending":
			return redirect('website_travel_incentive_bonus_status_list')
		elif data.status=="Processing":
			return redirect('website_incentive_bonus_status_processing_list')
		elif data.status =="Processed":
			return redirect('website_incentive_bonus_status_processed_list')
		else:
			return redirect('website_travel_incentive_bonus_status_list')


	
   

class IncentiveBonusUpdateIncentiveBonusIncentiveBonusProcessingListView(View):
    template = 'employee_website/employee_services/incentive_bonus/incentive_bonus_processing_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_authenticated:
            return redirect('index')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        data_list = EmployeeAdvancesSubmitIncentiveBonus.objects.filter( status ="Processing").order_by("-id")
        report_paginate = CommonPagination.paginattion(request, data_list, self.pagesize)
        context = {
            'responselistquery': report_paginate,
        }
        return render(request, self.template, context)


class IncentiveBonusUpdateIncentiveBonusIncentiveBonusProcessedListView(View):
    template = 'employee_website/employee_services/incentive_bonus/incentive_bonus_processed_list.html'
    pagesize = 10

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_authenticated:
            return redirect('index')

        get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
        get_data = EmployeeAdvancesSubmitIncentiveBonus.objects.filter( status ="Processed").order_by("-id")
        filter_type = request.GET.get('filter')
        if str(filter_type) == "1":
            today = date.today()
            get_data = get_data.filter(updated__date = today).order_by('-id')
        elif str(filter_type) == "2":
            current_month = datetime.now().month
            get_data = get_data.filter(updated__month = current_month).order_by('-id')
        elif str(filter_type) == "3":
            previous_month = datetime.now().month - 1
            get_data = get_data.filter(updated__month = previous_month).order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
        context = {
        'responselistquery': report_paginate,
        }
        return render(request, self.template, context)


# WEBSITE >>>>>>>>>>>>>>>>> Knowledge and Training
class KnowledgeandTrainingUpdateDocumentsView(View):
	template = 'know_and_training/update_dcuments.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': KnowledgeandTrainingUpdateDocumentsForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if id is None:
			form = KnowledgeandTrainingUpdateDocumentsForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				data.user_id = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		else:
			data = get_object_or_404(KnowledgeandTrainingUpdateDocuments,  pk=id)
			form = KnowledgeandTrainingUpdateDocumentsForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, "Something went wrong.")
		return redirect('crm_knowledgeandtraining_update_documents_view')


class KnowledgeandTrainingUpdateTrainingView(View):
	template = 'know_and_training/update_training.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': CrmManageProductTrainingModelForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		form = CrmManageProductTrainingModelForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
		else:
			messages.add_message(request, messages.ERROR, form.errors)
		return redirect('crm_knowledgeandtraining_update_training_view')


class KnowledgeandTrainingUpdatePromotionsView(View):
	template = 'know_and_training/update_pramotion.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': CrmManageProductPromotionsModelForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		form = CrmManageProductPromotionsModelForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save()
			data.user_id = request.user.id
			data.save()
			messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
		else:
			messages.add_message(request, messages.ERROR, form.errors)
		return redirect('crm_knowledgeandtraining_update_promotions_view')


class KnowledgeandTrainingKnowledgeSharingView(View):
	template = 'know_and_training/knowledge_sharing.html'

	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		context = {
			'form': KnowledgeandTrainingKnowledgeSharingForm,
		}
		return render(request, self.template, context)

	def post(self, request, id = None):
		if id is None:
			form = KnowledgeandTrainingKnowledgeSharingForm(request.POST, request.FILES)
			if form.is_valid():
				data = form.save()
				data.user_id = request.user.id
				data.save()
				messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
			else:
				messages.add_message(request, messages.ERROR, form.errors)
		else:
			data = get_object_or_404(KnowledgeandTrainingKnowledgeSharing,  pk=id)
			form = KnowledgeandTrainingKnowledgeSharingForm(request.POST, request.FILES, instance = data)
			if form.is_valid():
				data = form.save()
				messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
			else:
				messages.add_message(request, messages.ERROR, form.errors)
		return redirect('crm_knowledgeandtraining_update_knowledge_sharing')


class KnowledgeandTrainingUpcomingTraningListView(View):
	template = 'know_and_training/up_coming_training_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = ManageKnowledgeProductTraining.objects.filter(user_id__in = get_users, is_active = True, start_date__gt = date.today()).order_by('-id')
		get_report = ManageKnowledgeProductTraining.objects.filter( is_active = True).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class KnowledgeandTrainingCurrentTraningListView(View):
	template = 'know_and_training/current_training_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = ManageKnowledgeProductTraining.objects.filter( is_active = True).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class KnowledgeandTrainingPastraningListView(View):
	template = 'know_and_training/past_traning_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = ManageKnowledgeProductTraining.objects.filter( is_active = True, training_calander = date.today()).order_by('-id')
		get_report = ManageKnowledgeProductTraining.objects.filter( is_active = True).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class KnowledgeandTrainingRequestReceivedForTrainignListView(View):
	template = 'know_and_training/request_received_for_traning_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_report = ManageProductTrainingSendWishToAttend.objects.filter(status = 1).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class KnowledgeandTrainingCurrentPromotionsListView(View):
	template = 'know_and_training/current_promotions_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		today_date =  date.today()
		get_report = ManageKnowledgeProductPromotions.objects.filter( is_active = True).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)
###update
class KnowledgeandTrainingCurrentPromotionsUpdateView(View):
	template= 'know_and_training/current_promotions_update.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store =True)
	def get(self,request,id=None):
		if not request.user.is_authenticated:
			return redirect('index')
		form = GetAndManageHierarchyOfEmployeeForm()
		context ={
			'form' :form
			
		}
		return render(request,self.template,context)
#!
#2
	def post(self,request, id):
		if not request.user.is_authenticated:
			return render('index')
		
		try:
			get_data = get_object_or_404(ManageKnowledgeProductPromotions, pk=id)
			form = GetAndManageHierarchyOfEmployeeForm(request.POST,instance= get_data)
			if form.is_valid():
				form.save()
				messages.add_message(request,messages.SUCCESS,"Data added successfully")
			else:
				messages.add_message(request,messages.WARNING,"Data already exists")
			return redirect('crm_knowledgeandtraining_update_current_promotions_list')
		
		except:
			messages.add_message(request,messages.WARNING,"Something went wrong.")
			return redirect('crm_knowledgeandtraining_update_current_promotions_list')



class KnowledgeandTrainingUpcomingPromotionsListView(View):
	template = 'know_and_training/up_coming_pramotions_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		today_date =  date.today()
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = ManageKnowledgeProductPromotions.objects.filter( is_active = True, start_date__gt = date.today()).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class KnowledgeandTrainingPastPromotionsListView(View):
	template = 'know_and_training/past_promotions_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		today_date =  date.today()
		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		# get_report = ManageKnowledgeProductPromotions.objects.filter(is_active = True, start_date__lt = date.today()).order_by('-id')
		get_report = ManageKnowledgeProductPromotions.objects.filter(is_active = True).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class TrainingAttendListView(View):
	template = 'know_and_training/traning_attend_list.html'
	pagesize = 10
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')

		get_users = GetAndManageHierarchyOfEmployee.Employee_list(request)
		get_report = ManageProductTrainingSendWishToAttend.objects.all().order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		context = {
			'responselistquery': report_paginate
		}
		return render(request, self.template, context)


class send_request_to_for_attend_traning(View):
    def post(self, request):
	    if not request.user.is_authenticated:
	        return redirect('index')
	    if request.is_ajax:
	        try:
	            get_report = ManageProductTrainingSendWishToAttend.objects.get(traning_id_id = request.POST['id'], user_id = request.user.id)
	            data = ''
	        except:
	            save_dat = ManageProductTrainingSendWishToAttend()
	            save_dat.traning_id_id = request.POST['id']
	            save_dat.user_id = request.user.id
	            save_dat.save()
	            data = '1'
	        return JsonResponse({'data': data})
	    else:
	        return redirect('index')


class ApprovalVacancies(View):
	
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id, stauts_id, menu_level):
		if not request.user.is_authenticated:
			return redirect('index')

		if int(menu_level) == 1:
			get_report = EmployeeServicesRecruitementCreateRequirement.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_website_employeeservices_recruitement_approvevacancies_list")
		elif int(menu_level) == 2:
			get_report = CrmUserLoginApiLogs.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_attendance_status")
		elif int(menu_level) == 3:
			get_report = OvertimeManagementUpdateOvertime.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("website_edit_update_over_time_status_list")
		elif int(menu_level) == 4:
			get_report = TravelClaimManagementTravelConveyanceTravelRequest.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
		elif int(menu_level) == 5:
			get_report = EmployeeClaimandReimbursementSubmitClaims.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_claimandreimbursement_claim_claimprocessed_list")
		elif int(menu_level) == 6:
			get_report = EmployeeClaimandReimbursementSubmitReimbursement.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_reimbursementprocessed_list")
		elif int(menu_level) == 7:
			get_report = EmployeeAdvancesSubmitAdvanceRequest.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("website_travel_advance_request_processed_list")
		elif int(menu_level) == 8:
			get_report = EmployeeAdvancesSubmitIncentiveBonus.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("website_incentive_bonus_status_processed_list")
		elif int(menu_level) == 9:
			get_report = EmployeeHRPoliciesUpdatePolicies.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_hrpolicies_upload_update_policies_list")
		elif int(menu_level) == 10:
			get_report = EmployeeHrPoliciesUpdateCirculars.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_hrpolicies_upload_update_circulars_list")
		elif int(menu_level) == 11:
			get_report = EmployeeHRPoliciesUpdateForm.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_hrpolicies_upload_update_forms_list")
		elif int(menu_level) == 12:
			get_report = CrmManageProductTraining.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_knowledgeandtraining_update_current_traning_list")
		elif int(menu_level) == 13:
			get_report = CrmManageProductPromotions.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_knowledgeandtraining_update_current_promotions_list")
		elif int(menu_level) == 14:
			get_report = PayrollStatutoryDeductions.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_crmemployee_manageemployee_statutorydeductions_list")
		elif int(menu_level) == 15:
			get_report = PayrollSalaryVoucher.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_crmemployee_manageemployee_salaryvoucher_list")
		elif int(menu_level) == 16:
			get_report = PayrollSalaryDisbursement.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_crmemployee_manageemployee_salarydisbursement_list")
		elif int(menu_level) == 17:
			get_report = EmployeePayrollProcessingUpdateRecoveries.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_payroll_update_recovery_list")
		elif int(menu_level) == 18:
			get_report = EmployeePayrollProcessingUpdateTaxDeclaration.objects.get(id = id)
			data_append = get_report.approval_level_all_status+','+stauts_id
			get_report.approval_level_all_status = data_append.lstrip(',')
			get_report.approval_level_id  = stauts_id
			get_report.save()
			return redirect("crm_employee_services_payroll_tax_declaration_list")


#######



class Datapost(View):
    template = 'employee_website/employee_services/recruitement/add_edit_create_requirement.html'

    def get(self,request):
        form = EmployeeServicesRecruitementPublishVacanciesForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request):
        form = EmployeeServicesRecruitementPublishVacanciesForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('crm_website_employeeservices_recruitement_publishvacancies_update')

class Datapost1(View):
    template = 'employee_website/employee_services/recruitement/add_edit_create_requirement.html'

    def get(self,request):
        form = EmployeeServicesRecruitementInviteResumeAddForm1()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request):

        form = EmployeeServicesRecruitementInviteResumeAddForm1(request.POST, request.FILES)
		
        if form.is_valid(): 
			           
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('crm_website_employeeservices_recruitement_publishvacancies_update')

###

##
class EmployeeHolidaysAndLeavesList(View):
    template = 'employee_website/employee_services/leaves/manage_manage_holidays_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageHolidays.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        return render(request, self.template,{'responselistquery': report_paginate})


class AddEmployeeHolidaysAndLeaves(View):
    template = 'employee_website/employee_services/leaves/add_manage_holidays_leaves.html'
    
    def get(self,request):
        form = ManageHolidaysForm()
        context = {'form': form}
        return render(request, self.template, context)            


    def post(self, request, branch_id = None):
        form = ManageHolidaysForm(request.POST, request.FILES)
        if form.is_valid():             
            messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
            form.save()   
        else:
            messages.add_message(request, messages.WARNING,('Data already exists!!'))
        return redirect('EmployeeHolidaysAndLeaveslist')

def AddEditEmployeeHolidaysAndLeaves(request, id):

    manageproduct = get_object_or_404(ManageHolidays, pk=id)
    if request.method == "POST":
        form =ManageHolidaysForm(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('EmployeeHolidaysAndLeaveslist')
    else:
        form = ManageHolidaysForm(instance=manageproduct)
    return render(request,  'employee_website/employee_services/leaves/add_manage_holidays_leaves.html', {'form': form})


class EmployeeHolidaysAndLeavesDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageHolidays.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('EmployeeHolidaysAndLeaveslist')


# payroll_processed_list.html
       
def EmployeePayrollProcessedAddView(request):

	form = EmployeePayrollProcessedForm()
	if request.method=="POST":
		form = EmployeePayrollProcessedForm(request.POST)
		print(form.errors)
		if form.is_valid(): 
			form.save() 
			print(form)           
			messages.add_message(request, messages.SUCCESS,('Successfully added!! ')) 
			return redirect('crm_crmemployee_manageemployee_payrollprocessed_add')   
		else:
			messages.add_message(request, messages.WARNING,('Invalid Data !!'))
			return redirect('crm_crmemployee_manageemployee_payrollprocessed_add') 
	return render(request,'employee_website/employee_services/payroll/payroll_processed_add.html',{'form':form})

##
##
##
##

class EmployeePayrollProcessedListView(View):
	template = 'employee_website/employee_services/payroll/payroll_processed_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		# if not request.user.is_authenticated:
		# 	return redirect('index')

		
		# get_bank = EmployeeRegistrationUpdateBankDetails.objects.all().order_by('-id')[:1]
		# get_data = UserLoginApiLogs.objects.filter(status='Approved').order_by('-id')
		# filter_type = request.GET.get('filter')
		# if str(filter_type) == "1":
		# 	today = date.today()
		# 	get_data = get_data.filter(date_of_payment = today).order_by('-id')
		# elif str(filter_type) == "2":
		# 	current_month = datetime.now().month
		# 	get_data = get_data.filter(date_of_payment = current_month).order_by('-id')
		# elif str(filter_type) == "3":
		# 	previous_month = datetime.now().month - 1
		# 	get_data = get_data.filter(date_of_payment = previous_month).order_by('-id')
		# report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
		# context = {
        #     'responselistquery': report_paginate,
		# 	'get_bank':get_bank,
		# 	}
		# return render(request, self.template,context)
		get_all_user_ids = UserLoginApiLogs.objects.filter(attendance_status=2).order_by("-id")
		
		get_all_data  = ManageWorkingDays.objects.all().order_by('-id')  
		get_financial_year = ManageHolidays.objects.all().order_by('-id')
		get_leave_type = HolidaysandLeavesLeaveType.objects.all().order_by('-id')
		get_claim_type = ManageClaimType.objects.all().order_by('-id')
		get_reimbursement = ManageReimbursement.objects.all().order_by('-id')
		get_incentive = EmployeeAdvancesSubmitIncentiveBonus.objects.all().order_by('-id')[:1]
		get_bank = EmployeeRegistrationUpdateBankDetails.objects.all().order_by('-id')[:1]
		get_pancard = EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.all().order_by('-id')[:1]
		# get_processing = EmployeePayrollProcessed.objects.all().order_by('-id')[:1]
		

		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'get_all_data':get_all_data,
			'get_financial_year':get_financial_year,
			'stauts': ATTENDENCE_STATUS,
			'get_leave_type':get_leave_type,
			'get_claim_type':get_claim_type,
			'get_reimbursement':get_reimbursement,
			'get_incentive':get_incentive,
			'get_bank':get_bank,
			'get_pancard':get_pancard,
			# 'get_processing':get_processing,

			# 'get_monthly_holidays_days':get_monthly_holidays_days,
		
		}
		return render(request, self.template,context)



class EmployeePayrollProcessedPendingListView(View):
	template = 'employee_website/employee_services/payroll/payroll_processed_pending_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('index')
		
		get_data = EmployeePayrollProcessed.objects.all().order_by('-id')
		filter_type = request.GET.get('filter')
		if str(filter_type) == "1":
			today = date.today()
			get_data = get_data.filter(date_of_payment = today).order_by('-id')
		elif str(filter_type) == "2":
			current_month = datetime.now().month
			get_data = get_data.filter(date_of_payment = current_month).order_by('-id')
		elif str(filter_type) == "3":
			previous_month = datetime.now().month - 1
			get_data = get_data.filter(date_of_payment = previous_month).order_by('-id')
		report_paginate = CommonPagination.paginattion(request, get_data, self.pagesize)
		context = {
            'responselistquery': report_paginate
			}
		return render(request, self.template, context)


def EmployeePayrollProcessedListViewUpdate(request, id):

    manageproduct = get_object_or_404(EmployeePayrollProcessed, pk=id)
    if request.method == "POST":
        form =EmployeePayrollProcessedFormUpdate(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('crm_crmemployee_manageemployee_payrollprocessed_list')
    else:
        form = EmployeePayrollProcessedFormUpdate(instance=manageproduct)
    return render(request,  'employee_website/employee_services/payroll/payroll_processed_update.html',{'form':form})


class EmployeePayrollProcessedListViewDelete(View):
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = EmployeePayrollProcessed.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_manageemployee_payrollprocessed_list')
###
class EmployeePayrollstatusListView(View):
	template = 'employee_website/employee_services/payroll/payroll_status_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request):
		if not request.user.is_superuser:
			return redirect('adminlogin')
		# get_report = EmployeePayrollProcessed.objects.all().order_by('-id')
		
		# report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		# get_current_month = date.today().month
		# get_all_user_ids = UserLoginApiLogs.objects.filter(attendance_status=2).order_by("-id")
		
		# get_all_data  = ManageWorkingDays.objects.all().order_by('-id')  
		# get_financial_year = ManageHolidays.objects.all().order_by('-id')
		# get_leave_type = HolidaysandLeavesLeaveType.objects.all().order_by('-id')
		# get_claim_type = EmployeeClaimandReimbursementSubmitClaims.objects.all().order_by('-id')
		# get_reimbursement = ManageReimbursement.objects.all().order_by('-id')
		# get_incentive = EmployeeAdvancesSubmitIncentiveBonus.objects.all().order_by('-id')[:1]
		# get_bank = EmployeeRegistrationUpdateBankDetails.objects.all().order_by('-id')[:1]
		
		
		
	
		# report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		# context = {
		# 	'responselistquery': report_paginate,
		# 	'get_all_data':get_all_data,
		# 	'get_financial_year':get_financial_year,
		# 	'stauts': ATTENDENCE_STATUS,
		# 	'get_leave_type':get_leave_type,
		# 	'get_claim_type':get_claim_type,
		# 	'get_reimbursement':get_reimbursement,
		# 	'get_incentive':get_incentive,
		# 	'get_bank':get_bank,
			
		# 	# 'get_monthly_holidays_days':get_monthly_holidays_days,
		# }
		# return render(request, self.template,context)
		get_all_user_ids = UserLoginApiLogs.objects.all().order_by("-id")
		
		get_all_data  = ManageWorkingDays.objects.all().order_by('-id')  
		get_financial_year = ManageHolidays.objects.all().order_by('-id')
		get_leave_type = HolidaysandLeavesLeaveType.objects.all().order_by('-id')
		get_claim_type = ManageClaimType.objects.all().order_by('-id')
		get_reimbursement = ManageReimbursement.objects.all().order_by('-id')
		get_incentive = EmployeeAdvancesSubmitIncentiveBonus.objects.all().order_by('-id')[:1]
		get_bank = EmployeeRegistrationUpdateBankDetails.objects.all().order_by('-id')[:1]
		get_pancard = EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.all().order_by('-id')[:1]
		# get_processing = EmployeePayrollProcessed.objects.all().order_by('-id')[:1]
		

		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'get_all_data':get_all_data,
			'get_financial_year':get_financial_year,
			'stauts': ATTENDENCE_STATUS,
			'get_leave_type':get_leave_type,
			'get_claim_type':get_claim_type,
			'get_reimbursement':get_reimbursement,
			'get_incentive':get_incentive,
			'get_bank':get_bank,
			'get_pancard':get_pancard,
			# 'get_processing':get_processing,

			# 'get_monthly_holidays_days':get_monthly_holidays_days,
		
		}
		return render(request, self.template,context)



class EmployeePayrollProcessingListView(View):
	template = 'employee_website/employee_services/payroll/payroll_processing_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request, id = None):
		if not request.user.is_authenticated:
			return redirect('index')
		
		get_all_user_ids = UserLoginApiLogs.objects.filter(attendance_status=2).order_by("-id")
		location = request.GET.get('location')
		month_and_year = request.GET.get('login_time')
		if  location != None and str(location) != "":
			get_all_user_ids = get_all_user_ids.filter(location=str(location).strip())
			
		if month_and_year != None and str(month_and_year) != "":
			get_all_user_ids = get_all_user_ids.filter(month_and_year =str(month_and_year).strip())
		
		
		get_all_user_ids = UserLoginApiLogs.objects.filter(attendance_status=2).order_by("-id")
		
		get_all_data  = ManageWorkingDays.objects.all().order_by('-id')  
		get_financial_year = ManageHolidays.objects.all().order_by('-id')
		get_leave_type = HolidaysandLeavesLeaveType.objects.all().order_by('-id')
		get_claim_type = ManageClaimType.objects.all().order_by('-id')
		get_reimbursement = ManageReimbursement.objects.all().order_by('-id')
		get_incentive = EmployeeAdvancesSubmitIncentiveBonus.objects.all().order_by('-id')[:1]
		get_bank = EmployeeRegistrationUpdateBankDetails.objects.all().order_by('-id')[:1]
		get_pancard = EmployeeRegistrationUpdateRegistrationPersonalDetails.objects.all().order_by('-id')[:1]
		
		get_amount_offer = EmployeeRegistrationUpdateSalaryStructutre.objects.all().order_by('-id')[:1]
		
		print(get_amount_offer)
		get_processing = EmployeePayrollProcessed.objects.all().order_by('-id')[:1]
		

		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'get_all_data':get_all_data,
			'get_financial_year':get_financial_year,
			'stauts': ATTENDENCE_STATUS,
			'get_leave_type':get_leave_type,
			'get_claim_type':get_claim_type,
			'get_reimbursement':get_reimbursement,
			# 'get_incentive':get_incentive,
			'get_bank':get_bank,
			# 'get_pancard':get_pancard,
			# 'get_amount_offer':get_amount_offer,

			'get_processing':get_processing,

			# 'get_monthly_holidays_days':get_monthly_holidays_days,
		
		}
		return render(request, self.template,context)





def EmployeePayrollStatusListViewUpdate(request, id):

    manageproduct = get_object_or_404(EmployeePayrollProcessed, pk=id)
    if request.method == "POST":
        form =EmployeePayrollProcessedFormUpdate(request.POST, instance=manageproduct)
        if form.is_valid():
            form.save()
            return redirect('crm_crmemployee_manageemployee_payrollprocessed_list')
    else:
        form = EmployeePayrollProcessedFormUpdate(instance=manageproduct)
    return render(request,  'employee_website/employee_services/payroll/payroll_processed_update.html',{'form':form})

def EmployeesalarySlipAddView(request):
	form = EmployeesalarySlipForm()
	if request.method=='POST':
		form = EmployeesalarySlipForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('EmployeePayrollSlipListView')
		 


class EmployeePayrollSlipListView(View):
	template = 'employee_website/employee_services/payroll/payroll_salary_slip_list.html'
	pagesize = 10
	@cache_control(no_cache=True, must_revalidate=True, no_store=True)
	def get(self, request,id=None):
		if not request.user.is_superuser:
			return redirect('adminlogin')
		# get_report = EmployeePayrollProcessed.objects.filter(id=id)
		# get_report2= CompanySetup.objects.all().order_by('-id')[:1]
		# get_report3= ManageSalary.objects.all().order_by('-id')[:1]
		
		# report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
		# return render(request, self.template,{'responselistquery': report_paginate ,'get_report2':get_report2,'get_report3':get_report3})
		get_current_month = date.today().month
		get_all_user_ids = UserLoginApiLogs.objects.filter(attendance_status=2).order_by("-id")
		get_bank = EmployeeRegistrationUpdateBankDetails.objects.all().order_by('-id')[:1]
		get_report2= CompanySetup.objects.all().order_by('-id')[:1]
		get_report3= ManageSalary.objects.all().order_by('-id')[:1]
		get_all_data  = ManageWorkingDays.objects.all().order_by('-id')
		get_financial_year = ManageHolidays.objects.all().order_by('-id')
	
		report_paginate = CommonPagination.paginattion(request, get_all_user_ids, self.pagesize)
		context = {
			'responselistquery': report_paginate,
			'get_all_data':get_all_data,
			'get_financial_year':get_financial_year,
			'stauts': ATTENDENCE_STATUS,
			'get_report2':get_report2,			
			'get_report3':get_report3,
			'get_bank':get_bank,
			# 'get_monthly_holidays_days':get_monthly_holidays_days,
		}
		return render(request, self.template, context)