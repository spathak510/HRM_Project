from django import forms
from hrms_employees.models import *
from hrms_management.forms import *


class CustomEmployeeGrade(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.hod_id)

class EmployeeServiceEmployeeReportingStructureForm(forms.ModelForm):
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageEmployeeReportingStructure
        fields = ('department', 'designation','responsibilities','role', 'reporting_to', 'start_date', 'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'role': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'reporting_to': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class EmployeeIDForm(forms.ModelForm):
    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'
    # employee_id = CustomHeadOffice(queryset=ManageHeadOfficeSetup.objects.filter(is_active=1))
    # employee_id.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageEmployeeId
        fields = ('employee_id', 'description', 'is_active')
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManageGradeForm(forms.ModelForm):
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = ManageGrade
        fields = ('grade_type', 'designation' , 'description', 'is_active')
        widgets = {
            'grade_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class ManageSalaryRangeForm(forms.ModelForm):
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'

    
    class Meta:
        model = ManageSalaryRange
        fields = ('grade', 'designation' ,'start_salary', 'maximum_salary' ,'description', 'is_active')
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'start_salary': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum_salary': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class DefineSalaryForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageSalary
        fields = ('salary_code', 'salary_type', 'salary_frequency', 'measurement', 'taxablility', 'display_type', 'limit', 'start_date','description', 'is_active')
        widgets = {
            'salary_code': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_type': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'measurement': forms.TextInput(attrs={'class': 'form-control'}),
            'taxablility': forms.TextInput(attrs={'class': 'form-control'}),
            'display_type': forms.TextInput(attrs={'class': 'form-control'}),
            'limit': forms.TextInput(attrs={'class': 'form-control', 'type':'number', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }
##
class DefineDeductionsModelForm(forms.ModelForm):
    class Meta:
        model = ManageDeductionsStructure
        fields = ('deduction_category', 'deduction_type', 'deduction_name', 'deduction_amount', 'unit_value', 'frequency', 'basis_of_calculation', 'minimum','maximum', 'part_of_ctc', 'deduction_from_payroll')
        widgets = {
            'deduction_category': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_type': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_name': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_amount': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'unit_value': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'basis_of_calculation': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'minimum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'part_of_ctc': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'deduction_from_payroll': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }


class DefineOtherIncomeForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageOtherIncome
        fields = ('income_type', 'description',  'start_date', 'is_active')
        widgets = {
            'income_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class ManageLanguageForm(forms.ModelForm):
    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageLanguage
        fields = ('language', 'description', 'is_active')
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class ManageQualificationForm(forms.ModelForm):
    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageQualification
        fields = ('type_of_qualification', 'qualification', 'description', 'is_active')
        widgets = {
            'type_of_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class ManageExpereinceForm(forms.ModelForm):

    # start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageExpereince
        fields = ('experience_type', 'experience', 'unit_value', 'description', 'is_active')
        widgets = {
            'experience_type': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_value': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class ManageFamilyForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageFamily
        fields = ('relationship', 'description', 'start_date', 'is_active')
        widgets = {
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

# Manage Pay Roll
class ManagePayRollDefineTaxStructureModelForm(forms.ModelForm):


    class Meta:
        model = ManagePayRollTaxStructure
        fields = ('assessment_year','tax_type', 'minimum', 'maximum', 'tax_rate', 'cess_type', 'cess_rate', 'surcharge_rate', 'start_date', 'end_date' ,'description', 'is_active')
        widgets = {
            'assessment_year': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'minimum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'tax_rate': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'cess_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'cess_rate': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'surcharge_rate': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date", 'id':""}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date", 'id':""}),
        }


class ManagePayRollDefineReimbursementModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManagePayRollReimbursement
        fields = ('reimbursement_type', 'reimbursement_name', 'applicable_to', 'impact_on_tax','part_of_salary', 'description', 'start_date', 'is_active')
        widgets = {
            'reimbursement_type': forms.TextInput(attrs={'class': 'form-control'}),
            'reimbursement_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'applicable_to': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'impact_on_tax': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'part_of_salary': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManagePayRollDefineExemptedIncomeModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    end_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManagePayRollExemptedIncome
        fields = ('income_type','provision_of_tax_rules', 'maximum_limit', 'criteria',  'start_date', 'end_date', 'description', 'is_active')
        widgets = {
            'income_type': forms.Select(attrs={'class': 'form-control'}),
            'provision_of_tax_rules': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_limit': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number' }),
            'criteria': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class ManagePayRollDefineStatutoryDeductionsModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    end_date.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManagePayRollStatutoryDeductions
        fields = ('deduction_type', 'provision_of_rules', 'salary_code', 'minimum', 'maximum', 'employee_contribution', 'admin_charges', 'part_of_ctc', 'part_of_taxable_perquisite', 'start_date', 'end_date', 'description', 'is_active')
        widgets = {
            'deduction_type': forms.TextInput(attrs={'class': 'form-control'}),
            'provision_of_rules': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'salary_code': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'minimum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'employee_contribution': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'admin_charges': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'part_of_ctc': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'part_of_taxable_perquisite': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManagePayRollDefineAdvancesModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    end_date.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'


    class Meta:
        model = ManagePayRollDefineAdvances
        fields = ('advance_type', 'minimum_limit', 'maximum_limit', 'location', 'department', 'grades', 'base_rate', 'interest_rate', 'part_of_ctc', 'taxable', 'start_date', 'end_date', 'description', 'is_active')
        widgets = {
            'advance_type': forms.TextInput(attrs={'class': 'form-control'}),
            'minimum_limit': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum_limit': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'grades': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'base_rate': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'interest_rate': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'part_of_ctc': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'taxable': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

class ManagePayRollDefineDeductionsModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManagePayRollDeductions
        fields = ('deduction_type', 'nature_of_deduction', 'tax_exempted', 'grade', 'department','minimum', 'maximum', 'description','start_date', 'is_active')
        widgets = {
            'deduction_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'nature_of_deduction': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'tax_exempted': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'minimum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

# Holidays and Leaves
class HolidaysandLeavesDefineLeaveTypeModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'


    class Meta:
        model = HolidaysandLeavesLeaveType
        fields = ('short_name', 'leave_name', 'leave_type', 'applicable_to', 'impact_on_salary', 'start_date', 'is_active')
        widgets = {
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'leave_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'leave_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'applicable_to': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'impact_on_salary': forms.Select(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
        }


class HolidaysandLeavesManageLeaveQoutaModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'


    class Meta:
        model = HolidaysandLeavesManageLeaveQouta
        fields = ('short_name', 'leave_name', 'leave_type', 'applicable_to', 'start_month', 'end_month', 'maximum_leave_qouta' ,'impact_on_salary', 'permission_required', 'authority', 'carried_forward', 'start_date','description', 'is_active')
        widgets = {
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'leave_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'leave_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'applicable_to': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_month': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'end_month': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'maximum_leave_qouta': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'impact_on_salary': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'permission_required': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'authority': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'carried_forward': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManageClaimsDefineClaimTypeModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'


    class Meta:
        model = ManageClaimType
        fields = ('claim_type', 'start_date', 'is_active')
        widgets = {
            'claim_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManageClaimsDefineClaimEntitlementModelForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageClaimsClaimEntitlement
        fields = ('grade', 'location', 'department', 'designation', 'claim_type' ,'claim_limit', 'start_date', 'end_date' ,'is_active')
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'claim_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'claim_limit': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }

# Travel
class TravelandClaimTravelManagementDefineModeofTravelForm(forms.ModelForm):
    class Meta:
        model = TravelandClaimTravelManagementModeofTravel
        fields = ('mode_of_travel', 'description' ,'start_date', 'is_active')
        widgets = {
            'mode_of_travel': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type' :"date", 'id':""}),
        }

class TravelandClaimTravelManagementDefineTravelTypeForm(forms.ModelForm):
    class Meta:
        model = TravelandClaimTravelManagementTravelType
        fields = ('travel_type', 'description' ,'start_date', 'is_active')
        widgets = {
            'travel_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type' :"date", 'id':""}),
        }

class TravelandClaimTravelManagementDefineTravelPolicyForm(forms.ModelForm):
    class Meta:
        model = TravelandClaimTravelManagementTravelPolicy
        fields = ('policy_name','mode_of_travel', 'travel_type' ,'description' ,'start_date', 'is_active')
        widgets = {
            'policy_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'mode_of_travel': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'travel_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type' :"date", 'id':""}),
        }

class TravelandClaimTravelManagementManageTravelForm(forms.ModelForm):
    class Meta:
        model = TravelandClaimTravelManagementManageTravel
        fields = ('policy_name','travel_name', 'entitlement', 'maximum_limit' ,'description' ,'start_date', 'is_active')
        widgets = {
            'policy_name': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'travel_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'entitlement': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_limit': forms.TextInput(attrs={'class': 'form-control', 'required':'','type': "number"}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type' :"date", 'id':""}),
        }

# Manage Reimbursement 
class ManageReimbursementDefineReimbursementModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'


    class Meta:
        model = ManageReimbursement
        fields = ('reimbursement_type', 'start_date', 'is_active')
        widgets = {
            'reimbursement_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManageReimbursementReimbursementEntitilementModelForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageReimbursementReimbursementEntitilement
        fields = ('grade', 'location', 'department', 'designation', 'claim_type', 'claim_limit', 'start_date', 'end_date', 'is_active')
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'claim_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'claim_limit': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }
# Recruitement Policies 
# 1
class RecruitementPoliciesDefineEmployeeStrengthModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitementPoliciesEmployeeStrength
        fields = ('location', 'department', 'designation', 'maximum_employee' ,'start_date', 'is_active')
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'maximum_employee': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}), 
        }
# 2
class RecruitementPoliciesDefineQualificationModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitementPoliciesQualification
        fields = ('location', 'department', 'designation', 'responsibilities' ,'academic_qualification', 'professional_qualification' ,'start_date', 'is_active')
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'academic_qualification': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'professional_qualification': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }
# 3
class RecruitementPoliciesDefineExperienceModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'


    class Meta:
        model = RecruitementPoliciesExperience
        fields = ('location', 'department', 'designation', 'responsibilities' ,'min_experience', 'max_experience','language_fluency', 'other_requirement' ,'start_date', 'is_active')
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'min_experience': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'max_experience': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'language_fluency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'other_requirement': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }
# 4
class RecruitementPoliciesManageRecruitmentRulesModelForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitementPoliciesManageRecruitmentRules
        fields = ('location', 'department', 'designation', 'responsibilities' ,'recruitement_rules' ,'start_date', 'is_active')
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'academic_qualification': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'recruitement_rules': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }


class HRPoliciesPolicyTypeForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'


    class Meta:
        model = HRPoliciesPolicyType
        fields = ('policy_type', 'policy_name', 'applicable_to_location' ,'start_date', 'is_active')
        widgets = {
            'policy_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'policy_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'applicable_to_location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PoliciesandFormsManagementHRPoliciesFormModelForm(forms.ModelForm):
    class Meta:
        model = PoliciesandFormsManagementHRPolicies
        fields = ('form_type', 'form_name', 'applicable_to_location' ,'start_date', 'is_active')
        widgets = {
            'form_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'form_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'applicable_to_location': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'','type': "date", 'id':''}),
        }

# Recruitment Management
class RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitmentManagementRecruitmentPlanningEmployeeStrength
        fields = ('location', 'department', 'designation', 'maximum_employee' ,'start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'maximum_employee': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date','id':"id_start_date1"}),
            
        }

class RecruitmentManagementRecruitmentPlanningDefineQualificationForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitmentManagementRecruitmentPlanningQualification
        fields = ('location', 'department', 'designation', 'responsibilities', 'academic_qualification', 'personal_qualification', 'start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'academic_qualification': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'personal_qualification': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentManagementRecruitmentPlanningDefineExperienceForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitmentManagementRecruitmentPlanningExperience
        fields = ('location', 'department', 'designation', 'responsibilities', 'min_experience', 'max_experience', 'language_fluency', 'other_requirement' ,'start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'min_experience': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'max_experience': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'language_fluency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'other_requirement': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
            
        }


class RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecruitmentManagementRecruitmentPlanningManageRecruitmentRules
        fields = ('location', 'department', 'designation', 'responsibilities', 'recruitement_rules','start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'recruitement_rules': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentManagementCandidateSourcingManageJobPublishmentForm(forms.ModelForm):

    class Meta:
        model = RecruitmentManagementCandidateSourcingManageJobPublishment
        fields = ('publishment_type', 'description' ,'start_date', 'is_active')
        widgets = {
            'publishment_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentManagementCandidateSourcingManageReceiptofResumeForm(forms.ModelForm):

    class Meta:
        model = RecruitmentManagementCandidateSourcingManageReceiptofResume
        fields = ('mode_of_resume_receipt', 'description' ,'start_date', 'is_active')
        widgets = {
            'mode_of_resume_receipt': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


# 
RecruitmentManagementInterveiwProcessScreeningLevel




class RecruitmentManagementInterveiwProcessDefineScreeningLevelForm(forms.ModelForm):

    class Meta:
        model = RecruitmentManagementInterveiwProcessScreeningLevel
        fields = ('department','desigantion','screening_Process','sequencing_of_process', 'description' ,'start_date', 'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'desigantion': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'screening_Process': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'sequencing_of_process': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }

#66   
class RecruitmentManagementInterveiwProcessManageInterviewProcessForm(forms.ModelForm):

    class Meta:
        model = RecruitmentManagementInterveiwProcessManageInterviewProcess
        fields = ('mode_of_interview', 'description' ,'start_date', 'is_active')
        widgets = {
            'mode_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentManagementInterveiwProcessDefineScorecardForm(forms.ModelForm):

    class Meta:
        model = RecruitmentManagementInterveiwProcessScorecard
        fields = ('resume_screen_level', 'maximum_score', 'passing_score','description' ,'start_date', 'is_active')
        widgets = {
            'resume_screen_level': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_score': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'passing_score': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentManagementInterveiwManageCandidateShortlistingAuthorityForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    class Meta:
        model = RecruitmentManagementInterveiwManageCandidateShortlistingAuthority
        fields = ('location','department', 'designation', 'resume_screen_level', 'description' ,'start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'resume_screen_level': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentManagementInterveiwManageSelectionProcessForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = RecruitmentManagementInterveiwManageSelectionProcess
        fields = ('location','department', 'designation', 'responsibilities', 'resume_screen_level', 'maximum_score', 'passing_score' ,'description' ,'start_date', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'resume_screen_level': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_score': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'passing_score': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }

# Type of Job

class ManagementEmployeeTypeofJobForm(forms.ModelForm):

    class Meta:
        model = ManagementEmployeeTypeofJob
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ManagementEmployeePayrollofJobForm(forms.ModelForm):

    class Meta:
        model = ManagementEmployeePayrollofJob
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


# On boarding & Exit Management Master
class OnboardingExitRemunerationManagementForm(forms.ModelForm):

    class Meta:
        model = OnboardingExitRemunerationManagement
        fields = ('location', 'department', 'designation', 'grade')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class OnboardingExitRemunerationManagementGrossSalaryForm(forms.ModelForm):

    class Meta:
        model = OnboardingExitRemunerationManagement
        fields = ('salary_code', 'salary_type', 'salary_frequency', 'amount')
        widgets = {
            'salary_code': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'salary_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'salary_frequency': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"number"}),
        }



class OnboardingExitRemunerationManagementDeductionsForm(forms.ModelForm):

    class Meta:
        model = OnboardingExitRemunerationManagement
        fields = ('deduction_category', 'deduction_type', 'deduction_name', 'deduction_frequency', 'deduction_amount', 'is_active')
        widgets = {
            'deduction_category': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'deduction_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'deduction_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'deduction_frequency': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'deduction_amount': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"number"}),
        }

# Registration Management

class RegistrationManagementDefineEmploymentTypeForm(forms.ModelForm):

    class Meta:
        model = RegistrationManagementEmploymentType
        fields = ('employment_type', 'description','is_active')
        widgets = {
            'employment_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class RegistrationManagementDefinePayrollTypeForm(forms.ModelForm):

    class Meta:
        model = RegistrationManagementPayrollType
        fields = ('payroll_type', 'description','is_active')
        widgets = {
            'payroll_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class RegistrationManagementDefinePayrollAgencyForm(forms.ModelForm):

    class Meta:
        model = RegistrationManagementPayrollAgency
        fields = ('employment_type', 'payroll_type', 'payroll_agency', 'is_active')
        widgets = {
            'employment_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'payroll_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'payroll_agency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class RegistrationManagementDefineKeyResponsibilityAreasForm(forms.ModelForm):

    class Meta:
        model = RegistrationManagementKeyResponsibilityAreas
        fields = ('location', 'department', 'designation', 'responsibilities', 'kra_type', 'kra_details', 'kra_frequency', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'kra_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'kra_details': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'kra_frequency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ExitManagementDefineExitTypeForm(forms.ModelForm):

    class Meta:
        model = ExitManagementExitType
        fields = ('exit_type', 'description', 'is_active')
        widgets = {
            'exit_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ExitManagementDefineNoticePeriodeForm(forms.ModelForm):

    class Meta:
        model = ExitManagementNoticePeriod
        fields = ('department', 'grade', 'designation', 'notice_period_in_days', 'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'notice_period_in_days': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
        }


class ExitManagementDefineFinalSettlementForm(forms.ModelForm):

    class Meta:
        model = ExitManagementFinalSettlement
        fields = ('department', 'grade', 'designation', 'final_settlement_days', 'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'final_settlement_days': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
        }


class ExitManagementDefineExitInterviewForm(forms.ModelForm):

    class Meta:
        model = ExitManagementExitInterview
        fields = ('department', 'grade', 'designation', 'interview_type', 'requirement_type' ,'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'interview_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'requirement_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


# Asset Management  > Define Assets Type

class AssetManagementDefineAssetsTypeForm(forms.ModelForm):

    class Meta:
        model = AssetManagementAssetsType
        fields = ('assets_type', 'description', 'is_active')
        widgets = {
            'assets_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class AssetManagementManageAssetsForm(forms.ModelForm):

    class Meta:
        model = AssetManagementManageAssets
        fields = ('location', 'assets_type', 'assets_details','assets_number', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'assets_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'assets_details': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'assets_number': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }



class AssetManagementDefineAllocationPolicyForm(forms.ModelForm):

    class Meta:
        model = AssetManagementAllocationPolicy
        fields = ('location', 'department', 'grade', 'assets_type' ,'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'assets_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }



class PerformanceAppraisalManagementPerformanceManagementDefineTargetsForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalPerformanceManagementTargets
        fields = ('location', 'department', 'designation', 'responsibilities', 'role', 'kra_type', 'kra_frequency', 'target', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'role': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'kra_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'kra_frequency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'target': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalManagementPerformanceManagementDefineIncentiveForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalPerformanceManagementIncentive
        fields = ('incentive_type', 'incentive_name', 'incentive_frequency', 'basis_of_incentive', 'is_active')
        widgets = {
            'incentive_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_frequency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'basis_of_incentive': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalManagePerformanceIncentive
        fields = ('incentive_type', 'incentive_frequency', 'target_fulfilment', 'incentive_amount', 'is_active')
        widgets = {
            'incentive_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'incentive_frequency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'target_fulfilment': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_amount': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
        }


class PerformanceAppraisalManagementDefineAppraisalFrequencyForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalManagementAppraisalFrequency
        fields = ('appraisal_frequency', 'cut_off_date', 'description','is_active')
        widgets = {
            'appraisal_frequency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'cut_off_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date"}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalManagementDefineCrossDepartmentForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalManagementCrossDepartment
        fields = ('main_department', 'cross_department','is_active')
        widgets = {
            'main_department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'cross_department': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalDefineAppraisalRatingDefineWeightageForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalRatingWeightage
        fields = ('appraising_person', 'maximum_weightage', 'description', 'is_active')
        widgets = {
            'appraising_person': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_weightage': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalDefineAppraisalRatingManageRatingForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalRatingManageRating
        fields = ('weightage_range', 'rating', 'description', 'is_active')
        widgets = {
            'weightage_range': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalDefineAppraisalCommitteeForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalAppraisalCommittee
        fields = ('location', 'grade', 'no_of_members' ,'department', 'designation' ,'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'no_of_members': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }

# ************
class PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalAppraisalBenefitsDefineChangeinGrade
        fields = ('grade', 'no_of_grades', 'is_active')
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'no_of_grades': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalDefineAppraisalBenefitsManageGradeChangeForm(forms.ModelForm):
    
    class Meta:
        model = PerformanceAppraisalBenefitsManageGradeChange
        fields = ('location', 'department', 'grade', 'rating', 'no_of_grades', 'new_grades', 'is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'no_of_grades': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'new_grades': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementForm(forms.ModelForm):
    
    class Meta:
        model = PerformanceAppraisalBenefitsDefineIncrement
        fields = ('location', 'department', 'rating', 'increment','is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'increment': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveForm(forms.ModelForm):
    
    class Meta:
        model = PerformanceAppraisalBenefitsAppraisalIncentive
        fields = ('location', 'department', 'grade', 'rating','incentive_type', 'amount','is_active')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control' }),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }




class RecruitmentManagePsychometricTestForm(forms.ModelForm):

    class Meta:
        model = RecruitmentManagePsychometricTest
        fields = ('department', 'desigantion','test_required','test_type', 'description' ,'start_date', 'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'desigantion': forms.Select(attrs={'class': 'form-control', 'required':''}),
             'test_required': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'test_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }

 
class RecruitmentManageTestResultForm(forms.ModelForm):
    class Meta:
        model = RecruitmentManageTestResult
        fields = ('department', 'desigantion','test_type','minimum_points','maximum_points','passing_points','threshhold_limit', 'description' ,'start_date', 'is_active')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'desigantion': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'test_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            
             'minimum_points': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_points': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'passing_points': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'threshhold_limit': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }


class RecruitmentRecruitmentapprovingauthorityForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

    
    class Meta:
        model = Recruitmentapprovingauthority
        fields = ('department', 'designation', 'authority_type' ,'description' ,'start_date', 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'authority_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),          
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
        }
##############
class UpdateadvancetypeForm(forms.ModelForm):
    class Meta:
        model = Updateadvancetype
        fields = ('advance_type', 'description' , 'is_active')
        widgets = {
            'advance_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                    }

##AdvanceEntitlement

class AdvanceEntitlementForm(forms.ModelForm):
    class Meta:
        model = AdvanceEntitlement
        fields = ('department','designation', 'advance_type', 'maximum_amount','interest_required','rate_of_nterest','unit_value' , 'no_of_installments' , 'description' , 'is_active')
        widgets = {
            

            'department'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation'   : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'advance_type'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'maximum_amount' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'interest_required' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'rate_of_nterest'   : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'unit_value'    :  forms.Select(attrs={'class': 'form-control', 'required':''}),
            'no_of_installments'   : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description'          : forms.TextInput(attrs={'class': 'form-control', 'required':''}), 
                    }

#######UpdateOtherDeductions


class UpdateOtherDeductionsForm(forms.ModelForm):
    class Meta:
        model = UpdateOtherDeductions
        fields = ('department','designation', 'grade', 'maximum_limit','unit_value' , 'description' , 'is_active')
        widgets = {
            

            'department'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation'   : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'maximum_limit' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'unit_value'    :  forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description'          : forms.TextInput(attrs={'class': 'form-control', 'required':''}), 
                    }

#

class PerformanceAppraisalUpdateIncentiveTypeForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalUpdateIncentiveType
        fields = ('inventive_type','frequency_of_incentive', 'department', 'grade', 'description', 'is_active')
        widgets = {
            'inventive_type': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency_of_incentive': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }
##PerformanceAppraisalUpdateBonus Type



class PerformanceAppraisalUpdateBonusForm(forms.ModelForm):

    class Meta:
        model = PerformanceAppraisalUpdateBonus
        fields = ('bonus_type','frequency_of_bonus', 'description', 'is_active')
        widgets = {
            'bonus_type': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency_of_bonus': forms.TextInput(attrs={'class': 'form-control'}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

####PerformanceAppraisalManageBonus

class CustomModelFilterManageGradeChangeForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.maximum_limit)


class PerformanceAppraisalManageBonusForm(forms.ModelForm):

    maximum_limit = CustomModelFilterManageGradeChangeForm(queryset=UpdateOtherDeductions.objects.all())
    maximum_limit.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PerformanceAppraisalManageBonus
        fields = ('department','grade','bonus_type','frequency_of_bonus','maximum_limit','unit_value', 'description', 'is_active')
        widgets = {
            'department' : forms.Select(attrs={'class': 'form-control'}),
            'grade' : forms.Select(attrs={'class': 'form-control'}),
            'bonus_type' : forms.Select(attrs={'class': 'form-control'}),
            'frequency_of_bonus'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_limit' : forms.Select(attrs={'class': 'form-control'}),
            'unit_value' : forms.Select(attrs={'class': 'form-control'}),
          
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

                
##111

## UpdateExitApprovalAuthority
class CustomModelFilterUpdateExitApprovalAuthorityForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.authority_type)
    

class UpdateExitApprovalAuthorityForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

        
    authority_type = CustomModelFilterUpdateExitApprovalAuthorityForm(queryset=Recruitmentapprovingauthority.objects.all())
    authority_type.widget.attrs['class'] = 'form-control'

    
    class Meta:
        model = UpdateExitApprovalAuthority
        fields = ('department', 'designation', 'authority_type','department', 'designation' ,'exit_type','description' , 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'authority_type': forms.Select(attrs={'class': 'form-control', 'required':''}),  
            'department' : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation' : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'exit_type'        : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }
############

class CustomModelFilterUpdatePyschometricTestForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.threshhold_limit)


   

class UpdatePyschometricTestForm(forms.ModelForm):
    threshhold_limit = CustomModelFilterUpdatePyschometricTestForm(queryset=RecruitmentManageTestResult.objects.all())
    threshhold_limit.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UpdatePyschometricTest
        fields = ('department', 'designation', 'grade','test_required', 'test_type','minimum_points','maximum_points', 'threshhold_limit','passing_points' ,'description' , 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),             
            'test_required'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'test_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'minimum_points': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'maximum_points': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
             'threshhold_limit'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'passing_points' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }
############
class UpdateAppraisalBenefitTypeForm(forms.ModelForm):

    class Meta:
        model = UpdateAppraisalBenefitType
        fields = ('appraisal_benefit_type', 'is_active')
        widgets = {
           
             'appraisal_benefit_type'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),   
        }

#############
class CustomModelFilterManageGradeChangeForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.rating)
class ManageGradeChangeForm(forms.ModelForm):
    rating = CustomModelFilterManageGradeChangeForm(queryset=PerformanceAppraisalRatingManageRating.objects.all())
    rating.widget.attrs['class'] = 'form-control'


    class Meta:
        model = ManageGradeChange
        fields = ('department', 'designation', 'rating','new_grade', 'existing_grade','applicable_from','description' , 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.Select(attrs={'class': 'form-control', 'required':''}),             
            'new_grade'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'existing_grade': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'applicable_from': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }


##ManageIncrements 
class CustomModelFilterManageIncrementsForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.rating)

class CustomModelFilterManageIncrementsForm1(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.applicable_from)

    

class ManageIncrementsForm(forms.ModelForm):
    rating = CustomModelFilterManageIncrementsForm(queryset=PerformanceAppraisalRatingManageRating.objects.all())
    rating.widget.attrs['class'] = 'form-control'

    applicable_from = CustomModelFilterManageIncrementsForm1(queryset=ManageGradeChange.objects.all())
    applicable_from.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageIncrements
        fields = ('department', 'designation', 'rating','increment_amount', 'unit_value','applicable_from','description' , 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.Select(attrs={'class': 'form-control', 'required':''}),             
            'increment_amount'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'unit_value': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'applicable_from': forms.Select(attrs={'class': 'form-control', 'required':''}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }
# ManageAppraisalIncentive
class CustomModelFilterManageAppraisalIncentiveForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.rating)

class CustomModelFilterManageAppraisalIncentiveForm1(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.increment_amount)

class CustomModelFilterManageAppraisalIncentiveForm2(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.applicable_from)

class ManageAppraisalIncentiveForm(forms.ModelForm):

    rating = CustomModelFilterManageAppraisalIncentiveForm(queryset=PerformanceAppraisalRatingManageRating.objects.all())
    rating.widget.attrs['class'] = 'form-control'


    increment_amount = CustomModelFilterManageAppraisalIncentiveForm1(queryset=ManageIncrements.objects.all())
    increment_amount.widget.attrs['class'] = 'form-control'

    applicable_from = CustomModelFilterManageAppraisalIncentiveForm2(queryset=ManageGradeChange.objects.all())
    applicable_from.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageAppraisalIncentive
        fields = ('department', 'designation', 'rating','increment_amount', 'unit_value','applicable_from','description' , 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'rating': forms.Select(attrs={'class': 'form-control', 'required':''}),             
            'increment_amount'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'unit_value': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'applicable_from': forms.Select(attrs={'class': 'form-control', 'required':''}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }
class UpdateAppraisalProcessTypeForm(forms.ModelForm):

    class Meta:
        model = UpdateAppraisalProcessType
        fields = ('department', 'designation', 'grade','appraisal_process_type','description' , 'is_active')
        widgets = {
           
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'grade': forms.Select(attrs={'class': 'form-control', 'required':''}),             
            'appraisal_process_type'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
        }










# class CustomModelFilterManageGradeChangeForm(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s" % (obj.rating)


#     rating = CustomModelFilterManageGradeChangeForm(queryset=PerformanceAppraisalRatingManageRating.objects.all())
#     rating.widget.attrs['class'] = 'form-control'
