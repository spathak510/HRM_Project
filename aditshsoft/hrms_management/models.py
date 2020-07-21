from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from jsonfield import JSONField
from datetime import datetime
import random
import string
# Create your models here.


class Country(models.Model):
    name = models.CharField(unique = True, max_length=100, default = '', null= True, verbose_name="Country Name")
    sortname = models.CharField(max_length=100, default = '', null= True, verbose_name="Sort Name")
    phoneCode = models.CharField(max_length=100, default = '',null= True, verbose_name="Phone Code")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "manage_master_country"


class State(models.Model):
    name = models.CharField(max_length=100, verbose_name="State Name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name = "Country")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "manage_master_state"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name="City Name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True,blank=True)
    state  = models.ForeignKey(State, on_delete=models.CASCADE,null=True,blank=True)
    district = models.CharField(max_length=500, verbose_name="District",null=True,blank=True)
    uploaded_by_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = "manage_master_city"

# class City(models.Model):
#     name = models.CharField(max_length=100,  null=True,  blank=True, verbose_name = "City Name")
#     country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True,  blank=True, verbose_name = "Country")
#     state  = models.ForeignKey(State, on_delete=models.CASCADE, null=True,  blank=True, verbose_name = "State")
#     district = models.CharField(max_length=500, blank=True, null=True, verbose_name="District")
#     uploaded_by_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = "manage_master_city"


class TypeofCurrency(models.Model):
    type_of_currency = models.CharField(unique = True, max_length=100, null=False, default ='', verbose_name = "Type of Currency")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_of_currency

    class Meta:
         db_table = "manage_type_of_currency"


class PurposeofCurrency(models.Model):
    purpose_of_currency = models.CharField(unique = True, max_length=100, null=False, default ='', verbose_name = "Purpose of Currency")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purpose_of_currency

    class Meta:
         db_table = "manage_purpose_of_currency"


class CurrencySetup(models.Model):
    country = models.ForeignKey(Country, null=True,  on_delete=models.CASCADE, verbose_name = "Country")
    type_of_currency = models.ForeignKey(TypeofCurrency,  null=True,  on_delete=models.CASCADE, verbose_name = "Type of Currency")
    purpose_of_currency = models.ForeignKey(PurposeofCurrency,  null=True,  on_delete=models.CASCADE, verbose_name = "Purpose of Currency")
    description = models.CharField(max_length=250, null=False, default ='', verbose_name = "Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "manage_currency_set_up"
##############Currency Rate

class CurrencyRate(models.Model):
    date          = models.DateField(blank = True, null =True, verbose_name="Date")
    currency_type = models.CharField(unique = True, max_length=100, null=False, default ='', verbose_name = "Currency Type")
    buy_rate      = models.CharField(max_length=100, null=False, default ='', verbose_name = "Buy Rate")
    sell_rate     = models.CharField(max_length=100, null=False, default ='', verbose_name = "sell Rate")
    average       = models.CharField(max_length=100, null=False, default ='', verbose_name = "Average")
    description   = models.CharField(max_length=300, null=False, default ='', verbose_name = "Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_type

    class Meta:
         db_table = "currency_rate"



class ManageFinancialYear(models.Model):
    to_month = models.IntegerField(default=0,  blank=True, null=True, verbose_name="To Month")
    from_month = models.IntegerField(default=0,  blank=True, null=True, verbose_name="From Month")
    to_year = models.IntegerField(default=0,  blank=True, null=True, verbose_name="To Year")
    from_year = models.IntegerField(default=0,  blank=True, null=True, verbose_name="From Year")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return str(self.from_year)
        
    class Meta:

        db_table = "manage_financial_year"

#############  Assessment
class ManageAssessmentYear(models.Model):
    to_month = models.IntegerField(default=0,  blank=True, null=True, verbose_name="To Month")
    from_month = models.IntegerField(default=0,  blank=True, null=True, verbose_name="From Month")
    to_year = models.IntegerField(default=0,  blank=True, null=True, verbose_name="To Year")
    from_year = models.IntegerField(default=0,  blank=True, null=True, verbose_name="From Year")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return str(self.from_year)
        
    class Meta:

        db_table = "manage_assessment_year"
class ManageFinancialReport(models.Model):
    to_month = models.IntegerField(default=0,  blank=True, null=True, verbose_name="To Month")
    from_month = models.IntegerField(default=0,  blank=True, null=True, verbose_name="From Month")
    to_year = models.IntegerField(default=0,  blank=True, null=True, verbose_name="To Year")
    from_year = models.IntegerField(default=0,  blank=True, null=True, verbose_name="From Year")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:

        db_table = "manage_financial_report"


WORKINGDAYS = (
    (1, 'Normal Working Days'),
    (2, 'Week end working Days'),
    (2, 'Half Working Days'),
)


class ManageWorkingHours(models.Model):
    working_days = models.IntegerField(unique = True,choices=WORKINGDAYS, default=1,  blank=True, null=True, verbose_name="Working Days")
    start_date_time = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Start Time")
    end_date_time = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="End Time")
    lunch_break_from = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Lunch Break")
    lunch_break_to = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Lunch Break")
    logout_time = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Logout Time")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:

        db_table = "manage_working_hours"


WORKINGDAYS1 = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)


class ManageWorkingDays(models.Model):
    weekly_working_days = models.CharField(choices= WORKINGDAYS1, default='', blank=True, null=True, max_length=200, verbose_name="Weekly Working Days")
    weekly_off_working_days = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Weekly Off Working Days")
    half_days = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Weekly Off Working Days")
    alternate_week = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Alternate Week")
    alternate_week_days = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Weekly Off Working Days")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "manage_working_days"
        verbose_name = "Define Working Days"


YESNO = (
    (1, 'Yes'),
    (2, 'No')
)


YESNO1 = (
    ('Yes', 'Yes'),
    ('No', 'No')
)


APPLICABLE_TO = (
    (1, 'Parent Company'),
    (2, 'Head office'),
    (3, 'Branches - Location wise')
)

