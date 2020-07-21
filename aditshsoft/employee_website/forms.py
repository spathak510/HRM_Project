from django import forms
from employee_website.models import *
from hrms_management.forms import *

class CustomModelEmployeesManageExpereinceModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.experience)
class CustomModelEmployeesManageLanaguageModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.language)

class CustomModelCrmEmployeesEmployeeidModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s/%s" % (obj.employee, obj.unique_id )


class CustomModelCrmEmployeesCrmManageQualificationModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.qualification)
#!
#111
class EmployeeServicesRecruitementUpdateConsultantsmodelForm(forms.ModelForm):
    # designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    # designation.widget.attrs['class'] = 'form-control'
    # experience = CustomModelEmployeesManageExpereinceModel(queryset=ManageExpereince.objects.filter(is_active=1))
    # experience.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeServicesRecruitementUpdateConsultants
        fields = ('name', 'constitution','location')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'constitution': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control','required':'' }),

        }


#### correspondance address
class EmployeeServicesRecruitementUpdateConsultantsAddressForm(forms.ModelForm):
    # designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    # designation.widget.attrs['class'] = 'form-control'
    experience = CustomModelEmployeesManageExpereinceModel(queryset=ManageExpereince.objects.filter(is_active=1))
    experience.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeServicesRecruitementUpdateConsultants
        fields = ('name', 'constitution','location','building', 'block', 'sector' ,'country', 'state', 'city', 'district', 'zip_code','cin_number', 'date_of_incorporation', 'pan_card', 'gst_registration', 'contact_person', 'designations', 'mobile_number', 'mail_id', 'experience')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'constitution': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control', }),
            'correspondance_address': forms.TextInput(attrs={'class': 'form-control', 'required':'','label':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'required':'','label':'Correspondance Address'}),
            'block': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'number'}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'country': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'state': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'city': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'cin_number': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_incorporation': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'pan_card': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'gst_registration': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designations': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'mail_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email', 'required':''}),
            'services_offered': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'branches': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'experience': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
class CustomModelEmployeesManageLanaguageModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.language)
class CustomModelEmployeesManageSalaryRangeModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.start_salary)


class EmployeeServicesRecruitementCreateRequirementmodelForm(forms.ModelForm):
    experience = CustomModelEmployeesManageExpereinceModel(queryset=ManageExpereince.objects.filter(is_active=1))
    experience.widget.attrs['class'] = 'form-control'
    qualification = CustomModelCrmEmployeesCrmManageQualificationModel(queryset=ManageQualification.objects.filter(is_active=1))
    qualification.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    language = CustomModelEmployeesManageLanaguageModel(queryset=ManageLanguage.objects.filter(is_active=1))
    language.widget.attrs['class'] = 'form-control'

    start_salary = CustomModelEmployeesManageSalaryRangeModel(queryset=ManageSalaryRange.objects.filter(is_active=1))
    start_salary.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('location', 'department','designation','existing_strength', 'employees_required', 'start_salary', 'qualification', 'experience', 'language', 'urgency_of_requirement', 'type_of_job', 'pay_roll_job', 'place_of_job_posting','job_description')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level_all_status': forms.TextInput(attrs={'class': 'form-control'}),
            'existing_strength': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'employees_required': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_salary': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'place_of_job_posting': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'experience': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'language': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'urgency_of_requirement': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'type_of_job': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'pay_roll_job': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'action_required':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
   



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_description"].widget = forms.Textarea()
        self.fields["job_description"].widget.attrs['style'] = "margin: 15px; width: 585px; height: 441px;"


class EmployeeServicesRecruitementCreateRequirementmodelForm1(forms.ModelForm):
    experience = CustomModelEmployeesManageExpereinceModel(queryset=ManageExpereince.objects.filter(is_active=1))
    experience.widget.attrs['class'] = 'form-control'
    qualification = CustomModelCrmEmployeesCrmManageQualificationModel(queryset=ManageQualification.objects.filter(is_active=1))
    qualification.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    language = CustomModelEmployeesManageLanaguageModel(queryset=ManageLanguage.objects.filter(is_active=1))
    language.widget.attrs['class'] = 'form-control'

    start_salary = CustomModelEmployeesManageSalaryRangeModel(queryset=ManageSalaryRange.objects.filter(is_active=1))
    start_salary.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('location', 'department','designation','existing_strength', 'employees_required', 'start_salary', 'qualification', 'experience', 'language', 'urgency_of_requirement', 'type_of_job', 'pay_roll_job', 'place_of_job_posting','job_description')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level_all_status': forms.TextInput(attrs={'class': 'form-control'}),
            'existing_strength': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'employees_required': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_salary': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'place_of_job_posting': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'experience': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'language': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'urgency_of_requirement': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'type_of_job': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'pay_roll_job': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'action_required':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
   



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_description"].widget = forms.Textarea()
        self.fields["job_description"].widget.attrs['style'] = "margin: 15px; width: 585px; height: 441px;"



