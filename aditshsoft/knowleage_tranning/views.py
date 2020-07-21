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
from aditshsoft.common import CommonPagination
from aditshsoft.common import Getmonthlist, SiteUrl
from aditshsoft.common import Getyearlist, time_slots, Getyearlist1
from hrms_management.models import *
from admin_main.models import *
from hrms_management.forms import *
from knowleage_tranning.forms import *


# 1
class CrmKnowledgeandTrainingDefineKnowledgeTypeList(View):
    template = 'admin_template/knowledge_training/define_knowledge_type_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandTrainingDefineKnowledgeType(View):
    template = 'admin_template/knowledge_training/add_edit_define_knowledge_type.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmDefineKnowledgeTypeModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeType, pk=id)
            form = CrmDefineKnowledgeTypeModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmDefineKnowledgeTypeModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeType, pk=id)
            form = CrmDefineKnowledgeTypeModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_knowledgetype_list')


class CrmKnowledgeandTrainingDefineKnowledgeTypeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_knowledgetype_list')


# 2
class CrmKnowledgeandTrainingDefineKnowledgeLevelList(View):
    template = 'admin_template/knowledge_training/define_knowledge_level_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeLevel.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandTrainingDefineKnowledgeLevel(View):
    template = 'admin_template/knowledge_training/add_edit_define_knowledge_level.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmDefineKnowledgeLevelModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeLevel, pk=id)
            form = CrmDefineKnowledgeLevelModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmDefineKnowledgeLevelModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeLevel, pk=id)
            form = CrmDefineKnowledgeLevelModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_defineknowledgelevel_list')


class CrmKnowledgeandTrainingDefineKnowledgeLevelDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeLevel.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_defineknowledgelevel_list')


# 3
class CrmKnowledgeandTrainingManageKnowledgeList(View):
    template = 'admin_template/knowledge_training/manage_knowledge_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeTraningWithType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandTrainingManageKnowledge(View):
    template = 'admin_template/knowledge_training/add_edit_manage_knowledge.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmManageKnowledgeModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeTraningWithType, pk=id)
            form = CrmManageKnowledgeModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        
        if id is None:
            form = CrmManageKnowledgeModelForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeTraningWithType, pk=id)
            form = CrmManageKnowledgeModelForm(request.POST, request.FILES, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_manageknowledge_list')


class CrmKnowledgeandTrainingManageKnowledgeDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeTraningWithType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_manageknowledge_list')


# 4
class CrmKnowledgeandTrainingDefineProductTainingList(View):
    template = 'admin_template/knowledge_training/define_product_training_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductTrainingType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandTrainingDefineProductTaining(View):
    template = 'admin_template/knowledge_training/add_edit_define_product_training.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmDefineProductTainingModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeProductTrainingType, pk=id)
            form = CrmDefineProductTainingModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmDefineProductTainingModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeProductTrainingType, pk=id)
            form = CrmDefineProductTainingModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_defineproductraining_list')


class CrmKnowledgeandTrainingDefineProductTainingDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductTrainingType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_defineproductraining_list')


# 5
class CrmKnowledgeandTrainingManageProductTrainingList(View):
    template = 'admin_template/knowledge_training/manage_product_training_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductTraining.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandTrainingManageProductTraining(View):
    template = 'admin_template/knowledge_training/add_edit_manage_product_training.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmManageProductTrainingModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeProductTraining, pk=id)
            form = CrmManageProductTrainingModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmManageProductTrainingModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeProductTraining, pk=id)
            form = CrmManageProductTrainingModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_manageproducttraining_list')


class CrmKnowledgeandTrainingManageProductTrainingDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductTraining.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_manageproducttraining_list')


# 6
class CrmKnowledgeandTrainingDefineProductPromotionsList(View):
    template = 'admin_template/knowledge_training/define_product_promotions_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductPromotionType.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandTrainingDefineProductPromotions(View):
    template = 'admin_template/knowledge_training/add_edit_define_product_promotions.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmDefineProductPromotionsModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeProductPromotionType, pk=id)
            form = CrmDefineProductPromotionsModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmDefineProductPromotionsModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeProductPromotionType, pk=id)
            form = CrmDefineProductPromotionsModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_defineproductpromotions_list')


class CrmKnowledgeandTrainingDefineProductPromotionsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductPromotionType.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_defineproductpromotions_list')


# 7
class CrmKnowledgeandTrainingManageProductPromotionsList(View):
    template = 'admin_template/knowledge_training/maange_product_promotions_list.html'
    pagesize = 10
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductPromotions.objects.all().order_by('-id')
        report_paginate = CommonPagination.paginattion(request, get_report, self.pagesize)
        context = {
            'responselistquery': report_paginate
        }
        return render(request, self.template, context)


class CrmAddEditCrmKnowledgeandManageProductPromotions(View):
    template = 'admin_template/knowledge_training/add_edit_maange_product_promotions.html'
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, id = None):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        if id is None:
            form = CrmManageProductPromotionsModelForm()
        else:
            data = get_object_or_404(ManageKnowledgeProductPromotions, pk=id)
            form = CrmManageProductPromotionsModelForm(instance=data)
        context = {
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request, id = None):
        if id is None:
            form = CrmManageProductPromotionsModelForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data added Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        else:
            data = get_object_or_404(ManageKnowledgeProductPromotions, pk=id)
            form = CrmManageProductPromotionsModelForm(request.POST, instance = data)
            if form.is_valid():
                data = form.save()
                messages.add_message(request, messages.SUCCESS, "Data updated Successfully.")
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong.")
        return redirect('crm_crmemployee_knowledgetraining_manageproductpromotions_list')


class CrmKnowledgeandTrainingManageProductPromotionsDelete(View):
    
    def get(self, request, id):
        if not request.user.is_superuser:
            return redirect('adminlogin')
        get_report = ManageKnowledgeProductPromotions.objects.filter(id = id).delete()
        messages.add_message(request, messages.SUCCESS, "Data deleted Successfully.")
        return redirect('crm_crmemployee_knowledgetraining_manageproductpromotions_list')