WORKINGDAYS3 = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class ApprovalMatrixDefineProcesLevel(models.Model):
    process_level  = models.CharField(unique = True, max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Process Name')
    description  = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Description')
    is_active = models.BooleanField(default=0)
    start_date = models.DateTimeField(blank = True, null = True, verbose_name = 'Start Date')
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.process_level
        
    class Meta:
         db_table = "manage_approval_matrix_define_process_level"



class ResponseMangement(models.Model):
    name = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Name")
    type_of_response = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Type of Response")
    description = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    impace_on_data = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Impact on Data")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:

        db_table = "manage_response"


class RoleMangement(models.Model):
    name = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Name")
    sequence = models.IntegerField(default=0,  blank=True, null=True, verbose_name="sequence")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.name       

    class Meta:

        db_table = "manage_role"


class CompanySetup(models.Model):
    company_id = models.CharField(unique = True, max_length=4, blank=False, null=False, verbose_name="Company Id")
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name="Name")
    building = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Building")
    block_no = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Block Number")
    sector = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Sector")
    city = models.CharField(max_length=200,blank=True, null=True, verbose_name="City")
    district = models.CharField(max_length=200,default='', verbose_name="District")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="State")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Country")
    pincode = models.CharField(max_length=8,default='', verbose_name="Pin Code")
    cin_no = models.CharField(max_length=24,default='', verbose_name="CIN Number")
    pan_card = models.CharField(max_length=10,default='', verbose_name="Pan Card Number")
    gst_no = models.CharField(max_length=16,default='', verbose_name="GST Number")
    tan_no = models.CharField(max_length=20,default='', verbose_name="TAN Number")
    website = models.CharField(max_length=200,default='', verbose_name="Website")
    email_id = models.CharField(max_length=30,default='', verbose_name="Email Id")
    contact_no = models.CharField(max_length=10, default='', verbose_name="Contact Number")
    local_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Local Currency", related_name = "local_currency")
    reporting_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Reporting Currency", related_name = "reporting_currency")
    logo_upload = models.FileField(upload_to='documents/admin_image/',verbose_name="Upload Logo")
    start_date = models.CharField(max_length=200,default='', verbose_name="Start Date")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")

    def __str__(self):
        return self.company_id

    class Meta:
        db_table = "manage_company"
        verbose_name = "Define Company"


class CompanyLocalCurrency(models.Model):
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.SET_NULL, blank=True, null=True)
    local_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Local Currency", related_name = "local_currency_parent_com_one_to_many")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "company_local_currency"


class CompanyReportingCurrency(models.Model):
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.SET_NULL, blank=True, null=True)
    reporting_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Reporting Currency", related_name = "reporting_currency_parnt_one_to_many")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "company_reporting_currency"


class ManageHeadOfficeSetup(models.Model):
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.CASCADE, null=True, verbose_name="Parent Company")
    hod_id = models.CharField(unique = True, max_length=4, blank=False, null=False, verbose_name="HOD id")
    name =  models.CharField(max_length=30,default='', verbose_name="Name")
    building = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Building")
    block_no = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Block Number")
    sector = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Sector")
    city = models.CharField(max_length=200, blank = True ,null=True, verbose_name="City")
    district = models.CharField(max_length=200,default='', verbose_name="District")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name="State")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Country")
    pincode = models.CharField(max_length=8, default='', verbose_name="Pin Code")
    cin_no = models.CharField(max_length=24,default='', verbose_name="CIN Number")
    pan_card = models.CharField(max_length=10,default='', verbose_name="Pan Card Number")
    gst_no = models.CharField(max_length=16,default='', verbose_name="GST Number")
    website = models.CharField(max_length=200,default='', verbose_name="Website")
    email_id = models.CharField(max_length=30,default='', verbose_name="Email Id")
    contact_no = models.CharField(max_length=10,default='', verbose_name="Contact Number")
    local_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Local Currency", related_name = "office_local_currency")
    reporting_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Reporting Currency", related_name = "office_reporting_currency")
    is_active = models.BooleanField(default=1,verbose_name="Is Active")
    start_date = models.CharField(max_length=200,default='', verbose_name="Start Date")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.hod_id

    class Meta:
        db_table = "manage_head_office"
        verbose_name = "Define Manage Head Office"


class ManageHeadofficeLocalCurrency(models.Model):
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Head Office")
    local_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Local Currency", related_name = "local_currency_manageoffice_com_one_to_many")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "manage_head_office_local_currency"


class ManageHeadofficeReportingCurrency(models.Model):
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Head Office")
    reporting_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Reporting Currency", related_name = "reporting_currency_manageoffice_one_to_many")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "manage_head_office_reporting_currency"


class ManageBranch(models.Model):
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.CASCADE, null=True, verbose_name="Parent Company")
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.CASCADE, null=True, verbose_name="Head Office")
    branch_id = models.CharField(unique = True, max_length=3, blank=False, null=False, verbose_name="Branch Id")
    name_of_branch =  models.CharField(max_length=30, default='', verbose_name="Branch Name")
    building = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Building")
    block_no = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Block Number")
    sector = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Sector")
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name="City")
    district = models.CharField(max_length=200,default='', verbose_name="District")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="State")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Country")
    pincode = models.CharField(max_length=8,default='', verbose_name="Pin Code")
    gst_no = models.CharField(max_length=16,default='', verbose_name="GST Number")
    email_id = models.CharField(max_length=30,default='', verbose_name="Email Id")
    contact_no = models.CharField(max_length=10,default='', verbose_name="Contact Number")
    local_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Local Currency", related_name = "branch_local_currency")
    reporting_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Reporting Currency", related_name = "branch_reporting_currency")
    start_date = models.CharField(max_length=200,default='', verbose_name="Start Date")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")


    def __str__(self):
        return self.branch_id

    class Meta:
        db_table = "manage_branch"
        verbose_name = "Define Manage Branch"


class ManageBranchLocalCurrency(models.Model):
    branch_id = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True)
    local_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Local Currency", related_name = "local_currency_managebranch_com_one_to_many")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "manage_branch_local_currency"


class ManageBranchReportingCurrency(models.Model):
    branch_id = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True)
    reporting_currency = models.ForeignKey(TypeofCurrency, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Reporting Currency", related_name = "reporting_currency_managebranch_one_to_many")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "manage_branch_reporting_currency"


class ManageHolidays(models.Model):
    holidays_type = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Holiday Type")
    holidays_date = models.DateField(blank = True, null =True)
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Branch")
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Head Office")
    impact_on_salary = models.IntegerField(choices= YESNO, default=1,  blank=True, null=True, verbose_name="Impact on Salary")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "manage_holidays"
        verbose_name = "Define Manage Holidays"


class ManageHolidaysBranches(models.Model):
    holiday = models.ForeignKey(ManageHolidays, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Holiday")
    branch = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, null=True, verbose_name = "Branch")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "manage_holidays_branches"


class MapCityBranches(models.Model):
    parent_company =  models.ForeignKey(CompanySetup, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Parent Company")
    head_office =  models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Head Office")
    branch =  models.ForeignKey(ManageBranch, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Branch")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Country")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1, verbose_name="Is Activate")



    class Meta:
        db_table = "manage_map_city"


class MapCityMultipleWithBranches(models.Model):
    city_map = models.ForeignKey(MapCityBranches, on_delete=models.CASCADE, blank=True, null=True, verbose_name = "map_city")
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, verbose_name = "City")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "manage_city_with_multiple_branches"


# ******************* USER Master *********************************************
class ManageDepartment(models.Model):
    department = models.CharField(unique = True, max_length=50, blank=False, null=False, verbose_name = "Department")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.department

    class Meta:
        db_table  = "manage_department"


class ManageDesignation(models.Model):
    designation = models.CharField(unique = True, max_length=50, blank=False, null=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table  = "manage_designation"

    def __str__(self):
        return self.designation


class UserType(models.Model):
    user_type = models.CharField(unique=True,max_length=50, blank=True, null=True)
    is_agent = models.BooleanField(default =False)
    is_sales = models.BooleanField(default =False)
    is_active = models.BooleanField(default =1)
    class Meta:
        db_table  = "users_type"

    def __str__(self):
        return self.user_type


class ManageResponsibility(models.Model):
    responsibilities = models.CharField(unique = True, max_length=50, blank=False, null=False, verbose_name = "Responsibility")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    def __str__(self):
        return self.responsibilities

    class Meta:
        db_table  = "manage_responsibilities"


class UnitValue(models.Model):
    unit_value = models.CharField(unique=True,max_length=50, blank=True, null=True,verbose_name="Unit Value ")
    description = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default =1)
    

    class Meta:
        db_table = "unit_value"

    def __str__(self):
        return self.unit_value


def upload_user_imge(instance, filename):
    file_save_path2 = settings.MEDIA_ROOT + \
        'user_pics/user_{0}/{1}/{2}'.format(instance.id,
                                              datetime.now().strftime('%d%m%Y%H%M%S'), filename)
    file_save_pa = file_save_path2.split("media/")[1]
    return file_save_pa


class User(AbstractUser):

    ''' User model to user info '''

    def f():
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(10))
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name="Name")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, null=True, verbose_name="Designation")
    mobile_no = models.CharField(max_length=10, blank=False, null=False, verbose_name="Mobile Number")
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Parent Company")
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Head Office")
    reporting_to =  models.ForeignKey('self', on_delete=models.SET_NULL, default=None, blank=True, null=True, verbose_name="Reported To")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL, null=True, verbose_name="Responsibility")
    user_role = models.ForeignKey(RoleMangement, on_delete=models.SET_NULL, null=True, verbose_name="User Role")
    user_pics = models.FileField(upload_to='documents/admin_image/',verbose_name="Image")
    
    start_date = models.CharField(max_length=50, default='', blank=False, null=False, verbose_name="Start Date")
    status = models.CharField(max_length=50, null=True)
    gen_password = models.CharField(max_length=20, default=f,blank=True, null=True, verbose_name="Gen Password")
    fcm_key = models.TextField(blank = True, null = True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_uniqueid = models.CharField(max_length=1000, default='', blank=False, null=False, verbose_name="User Id")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")    # false
    is_sub_staff = models.BooleanField(default=0, verbose_name="Is Sub Staff")
    manual_create_admin = models.BooleanField(default=1, verbose_name="Is Sub Staff")
    allocate_user = models.BooleanField(default=False, verbose_name="Allocate user")
    is_agent = models.BooleanField(default=False)
    is_verification_agency = models.BooleanField(default=False)
    is_legal_team = models.BooleanField(default=False)
    is_technical_team = models.BooleanField(default=False)
    is_valuation_team = models.BooleanField(default=False)
    is_fraud_investigation_team = models.BooleanField(default=False)
    is_document_verification_team = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_detailed_filled = models.BooleanField(default=False)
    is_eligible = models.BooleanField(default=False)

    

    def __str__(self):
        return self.name       

    class Meta:
        db_table = "auth_user"


class UserMultipleBranch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    branch_allocated = models.ForeignKey(ManageBranch, on_delete=models.CASCADE, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "manage_user_multiple_branch"


class ManageUserMultipleRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name = "User Id")
    user_role = models.ForeignKey(RoleMangement, on_delete=models.SET_NULL, null=True, verbose_name="Role")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "manage_user_multiple_role"


class ManageProductType(models.Model):
    product_type = models.CharField(unique = True, max_length=50, blank=False, null=False, verbose_name = "Product Type")
    product_description = models.CharField(max_length=50, blank=False, null=False, verbose_name = "Product Description")
    start_date = models.CharField(max_length=50, blank=False, null=False)
    end_date = models.CharField(max_length=50, blank=False, null=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.product_type

    class Meta:
        db_table = "manage_product_type"


class ManageProductCategory(models.Model):
    product_category = models.CharField(unique = True, max_length=50, blank=True, null=True, verbose_name="Product Category")
    description = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)

    def __str__(self):
        return self.product_category

    class Meta:
        db_table = "manage_product_category"


class ManageProductName(models.Model):
    product_name = models.CharField(unique = True, max_length=50, blank=True, null=True,verbose_name="Product Name")
    description = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank = True, null =True)
    end_date = models.DateField(blank = True, null =True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)

    
    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "manage_product_name"

class ProductFacility(models.Model):

    product_facility = models.CharField(unique=True,max_length=50, blank=True, null=True,verbose_name="Product Facility")
    description = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)
    

    class Meta:
        db_table = "product_facility"

    def __str__(self):
        return self.product_facility
DATA_STATUS = (
    (1, 'Pending'),
    (2, 'Interested'),
    (3, 'InProcess')
)


CALL_STATUS = (
    (1, 'Calls Received'),
    (2, 'Calls Attended'),
    (3, 'Calls Missed')
)


class ManageOverTime(models.Model):
    start_date_time = models.CharField(default='', blank=True, null=True, max_length=200)
    end_date_time = models.CharField(default='', blank=True, null=True, max_length=200)
    impact_on_salary = models.IntegerField(choices= YESNO, default=1,  blank=True, null=True)
    days = models.CharField(choices= WORKINGDAYS3, default='', blank=True, null=True, max_length=200)
    parent_com = models.ForeignKey(CompanySetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Parent Company")
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Head Office")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:

        db_table = "manage_over_time"


class ManageOvertimeApplicable(models.Model):
    over_time = models.ForeignKey(ManageOverTime, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    brach = models.ForeignKey(ManageBranch, blank=True, null=True, max_length=200 , on_delete=models.SET_NULL)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:

        db_table = "manage_over_time_aplicable"
        

class ManageClientType(models.Model):
    client_type = models.CharField(unique = True, max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_type

    class Meta:
         db_table = "manage_client_type"


class ManageClientCategory(models.Model):
    client_category  = models.CharField(unique = True, max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_category

    class Meta:
         db_table = "manage_client_category"


class ManageClientLead(models.Model):
    define_lead_values  = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
         db_table = "manage_client_lead"


class ManageClientTypeofData(models.Model):
    type_of_Data = models.CharField(unique = True, max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)
    
    class Meta:
         db_table = "manage_client_type_of_data"


class TemplateSetupClientType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)

    class Meta:
         db_table = "template_set_up_client_type"
########

class TemplateSetupClientCategory(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)

    class Meta:
         db_table = "temaplate_set_up_client_category"
###
class CustomizeTemplate(models.Model):
    template_type = models.CharField(unique= True ,default='', blank=True, null=True, max_length=200,verbose_name="Template Type")
    template_name = models.CharField(default='', blank=True, null=True, max_length=200,verbose_name="Template Name") 
    purpose =models.CharField(default='', blank=True, null=True, max_length=200,verbose_name="Purpose") 
    upload = models.FileField(upload_to='documents/%Y/%m/%d/',verbose_name="Template Upload")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)

    class Meta:
        db_table = "customized_templates"

#######################


class UpdateTemplateType(models.Model):
    template_type = models.ForeignKey(CustomizeTemplate,on_delete=models.SET_NULL, blank=True, null=True ,verbose_name="Template Type")
    description = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    is_active = models.BooleanField(default =1)
    def __str__(self):
        return self.template_type
    class Meta:

        db_table = "update_template_type"





# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
VALIDATION_REQUIRED = (
    (1, 'Yes'),
    (2, 'No')
)


# Client Support
class AllocationMatrixClientSupport(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "allocation_matrix_client_support"


class AllocationClientSupportUserCity(models.Model):
    client_support_allocation =  models.ForeignKey(AllocationMatrixClientSupport, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="City")
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_matrix_client_support_city"


class AllocationUserClientSupportProductType(models.Model):
    client_support_allocation =  models.ForeignKey(AllocationMatrixClientSupport, on_delete=models.CASCADE, null=True)
    product_type  = models.ForeignKey(ManageProductType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_matrix_client_support_product_type"


class AllocationClientSupportProductCategory(models.Model):
    client_support_allocation =  models.ForeignKey(AllocationMatrixClientSupport, on_delete=models.CASCADE, null=True)
    product_category  = models.ForeignKey(ManageProductCategory, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_client_support_product_category"


class AllocationClientSupportProductName(models.Model):
    client_support_allocation =  models.ForeignKey(AllocationMatrixClientSupport, on_delete=models.CASCADE, null=True)
    product_name  = models.ForeignKey(ManageProductName, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_client_support_product_name"


class AllocationClientSupportClientType(models.Model):
    client_support_allocation =  models.ForeignKey(AllocationMatrixClientSupport, on_delete=models.CASCADE, null=True)
    client_type  = models.ForeignKey(ManageClientType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_client_support_client_type"


class AllocationClientSupportClientCategory(models.Model):
    client_support_allocation =  models.ForeignKey(AllocationMatrixClientSupport, on_delete=models.CASCADE, null=True)
    client_category  = models.ForeignKey(ManageClientCategory, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_client_category_client_support"


# Vendor Support
class AllocationMatrixVendorSupport(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "allocation_matrix_vendor_support"


class AllocationMatrixVendorSupportUserCity(models.Model):
    vendor_support =  models.ForeignKey(AllocationMatrixVendorSupport, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="City")
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_user_matrix_city_vendor_support"


class AllocationMatrixVendorSupportProductType(models.Model):
    vendor_support =  models.ForeignKey(AllocationMatrixVendorSupport, on_delete=models.CASCADE, null=True)
    product_type  = models.ForeignKey(ManageProductType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_matrix_vendor_support_product_type"


class AllocationMatrixVendorSupportProductCategory(models.Model):
    vendor_support =  models.ForeignKey(AllocationMatrixVendorSupport, on_delete=models.CASCADE, null=True)
    product_category  = models.ForeignKey(ManageProductCategory, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_matrix_vendor_support_product_category"


class AllocationMatrixVendorSupportProductName(models.Model):
    vendor_support =  models.ForeignKey(AllocationMatrixVendorSupport, on_delete=models.CASCADE, null=True)
    product_name  = models.ForeignKey(ManageProductName, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "llocation_matrix_vendor_support_product_name"


class AllocationMatrixVendorSupportClientType(models.Model):
    vendor_support =  models.ForeignKey(AllocationMatrixVendorSupport, on_delete=models.CASCADE, null=True)
    client_type  = models.ForeignKey(ManageClientType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "llocation_matrix_vendor_support_client_type"


class AllocationMatrixVendorSupportClientCategory(models.Model):
    vendor_support =  models.ForeignKey(AllocationMatrixVendorSupport, on_delete=models.CASCADE, null=True)
    client_category  = models.ForeignKey(ManageClientCategory, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_matrix_vendor_support_client_category"


class bulksms(models.Model):
    name = models.CharField(max_length=100, null=False, default ='')
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "bulk_sms"


class mailsms(models.Model):
    name = models.CharField(max_length=250, null=False, default ='')
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "bulk_email"


class EscalationMatrixDefineLevel(models.Model):
    level = models.CharField(unique = True, max_length=250, null=False, default ='')
    department = models.ForeignKey(ManageDepartment, on_delete=models.CASCADE, null=True)
    designation = models.ForeignKey(ManageDesignation, on_delete=models.CASCADE, null=True)
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "escalation_matrix_define_level"
         verbose_name = "Define Matrix Level"


class EscalationMatrixDefineTurnAroundTime(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    tat_in_hours_days = models.CharField(max_length=250, null=False, default ='', verbose_name="Turnaround Time In Minutes")
    purpose = models.CharField(max_length=250, null=False, default ='', verbose_name="Purpose")
    remark = models.CharField(max_length=250, null=False, default ='', verbose_name="Remark")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "escalation_matrix_define_turn_around_time"


class EscalationMatrixDefineTurnAroundTimeProcessName(models.Model):
    turn_around = models.ForeignKey(EscalationMatrixDefineTurnAroundTime, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    process_name_level = models.ForeignKey(ApprovalMatrixDefineProcesLevel, on_delete=models.SET_NULL, null=True, verbose_name="Process Name")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "escalation_matrix_define_turn_around_process_name"


class EscalationMatrixDefineTurnAroundTimeEscalationName(models.Model):
    turn_around = models.ForeignKey(EscalationMatrixDefineTurnAroundTime, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    escalation_name = models.ForeignKey(EscalationMatrixDefineLevel, on_delete=models.SET_NULL, null=True, verbose_name="Escalation Level")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "escalation_matrix_define_turn_around_escalation_name"


class EscalationMatrixDefineTurnAroundTimeUser(models.Model):
    turn_around = models.ForeignKey(EscalationMatrixDefineTurnAroundTime, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    escalation_user = models.ForeignKey(User, blank=True, null=True, max_length=200 , on_delete=models.SET_NULL, verbose_name = "Escalation To", related_name = "escalation_to")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "escalation_matrix_define_turn_around_user"


class NotificationSubject(models.Model):
    notification_subject = models.CharField(unique = True, max_length=250, null=False, default ='', verbose_name="Notification Method")
    description = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_subject

    class Meta:
         db_table = "notification_subject"
         verbose_name = "Define Notification Method"


class NotificationType(models.Model):
    notification_type = models.CharField(max_length=250, null=False, default ='', verbose_name="Notification Type")
    purpose = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_type

    class Meta:
         db_table = "notification_type"
         verbose_name = "Define Notification Type"


class NotificationFrequency(models.Model):
    notification_frequency = models.CharField(max_length=250, null=False, default ='', verbose_name="Frequency Type")
    days = models.CharField(choices= WORKINGDAYS1, max_length=250, null=False, default ='', verbose_name="Days")
    date = models.DateField(blank = True, null = True, verbose_name="Date")
    purpose = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    time = models.CharField(max_length=250, null=False, default ='', verbose_name="Timing")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "notification_frequency"
         verbose_name = "Define Notification Frequency"


class ImportanceofNotification(models.Model):
    importance_type  = models.CharField(max_length=250, null=False, default ='', verbose_name="Importance Type")
    time_interval  = models.IntegerField(null=False, default =0, verbose_name="Time Interval(In Minutes)")
    purpose = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "import_of_notification"
         verbose_name = "Define Importance Type"


class TargetAudience(models.Model):
    target_audience  = models.CharField(max_length=250, null=False, default ='', verbose_name="Target Audience")
    source  = models.CharField(max_length=250, null=False, default ='', verbose_name="Source")
    purpose = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.target_audience)

    class Meta:
         db_table = "target_audience"
         verbose_name = "Define Target Audience"



class NotificationAction(models.Model):
    notification_action = models.CharField(unique=True, max_length=250, null=False, default ='', verbose_name="Notification Action")
    description = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.notification_action)

    class Meta:
         db_table = "notification_action"
         verbose_name = "Define Notification Action"


class NotificationGroup(models.Model):
    notification_group  = models.CharField(max_length=250, null=False, default ='', verbose_name="Notification Group")
    notification_method  = models.ForeignKey(NotificationSubject, blank = True, null = True, on_delete=models.CASCADE, verbose_name="Notification Method")
    notification_type  = models.ForeignKey(NotificationType, blank = True, null = True, on_delete=models.CASCADE, verbose_name="Notification Type")
    purpose = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "notification_group"


class TemplateForNotification(models.Model):
    notification_method  = models.ForeignKey(NotificationSubject, blank = True, null = True, on_delete = models.CASCADE, verbose_name="Notification Method")
    notification_subject  = models.CharField(max_length=250, null=False, default ='', verbose_name="Subject")
    notification_importance = models.ForeignKey(ImportanceofNotification, blank = True, null = True, on_delete = models.SET_NULL, verbose_name="Audience Importance")
    target_audience = models.ForeignKey(TargetAudience, blank = True, null = True, on_delete = models.SET_NULL, verbose_name="Target Audience", related_name = "notification_target_audience")
    action = models.ForeignKey(NotificationAction, blank = True, null = True, on_delete = models.SET_NULL, verbose_name="Action")
    notification_frequency_type = models.ForeignKey(NotificationFrequency, blank = True, null = True, on_delete = models.SET_NULL, verbose_name="Notification Frequency Type")
    notification_type  = models.ForeignKey(NotificationType, blank = True, null = True, on_delete = models.SET_NULL, verbose_name="Notification Type")
    template  = models.CharField(max_length=250, null=False, default ='', verbose_name="Template")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "template_for_notification"


PREDEDFIEND_NOTIFICATION_TYPE = (
    (1, 'New Follow ups'),
    (2, 'Refollow ups'),
    (3, 'New Meetings'),
    (4, 'Meeting Rescheduled'),
    (5, 'Meeting Attended'),
    (6, 'Meeting Cancelled'),
    (7, 'Successful Meetings'),
    (8, 'Login Attendence'),
    (9, 'Send Mobile APP'),
)


TYPE_OF_MESSAGE = (
    (1, 'Transactional'),
    (2, 'Promotional'),
)


# ============================ Access and Permission Rules ============================
class ManagePermissionTypes(models.Model):
    permission_type  = models.CharField(max_length=250, null=False, default ='', verbose_name="Permission Type")
    description = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "manage_permission_types"
         verbose_name = "Define Permission Type"


class ManagePermissionLevel(models.Model):
    permission_level  = models.CharField(max_length=250, null=False, default ='', verbose_name="Permission Level")
    description = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "manage_permission_level"
         verbose_name = "Define Permission Level"

class DefinePermissionLevel(models.Model):
    permission_level  = models.CharField(max_length=250, null=False, default ='', verbose_name="Permission Level")
    description = models.CharField(max_length=250, null=False, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "define_permission_level"
         
class ManagePermissionReportingType(models.Model):
    name  = models.CharField(max_length=250, null=False, default ='', verbose_name="Name")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
         db_table = "manage_permission_reporting_type"
         verbose_name = "Define Permission Reporting Type"


class ManagePermissionReportingLevel(models.Model):
    name  = models.CharField(max_length=250, null=False, default ='', verbose_name="Name")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
         db_table = "manage_permission_reporting_level"


class ManagePermissionReportingHierarchy(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)
    reporting_type = models.ForeignKey(ManagePermissionReportingType, blank=False, null=False, max_length=200 , on_delete=models.CASCADE)
    reporting_level = models.ForeignKey(ManagePermissionLevel, blank=False, null=False, max_length=200 , on_delete=models.CASCADE)
    designation = models.CharField(max_length=250, null=False, default ='', verbose_name="Designation")
    department = models.CharField(max_length=250, null=False, default ='', verbose_name="Department")
    responsibility = models.CharField(max_length=250, null=False, default ='', verbose_name="Responsibilities")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "manage_permission_reporting_hierarchy"

# ***********************************************

class UserAccessPermissonModelsPermission(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)
    main_function = models.IntegerField(default=0,  blank=True, null=True)
    function_level = models.CharField(max_length=250, null=False, default ='')
    sub_function_level = models.CharField(max_length=250, null=False, default ='')
    add =models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    delete =models.BooleanField(default=False)
    view = models.BooleanField(default=False)
    sequence = models.IntegerField(default=0,  blank=True, null=True)
    sub_menu_sequence = models.IntegerField(default=0,  blank=True, null=True)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "user_access_models_permission"

#  >>>>>>>>>>>>>>>>> MIS and  Reporting Set up >    Define Target  >>>>>>>>>> 
class MisManagePerformanceDefineTarget(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User")
    target_type = models.CharField( default='', blank=True, null=True, max_length=200, verbose_name="Target Type")
    target = models.CharField(max_length=250,  blank=True, null=True, default ='', verbose_name="Target")
    period_of_type = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Period For Target")
    nature_of_target = models.IntegerField(default =0, verbose_name="Nature of Target")
    description = models.CharField(max_length=250, null=False, blank=True, default ='')
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    class Meta:
         db_table = "mis_manage_performance_define_target"


class MisManageReportingReportFormat(models.Model):
    format_type = models.CharField(max_length=250, null=False, blank=True, default ='', verbose_name="Format Type")
    description = models.CharField(max_length=250, null=False, blank=True, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
    class Meta:
         db_table = "mis_manage_reporting_report_format"


class MisManageReportingReportFrequency(models.Model):
    reporting_frequency = models.CharField(max_length=250, null=False, blank=True, default ='', verbose_name="Format Type")
    description = models.CharField(max_length=250, null=False, blank=True, default ='', verbose_name="Description")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
    class Meta:
         db_table = "mis_manage_reporting_report_frequency"


ACTION_LEVEL = (
    (1, 'SMS and Mail Campaign'),
    (2, 'Data Management'),
    (3, 'Lead Allocation'),
    (4, 'Lead Generation'),
    (5, 'Lead Confirmations'),
    (6, 'Lead Verification'),
    (7, 'Follow ups'),
    (8, 'Meeting Scheduled'),
    (9, 'Business Conversion'),
    (10,'Rejected Leads'),
)

class MisManageReportingReportFrequencyTemplate(models.Model):
    activity_level = models.IntegerField(choices = ACTION_LEVEL ,default = 0, verbose_name="Activity Level")
    peridodic_level = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Period For Target")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
         db_table = "mis_manage_reporting_report_template"


class MisManageReportingReportFrequencyTemplateUser(models.Model):
    template = models.ForeignKey(MisManageReportingReportFrequencyTemplate, blank=False, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "mis_manage_reporting_report_template_user"


class MisManageReportingReportFrequencyTemplateCompany(models.Model):
    template = models.ForeignKey(MisManageReportingReportFrequencyTemplate, blank=False, null=True, on_delete=models.CASCADE)
    parent_company = models.ForeignKey(CompanySetup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Place Of Working")
    head_office = models.ForeignKey(ManageHeadOfficeSetup, on_delete=models.SET_NULL, null=True, verbose_name="Place of Posting")
    
    class Meta:
         db_table = "mis_manage_reporting_report_template_company"


class UserMultipleBranchReporting(models.Model):
    template = models.ForeignKey(MisManageReportingReportFrequencyTemplate, blank=True, null=True, on_delete=models.CASCADE)
    brach = models.ForeignKey(ManageBranch, on_delete=models.CASCADE, null=True)
    

    class Meta:
        db_table = "mis_manage_reporting_report_template_branches"

MESSAGE_TYPE = (
    (1, 'Received'),
    (2, 'Sender'),
)

MESSAGE = (
    (1, 'Text Messages'),
    (2, 'Whatsapp Messages'),
    (3, 'Email Messages'),
)

class ActivityNotification(models.Model):
    sender = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name="sender_id")
    receiver = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name="receiver_id")
    body_messages = models.TextField(default='', blank=True, null=True, max_length=200)
    is_read = models.BooleanField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "notification_activity_user"


# 3- Approval Matrix
class ApprovalMatrixiDefineApprovalLevel(models.Model):
    approval_level  = models.CharField(unique = True, max_length = 50 ,default='', blank=True, null=True, verbose_name = 'Approval Level')
    description  = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Description')
    is_active = models.BooleanField(default=0)
    start_date = models.DateTimeField(blank = True, null = True, verbose_name = 'Start Date')
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.approval_level
        
    class Meta:
         db_table = "approval_matrix_approval_level"


class ApprovalMatrixMapApprovalLevelWithUsers(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    description  = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Description')
    start_date = models.DateTimeField(blank = True, null = True, verbose_name = 'Start Date')
    is_active = models.BooleanField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "approval_matrix_map_approval_level_with_users"


class ApprovalMatrixMapApprovalLevelWithUsersLocation(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")

    class Meta:
         db_table = "approval_matrix_map_approval_level_with_users_location"


class MapApprovalMatrixWithUsersProductType(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    product_type  = models.ForeignKey(ManageProductType, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Product Type")

    class Meta:
         db_table = "map_approval_matrix_with_users_product_type"


class MapApprovalMatrixWithUsersProductCategory(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    product_category  = models.ForeignKey(ManageProductCategory, blank=False, null=True, on_delete=models.SET_NULL, verbose_name = 'Product Category')

    class Meta:
         db_table = "map_approval_matrix_with_users_product_category"


class MapApprovalMatrixWithUsersProductName(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    product_name  = models.ForeignKey(ManageProductName, blank=False, null=True, on_delete=models.SET_NULL, verbose_name = 'Product Category')

    class Meta:
         db_table = "map_approval_matrix_with_users_product_name"


class ApprovalMatrixMapApprovalLevelWithUsersClientType(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    client_type  = models.ForeignKey(ManageClientType, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Client Type")

    class Meta:
         db_table = "approval_matrix_map_approval_level_with_users_client_type"


class ApprovalMatrixMapApprovalLevelWithUsersClientCategory(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    client_category = models.ForeignKey(ManageClientCategory, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Client Category")

    class Meta:
         db_table = "approval_matrix_map_approval_level_with_users_category"


class MapApprovalMatrixWithusersProcessName(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    process = models.ForeignKey(ApprovalMatrixDefineProcesLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Process Name")

    class Meta:
         db_table = "map_approval_matrix_with_users_process_name"


class ApprovalMatrixMapApprovalLevelWithUsersProcessLevel(models.Model):
    map_user = models.ForeignKey(ApprovalMatrixMapApprovalLevelWithUsers, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")

    class Meta:
         db_table = "approval_matrix_map_approval_level_with_users_process_level"


class ProcessNameWithNumberOfData(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    process_name = models.ForeignKey(ApprovalMatrixDefineProcesLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Process Name")
    is_active = models.BooleanField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "process_name_with_number_of_data"
        unique_together = ('user', 'process_name',)


######### 
#
class DefineProcessAllocation(models.Model):
    process_name = models.CharField(max_length = 200 ,default='', verbose_name = 'Name Of Process')
    sub_process_name = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'SubProcess Name')
    child_process_name = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Child Process Name')
    description = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Description')
    is_active = models.BooleanField(default=1)
    # added = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.process_name +'>'+self.sub_process_name  +'>'+ self.child_process_name

    class Meta:
         db_table = "define_process_allocation_matrixx"
#2
class AllocationManagementUpdateReallocationCriteria(models.Model):
    process_name = models.ForeignKey(DefineProcessAllocation, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Process Name")
    # process_name = models.CharField(max_length=200, blank=False, null=True, verbose_name="Process Name")
    
    reallocation_criteria = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Reallocation Criteria")
    description = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Description")
    is_active = models.BooleanField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reallocation_criteria

    class Meta:
         db_table = "allocation_management_update_reallocation_criterial"
         unique_together = ('process_name', 'reallocation_criteria')
##4
class AllocationMatrixLeadAllocation(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "allocation_matrix_lead_allocation"

    def __str__(self):
        return self.user.email
##########


####################
#@1
class AllocationManagementManageReallocation(models.Model):
    process_name = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Process Name")
    reallocation_criteria = models.ForeignKey(AllocationManagementUpdateReallocationCriteria, on_delete=models.SET_NULL, blank=False, null=True,verbose_name="Reallocation Criteria")
    existing_user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name="Exist User", related_name = "existing_user")
    new_user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name="New User", related_name = "new_user")
    description = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Description")
    is_active = models.BooleanField(default=0)

    class Meta:
         db_table = "allocation_management_manage_reallocation"
         unique_together = ('process_name', 'reallocation_criteria', 'new_user')

#########
class AllocationProcessMultipleReallocation(models.Model):
    allocation_reallocation = models.ForeignKey(AllocationManagementManageReallocation, on_delete=models.SET_NULL, blank=False, null=True,verbose_name="Reallocation Criteria")
    process_name = models.ForeignKey(DefineProcessAllocation, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Process Name")
    description = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Description")
    is_active = models.BooleanField(default=0)

    class Meta:
         db_table = "allocation_process_multiple_reallocation"


#@!!
class MapApprovalLevelWithJointApproval(models.Model):
    group_name = models.CharField(max_length = 200 ,default='', blank=False, null=True,verbose_name="Group Name")
    no_of_users = models.CharField(max_length = 200 ,default='', blank=False, null=True, verbose_name = 'No of Users')
    works_flow_process = models.CharField(max_length = 200, default='', blank=True, null=True, verbose_name = 'Work Flow Process')
    user_joint_approval = models.CharField(max_length = 200 ,default='', blank=True, null=True,verbose_name='User Name')
    department = models.ForeignKey(ManageDepartment,blank=True, on_delete=models.CASCADE, null=True,verbose_name='Department')
    designation = models.ForeignKey(ManageDesignation,blank=True, on_delete=models.CASCADE, null=True,verbose_name='Designation')
    responsibilities = models.ForeignKey(ManageResponsibility,blank=True, on_delete=models.PROTECT, null=True, verbose_name="Responsibilities")
    loan_limit = models.CharField(max_length = 200 ,default='', blank=False, null=True, verbose_name = 'Loan Limit')
    approval_level=models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Approval Level')

    is_active = models.BooleanField(default=1)


    def __str__(self):
        return self.group_name
        
    class Meta:
         db_table = "map_approval_matrix_joint_approval"
         verbose_name = "Map Joint Approval"
         unique_together = ('group_name','no_of_users','user_joint_approval')
##########
class MapApprovalLevelWithJointApprovalUsers(models.Model):
    map_joint_user = models.ForeignKey(MapApprovalLevelWithJointApproval, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Process Name")

    class Meta:
         db_table = "joint_approval_users_name"


#########
class setupescalationmatrixdefinelevel(models.Model):
    level = models.CharField(unique=True,max_length=250, null=True, default ='')
    # department = models.ForeignKey(ManageDepartment, on_delete=models.CASCADE, null=True)
    # designation = models.ForeignKey(ManageDesignation, on_delete=models.CASCADE, null=True)
    # location = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    description  = models.CharField(max_length = 200 ,default='', blank=True, null=True, verbose_name = 'Description')
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         db_table = "setup_escalation_matrix_define_level"


#######1
class EscalationManagementManageEscalation(models.Model):
    user = models.ForeignKey(AllocationMatrixLeadAllocation, blank=False, null=True, on_delete=models.CASCADE, verbose_name = "User")
    effect_of_escalation_level = models.ForeignKey(AllocationManagementUpdateReallocationCriteria, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Effect of Escalation Level")
    escalation_to = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name="Escalation to")

    process_name = models.ForeignKey(ApprovalMatrixDefineProcesLevel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Process Name")
    # escalation_level = models.ForeignKey(setupescalationmatrixdefinelevel, on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Escalation Level")
    
    escalation_level = models.CharField(max_length=250, null=True, default ='',verbose_name="Escalation Level")
    is_active = models.BooleanField(default=0)

    class Meta:
         db_table = "escalation_management_manage_escalation"
         unique_together = ('process_name', 'escalation_level', 'effect_of_escalation_level', 'escalation_to')


class ManageEscalationProcessName(models.Model):
    escalation = models.ForeignKey(EscalationManagementManageEscalation, blank=False, null=True, on_delete=models.CASCADE, verbose_name="User Id")
    process_name = models.ForeignKey(DefineProcessAllocation, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Process Name")

    class Meta:
         db_table = "manage_escalation_process_name"


class DefineProductType(models.Model):

	product_type = models.CharField(unique=True,max_length=50,verbose_name="Product Type")
	description = models.CharField(max_length=50, blank=True, null=True)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default =1)
	

	class Meta:
		db_table = "define_product_type"

class DefineClientType(models.Model):
    client_type = models.CharField(unique=True,default='', blank=False, null=True, max_length=200,verbose_name="Client Type")
    purpose = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default =1)

    class Meta:

        db_table = "define_client_type"

    def __str__(self):
        return self.client_type
class AllocationMatrixLeadUserCity(models.Model):
    lead_allocation =  models.ForeignKey(AllocationMatrixLeadAllocation, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="City")
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "allocation_matrix_lead_allocation_city"


class LeadAllocationProcessName(models.Model):
    lead_allocation =  models.ForeignKey(AllocationMatrixLeadAllocation, on_delete=models.CASCADE, null=True)
    process_name  = models.ForeignKey(DefineProcessAllocation, blank=True, null=True, max_length=200 , on_delete=models.PROTECT)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "lead_allocation_process_name"

class ManageMonthEndProcess(models.Model):
    # month_end_type= models.ForeignKey(MonthEndProcessType, on_delete=models.PROTECT, verbose_name="Month End Type")
    # monthyear = models.DateField(verbose_name="Start Date")
    process_name  = models.ForeignKey(DefineProcessAllocation, blank=True, null=True, max_length=200 , on_delete=models.PROTECT)
    monthandyear = models.DateField(blank=True,null=True,verbose_name="Month & Year")
    extended_by_days = models.CharField(default='', max_length=2,verbose_name="Extended By Days")
    new_date = models.CharField(default='', max_length=20,verbose_name="New Date")    
    description = models.CharField(default='', max_length=80)
    is_active = models.BooleanField(default =1)

    class Meta:
        verbose_name = "Manage Month End Process"
        db_table = "manage_month_end_process"

    def __str__(self):
        return str(self.month_year)



######### new Manage Products
class ManageProducts(models.Model):
    product_type = models.CharField(default='', max_length=200,blank=True, null=True , verbose_name= 'Product Type')
    product_name = models.CharField(default='', max_length=200,blank=True, null=True,  verbose_name= 'Product Name')
    description = models.CharField(default='', max_length=280 , blank=True, null=True)
    is_active = models.BooleanField(default =1)

    class Meta:
       
        db_table = "manage_product"

    def __str__(self):
        return str(self.product_type)
########UpdateRevenue
class ManageUpdateRevenue(models.Model):
    revenue_type = models.CharField(unique = True, max_length=50, blank=True, null=True, verbose_name="Revenue Type")
    revenue_name = models.CharField(unique = True, max_length=50, blank=True, null=True, verbose_name="Revenue Name")
    description = models.CharField(max_length=50, blank=True, null=True)
    # start_date = models.CharField(max_length=50, blank=True, null=True)
    # end_date = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)


    class Meta:
        db_table = "manage_updaterevenue"
########Update Tax Rates 
class ManageUpdateTaxRates(models.Model):
    taxation_type = models.CharField(unique = True, max_length=50, blank=True, null=True, verbose_name="Taxation Type")
    taxation_name = models.CharField( unique = True,max_length=50, blank=True, null=True, verbose_name="Taxation Name")
    rate = models.CharField(unique = True, max_length=50, blank=True, null=True, verbose_name="Rate")
    unit_value  = models.ForeignKey(UnitValue,  null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)
    class Meta:
        db_table = "manage_updateupdatetaxrates"

######## ManagePricing relative_name 
class ManagePricing(models.Model):
    product_type = models.CharField(unique = True, max_length=50, blank=True, null=True, verbose_name="Product Type")
    product_name = models.CharField( max_length=50, blank=True, null=True, verbose_name="Product Name")
   
    revenue_type = models.CharField( max_length=50,  blank=True, null=True, verbose_name='Revenue Type')
    revenue_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Revenue Name" )
    revenue_rate = models.CharField(max_length=50, blank=True, null=True, verbose_name="Revenue Rate" )
    unit_value   = models.CharField(max_length=50, blank=True, null=True, verbose_name="Unit Value" )
    
    taxation_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Taxation Type")
    taxation_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Taxation Name')
    
    rate          = models.CharField(max_length=50, blank=True, null=True, verbose_name="Rate")
    unit_value  = models.ForeignKey(UnitValue, null=True, on_delete=models.SET_NULL)
    
    description = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =1)


    class Meta:
        db_table = "manage_managepricing"
 	
	 				
    #resume_screen_level = models.OneToOneField(RecruitmentManagementInterveiwProcessScreeningLevel, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Resume  Screen Level")


################### Manage Update Employment Type

class ManageUpdateEmploymentType(models.Model):
    employee_type = models.CharField(unique = True, max_length=50, blank=False, null=False, verbose_name = "Employment Type")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.employee_type

    class Meta:
        db_table  = "manage_employmenttype"



#
##


class UpdatePurposeofTemplate(models.Model):
    template_type = models.ForeignKey(CustomizeTemplate,on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Template Type")
    purpose = models.CharField(default='', blank=False, null=True, max_length=200)
    description = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    is_active = models.BooleanField(default =1)
    def __str__(self):
        return self.template_type
    class Meta:

        db_table = "define_template_purpose"


class UpdateTemplateRequirement(models.Model):
    client_type  = models.ForeignKey(ManageClientType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    # # client_type = models.CharField(unique=True,default='', blank=False, null=True, max_length=200,verbose_name="Client Type")
    client_role = models.CharField(default='', blank=True, null=True, max_length=200,verbose_name="Client Role")
    client_category = models.ForeignKey(ManageClientCategory, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Client Category")

    added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default =1)

    class Meta:

        db_table = "update_template_requirement"



validation_type = (
	('Plain Text','Plain Text'),
	('DD/MM/YYYY','DD/MM/YYYY'),
	('MM/DD/YYYY','MM/DD/YYYY'),
	('DD/MM/YYYY With Time','DD/MM/YYYY With Time'),
	('Alpbhanumeric','Alpbhanumeric'),
	('Formula','Formula'),
	('HH:MM','HH:MM'),
	('Numbers','Numbers')
)

FIELD_TYPE = (
	('text','Text'),
	('email','Email'),
	('file','File'),
	('number','Number'),
	('date','Date'),
	# ('calander', 'Calander'),
	('url','Url'),
	('week','Week'),
	('month','Month'),
	('tel','Tel'),
	('time','Time'),
	('select','DropDown'),
	('textarea','TextArea')
)


class TemplateCreateFields(models.Model):
	subfield_name = models.CharField(default='', blank=False, null=True, max_length=200,verbose_name=" Field ")
	length_of_field  =  models.CharField(default='', blank=True, null=True, max_length=200,verbose_name="Length Of Field ")
	field_type = models.CharField(choices=FIELD_TYPE,default='', blank=True, null=True, max_length=200,verbose_name="Field Type")
	validation_required = models.CharField(choices=YESNO1,default='', blank=True, null=True, max_length=200,verbose_name="validation Required")
	validation_type = models.CharField(choices=validation_type,default='', blank=True, null=True, max_length=200,verbose_name="validation Type")
	mandatory = models.CharField(choices=YESNO1,default='', blank=True, null=True, max_length=200,verbose_name="Mandatory")
	sort_order = models.IntegerField(default =0, blank=True,null=True)

	select_model = models.CharField(default='', blank=True, null=True, max_length=200,
										   verbose_name="Select Form")

	
	def __str__(self):
			return self.subfield_name


	class Meta:
		db_table = "template_create_fields"



##    AdditionalTemplate


field_header = (
    ('Header'  , 'Header'),
   )
form_disp = (
    ('Horizontal'  , 'Horizontal'),
    (' Vertical' , 'Vertical')
   )





class AdditionalTemplate(models.Model):
    template_type = models.ForeignKey(CustomizeTemplate,on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Template Type")
    client_type  = models.ForeignKey(ManageClientType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    client_role = models.ForeignKey(UpdateTemplateRequirement, blank=True, null=True, max_length=200, on_delete=models.CASCADE ,verbose_name="Client Role")
    client_category = models.ForeignKey(ManageClientCategory, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Client Category")
    
    select_field =  models.CharField( default='', blank=False, null=True, max_length=200,verbose_name="Select Field")
    master =models.CharField(default='', blank=False, null=True, max_length=200,verbose_name=" Master")
    Field_role = models.CharField(choices=field_header, default='', blank=False, null=True, max_length=200,verbose_name="Select Field Role")
    form_display  = models.CharField(choices=form_disp,  default='', blank=False, null=True, max_length=200,verbose_name=" Form Diplay")
    added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default =1)

    class Meta:
        db_table = "additional_template"
            
class ApplicationForm(models.Model):
    template_type = models.ForeignKey(CustomizeTemplate,on_delete=models.SET_NULL, blank=True, null=True)
    client_type  = models.ForeignKey(ManageClientType, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    client_role = models.ForeignKey(UpdateTemplateRequirement, blank=True, null=True, max_length=200, on_delete=models.CASCADE ,verbose_name="Client Role")
    client_category = models.ForeignKey(ManageClientCategory, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Client Category")
    
    select_field =  models.CharField( default='', blank=False, null=True, max_length=200,verbose_name="Select Field")
    master =models.CharField(default='', blank=False, null=True, max_length=200,verbose_name=" Master")
    Field_role = models.CharField(choices=field_header, default='', blank=False, null=True, max_length=200,verbose_name="Select Field Role")
    form_display  = models.CharField(choices=form_disp,  default='', blank=False, null=True, max_length=200,verbose_name=" Form Diplay")
    added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_active = models.BooleanField(default =1)

    class Meta:

        db_table = "application_form"
    

#########
class AllocationMatrixsClientSupport(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, max_length=200 , on_delete=models.CASCADE)
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL, null=True, verbose_name="Responsibility")
    branch_id = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, null=True, verbose_name="Branch Id")
    client_type  = models.ForeignKey(ManageClientType, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Client Type")
    name = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, verbose_name = "City")
    is_active = models.BooleanField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "allocation_matrixs_client_support"