class EmployeeServicesRecruitementCreateRequirementmodelUpdateForm(forms.ModelForm):
    experience = CustomModelEmployeesManageExpereinceModel(queryset=ManageExpereince.objects.filter(is_active=1))
    experience.widget.attrs['class'] = 'form-control'
    qualification = CustomModelCrmEmployeesCrmManageQualificationModel(queryset=ManageQualification.objects.filter(is_active=1))
    qualification.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'

    language = CustomModelEmployeesManageLanaguageModel(queryset=ManageLanguage.objects.filter(is_active=1))
    language.widget.attrs['class'] = 'form-control'

    class Meta: 
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('location', 'department', 'existing_strength', 'employees_required', 'start_salary', 'qualification', 'experience', 'language', 'urgency_of_requirement', 'type_of_job', 'pay_roll_job','approval_level','job_description','comment')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control','readonly':'readonly'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'existing_strength': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'employees_required': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number",'readonly':'readonly'}),
            'start_salary': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'experience': forms.Select(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'urgency_of_requirement': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'type_of_job': forms.Select(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'pay_roll_job': forms.Select(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'approval_level' : forms.Select(attrs={'class': 'form-control'}),
            'job_description' : forms.Textarea(attrs={'class': 'form-control','rows':12, 'cols':35, 'required':'','readonly':'readonly'}),
            'comment' : forms.Textarea(attrs={'class': 'form-control','rows':12, 'cols':35, 'required':''}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.fields["job_description"].widget = forms.Textarea()
    #     self.fields["job_description"].widget.attrs['style'] = "margin: 10px; width: 455px; height: 341px;"

    #     self.fields["comment"].widget = forms.Textarea()
        # self.fields["comment"].widget.attrs['style'] = "margin: 10px; width: 455px; height: 341px;"
        self.fields['approval_level'].widget.attrs['readonly'] = True

#######
#### 
class EmployeeServicesRecruitementCreateRequirementmodelUpdateForm1(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('location', 'department', 'type_of_job', 'pay_roll_job','job_description', 'valid_upto','mode_of_publishing','job_link','response_mode','position_available','position_publish','status','place_of_job_posting')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control','readonly':'readonly'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'mode_of_publishing': forms.Select(attrs={'class': 'form-control', 'required':''}),
            # 'employees_required': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number",'readonly':'readonly'}),
            'position_available': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'position_publish': forms.TextInput(attrs={'class': 'form-control', 'required':''}),

            'vacancy_approved': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'job_link': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'response_mode': forms.Select(attrs={'class': 'form-control', 'required':''}),

            'place_of_job_posting': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'urgency_of_requirement': forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'type_of_job': forms.Select(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'pay_roll_job': forms.Select(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'approval_level' : forms.Select(attrs={'class': 'form-control'}),
            'job_description' : forms.TextInput(attrs={'class': 'form-control', 'required':'','readonly':'readonly'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),

            'valid_upto': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date",'placeholder': 'Position Valid Upto'}),

        }

##############
class EmployeeServicesRecruitementCreateRequirementmodelForm2(forms.ModelForm):
    experience = CustomModelEmployeesManageExpereinceModel(queryset=ManageExpereince.objects.filter(is_active=1))
    experience.widget.attrs['class'] = 'form-control'
    qualification = CustomModelCrmEmployeesCrmManageQualificationModel(queryset=ManageQualification.objects.filter(is_active=1))
    qualification.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    language = CustomModelEmployeesManageLanaguageModel(queryset=ManageLanguage.objects.filter(is_active=1))
    language.widget.attrs['class'] = 'form-control'

    start_salary = CustomModelEmployeesManageSalaryRangeModel(queryset=ManageSalaryRange.objects.filter(is_active=1))
    start_salary.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('location', 'department','existing_strength', 'employees_required', 'start_salary', 'qualification', 'experience', 'language', 'urgency_of_requirement', 'type_of_job', 'pay_roll_job','approval_level','action_required', 'job_description')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'departments': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level_all_status': forms.TextInput(attrs={'class': 'form-control'}),
            'existing_strength': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'employees_required': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'start_salary': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'experience': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'language': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'urgency_of_requirement': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'type_of_job': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'pay_roll_job': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level':forms.Select(attrs={'class': 'form-control', 'required':''}),
             'action_required': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
   



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_description"].widget = forms.Textarea()
        self.fields["job_description"].widget.attrs['style'] = "margin: 15px; width: 585px; height: 441px;"

####################

####123




class EmployeeServicesRecruitementApproveVacanciesUpdateForm(forms.ModelForm):

    class Meta:
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('vacancy_approved', )
        widgets = {
            'vacancy_approved': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeServicesRecruitementPublishVacanciesForm(forms.ModelForm):
    class Meta:
        model = EmployeeServicesRecruitementCreateRequirement
        fields = ('mode_of_publishing','job_link','position_available', 'position_publish', 'place_of_job_posting', 'response_mode', 'valid_upto')
        widgets = {
            'mode_of_publishing': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'job_link': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'position_available': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'position_publish': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'place_of_job_posting': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'response_mode': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'valid_upto': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date"}),
        }

 
class CustomModelCrmEmployeeServicesRecruitementInviteResumeJobModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.job_link)

class EmployeeServicesRecruitementInviteResumeAddForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    # job_link = CustomModelCrmEmployeeServicesRecruitementInviteResumeJobModel(queryset=EmployeeServicesRecruitementCreateRequirement.objects.filter(is_active=1))
    # job_link.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('location', 'department','designation')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'job_link': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'profile_summary': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'number'}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'email'}),
           
        }

class EmployeeServicesRecruitementesumeAddForm1(forms.ModelForm):
    # department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    # department.widget.attrs['class'] = 'form-control'
    job_link = CustomModelCrmEmployeeServicesRecruitementInviteResumeJobModel(queryset=EmployeeServicesRecruitementCreateRequirement.objects.filter(is_active=1))
    job_link.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('job_link', 'name_of_candidate','phone_no','email_id', 'resume_received_doc')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'job_link': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'profile_summary': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'number'}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'email'}),
           
        }

################# add  PsychometricTest
class EmployeeServicesRecruitementPsychometricTestAddForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementPsychometricTest
        fields = ('location', 'department','designation', 'name_of_candidate', 'status', 'email')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'email' : forms.TextInput(attrs={'class': 'form-control', 'required':'',"type":"email"}),
           
        }
 
###
################update PsychometricTest
class EmployeeServicesRecruitementPsychometricTestUpdateForm(forms.ModelForm):
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementPsychometricTest
        fields = ('location', 'department','designation', 'name_of_candidate', 'status', 'email')
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control','required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'email' : forms.TextInput(attrs={'class': 'form-control', 'required':'',"type":"email"}),
           
        }

#######




class EmployeeServicesRecruitementInviteResumeUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('resume_status',)
        widgets = {
            'interview_date': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'place_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'timing_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'resume_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'interview_details_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'interview_time': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
# EmployeeServicesRecruitementInviteResume
class AddUpdateEmployeeServicesRecruitementResume(forms.ModelForm):

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('name_of_candidate','phone_no','email_id','resume_received_doc')
        widgets = {
            'name_of_candidate' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'number'}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'email'}),
            
            
        }

       





class EmployeeServicesRecruitementCandidatesShortlistedUpdateForm(forms.ModelForm):

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('name_of_candidate', 'department','designation','interview_committee','place_of_interview','timing_of_interview','date_of_interview', 'contact_person')
        widgets = {
            'interview_committee': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'interview_details_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'place_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'timing_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'recommendation_1': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required':''}),
        }

        def __init__(self, *args, **kwargs):
            super(EmployeeServicesRecruitementCandidatesShortlistedUpdateForm,self).__init__(*args, **kwargs)
            self.fields["comment"].widget = forms.Textarea()
            self.fields["comment"].widget.attrs['style'] = "margin: 15px; width: 585px; height: 441px;"
class EmployeeServicesRecruitementInterViewStatusForm(forms.ModelForm):
    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }

##
###

class EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm(forms.ModelForm):
    # designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    # designation.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('interview_of_status','new_date','new_time','new_contact_person','new_place_of_interview','interview_result_1')
        widgets = {
            'interview_of_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
          
            'new_date': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'date'}),
            'new_time': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'new_contact_person': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'new_place_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'interview_result_1': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }
    
##111

class EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm1(forms.ModelForm):
    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('location','department','designation',  'name_of_candidate','phone_no','email_id', 'date_of_interview', 'document_name','comment')
        widgets = {
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"email"}),
            'location': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'date_of_interview': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date"}),
            'offer_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date"}),
            'date_joining_candition': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_joining': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date", 
                'id':""}),  
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'interview_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'document_name': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'candidate_shortlist_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required':''}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeServicesRecruitementInterViewStatusShortlistedCandidateForm1, self).__init__(*args, **kwargs)
        self.fields["comment"].widget = forms.Textarea()
        self.fields["comment"].widget.attrs['style'] = "margin: 20px; width: 585px; height: 541px;"

###
class EmployeeServicesRecruitementDocumentForm(forms.ModelForm):
    

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('name_of_candidate','interview_status', 'document_name','comment', 'document_submission')
        widgets = {
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
       
            'document_name': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'interview_status': forms.Select(attrs={'class': 'form-control', 'required':'',}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required':''}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeServicesRecruitementDocumentForm, self).__init__(*args, **kwargs)
        self.fields["comment"].widget = forms.Textarea()
        self.fields["comment"].widget.attrs['style'] = "margin: 15px; width: 485px; height: 441px;"

###
class EmployeeServicesRecruitementOfferStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields = ('name_of_candidate','interview_status','offer_letter_date')
        widgets = {
            'name_of_candidate': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'offer_letter_date': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'interview_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }




# Employee Registration >  Update Registrations
class EmployeeEmployeeRegistrationUpdateRegistrationPersonalDetailsmodelForm(forms.ModelForm):
    # employee_id = CustomModelCrmEmployeesEmployeeidModel(queryset=ManageEmployeeId.objects.filter(is_active=1))
    language = CustomModelEmployeesManageLanaguageModel(queryset=ManageLanguage.objects.filter(is_active=1))
    language.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeRegistrationUpdateRegistrationPersonalDetails
        fields = ('employee_id', 'mode_of_sourcing_1', 'photo', 'type_of_job', 'pay_roll_job', 'name_salute_1', 'first_name','date_of_birth', 'caste', 'religion', 'marital_status_1', 'mobile_no', 'email', 'landline_number', 'emergency_number',  'relationship', 'pan_card', 'adhar_card', 'driving_license','language', 'date_of_anniversary')
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'type':"date"}),
            'mode_of_sourcing_1': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'name_salute_1': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'language': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'marital_status_1': forms.Select(attrs={'class': 'form-control', 'required':''}),

            'date_of_anniversary': forms.TextInput(attrs={'type':"date"}),
            'type_of_job': forms.Select(attrs={'required':""}),
            'pay_roll_job': forms.Select(attrs={'required':""}),
            'mobile_no': forms.TextInput(attrs={'required':"", 'type':"number"}),
            'landline_number': forms.TextInput(attrs={'required':"", 'type':"number"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationPersonalDetailsmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name != "photo":
                field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelMotherForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationFamilityDetails
        fields = ('mother_name', 'mother_dob', 'mother_occupation', 'mother_contact_number')
        widgets = {
            'mother_dob': forms.TextInput(attrs={'type':"date"}),
            'mother_contact_number': forms.TextInput(attrs={'type':"number"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelMotherForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelFatherForm(forms.ModelForm):
    class Meta:
        model = EmployeeRegistrationUpdateRegistrationFamilityDetails
        fields = ('father_name', 'father_dob', 'father_occupation', 'father_contact_number')
        widgets = {
            'father_dob': forms.TextInput(attrs={'type':"date"}),
            'father_contact_number': forms.TextInput(attrs={'type':"number"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelFatherForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelSpouseForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationFamilityDetails
        fields = ('spouse_name', 'spouse_dob', 'spouse_occupation', 'spouse_contact_number')
        widgets = {
            'spouse_dob': forms.TextInput(attrs={'type':"date"}),
            'spouse_contact_number': forms.TextInput(attrs={'type':"number"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelSpouseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelChildrenForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationFamilityChildren
        fields = ('children_name_1', 'children_dob_1', 'children_occupation_1', 'children_contact_number_1')
        widgets = {
            'children_dob_1': forms.TextInput(attrs={'type':"date"}),
            'children_contact_number_1': forms.TextInput(attrs={'type':"number"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationFamilityDetailsmodelChildrenForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['id'] = ''
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationFamilityOtherRelationshipForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationFamiliyOtherDetails
        fields = ('other_name_1', 'other_dob_1', 'other_relationship','other_occupation_1', 'other_contact_number_1')
        widgets = {
            'other_dob_1': forms.TextInput(attrs={'type':"date"}),
            'other_contact_number_1': forms.TextInput(attrs={'type':"number"}),
            'other_relationship': forms.Select(attrs={'class': 'form-control', 'required':''}),

        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationFamilityOtherRelationshipForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['id'] = ''
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationMedicalHistorymodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationMedicalHistory
        fields = ('name_1', 'blood_group_1', 'type_of_illness_1', 'result_1')

    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationMedicalHistorymodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['id'] = ''
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationCorrespondenceAddressForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationCorrespondenceAddress
        fields = ('building', 'block', 'sector', 'country', 'state', 'city', 'district' ,'zip_code', 'staying_since', 'ownership_1')
        widgets = {
            'staying_since': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'ownership_1': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):

        super(EmployeeEmployeeRegistrationCorrespondenceAddressForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationPermanentAddressForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationPermanentAddress
        fields = ('building_1', 'block_1', 'sector_1', 'country_1', 'state_1', 'city_1', 'district_1' ,'zip_code_1', 'staying_since_1', 'ownership_1')
        widgets = {
            'staying_since': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationPermanentAddressForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetailsmodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationJoiningDetails
        fields = ('joining_location', 'joining_date_of_joining', 'joining_time', 'joining_grade_offered', 'joining_next_date_of_increment',  'joining_designation', 'joining_department', 'joining_responsibilities', 'joining_role' ,'joining_reporting_to', 'joining_probation_period', 'contract_valid_up_to')
        widgets = {
            'joining_date_of_joining': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'joining_next_date_of_increment': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'joining_probation_period': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'contract_valid_up_to': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateRegistrationJoiningDetailsmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
####
class EmployeeRegistrationUpdateRegistrationJoiningDetailsFormUpdate(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateRegistrationJoiningDetails
        fields = ('joining_location', 'joining_date_of_joining', 'joining_time', 'joining_grade_offered', 'joining_next_date_of_increment',  'joining_designation', 'joining_department', 'joining_responsibilities', 'joining_role' ,'joining_reporting_to', 'joining_probation_period', 'contract_valid_up_to')
        widgets = {
            'joining_date_of_joining': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'joining_next_date_of_increment': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'joining_probation_period': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'contract_valid_up_to': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationUpdateRegistrationJoiningDetailsFormUpdate, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''


####

class EmployeeEmployeeRegistrationUpdateEducationalQualificationmodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateEducationalQualification
        fields = ('educational_qualificationcourse_name_1', 'educational_qualificationroll_number_1', 'educational_qualificationmarks_division_1', 'educational_qualificationuniversity_institution_1', 'educational_qualificationstart_date_1', 'educational_qualificationend_date_1')
        widgets = {
            'educational_qualificationstart_date_1': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'educational_qualificationend_date_1': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateEducationalQualificationmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''

class EmployeeEmployeeRegistrationUpdateProfessionalJourneymodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateProfessionalJourney
        fields = ('professional_journeycompany_1', 'professional_journeystart_date_1', 'professional_journeyend_date_1', 'professional_journeylast_desgination_1', 'professional_journeynature_of_duties_1', 'professional_journeylast_drawn_dalary_1', 'reason_for_leaving_1')
        widgets = {
            'professional_journeystart_date_1': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'professional_journeyend_date_1': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateProfessionalJourneymodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['id'] = ''
                field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateSalaryStructutremodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateSalaryStructutre
        fields = ('salary_structut_salary_code_1', 'salary_structut_salary_name_1', 'salary_structut_salary_frequency_1', 'salary_structut_amount_offered_1', 'salary_structut_percentage_value_flag_1', 'salary_structut_taxability_status')
        widgets = {
            'salary_structut_salary_frequency_1': forms.Select(attrs={'class': 'form-control ',"required":"", "id":""}),
            'salary_structut_taxability_status': forms.Select(attrs={'class': 'form-control'}),
            'salary_structut_amount_offered_1': forms.TextInput(attrs={'class': 'form-control salrytru',"required":"", "type": "number", "id":""}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateSalaryStructutremodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                if field_name == "salary_structut_amount_offered_1":
                    field.widget.attrs['class'] = 'form-control salrytru'
                else:
                    field.widget.attrs['class'] = 'form-control'

                field.widget.attrs['required'] = ''
                field.widget.attrs['id'] = ''


class EmployeeEmployeeRegistrationDeductionAndPerquisitesForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationDeductionAndPerquisites
        fields = ('appicablitity_1', 'perquisitec_category_1','perquisitec_name_1',  'perquisite_frequency_1', 'percentage_value_flag_1' ,'perquisite_amount_1')

    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationDeductionAndPerquisitesForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                if field_name == "perquisite_amount_1":
                    field.widget.attrs['class'] = 'form-control salrytru1'
                elif field_name == "appicablitity_1":
                    field.widget.attrs['class'] = 'form-control applicablity'
                else:
                    field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
                field.widget.attrs['id'] = ''

class EmployeeEmployeeRegistrationDeductionForm(forms.ModelForm):
    class Meta:
        model = EmployeeRegistrationDeduction
        fields = ('applicated', 'deduction_code', 'deduction_name','deduction_frequancy','deduction_ammount')
        widgets = {
            'applicated': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_code': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_name': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_frequancy': forms.TextInput(attrs={'class': 'form-control'}),
            'deduction_ammount': forms.TextInput(attrs={'class': 'form-control'}),
            }



class EmployeeEmployeeRegistrationUpdateBankDetailsmodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateBankDetails
        fields = ('account_type', 'bank_account_number', 'bank_name', 'branch', 'ifscc_code', 'micr')

    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateBankDetailsmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationVerificationReportmodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationVerificationReport
        fields = ('verification_agency_1', 'finding_1', 'upload_report_1')

    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationVerificationReportmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                if field_name != "upload_report_1":
                    field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationReferencesmodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationReferences
        fields = ('referencename_1', 'referencerelationship_1', 'referencecontact_number_1', 'referenceemail_id_1', 'referenceaddress_1', 'referenceknown_since_1')
        widgets = {
            'referenceknown_since_1': forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'referenceemail_id_1': forms.TextInput(attrs={'class': 'form-control',"type":"email"}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationReferencesmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''


class CrmEmployeeEmployeeRegistrationDocumentsmodelForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationDocuments
        fields = ('name_of_documents_1', 'upload_1')

    def __init__(self, *args, **kwargs):
        super(CrmEmployeeEmployeeRegistrationDocumentsmodelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''


class EmployeeEmployeeRegistrationUpdateDepartmentForm(forms.ModelForm):

    class Meta:
        model = EmployeeRegistrationUpdateDepartment
        fields = ('employee_id', 'employee_name', 'current_designation', 'new_designation', 'current_department', 'new_department', 'current_reporting_to', 'new_reporting_to', 'current_responsibilites', 'new_responsibilities', 'current_location', 'new_location', 'current_salary', 'new_salary')

    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeRegistrationUpdateDepartmentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''


class EmployeeEmployeeAssetAllocatedForm(forms.ModelForm):

    class Meta:
        model = EmployeeAssetAllocated
        fields = ('asset_code_1', 'asset_serial_number_1', 'asset_name_1', 'asset_condition_1', 'asset_location_1')

    def __init__(self, *args, **kwargs):
        super(EmployeeEmployeeAssetAllocatedForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''


class EmployeeEmployeeAccessControlsForm(forms.ModelForm):

    class Meta:
        model = EmployeeAccessControls
        fields = ('official_email_id', 'official_contact_number', 'id_card_number', 'system_access_id', 'attendance_card_number')
        widgets = {
            'official_email_id': forms.TextInput(attrs={'class': 'form-control',"type":"email", "required":""}),
            'official_contact_number': forms.TextInput(attrs={'class': 'form-control', "required":"", "type":"number"}),
            'id_card_number': forms.TextInput(attrs={'class': 'form-control',"required":""}),
            'system_access_id': forms.TextInput(attrs={'class': 'form-control',"required":""}),
            'attendance_card_number': forms.TextInput(attrs={'class': 'form-control',"required":""}),
        }


# Leaves
class EmployeeLeavesLeaveRequestForm(forms.ModelForm):

    class Meta:
        model = EmployeeLeavesLeaveRequest
        fields = ('employee_id','employee_names', 'designation', 'department','location', 'type_of_leave', 'leave_available', 'start_date', 'end_date', 'total_leave', 'explaination')

    def __init__(self, *args, **kwargs):
        super(EmployeeLeavesLeaveRequestForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
        self.fields["explaination"].widget = forms.Textarea()
        self.fields["explaination"].widget.attrs['style'] = "margin: 0px; width: 663px; height: 141px;"


class EmployeeLeavesLeaveRequestUpdateStatusForm(forms.ModelForm):

    class Meta:
        model = EmployeeLeavesLeaveRequest
        fields = ('status', 'explaination')

    def __init__(self, *args, **kwargs):
        super(EmployeeLeavesLeaveRequestUpdateStatusForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
        self.fields["explaination"].widget = forms.Textarea()
        self.fields["explaination"].widget.attrs['style'] = "margin: 0px; width: 668px; height: 37px;"
        self.fields["explaination"].widget.attrs['required'] = ""


class UserAttendenceSerializersForm(forms.ModelForm):

    class Meta:
        model = UserLoginApiLogs
        fields = ('employee_id', 'attendance_type', 'date_field'  ,'login_time', 'address', 'logout_time', 'logout_address')
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'attendance_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'date_field': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"month"}),
            'login_time': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'logout_time': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'logout_address': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class UserAttendenceSerializersUpdateForm(forms.ModelForm):
    class Meta:
        model = UserLoginApiLogs
        fields = ('attendance_status', 'attendance_correction' )
        widgets = {
            'attendance_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'attendance_correction': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

###
class UserAcceptAttendanceUpdateForm(forms.ModelForm):
    class Meta:
        model = UserLoginApiLogs
        fields = ('attendance_status',  )
        widgets = {
            'attendance_status': forms.Select(attrs={'class': 'form-control', 'required':''}),
           
        }



# Leaves Section
class EmployeeHRPoliciesUpdatePoliciesmodelForm(forms.ModelForm):

    location = CustomModelFilterCrmManageBranch(queryset=ManageBranch.objects.filter(is_active=1))
    location.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeHRPoliciesUpdatePolicies
        fields = ('policy_type', 'location', 'upload', 'effect_date','approval_level')
        widgets = {
            'policy_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control', 'id':""}),
            'approval_level': forms.Select(attrs={'class': 'form-control'}),
            'effect_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date", 'id':""}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeHRPoliciesUpdatePoliciesmodelForm, self).__init__(*args, **kwargs)
        self.fields['upload'].widget.attrs.update({'class' : 'form-control','accept':'application/pdf'})


class EmployeeHRPoliciesUpdateFormmodelForm(forms.ModelForm):
    location = CustomModelFilterCrmManageBranch(queryset=ManageBranch.objects.filter(is_active=1))
    location.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeHRPoliciesUpdateForm
        fields = ('form_type', 'location', 'upload', 'effect_date','approval_level')
        widgets = {
            'form_type': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'approval_level': forms.Select(attrs={'class': 'form-control'}),
            'effect_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date", 'id':""}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeHRPoliciesUpdateFormmodelForm, self).__init__(*args, **kwargs)
        self.fields['upload'].widget.attrs.update({'class' : 'form-control','accept':'application/pdf'})


class EmployeeHRPoliciesUpdateCircularsForm(forms.ModelForm):
    location = CustomModelFilterCrmManageBranch(queryset=ManageBranch.objects.filter(is_active=1))
    location.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeHrPoliciesUpdateCirculars
        fields = ('circular_type', 'location', 'upload', 'effect_date','approval_level')
        widgets = {
            'circular_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'approval_level': forms.Select(attrs={'class': 'form-control'}),
            'effect_date': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date", 'id':""}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeHRPoliciesUpdateCircularsForm, self).__init__(*args, **kwargs)
        self.fields['upload'].widget.attrs.update({'class' : 'form-control','accept':'application/pdf'})

####
class EmployeePayrollProcessingTaxCalculationForm(forms.ModelForm):
    class Meta:
        model = EmployeePayrollProcessingTaxCalculation
        fields = ('location', 'departments', 'assessment_year','year_to_date_salary','annual_salary','other_income','total_income','exemption','deduction','taxable_income','tax','cess' , 'total_tax_payable' ,'tax_deducted', 'tax_paid','balance_tax_payable','status')
        widgets ={
         
            'location' : forms.TextInput(attrs={'class': 'form-control'}),
            'departments' : forms.TextInput(attrs={'class': 'form-control'}),
            'assessment_year'  : forms.TextInput(attrs={'class': 'form-control'}),
            'year_to_date_salary'  : forms.TextInput(attrs={'class': 'form-control'}),
            'annual_salary'  : forms.TextInput(attrs={'class': 'form-control'}),
            'other_income'  : forms.TextInput(attrs={'class': 'form-control'}),
            'total_income'  : forms.TextInput(attrs={'class': 'form-control'}),
            'exemption'  : forms.TextInput(attrs={'class': 'form-control'}),
            'deduction'  : forms.TextInput(attrs={'class': 'form-control'}),
            'taxable_income'  : forms.TextInput(attrs={'class': 'form-control'}),
            'tax'  : forms.TextInput(attrs={'class': 'form-control'}),
            'cess'  : forms.TextInput(attrs={'class': 'form-control'}),
            'total_tax_payable'  : forms.TextInput(attrs={'class': 'form-control'}),
            'tax_deducted'  : forms.TextInput(attrs={'class': 'form-control'}),
            'tax_paid'   : forms.TextInput(attrs={'class': 'form-control'}),
            'balance_tax_payable'  : forms.TextInput(attrs={'class': 'form-control'}),
            'status'  : forms.Select(attrs={'class': 'form-control'}),
        }



####################
class EmployeePayrollProcessingUpdateTaxDeclarationForm(forms.ModelForm):
    class Meta:
        model = EmployeePayrollProcessingUpdateTaxDeclaration
        fields = ('location', 'departments', 'assessment_year','employee_id','employee_names' ,'tax_declaration_type','tax_rule','exemption_claimed','exemption_approved','maximum_limit','approval_level','approval_level_all_status','status1')
        widgets ={
            'employee_id'  : forms.Select(attrs={'class': 'form-control'}),
            'employee_names'  : forms.TextInput(attrs={'class': 'form-control'}),
            
            'location' : forms.TextInput(attrs={'class': 'form-control'}),
            'departments' : forms.TextInput(attrs={'class': 'form-control'}),
            'assessment_year'  : forms.TextInput(attrs={'class': 'form-control'}),
            'tax_declaration_type'  : forms.TextInput(attrs={'class': 'form-control'}),
            'tax_rule'  : forms.TextInput(attrs={'class': 'form-control'}),
            'exemption_claimed'  : forms.TextInput(attrs={'class': 'form-control'}),
            'exemption_approved'  : forms.TextInput(attrs={'class': 'form-control'}),
            'maximum_limit'  : forms.TextInput(attrs={'class': 'form-control'}),
            'approval_level'  : forms.Select(attrs={'class': 'form-control'}),
            'approval_level_all_status'  : forms.TextInput(attrs={'class': 'form-control'}),
            'status1'  : forms.Select(attrs={'class': 'form-control'}),
            }

###!

class EmployeePayrollProcessingUpdateTaxRecoveryForm(forms.ModelForm):
    class Meta:
        model = EmployeePayrollProcessingUpdateTaxRecovery
        fields = ('location', 'departments', 'assessment_year','employee_id','employee_names' ,'year_to_date_salary','annual_salary',
        'total_tax_payable','tax_already_recovered','recovery_during_current_month','total_tax_recovered','balance_tax_payable')
        widgets ={
            'employee_id'  : forms.TextInput(attrs={'class': 'form-control'}),
            'employee_names'  : forms.TextInput(attrs={'class': 'form-control'}),
            
            'location' : forms.TextInput(attrs={'class': 'form-control'}),
            'departments' : forms.TextInput(attrs={'class': 'form-control'}),
            'assessment_year'  : forms.TextInput(attrs={'class': 'form-control'}),
            'year_to_date_salary'  : forms.TextInput(attrs={'class': 'form-control'}),
            'annual_salary'  : forms.TextInput(attrs={'class': 'form-control'}),
            'total_tax_payable'  : forms.TextInput(attrs={'class': 'form-control'}),
            'tax_already_recovered'  : forms.TextInput(attrs={'class': 'form-control'}),
            'recovery_during_current_month'  : forms.TextInput(attrs={'class': 'form-control'}),
            'total_tax_recovered'  : forms.TextInput(attrs={'class': 'form-control'}),
            'balance_tax_payable'  : forms.TextInput(attrs={'class': 'form-control'}),
            'status'  : forms.Select(attrs={'class': 'form-control'}),
            }


####
class EmployeePayrollProcessingUpdateRecoveriesAddForm(forms.ModelForm):
    class Meta:
        model = EmployeePayrollProcessingUpdateRecoveries
        fields = ('employee_id','employee_names' ,'location', 'departments', 'month_and_year','recovery_period','recovery_type','recovery_amount','approval_level','approval_level_all_status','status')
        widgets ={
            'employee_id'  : forms.Select(attrs={'class': 'form-control'}),
            'employee_names'  : forms.TextInput(attrs={'class': 'form-control'}),
            
            'location' : forms.TextInput(attrs={'class': 'form-control'}),
            'departments' : forms.TextInput(attrs={'class': 'form-control'}),
            'month_and_year'  : forms.TextInput(attrs={'class': 'form-control'}),
            'recovery_period'  : forms.TextInput(attrs={'class': 'form-control'}),
            'recovery_type'  : forms.TextInput(attrs={'class': 'form-control'}),
            'recovery_amount'  : forms.TextInput(attrs={'class': 'form-control'}),
            'approval_level'  : forms.Select(attrs={'class': 'form-control'}),
            'approval_level_all_status'  : forms.TextInput(attrs={'class': 'form-control'}),
            'status'  : forms.Select(attrs={'class': 'form-control'}),
            }


####
class PayrollSalaryDisbursementAddForm(forms.ModelForm):
    class Meta:
        model = PayrollSalaryDisbursement
        fields = ('month_and_year','employee_id','employee_names' , 
        'bank_name','ifsc_code','account_number', 'amount','mode_of_payment', 'date_of_payment' ,'approval_level')
        widgets ={
            'employee_id'  : forms.Select(attrs={'class': 'form-control'}),
            'employee_names'  : forms.TextInput(attrs={'class': 'form-control'}),
            
            'month_and_year'  : forms.TextInput(attrs={'class': 'form-control',"type":"date"}),
            'bank_name'  : forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code'  : forms.TextInput(attrs={'class': 'form-control'}),
            'account_number'  : forms.TextInput(attrs={'class': 'form-control',"type":'number'}),
            'amount'  : forms.TextInput(attrs={'class': 'form-control',"type":'number'}),
            'mode_of_payment'  : forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_payment'  : forms.TextInput(attrs={'class': 'form-control','type':'date'}),
            'approval_level'  : forms.Select(attrs={'class': 'form-control'}),
            'approval_level_all_status'  : forms.TextInput(attrs={'class': 'form-control'}),
            'status'  : forms.Select(attrs={'class': 'form-control'}),
            }



# Claim and Reimbursement
class EmployeeClaimandReimbursementSubmitClaimsForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitClaims
        fields = ('claim_date_1', 'claim_type_1', 'claim_period_1', 'claim_details_1' ,'claim_amount_1', 'claim_restriced_to_1', 'comment_1','status','upload_1')
        widgets = {
            'claim_date_1': forms.TextInput(attrs={'class': 'form-control', 'required':'', "type":"date"}),
            'claim_type_1': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'claim_period_1': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'claim_details_1': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'claim_amount_1': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"number"}),
            'claim_restriced_to_1': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'comment_1': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeClaimandReimbursementSubmitClaimsForm, self).__init__(*args, **kwargs)
        self.fields['upload_1'].widget.attrs.update({'class' : 'form-control','accept':'application/pdf'})


class EmployeeClaimandReimbursementSubmitClaimsApprovedForm(forms.ModelForm):
    # status = EmployeeClaimandReimbursementSubmitClaimsApprovedModel(queryset=EmployeeClaimandReimbursementSubmitReimbursement.objects.filter(is_active=1))
    # status.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeeClaimandReimbursementSubmitReimbursement
        fields = ('employee_id', 'employee_names','location','department','status' ,'approved_amount',)
        widgets = {
            'employee_id': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'approved_amount': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"number"}),
            'location': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            
            
        }


class EmployeeReimbursementSubmitClaimsApprovedForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitClaims
        fields = ('approved_amount_1',)
        widgets = {
            'approved_amount_1': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"number"}),
        }



#
class EmployeeClaimandReimbursementSubmitAmountApprovedProcessingForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitClaims
        fields = ('date_of_processing','employee_id', 'employee_names','location','department' , 'status')
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'employee_names': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_processing': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'location': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeReimbursementSubmitAmountApprovedProcessingForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitClaims
        fields = ('date_of_processing', 'status')
        widgets = {
            'date_of_processing': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }

class EmployeeClaimandReimbursementSubmitClaimsUpdatesForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitClaims
        fields = ( 'status','employee_id','employee_names','date_of_processing')
        widgets = {
            
            'employee_id' : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_processing' : forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


##
class EmployeeClaimandReimbursementSubmitReimbursementSubmitUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitReimbursement
        fields = ('approval_level','employee_id','employee_names','date_of_processing','approved_amount_1')
        widgets = {
            
            'approval_level': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_id': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'date_of_processing': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'date'}),
            'approved_amount_1': forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'number'}),
           
        }



class EmployeeClaimandReimbursementSubmitReimbursementForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitReimbursement
        fields = ('reimbursement_month_1', 'reimbursement_type_1', 'reimbursement_period_1','employee_id','employee_names' ,'amount_1', 'maximum_limit_1', 'comment_1', 'upload_1')
        widgets = {
            'employee_id': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            
            'reimbursement_month_1': forms.TextInput(attrs={'class': 'form-control', 'required':'', "type":"month", 'id':""}),
            'reimbursement_type_1': forms.Select(attrs={'class': 'form-control', 'required':'', 'id':""}),
            'reimbursement_period_1': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'id':""}),
            'amount_1': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'id':"", "type":"number"}),
            'maximum_limit_1': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'id':""}),
            'comment_1': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'id':""}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeClaimandReimbursementSubmitReimbursementForm, self).__init__(*args, **kwargs)
        self.fields['upload_1'].widget.attrs.update({'class' : 'form-control','accept':'application/pdf', 'id':""})


class EmployeeClaimandReimbursementSubmitReimbursementFormApprovedForm(forms.ModelForm):
    class Meta:
        model = EmployeeClaimandReimbursementSubmitReimbursement
        fields = ('status', 'approved_amount_1')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approved_amount_1': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


# Key Responsibility Areas & Targets
# class CustomModelEmployeePayrollProcessedHolidaysModel(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s" % (obj.leave_balance)
# class CustomModelEmployeePayrollProcessedModel(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s" % (obj.claim_amount_1)

# class EmployeePayrollProcessedForm(forms.ModelForm):
#     leave_balance = CustomModelEmployeePayrollProcessedHolidaysModel(queryset=LeaveandHolidaysManagementUpdateLeavesQuota.objects.filter(is_active=1))
#     leave_balance.widget.attrs['class'] = 'form-control'
#     claim_amount_1 = CustomModelEmployeePayrollProcessedModel(queryset=EmployeeClaimandReimbursementSubmitClaims.objects.filter(is_active=1))
#     claim_amount_1.widget.attrs['class'] = 'form-control'

class KeyResponsibilityAreasTargetsUpdateKRATargetsForm(forms.ModelForm):
    class Meta:
        model = KeyResponsibilityAreasTargetsUpdateKRATargets
        fields = ('employee_id', 'location', 'employee_names','kra_fulfilment' , 'designation', 'department','month_and_year', 'kra_type', 'kra_frequency', 'reporting_officer','kra_details')
        widgets = {
            'employee_names' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'kra_fulfilment' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),

            'employee_id': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'designation' : forms.Select(attrs={'class': 'form-control'}),
            'department' : forms.Select(attrs={'class': 'form-control'}),
            'month_and_year': forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"date"}),
            'kra_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'kra_frequency': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'reporting_officer': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'kra_details': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class KeyResponsibilityAreasTargetsUpdateKRATargetsUpdateForm(forms.ModelForm):
    class Meta:
        model = KeyResponsibilityAreasTargetsUpdateKRATargets
        fields = ('status',)
        widgets = {
            'staus': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'kra_fulfilment': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeExitEmployeeResignationForm(forms.ModelForm):
    class Meta:
        model = EmployeeExitEmployeeResignation
        fields = ('employee_id','employee_names','location', 'department', 'designation', 'reporting_officer', 'resignation_date', 'reasons_for_resignation', 'notice_period_applicability', 'notice_period_required')
        widgets = {
            'employee_id':forms.Select(attrs={'class': 'form-control'}),
            'employee_names':forms.TextInput(attrs={'class': 'form-control'}),
            'location':forms.Select(attrs={'class': 'form-control'}),
            'department':forms.Select(attrs={'class': 'form-control'}),
            'designation':forms.Select(attrs={'class': 'form-control'}),
            'reporting_officer':forms.Select(attrs={'class': 'form-control'}),
            'resignation_date':forms.TextInput(attrs={'class': 'form-control', 'type':"date", 'required':''}),
            'reasons_for_resignation':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'notice_period_applicability': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'notice_period_required': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeExitEmployeeResignationUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = EmployeeExitEmployeeResignation
        fields = ('notice_period_waived', 'notice_period_to_be_served', 'status')
        widgets = {
            'notice_period_waived':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'notice_period_to_be_served':forms.TextInput(attrs={'class': 'form-control','required':"", "type":"number"}),
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeExitEmployeeRelievingUpdateStatusForm(forms.ModelForm):
    
    class Meta:
        model = EmployeeExitEmployeeResignation
        fields = ('notice_pay_deducted','status_of_assets_allocated', 'status_of_responsibility_handover', 'status_of_formalities_completed_status_of_exit_interview', 'status_of_relieving_letters_status_of_full_and_final_settlement' ,'status')
        widgets = {
            'notice_pay_deducted':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'status_of_assets_allocated':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'status_of_responsibility_handover':forms.Select(attrs={'class': 'form-control','required':"", "type":"number"}),
            'status_of_formalities_completed_status_of_exit_interview':forms.Select(attrs={'class': 'form-control','required':"", "type":"number"}),
            'status_of_relieving_letters_status_of_full_and_final_settlement':forms.Select(attrs={'class': 'form-control','required':"", "type":"number"}),
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeExitEmployeeFullandFinalSettlementUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = EmployeeExitEmployeeResignation
        fields = ('final_salary_status','status')
        widgets = {
            'final_salary_status':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }

class EmployeeExitEmployeeFullandFinalSettlementUpdateStatusseForm(forms.ModelForm):
    class Meta:
        model = EmployeeExitEmployeeResignation
        fields = ('status','final_sal_status','net_salary')
        widgets = {
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'final_sal_status':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'net_salary':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }






class LeaveandHolidaysManagementLeavesForm(forms.ModelForm):
    
    class Meta:
        model = LeaveandHolidaysManagementUpdateLeavesQuota
        fields = ('employee_id','employee_names','department', 'designation', 'leave_type', 'financial_year' ,'leave_balance', 'leave_added', 'frequency_of_leave', 'impact_on_salary', 'maximum_limit_carry_forward_allowed', 'encashment_allowed')
        widgets = {
            'employee_id':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'department':forms.Select(attrs={'class': 'form-control', 'required':'', 'id':"Department"}),
            'designation':forms.Select(attrs={'class': 'form-control','required':"",  'id':"Designation"}),
            'leave_type':forms.Select(attrs={'class': 'form-control', "type":"number"}),
            'financial_year':forms.Select(attrs={'class': 'form-control'}),
            'leave_balance':forms.TextInput(attrs={'class': 'form-control', 'required':'', "type":"number"}),
            'leave_added':forms.TextInput(attrs={'class': 'form-control', 'required':'','type':"date"}),
            'frequency_of_leave':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'impact_on_salary':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'maximum_limit_carry_forward_allowed':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':"number"}),
            'encashment_allowed':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class OvertimeManagementUpdateOvertimeStatusListViewUpdateStatusViewForm(forms.ModelForm):
    class Meta:
        model = OvertimeManagementUpdateOvertime
        fields = ('reason','status')
        widgets = {
            'reason':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }

#####11
class OvertimeManagementUpdateOvertimeForm(forms.ModelForm):
    class Meta:
        model = OvertimeManagementUpdateOvertime
        fields = ('employee_id','employee_names','designation','department','location','month_and_year_date', 'overtime_start', 'overtime_end','total_hours', 'approval_level_all_status', 'approval_level','reason','status')
        widgets = {
            
           
         
            'user'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_id' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designation'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'month_and_year_date' :forms.TextInput(attrs={'class': 'form-control', 'required':'','type':'date'}),
            'overtime_start' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'overtime_end' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'total_hours' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'approval_level_all_status'  :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            
            'reason':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }

#####
class TravelClaimManagementTravelConveyanceTravelRequestForm(forms.ModelForm):
    class Meta:
        model = TravelClaimManagementTravelConveyanceTravelRequest
        fields = ('employee_id', 'employee_names', 'designation','department', 'location',   'mode_of_travel', 'travel_start_date' ,'travel_end_date', 'stay_arrangement', 'total_travel_cost', 'advance_required', 'reasons_for_travel')
        widgets = {
            'employee_id':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designation':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location':forms.Select(attrs={'class': 'form-control', 'required':''}),
            

            'mode_of_travel':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'no_of_days':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'travel_start_date':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date'}),
            'travel_end_date':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date'}),
            'stay_arrangement':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'total_travel_cost':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'advance_required':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'reasons_for_travel':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


######
class TravelClaimManagementTravelConveyanceTravelRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = TravelClaimManagementTravelConveyanceTravelRequest
        fields = ('employee_id', 'employee_names', 'designation','department', 'location',   'mode_of_travel', 'travel_start_date' ,'travel_end_date', 'stay_arrangement', 'total_travel_cost', 'advance_required', 'reasons_for_travel','status')
        widgets = {
            'employee_id':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'employee_names':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designation':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location':forms.Select(attrs={'class': 'form-control', 'required':''}),
            

            'mode_of_travel':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'no_of_days':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'travel_start_date':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date'}),
            'travel_end_date':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date'}),
            'stay_arrangement':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'total_travel_cost':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number'}),
            'advance_required':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'reasons_for_travel':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


# Employee Advances 
class EmployeeAdvancesSubmitAdvanceRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeAdvancesSubmitAdvanceRequest
        fields = ('employee_id', 'employee_names','designation','department','location' ,'advance_type_1', 'advance_amount_1', 'recovery_start_from_1', 'recovery_period_1', 'justification_1', 'advance_approved_1')
        widgets = {
            'employee_id':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_names':forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designation':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location':forms.Select(attrs={'class': 'form-control', 'required':''}),


            'advance_type_1':forms.Select(attrs={'class': 'form-control', 'required':'', 'id':""}),
            'advance_amount_1':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'number', 'id':""}),
            'recovery_start_from_1':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
            'recovery_period_1':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'type':'date', 'id':""}),
            'justification_1':forms.TextInput(attrs={'class': 'form-control', 'required':'', 'id':""}),
            'advance_approved_1':forms.Select(attrs={'class': 'form-control', 'required':'', 'id':""}),
        }

class EmployeeAdvancesSubmitAdvanceRequestUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = EmployeeAdvancesSubmitAdvanceRequest
        fields = ('status','payment_status')
        widgets = {
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
            'payment_status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }
####

class EmployeeAdvancesSubmitIncentiveBonusForm(forms.ModelForm):
    class Meta:
        model = EmployeeAdvancesSubmitIncentiveBonus
        fields = ('user','incentive_type', 'incentive_period', 'incentive_amount' ,'status',  'approval_level', 'approval_level_all_status' )
        widgets = {
            'user'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'incentive_type' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_period' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_amount' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status'   :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level_all_status' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        
        }

  ###
class EmployeeAdvanceSubmitIncentiveBonusForm(forms.ModelForm):
    class Meta:
        model = EmployeeAdvancesSubmitIncentiveBonus
        fields = ('employee_id' ,  'employee_names', 'department','location','approved_by' ,'incentive_type', 'incentive_period', 'incentive_amount','approval_level')
        widgets = {
            'user'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'employee_id' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            "employee_names" :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'designation'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'location' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approved_by' :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'incentive_type' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_period' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'incentive_amount' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status'   :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level'  :forms.Select(attrs={'class': 'form-control', 'required':''}),
            'approval_level_all_status' :forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        
        }
       



class EmployeeAdvancesSubmitIncentiveBonusUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = EmployeeAdvancesSubmitIncentiveBonus
        fields = ('status',)
        widgets = {
            'status':forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class KnowledgeandTrainingUpdateDocumentsForm(forms.ModelForm):
    location = CustomModelFilterCrmManageBranch(queryset=ManageBranch.objects.filter(is_active=1))
    location.widget.attrs['class'] = 'form-control'
    class Meta:
        model = KnowledgeandTrainingUpdateDocuments
        fields = ('document_type', 'location',  'subject', 'upload')
        widgets = {
            'document_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(KnowledgeandTrainingUpdateDocumentsForm, self).__init__(*args, **kwargs)
        self.fields['upload'].widget.attrs.update({'class' : 'form-control','accept':'application/pdf'})

###
class KnowledgeandTrainingKnowledgeSharingForm(forms.ModelForm):

    """ docstring for ClassName"""
    
    class Meta:
        model = KnowledgeandTrainingKnowledgeSharing
        fields = ('documents_type', 'subject', 'status')
        widgets = {
            'documents_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'status': forms.Select(attrs={'class': 'form-control', 'required':''}),
        }


class EmployeeServicesRecruitementInviteResumeAddForm1(forms.ModelForm):

    class Meta:
        model = EmployeeServicesRecruitementInviteResume
        fields ='__all__'



####
class ManageHolidaysForm(forms.ModelForm):
    class Meta:
        model = ManageHolidays
        fields = ('holidays_type', 'holidays_date','branch', 'parent_company', 'head_office', 'impact_on_salary')
        widgets = {
                'holidays_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'holidays_date': forms.TextInput(attrs={'class': 'form-control', 'required':'' ,'type':"date"}),
                'branch': forms.Select(attrs={'class': 'form-control', 'required':''}),
                'parent_company': forms.Select(attrs={'class': 'form-control', 'required':''}),
                'head_office': forms.Select(attrs={'class': 'form-control', 'required':''}),
                'impact_on_salary': forms.Select(attrs={'class': 'form-control', 'required':''}),
            }




##UserLoginApiLogsForm
class UserLoginApiLogsForm(forms.ModelForm):
    class Meta:
        model = UserLoginApiLogs
        fields = ( 'employee_id','employee_names','location','department', 'designation','responsibilities'  ,'approval_level','attendance_correction','attendance_status')
        widgets = {
        
                'approval_level'   : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'employee_id'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'employee_names'  : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'location'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'department'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'designation'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'responsibilities'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'attendance_status'  : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'attendance_correction'   : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            }

##
class PayrollSalaryVoucherForm(forms.ModelForm):
    class Meta:
        model = PayrollSalaryVoucher
        fields = ('month_and_year','gl_code','particulars', 'debit_amount','credit_amount')
        widgets = {
                'month_and_year' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'gl_code':  forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'particulars' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'debit_amount' : forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'credit_amount': forms.TextInput(attrs={'class': 'form-control', 'required':''}),

            }
class CustomModelEmployeePayrollProcessedHolidaysModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.leave_balance)
class CustomModelEmployeePayrollProcessedModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.claim_amount_1)
class CustomModelEmployeePayrollmonthandyeardModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.month_and_year)
class CustomModelEmployeePayrollGraddModel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.joining_grade_offered)
class EmployeePayrollProcessedForm(forms.ModelForm):
    leave_balance = CustomModelEmployeePayrollProcessedHolidaysModel(queryset=LeaveandHolidaysManagementUpdateLeavesQuota.objects.filter(is_active=1))
    leave_balance.widget.attrs['class'] = 'form-control'
    claim_amount_1 = CustomModelEmployeePayrollProcessedModel(queryset=EmployeeClaimandReimbursementSubmitClaims.objects.filter(is_active=1))
    claim_amount_1.widget.attrs['class'] = 'form-control'
    month_and_year = CustomModelEmployeePayrollmonthandyeardModel(queryset=EmployeePayrollProcessingUpdateAdvances.objects.filter(is_active=1))
    month_and_year.widget.attrs['class'] = 'form-control'


    joining_grade_offered = CustomModelEmployeePayrollGraddModel(queryset=EmployeeRegistrationUpdateRegistrationJoiningDetails.objects.filter(is_active=1))
    joining_grade_offered.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EmployeePayrollProcessed
        fields =('location','department','designation','month_and_year','employee_id','employee_names','pan_card_1', 'leave_without_pay','joining_grade_offered','days_in_month','monthly_off','working_days','holidays','leave_balance','leave_type',
            'basic_pay','hra_allowances','conveyance','claim_type','reimbursement_type_1','Incentive_1','performance_bonus','total','basic_pay','hra_allowances_1','conveyance_1',
            'claim_amount_1','Reimbursement','incentive_2','performance_bonus','total_1','pf','esic','absent','income','tax','loan_recovery','total_2','net_salary_payable',
            'bank_name','ifsc_code','account_number','amount','mode_of_payment','date_of_payment','date_of_processing')
        widgets = {
            'location' : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'designation' : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'department' : forms.Select(attrs={'class': 'form-control', 'required':''}),
            'month_and_year' : forms.Select(attrs={'class': 'form-control'}),
            'employee_id' : forms.Select(attrs={'class': 'form-control'}),
            'employee_names'  : forms.TextInput(attrs={'class': 'form-control'}),
            'days_in_month' : forms.Select(attrs={'class': 'form-control'}),
            'monthly_off' : forms.Select(attrs={'class': 'form-control'}),
            'working_days' : forms.Select(attrs={'class': 'form-control'}),
            'joining_grade_offered' : forms.Select(attrs={'class': 'form-control'}),
            'pan_card_1' : forms.TextInput(attrs={'class': 'form-control'}),
            'leave_without_pay' : forms.TextInput(attrs={'class': 'form-control'}),
            'holidays' : forms.TextInput(attrs={'class': 'form-control'}),
            'leave_balance' : forms.Select(attrs={'class': 'form-control'}),
            'leave_type' : forms.Select(attrs={'class': 'form-control'}),
            'basic_pay' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'hra_allowances' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'conveyance' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'claim_type' : forms.Select(attrs={'class': 'form-control'}),
            'reimbursement_type_1' : forms.Select(attrs={'class': 'form-control'}),   
            'Incentive_1' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'performance_bonus' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'total' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'basic_pay' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'hra_allowances_1' : forms.TextInput(attrs={'class': 'form-control'}),
            'conveyance_1' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'claim_amount_1': forms.Select(attrs={'class': 'form-control'}) ,
            'Reimbursement' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'incentive_2': forms.TextInput(attrs={'class': 'form-control','type':'number'}) ,
            'performance_bonus' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'total_1' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'pf' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'esic' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'absent' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'income' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'tax' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'loan_recovery' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'total_2' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'net_salary_payable' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'bank_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code' : forms.TextInput(attrs={'class': 'form-control'}),
            'account_number' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'amount' : forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'mode_of_payment' : forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_payment' : forms.TextInput(attrs={'class': 'form-control',"type":'date'}),
            'date_of_processing' : forms.TextInput(attrs={'class': 'form-control',"type":'date'}),
            # 'status' : forms.Select(attrs={'class': 'form-control'}),
        }

class EmployeePayrollProcessedFormUpdate(forms.ModelForm):
    class Meta:
        model = EmployeePayrollProcessed
        fields =('status',)
        widgets = {

            'status' : forms.Select(attrs={'class': 'form-control'}),
        }

class PayrollSalaryVoucherUpdateForm(forms.ModelForm):
    class Meta:
        model = PayrollSalaryVoucher
        fields =('approval_level',)
        widgets = {

            'approval_level' : forms.Select(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),

        }        

class PayrollStatutoryDeductionsForm(forms.ModelForm):
    class Meta:
        model = PayrollStatutoryDeductions
        fields =('user','deduction_type','employer_contribution','employee_contribution','month_and_year','others','total_deduction',
                    'approval_level'
        )
        widgets={
            'user' : forms.Select(attrs={'class': 'form-control'}),
            'deduction_type' : forms.Select(attrs={'class': 'form-control'}),
            'employer_contribution'  : forms.TextInput(attrs={'class': 'form-control'}),
            'employee_contribution' : forms.TextInput(attrs={'class': 'form-control'}),
            'month_and_year' : forms.TextInput(attrs={'class': 'form-control','type':'date'}),
            'others' : forms.TextInput(attrs={'class': 'form-control'}),
            'total_deduction' : forms.TextInput(attrs={'class': 'form-control'}),
            'status' : forms.Select(attrs={'class': 'form-control'}),
            'approval_level' : forms.Select(attrs={'class': 'form-control'}),
            'approval_level_all_status': forms.TextInput(attrs={'class': 'form-control'}),
             }

class PayrollStatutoryDeductionsUpdateForm(forms.ModelForm):
    class Meta:
        model = PayrollStatutoryDeductions
        fields =('status',)
        widgets = {

            
            'status' : forms.Select(attrs={'class': 'form-control'}),

        }        


