from django import forms
from .models import *
from django.db.models import Q

# =================== Custom Filters 

class CustomModelFilter(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class CustomModelFilterCrmManageBranch(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.branch_id)


class CustomModelFilterUser(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CustomModelFilterReportedUserUser(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CustomModelFilter1(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.type_of_currency)


class CustomHeadOffice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.hod_id)


class CustomModelFilter2(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.purpose_of_currency)


class CustomModelDesignation(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.designation)


class CustomModelDepartment(forms.ModelChoiceField):
    def label_frominstance(self, obj):
        return "%s" % (obj.department)


class CustomModelResponsibility(forms.ModelChoiceField):
    def label_frominstance(self, obj):
        return "%s" % (obj.responsibilities)

class CustomModelUserLevel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.email)

class CustomModelReportingType(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CustomModelReportingLevel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

# =================== End Custom Filters 

class CrmProductForm(forms.ModelForm):

    class Meta:

        model = CompanySetup
        fields = ('company_id', 'name','building','block_no','sector','country','state','city','district','pincode','cin_no',
            'pan_card','gst_no','tan_no','website','email_id','contact_no','local_currency','reporting_currency','start_date', 'logo_upload','is_active')
        
        widgets = {
            'company_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'country': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'cin_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'pan_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'tan_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'local_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'reporting_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.fields['local_currency'].queryset = TypeofCurrency.objects.filter(is_active = True)
    #         self.fields['reporting_currency'].queryset = reporting_currency.objects.filter(is_active = True)
            
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['state'].queryset = State.objects.none()
    #     self.fields['city'].queryset = City.objects.none()


class UpdateCrmProductForm(forms.ModelForm):

    class Meta:
        model = CompanySetup
        fields = ('company_id', 'name','building','block_no','sector','country','state','city','district','pincode','cin_no',
            'pan_card','gst_no','tan_no','website','email_id','contact_no','local_currency','reporting_currency','start_date', 'logo_upload','is_active')
        
        widgets = {
            'company_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'country': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'cin_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'pan_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'tan_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'local_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'reporting_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['local_currency'].queryset = TypeofCurrency.objects.filter(is_active = True)
            self.fields['reporting_currency'].queryset = reporting_currency.objects.filter(is_active = True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('-id')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['state'].queryset = State.objects.filter(country_id=self.instance.country_id).order_by('-id')
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('-id')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(state_id=self.instance.state_id).order_by('-id')


class CrmAddHeadofficeForm(forms.ModelForm):

    class Meta:
        model = ManageHeadOfficeSetup

        fields = ('parent_company','hod_id', 'name','building','block_no','sector','country','state','city','district','pincode','cin_no',
            'pan_card','gst_no','website','email_id','contact_no','local_currency','reporting_currency','start_date','is_active')

        widgets = {
            'parent_company': forms.Select( attrs={'class': 'form-control'}),
            'hod_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'city': forms.TextInput( attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'state': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'country': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'cin_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'pan_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'local_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'reporting_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['local_currency'].queryset = TypeofCurrency.objects.filter(is_active = True)
            self.fields['reporting_currency'].queryset = reporting_currency.objects.filter(is_active = True)
            self.fields['parent_company'].queryset = CompanySetup.objects.filter(is_active=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()


class CrmUpdateHeadofficeForm(forms.ModelForm):



    class Meta:
        model = ManageHeadOfficeSetup
        fields = ('parent_company','hod_id', 'name','building','block_no','sector','country','state','city','district','pincode','cin_no',
            'pan_card','gst_no','website','email_id','contact_no','local_currency','reporting_currency','start_date','is_active')

        widgets = {
            'parent_company': forms.Select( attrs={'class': 'form-control'}),
            'hod_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'city': forms.Select( attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'state': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'country': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'cin_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'pan_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'typr':'number'}),
            'local_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'reporting_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['local_currency'].queryset = TypeofCurrency.objects.filter(is_active = True)
            self.fields['reporting_currency'].queryset = reporting_currency.objects.filter(is_active = True)
            self.fields['parent_company'].queryset = CompanySetup.objects.filter(is_active=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('-id')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['state'].queryset = State.objects.filter(country_id=self.instance.country_id).order_by('-id')
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('-id')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(state_id=self.instance.state_id).order_by('-id')


class CrmAddBranchForm(forms.ModelForm):

    head_office = CustomHeadOffice(queryset=ManageHeadOfficeSetup.objects.filter( is_active=1))
    head_office.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageBranch
        fields = ('parent_company','head_office','branch_id', 'name_of_branch','building','block_no','sector','country','state','city','district','pincode',
           'gst_no','email_id','contact_no','local_currency','reporting_currency','start_date', 'is_active')
        
        widgets = {
            'parent_company': forms.Select( attrs={'class': 'form-control'}),
            'head_office': forms.Select( attrs={'class': 'form-control'}),
            'branch_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'name_of_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'city': forms.TextInput( attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'state': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'country': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'local_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'reporting_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['local_currency'].queryset = TypeofCurrency.objects.filter(is_active = True)
            self.fields['reporting_currency'].queryset = reporting_currency.objects.filter(is_active = True)
            self.fields['parent_company'].queryset = CompanySetup.objects.filter(is_active=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()


class CrmUpdateBranchForm(forms.ModelForm):

    head_office = CustomHeadOffice(queryset=ManageHeadOfficeSetup.objects.filter( is_active=1))
    head_office.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageBranch
        fields = ('parent_company','head_office','branch_id', 'name_of_branch','building','block_no','sector','country','state','city','district','pincode',
           'gst_no','email_id','contact_no','local_currency','reporting_currency','start_date', 'is_active')
        
        widgets = {
            'parent_company': forms.Select( attrs={'class': 'form-control'}),
            'head_office': forms.Select( attrs={'class': 'form-control'}),
            'branch_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'name_of_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'block_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'city': forms.Select( attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'state': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'country': forms.Select( attrs={'class': 'form-control', 'required': ''}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'local_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'reporting_currency': forms.Select(attrs={'class': 'form-control multiselect', 'multiple': 'multiple'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['local_currency'].queryset = TypeofCurrency.objects.filter(is_active = True)
            self.fields['reporting_currency'].queryset = reporting_currency.objects.filter(is_active = True)
            self.fields['parent_company'].queryset = CompanySetup.objects.filter(is_active=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('-id')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['state'].queryset = State.objects.filter(country_id=self.instance.country_id).order_by('-id')
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('-id')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(state_id=self.instance.state_id).order_by('-id')


class CrmCityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('country', 'state', 'name','district','is_active')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':'', "id":"manage_city"}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'state': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()


class CrmCityEditForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('country', 'state', 'name','district','is_active')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':'', "id":"manage_city"}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'state': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomCrmRoleManagementForm(forms.ModelChoiceField):
    def label_frominstance(self, obj):
        return "%s" % (obj.name)

class CrmUserSetupForm(forms.ModelForm):


    user_role = CustomCrmRoleManagementForm(queryset=RoleMangement.objects.filter(is_active=1))
    user_role.widget.attrs['class'] = 'form-control'
    user_role.widget.attrs['class'] = 'multiselect'
    user_role.widget.attrs['multiple'] = 'multiple'

    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'


    reporting_to = CustomModelFilterReportedUserUser(queryset=User.objects.filter(manual_create_admin = 1, is_active=1))
    reporting_to.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('name','designation','department','email','mobile_no','parent_company', 'head_office','user_role', 'responsibilities', 'reporting_to', 'start_date','user_pics','is_active')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'designation': forms.Select( attrs={'class': 'form-control'}),
            'department': forms.Select( attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'parent_company': forms.Select(attrs={'class': 'form-control', 'id':''}),
            'head_office': forms.Select(attrs={'class': 'form-control', 'id':''}),
            'user_role': forms.Select(attrs={'class': 'form-control ', 'placeholder':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'reporting_to': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            }


class CrmUserSetupEditForm(forms.ModelForm):

    user_role = CustomCrmRoleManagementForm(queryset=RoleMangement.objects.filter(is_active=1))
    user_role.widget.attrs['class'] = 'form-control'
    user_role.widget.attrs['class'] = 'multiselect'
    user_role.widget.attrs['multiple'] = 'multiple'
    reporting_to = CustomModelFilterReportedUserUser(queryset=User.objects.filter(manual_create_admin = 1, is_active=1))
    reporting_to.widget.attrs['class'] = 'form-control'
    responsibilities = CustomModelResponsibility(queryset=ManageResponsibility.objects.filter(is_active=1))
    responsibilities.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('name','designation','department','email','mobile_no', 'parent_company', 'head_office','user_role', 'responsibilities', 'reporting_to', 'start_date', 'user_pics', 'gen_password','is_active')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'designation': forms.Select( attrs={'class': 'form-control'}),
            'department': forms.Select( attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'parent_company': forms.Select(attrs={'class': 'form-control', 'id':''}),
            'head_office': forms.Select(attrs={'class': 'form-control', 'id':''}),
            'user_role': forms.Select(attrs={'class': 'form-control multiselect', 'placeholder':'', 'multiple':''}),
            'responsibilities': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'reporting_to': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'gen_password': forms.TextInput(attrs={'class': 'form-control', 'minlength':'10'}),
            }


class CrmDepartmentAddForm(forms.ModelForm):

    class Meta:
        model = ManageDepartment
        fields = ('department', 'is_active')

        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }

class CrmDesignationAddForm(forms.ModelForm):

    class Meta:
        model = ManageDesignation
        fields = ('designation','is_active')

        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmResponsibilityAddForm(forms.ModelForm):

    class Meta:
        model = ManageResponsibility
        fields = ('responsibilities', 'is_active')

        widgets = {
            'responsibilities': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }



class UserTypeAddForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ('user_type','is_active')

        widgets = {
            'user_type': forms.TextInput(attrs={'class': 'form-control', 'required':''}),}




class UnitValueForm(forms.ModelForm):
    class Meta:
        model = UnitValue
        fields = ('unit_value','description','start_date','end_date','is_active')

        widgets = {
                'unit_value': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
                }

class CrmProductSetupForm(forms.ModelForm):

    class Meta:
        model = ManageProductType
        fields = ('product_type','product_description','start_date','end_date', 'is_active')

        widgets = {
                'product_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
                'product_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
                'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
                'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            }

# Product Management
class ManageProductCategoryForm(forms.ModelForm):

    class Meta:
        model = ManageProductCategory
        fields = ('product_category','description','start_date','end_date','is_active')

        widgets = {
                'product_category': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
               
                }

class ProductNameForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    start_date.widget.attrs['class'] = 'form-control'
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    end_date.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ManageProductName
        fields = ('product_name','description','start_date','end_date','is_active')
        widgets = {
                'product_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ProductFacilityForm(forms.ModelForm):
    class Meta:
        model = ProductFacility
        fields = ('product_facility','description','start_date','end_date','is_active')

        widgets = {
                'product_facility': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
                }

class CrmtemplateclienttypeForm(forms.ModelForm):

    class Meta:
        model = TemplateSetupClientType
        fields = ('name','is_active')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmtemplateclientcategoryForm(forms.ModelForm):

    class Meta:
        model = TemplateSetupClientCategory
        fields = ('name','is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
##################################
class CustomModelFilterUpdateTemplateTypeForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.template_type)


    


class UpdateTemplateTypeForm(forms.ModelForm):
    template_type = CustomModelFilterUpdateTemplateTypeForm(queryset=CustomizeTemplate.objects.filter(is_active=1))
    template_type.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UpdateTemplateType
        fields = ('template_type','description','is_active')

        widgets = {
                'template_type' : forms.Select(attrs={'class': 'form-control', 'required':''}),
                'description': forms.TextInput(attrs={'class': 'form-control'}),
                
                }



##


class CustomModelFilterUpdatePurposeofTemplateForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.rating)

    

class UpdatePurposeofTemplateForm(forms.ModelForm):
    template_type = CustomModelFilterUpdatePurposeofTemplateForm(queryset=CustomizeTemplate.objects.all())
    template_type.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = UpdatePurposeofTemplate
        fields = ('template_type','purpose','description','is_active')

        widgets = {
                'template_type' : forms.Select( attrs={'class': 'form-control'}),
                'purpose': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'description': forms.TextInput(attrs={'class': 'form-control'}),
                
                }

##############
class AdditionalTemplateForm(forms.ModelForm):  
    class Meta:
        model = AdditionalTemplate
        fields = ('template_type','client_type','client_role','client_category','select_field','master','Field_role','form_display','is_active')

        widgets = {
                'template_type' : forms.Select( attrs={'class': 'form-control'}),
                'client_type' : forms.Select( attrs={'class': 'form-control'}),
                'client_role' : forms.Select( attrs={'class': 'form-control'}),
                'client_category' : forms.Select( attrs={'class': 'form-control'}),
                'select_field' : forms.TextInput( attrs={'class': 'form-control'}),
                'master' : forms.TextInput( attrs={'class': 'form-control'}),
                'Field_role' : forms.Select( attrs={'class': 'form-control'}),
                'form_display' : forms.Select( attrs={'class': 'form-control'}),
                
              
                }


##

class ApplicationFormForm(forms.ModelForm):  
    class Meta:
        model = ApplicationForm
        fields = ('template_type','client_type','client_role','client_category','select_field','master','Field_role','form_display','is_active')

        widgets = {
                'template_type' : forms.Select( attrs={'class': 'form-control'}),
                'client_type' : forms.Select( attrs={'class': 'form-control'}),
                'client_role' : forms.Select( attrs={'class': 'form-control'}),
                'client_category' : forms.Select( attrs={'class': 'form-control'}),
                'select_field' : forms.TextInput( attrs={'class': 'form-control'}),
                'master' : forms.TextInput( attrs={'class': 'form-control'}),
                'Field_role' : forms.Select( attrs={'class': 'form-control'}),
                'form_display' : forms.Select( attrs={'class': 'form-control'}),
                
              
                }














class CrmCustomizeTemplateForm(forms.ModelForm):

    class Meta:
        model = CustomizeTemplate
        fields = ('template_type','template_name','purpose','upload')

        widgets = {
            'template_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'template_name': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TypeofcurrencyForm(forms.ModelForm):

    class Meta:
        model = TypeofCurrency
        fields = ('type_of_currency','is_active')

        widgets = {
            'type_of_currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class PurposeofcurrencyForm(forms.ModelForm):

    class Meta:
        model = PurposeofCurrency
        fields = ('purpose_of_currency','is_active')

        widgets = {
            'purpose_of_currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }

#########currency Rate 

class CurrencyRateForm(forms.ModelForm):

    class Meta:
        model = CurrencyRate
        fields = ("date","currency_type","buy_rate", "sell_rate","average" ,"description","is_active")





        widgets = {
            'date' : forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'buy_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
             'sell_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'average': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
           
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }



class CrmCurrencySetUpForm(forms.ModelForm):

    country = CustomModelFilter(queryset=Country.objects.filter(is_active=1))
    country.widget.attrs['class'] = 'form-control'
    type_of_currency = CustomModelFilter1(queryset=TypeofCurrency.objects.filter(is_active=1))
    type_of_currency.widget.attrs['class'] = 'form-control'
    purpose_of_currency = CustomModelFilter2(queryset=PurposeofCurrency.objects.filter(is_active=1))
    purpose_of_currency.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CurrencySetup
        fields = ('country','type_of_currency','purpose_of_currency','description', 'is_active')

        widgets = {
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'type_of_currency': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'purpose_of_currency': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class EscalationMatrixDefineLevelForm(forms.ModelForm):

    designation = CustomModelDesignation(queryset=ManageDesignation.objects.filter(is_active=1))
    designation.widget.attrs['class'] = 'form-control'
    department = CustomModelDepartment(queryset=ManageDepartment.objects.filter(is_active=1))
    department.widget.attrs['class'] = 'form-control'
    class Meta:
        model = EscalationMatrixDefineLevel
        fields = ('level','department','designation','location', 'is_active')

        widgets = {
            'level': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'location': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmNotificationEscalationMatrixDefineTurnAroundTimeForm(forms.ModelForm):
    user = CustomModelFilterUser(queryset=User.objects.filter(~Q(is_superuser = 1), is_active=1))
    user.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EscalationMatrixDefineTurnAroundTime
        fields = ('user','tat_in_hours_days','purpose','remark', 'is_active')

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'tat_in_hours_days': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'tat_in_hours_days': forms.TextInput(attrs={'class': 'form-control', 'type':'number'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmNotificationNotificationSubjectForm(forms.ModelForm):

    class Meta:
        model = NotificationSubject
        fields = ('notification_subject','description','is_active')

        widgets = {
            'notification_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


########################  Notification Method ###############
class DefineSmsNotificationActionFrom(forms.ModelForm):

    class Meta:
        model = NotificationAction
        fields = ('notification_action','description','is_active')
        widgets = {
            'notification_action': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }



class CrmSmsNotificationTypeForm(forms.ModelForm):

    class Meta:
        model = NotificationType
        fields = ('notification_type','purpose','is_active')

        widgets = {
            'notification_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmSmsNotificationFrequencyForm(forms.ModelForm):

    class Meta:
        model = NotificationFrequency
        fields = ('notification_frequency','days', 'date' ,'time','purpose','is_active')

        widgets = {
            'notification_frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'days': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmSmsDefineTypeofMessageForm(forms.ModelForm):

    class Meta:
        model = ImportanceofNotification
        fields = ('importance_type','purpose','is_active')

        widgets = {
            'importance_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmSmsDefineImportofMessageForm(forms.ModelForm):

    class Meta:
        model = TargetAudience
        fields = ('target_audience', 'source', 'purpose','is_active')

        widgets = {
            'target_audience': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            }


class CrmSmsDefineGroupofMessageForm(forms.ModelForm):

    class Meta:
        model = NotificationGroup
        fields = ('notification_group', 'notification_method','notification_type','purpose','is_active')

        widgets = {
            'notification_group': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'notification_method': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'notification_type': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }

#  ======================== Access and Permisson SetUp ===========================
class CrmDefinePermissionTypesForm(forms.ModelForm):

    class Meta:
        model = ManagePermissionTypes
        fields = ('permission_type','description', 'is_active')

        widgets = {
            'permission_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }

class CrmCrmDefinePermissionLevelForm(forms.ModelForm):

    class Meta:
        model = ManagePermissionLevel
        fields = ('permission_level','description', 'is_active')

        widgets = {
            'permission_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }

class CrmDefinePermissionReportingTypeForm(forms.ModelForm):

    class Meta:
        model = ManagePermissionReportingType
        fields = ('name', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmDefinePermissionReportingLevelForm(forms.ModelForm):

    class Meta:

        model = ManagePermissionReportingLevel
        fields = ('name', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmDefinePermissionDefineHierarchyForm(forms.ModelForm):

    reporting_type = CustomModelReportingType(queryset=ManagePermissionReportingType.objects.filter(is_active=1))
    reporting_type.widget.attrs['class'] = 'form-control'
    reporting_level = CustomModelReportingLevel(queryset=ManagePermissionReportingLevel.objects.filter(is_active=1))
    reporting_level.widget.attrs['class'] = 'form-control'
    user = CustomModelUserLevel(queryset=User.objects.filter(is_active=1, is_superuser= 0))
    user.widget.attrs['class'] = 'form-control'
    
    class Meta:

        model = ManagePermissionReportingHierarchy
        fields = ('user','designation','department','responsibility','reporting_type','reporting_level','is_active')
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'reporting_type': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'reporting_level': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'', 'readonly':""}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'', 'readonly':""}),
            'responsibility': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'', 'readonly':""}),
        }

# ============================ Calls and GPS Setup – Masters > Manage Call Recording > Preference

class CustomModelCallTypeLevel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class CustomModelCallPreferenceLevel(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class CrmAddEditMisReportingManagePerformanceDefineTargetForm(forms.ModelForm):
    # user = CustomModelUserLevel(queryset=User.objects.filter(is_active=1, is_superuser= 0))
    # user.widget.attrs['class'] = 'form-control'
    
    class Meta:

        model = MisManagePerformanceDefineTarget
        fields = ('user', 'target_type', 'target', 'period_of_type', 'nature_of_target', 'description' ,'is_active')
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'target_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'','multiple':''}),
            'target': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'period_of_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'', 'multiple':''}),
            'nature_of_target': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'','type':'number'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmAddEditManageReportManageReportFormatForm(forms.ModelForm):
    
    class Meta:

        model = MisManageReportingReportFormat
        fields = ('format_type', 'description', 'is_active')
        widgets = {
            'format_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CrmMisReportingManageReportFrequencyForm(forms.ModelForm):
    
    class Meta:
        
        model = MisManageReportingReportFrequency
        fields = ('reporting_frequency', 'description', 'is_active')
        widgets = {
            'reporting_frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class CustomModelNotificationSubject(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.notification_subject)

class CustomModelNotificationType(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.notification_type)

class CustomModelNotificationGroup(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.notification_group)

class CustomModelNotificationimportance(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.importance_type)

class CustomModelNotificationTargetAudience(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.target_audience)


class CustomModelNotificationSource(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.source)


class CustomModelNotificationFrequencyType(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.notification_frequency)


class CrmDefineTemplateForNotificationForm(forms.ModelForm):

    notification_method = CustomModelNotificationSubject(queryset=NotificationSubject.objects.filter(is_active=1))
    notification_method.widget.attrs['class'] = 'form-control'

    notification_importance = CustomModelNotificationimportance(queryset=ImportanceofNotification.objects.filter(is_active=1))
    notification_importance.widget.attrs['class'] = 'form-control'

    notification_frequency_type = CustomModelNotificationFrequencyType(queryset=NotificationFrequency.objects.filter(is_active=1))
    notification_frequency_type.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TemplateForNotification
        fields = ('notification_method', 'action', 'notification_subject', 'notification_importance', 'notification_frequency_type', 'target_audience' ,'template', 'is_active')
        widgets = {
            'notification_method': forms.Select(attrs={'class': 'form-control'}),
            'action': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'notification_subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'notification_importance': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'predefined_notification': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'target_audience': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            'template': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["template"].widget = forms.Textarea()


class UpdateAdministratorProfielForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_no')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
        }

class UpdateSuperUserAdministratorProfielForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_no','gen_password','user_pics', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type':'email'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gen_password': forms.TextInput(attrs={'class': 'form-control', 'minlength':'10'}),
        }


class CrmApprovalMatrixiDefineApprovalLevelForm(forms.ModelForm):
    
    class Meta:
        model = ApprovalMatrixiDefineApprovalLevel
        fields = ('approval_level', 'description', 'is_active')
        widgets = {
            'approval_level': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmApprovalMatrixiDefineProcessLevelForm(forms.ModelForm):
    
    class Meta:
        model = ApprovalMatrixDefineProcesLevel
        fields = ('process_level', 'description', 'is_active')
        widgets = {
            'process_level': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class CrmApprovalMatrixMapApprovalLevelWithUsersForm(forms.ModelForm):
    user = CustomModelFilterUser(queryset=User.objects.filter(~Q(is_superuser = 1), is_active=1))
    user.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ApprovalMatrixMapApprovalLevelWithUsers
        fields = ('user', 'description', 'is_active')
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'required':''}),
            'description': forms.TextInput(attrs={'class': 'form-control ', 'required':''}),
        }



# Product Category
class ManageProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ManageProductCategory
        fields = ('product_category','description','start_date','end_date','is_active')

        widgets = {
                'product_category': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'start_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                'end_date': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
               
                }

class CountryAddForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = ('name','is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':'', "id":"manage_city"}),
            
            }

class CrmStateAddForm(forms.ModelForm):

    class Meta:
        model = State
        fields = ('country', 'name', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'country': forms.Select(attrs={'class': 'form-control', 'required':'', "id":"manage_country"}),
            }

#######################
#@2

class DefineProcessAllocationForm(forms.ModelForm):

    class Meta:
        model = DefineProcessAllocation
        fields=('process_name', 'sub_process_name', 'child_process_name' ,'description','is_active')
        widgets={
        'process_name':forms.TextInput(attrs={'class': 'form-control' }),
        'sub_process_name':forms.TextInput(attrs={'class': 'form-control' }),
        'child_process_name':forms.TextInput(attrs={'class': 'form-control' }),
        'description':forms.TextInput(attrs={'class': 'form-control' }),
    }


#
class AllocationManagementUpdateReallocationCriteriaForm(forms.ModelForm):
    class Meta:
        model = AllocationManagementUpdateReallocationCriteria
        fields = ('reallocation_criteria', 'description', 'is_active')
        widgets = {
            # 'process_name': forms.Select( attrs={'class': 'form-control'}),
            'reallocation_criteria': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


#@1


class AllocationManagementManageReallocationForm(forms.ModelForm):

    new_user = CustomModelFilterReportedUserUser(queryset=User.objects.filter(manual_create_admin = 1, is_active =True, is_superuser=0,is_client=0,is_agent=0,is_verification_agency=0,is_legal_team=0,is_technical_team=0,is_valuation_team=0,is_fraud_investigation_team=0,is_document_verification_team=0))
    new_user.widget.attrs['class'] = 'form-control'

    class Meta:
        model = AllocationManagementManageReallocation
        fields = ('existing_user', 'process_name', 'reallocation_criteria', 'new_user', 'is_active')
        widgets = {
            'existing_user' : forms.Select( attrs={'class': 'form-control'}),
            'process_name': forms.TextInput(attrs={'class': 'form-control'}),
            'reallocation_criteria': forms.Select(attrs={'class': 'form-control'}),
            'existing_user': forms.Select(attrs={'class': 'form-control'}),
            'new_user': forms.Select(attrs={'class': 'form-control'}),
        }
        def __init__(self, user, *args, **kwargs):
            super(AllocationManagementManageReallocationForm, self).__init__(*args, **kwargs)
            self.fields['reallocation_criteria'].queryset = AllocationManagementUpdateReallocationCriteria.objects.filter( is_active=1)

#@!!

class MapApprovalLevelWithJointApprovalForm(forms.ModelForm):
    # user_joint_approval = CustomModelFilterUser(queryset=User.objects.filter(is_superuser=0,is_client=0,is_agent=0,is_verification_agency=0,is_legal_team=0,is_technical_team=0,is_valuation_team=0,is_fraud_investigation_team=0,is_document_verification_team=0))
    # user_joint_approval.widget.attrs['class'] = 'form-control'
    # user_joint_approval.widget.attrs['multiple'] = ''
    

    class Meta:
        model = MapApprovalLevelWithJointApproval
        fields = ('group_name','no_of_users','user_joint_approval','works_flow_process','approval_level','loan_limit','is_active')
        widgets = {
            # 'work_flow_process': forms.Select(attrs={'class': 'form-control', 'required':''}),

            'group_name':forms.TextInput(attrs={'class': 'form-control' , 'required':''}),
            'no_of_users':forms.TextInput(attrs={'class': 'form-control' , 'required':''}),
            'works_flow_process': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'user_joint_approval':forms.Select(attrs={'class': 'form-control' , 'required':'','multiple':''}),
            # 'department':forms.Select(attrs={'class': 'form-control' , 'required':''}),
            # 'designation':forms.Select(attrs={'class': 'form-control' , 'required':''}),
            # 'responsibilities':forms.Select(attrs={'class': 'form-control' , 'required':''}),
            'approval_level':forms.Select(attrs={'class': 'form-control' , 'required':'', 'multiple':''}),
            'loan_limit':forms.TextInput(attrs={'class': 'form-control' , 'required':''}),
                    }

    # def __init__(self, *args, **kwargs):
    #     super(MapApprovalLevelWithJointApprovalForm, self).__init__(*args, **kwargs)
    #     self.fields['user_joint_approval'].label = "User Name"

###1
class EscalationManagementManageEscalationForm(forms.ModelForm):
    # user = CustomModelFilterUser(queryset=User.objects.filter(~Q(is_superuser = 1), is_active=1))
    # user.widget.attrs['class'] = 'form-control'
    escalation_to = CustomModelFilterReportedUserUser(queryset=User.objects.filter(manual_create_admin = 1, is_active =True, is_superuser=0,is_client=0,is_agent=0,is_verification_agency=0,is_legal_team=0,is_technical_team=0,is_valuation_team=0,is_fraud_investigation_team=0,is_document_verification_team=0))
    escalation_to.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EscalationManagementManageEscalation   
        fields = ('user', 'effect_of_escalation_level','process_name', 'escalation_to', 'is_active')
        widgets = {
            'user': forms.Select( attrs={'class': 'form-control'}),
            'effect_of_escalation_level': forms.Select(attrs={'class': 'form-control'}),
            'process_name': forms.Select(attrs={'class': 'form-control'}),
            'escalation_to': forms.Select(attrs={'class': 'form-control'}),
        }

class ManageMonthEndProcessForm(forms.ModelForm):

    # monthandyear = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),input_formats=('%d/%m/%Y', ))
    # monthandyear.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ManageMonthEndProcess
        fields = ('monthandyear','extended_by_days','new_date','description','is_active')
        widgets = {
            'process_name': forms.Select( attrs={'class': 'form-control'}),
            
            'month_end_type': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthandyear': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'extended_by_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'new_date': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'})
            }


    def __init__(self, *args, **kwargs):
        super(ManageMonthEndProcessForm, self).__init__(*args, **kwargs)
        self.fields['monthandyear'].label = "Month & Year"

#
class ManageProductsForm(forms.ModelForm):

    class Meta:
        model = ManageProducts
        fields = ('product_type','product_name','description','is_active')
        widgets = {
                'product_type': forms.TextInput(attrs={'class': 'form-control'}),
                'product_name': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
        }





class ManageUpdateRevenueForm(forms.ModelForm):

    class Meta:
        model = ManageUpdateRevenue
        fields = ('revenue_type','revenue_name','description','is_active')
        widgets = {
                'revenue_type': forms.TextInput(attrs={'class': 'form-control'}),
                'revenue_name': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
        }

class ManageUpdateTaxRatesForm(forms.ModelForm):

    class Meta:
        model = ManageUpdateTaxRates
        fields = ('taxation_type','taxation_name','rate', 'unit_value','description','is_active')
        widgets = {
                'taxation_type': forms.TextInput(attrs={'class': 'form-control'}),
                'taxation_name': forms.TextInput(attrs={'class': 'form-control'}),
                'rate': forms.TextInput(attrs={'class': 'form-control'}),
                'unit_value': forms.Select(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
        }



class ManagePricingForm(forms.ModelForm):
    class Meta:
        model = ManagePricing 
        
        fields = ('product_type','product_name','revenue_type','revenue_name','revenue_rate', 'unit_value','taxation_type','taxation_name','rate', 'unit_value','description','is_active')
        widgets = {
                 'product_type': forms.TextInput(attrs={'class': 'form-control'}),
                  'product_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'revenue_type': forms.TextInput(attrs={'class': 'form-control'}),
                   'revenue_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'revenue_rate' : forms.TextInput(attrs={'class': 'form-control'}),
                   'unit_value' : forms.TextInput(attrs={'class': 'form-control'}),
                    
                'taxation_type': forms.TextInput(attrs={'class': 'form-control'}),
                'taxation_name': forms.TextInput(attrs={'class': 'form-control'}),
                'rate': forms.TextInput(attrs={'class': 'form-control'}),
                'unit_value': forms.Select(attrs={'class': 'form-control'}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
                
        }



################
class ManageUpdateEmploymentTypeForm(forms.ModelForm):

    class Meta:
        model = ManageUpdateEmploymentType
        fields = ('employee_type', 'is_active')

        widgets = {
            'employee_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


###########Country 
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("name","sortname","phoneCode","is_active")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'sortname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'phoneCode': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }



#####State
class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ("name","country","is_active")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            
        }

############

class UpdateTemplateRequirementForm(forms.ModelForm):
    class Meta:
        model = UpdateTemplateRequirement
        fields = ("client_type","client_role","client_category", "is_active")
        widgets = {
            'client_type': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
 
            'client_role': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'client_category': forms.Select(attrs={'class': 'form-control', 'placeholder':''}),
            
        }



class TemplateCreateFieldsForm(forms.ModelForm):
    class Meta:
        model = TemplateCreateFields
        fields = ('subfield_name','length_of_field','field_type','validation_required','validation_type','mandatory')

        widgets = {
            'subfield_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'length_of_field': forms.TextInput(attrs={'class': 'form-control'}),
            'field_type': forms.Select(attrs={'class': 'form-control'}),
            

            'validation_required': forms.Select(attrs={'class': 'form-control'}),
            'validation_type': forms.Select(attrs={'class': 'form-control'}),
            'mandatory': forms.Select(attrs={'class': 'form-control'}),}

###############
class AllocationMatrixsClientSupportForm(forms.ModelForm):
    class Meta:
        model = AllocationMatrixsClientSupport
        fields =( 'user','department','designation','responsibilities','branch_id','client_type','name','is_active')
        
        widgets ={
        'user'  : forms.Select(attrs={'class': 'form-control'}),
        'department' : forms.Select(attrs={'class': 'form-control'}),
        'designation' : forms.Select(attrs={'class': 'form-control'}),
        'responsibilities' : forms.Select(attrs={'class': 'form-control'}),
        'branch_id' : forms.Select(attrs={'class': 'form-control'}),
        'client_type' : forms.Select(attrs={'class': 'form-control'}),
        'name' : forms.Select(attrs={'class': 'form-control'}),
        }