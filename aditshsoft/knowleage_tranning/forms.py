from django import forms
from knowleage_tranning.models import *
from hrms_management.forms import *


class CrmDefineKnowledgeTypeModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageKnowledgeType
        fields = ('knowledge_type', 'description', 'start_date', 'is_active')
        widgets = {
            'knowledge_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmDefineKnowledgeLevelModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageKnowledgeLevel
        fields = ('knowledge_level', 'description', 'start_date', 'is_active')
        widgets = {
            'knowledge_level': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmManageKnowledgeModelForm(forms.ModelForm):
    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageKnowledgeTraningWithType
        fields = ('knowledge_type', 'knowledge_level', 'knowledge_name', 'upload_documents','start_date', 'is_active')
        widgets = {
            'knowledge_type': forms.Select(attrs={'class': 'form-control'}),
            'knowledge_level': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'knowledge_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmDefineProductTainingModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageKnowledgeProductTrainingType
        fields = ('product', 'training_type', 'nature_of_training','training_name', 'purpose', 'start_date', 'is_active')
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'training_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'nature_of_training': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'training_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmManageProductTrainingModelForm(forms.ModelForm):
    class Meta:
        model = ManageKnowledgeProductTraining
        fields = ('location', 'department', 'designation','product', 'training_type', 'nature_of_training', 'training_name' ,'purpose_of_training', 'max_no_of_participant', 'faculty', 'venue_of_training', 'training_calander' ,'start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'product': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'training_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'nature_of_training': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'training_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'purpose_of_training': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'max_no_of_participant': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'venue_of_training': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'training_calander': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date", 'id':""}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date", 'id':""}),
        }


class CrmDefineProductPromotionsModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageKnowledgeProductPromotionType
        fields = ('promotion_type', 'details_of_promotion', 'start_date', 'is_active')
        widgets = {
            'promotion_type': forms.TextInput(attrs={'class': 'form-control'}),
            'details_of_promotion': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmManageProductPromotionsModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageKnowledgeProductPromotions
        fields = ('location', 'product', 'promotion_type', 'details_of_promotion', 'applicable_to', 'purpose_of_promotion', 'promotion_period', 'start_date','approval_level')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'promotion_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'details_of_promotion': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'applicable_to': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'purpose_of_promotion': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'promotion_period': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'approval_level': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
class GetAndManageHierarchyOfEmployeeForm(forms.ModelForm):
   
    class Meta:
        model = ManageKnowledgeProductPromotions
        fields = ( 'approval_level',)
        widgets = {
            
            'approval_level': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }