from datetime import datetime 
from django.db import models
from django.conf import settings
from hrms_management.models import *
from hrms_employees.models import *
from knowleage_tranning.models import *

# Create your models here.
class EmployeeServicesRecruitementUpdateConsultantsDetails(models.Model):
    name = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    constitution = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Constitution")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Location")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_services_recruitement_update_consultants_details"
#
class EmployeeServicesRecruitementUpdateConsultants(models.Model):
    name = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    constitution = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Constitution")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Location")
    correspondance_address = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = " Address")
    building = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Building")
    block = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Block")
    sector = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Sector")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="City")
    district = models.CharField(max_length=200,default='', verbose_name="District")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="State")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Country")
    zip_code = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Pin code")
    cin_number = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "CIN Number")
    date_of_incorporation = models.DateField(blank = True, null = True, verbose_name = "Date of Incorporation")
    pan_card = models.CharField(unique=True,default='', blank=True, null=True, max_length=200, verbose_name = "Pan Card")
    gst_registration = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "GST Registration")
    contact_person  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Person")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    designations = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Designation")
    mobile_number  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Mobile Number")
    mail_id  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Mail id")
    services_offered  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Services Offered")
    branches  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Branches")
    experience  = models.ForeignKey(ManageExpereince, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Experience")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_services_recruitement_update_consultants"


EMPLOYEE_VACANCIES_STATUS = (
    (1, 'Request Received'),
    (2, 'Recommended'),
    (3, 'Recommended By HR'),
    (4, 'Approved'),
)


EMPLOYEE_MODE_OF_PUBLISHING = (
    (1, 'Consultant'),
    (2, 'On-Website Publicity'),
    (3, 'Advertisement'),
)


STATUS_CHOICE = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
    ('Expired', 'Expired'),
)

Urgency_CHOICE = (
    ('With in 15 days', 'With in 15 days'),
    ('With in 30 days', 'With in 30 days'),
    ('With in 3 month', 'With in 3 month'),
    ('With in 6 month', 'With in 6 month'),
)

PUBLISHING_CHOICE =(
     ('Website', 'Website'),
     ('Third Party', 'Third Party'),
     ('Consultant', 'Consultant'),
     ('Social Media', 'Social Media'),
        )
RESPONSE_CHOICE = (
     ('Online', 'Online'),
     ('Offline', 'Offline'),
     )
ACTION_STATUS = (
        
        ( "Approved", "Approved"),
         ("Hold", "Hold"),
        ("Rejected", "Rejected"),
       
    )



class EmployeeServicesRecruitementCreateRequirement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Location")
    department = models.ForeignKey(ManageDepartment,blank=True, on_delete=models.CASCADE, null=True,verbose_name='Department')    
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    existing_strength = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Existing Strength")
    employees_required  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Employees Required")
    start_salary  = models.ForeignKey(ManageSalaryRange,on_delete=models.SET_NULL, blank=True, null=True, max_length=200, verbose_name = "Salary Range")
    # salary_range  = models.ForeignKey(ManageSalaryRange,on_delete=models.SET_NULL, blank=True, null=True, max_length=200, verbose_name = "Salary Range")
    qualification  = models.ForeignKey(ManageQualification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Qualification")
    experience  = models.ForeignKey(ManageExpereince, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Experience")
    language  = models.ForeignKey(ManageLanguage,  on_delete=models.SET_NULL,blank=True, null=True, max_length=200, verbose_name = "Language")
    urgency_of_requirement   = models.CharField(choices= Urgency_CHOICE,default='With in 3 month', blank=True, null=True, max_length=200, verbose_name = "Urgency of Requirement")
    type_of_job   = models.ForeignKey(ManagementEmployeeTypeofJob, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Type of Job")
    pay_roll_job   = models.ForeignKey(ManagementEmployeePayrollofJob, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Payroll of")
    job_description   = models.TextField(default='', blank=True, null=True, max_length=200, verbose_name = "Job Description")
    valid_upto = models.DateField(blank = True, null = True, verbose_name = "Position Valid upto")
    mode_of_publishing = models.CharField(choices=PUBLISHING_CHOICE  ,default='', max_length=200, blank=True, null=True, verbose_name="Mode of Publishment")
    position_available   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Position Available")
    position_publish   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Position Published")
    place_of_job_posting   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Place of Job Posting")
    response_mode   = models.CharField(choices=RESPONSE_CHOICE  ,default='', blank=True, null=True, max_length=200, verbose_name = "Response Mode")
    vacancy_approved   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Vacancies Approved")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    comment   = models.CharField( max_length=600,blank=True, null=True,verbose_name="Comment")  
    job_link   = models.CharField( max_length=600,blank=True, null=True,verbose_name="Name")
    status = models.CharField(choices= STATUS_CHOICE, max_length=60 , default='Open',  blank=True, null=True, verbose_name="STATUS")
    action_required = models.CharField( max_length=200,choices=ACTION_STATUS, default="",  blank=True, null=True, verbose_name="Action Required")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_services_recruitement_create_requirement_model"

    # def __str__(self):
    #     return self.salary_range
        

EMPLOYEE_CANDIDATE_RESUME_STATUS = (
    (1, 'Resume Received'),
    (2, 'Resume Shortlisted'),
    (3, 'Candidates Shortlisted'),
    (4, 'Candidates Joined'),
    (5, 'Rejected'),
)


INTERVIEW_STATUS = (
    (1, 'Accept'),
    (2, 'Rejected'),
     (3, 'Hold'),
      (4, 'Delete'),
)
RESUME_STATUS_1 = (
    ('Accept', 'Accept'),
    ('Rejected', 'Rejected'),
     ('Hold', 'Hold'),
      ('Delete', 'Delete'),
)


OFFER_LETTER_STATUS = (
    (1, 'Pending'),
    (2, 'Inprogress'),
    (3, 'Completed'),
)
INTERVIEW_DETAILS = (
    ('Place of Interview', 'Place of Interview'),
    ('Timing of Interview', 'Timing of Interview'),
    ('Date of Interview', 'Date of Interview'),
    ('Contact Person', 'Contact Person'),
    
)
RECOMMENDATION_STATUS_1 =  (
    ('Interview Held', 'Interview Held'), 
    ('Postpone', 'Postpone'),
     ('Hold', 'Hold'),
     ('Cancelled', 'Cancelled'),
)
RECOMMENDATION_STATUS_1 =  (
    ('Interview Held', 'Interview Held'), 
    ('Postpone', 'Postpone'),
     ('Hold', 'Hold'),
     ('Cancelled', 'Cancelled'),
)
DOCUMNET_NAME  = (
    ('10th Certificate ', '10th Certificate '), 
    (' Graduation Certificate ', ' Graduation Certificate'), 
    ('Post Graduation Certificate', 'Post Graduation Certificate'), 
    ('Experience Certificate ', 'Experience Certificate'), 
    ('Relieving Letter ', ' Relieving Letter'), 
    ('Pan Card ', 'Pan Card '), 
    ('Aadhar Card ', 'Aadhar Card'), 
    (' Photo', 'Photo '), 
    (' Bank Statement', 'Bank Statement '), 
    (' Salary Slip', 'Salary Slip '), 
    
    )

CANDIDATE_SHORTLIST_STATUS =  (
    ('Offer Issues', 'Offer Issues'), 
    ('Expired', 'Expired'),
     ('Withdraw', 'Withdraw'),
     ('Join', 'Join'),
)
STATUS_OF_INTERVIEW =  (
    (' Attended', 'Attended '), 
    ('Postponed ', 'Postponed '), 
    (' Absent', 'Absent '), 
    
)
INTERVIEW_SCHEDULED_STATUS=  (
    (' Interview Scheduled', 'Interview Scheduled '),    
)
INTERVIEW_RESULT=  (
    (' Qualified ', ' Qualified '), 
    (' Rejected ', ' Rejected '), 
    (' Hold ', ' Hold '), 
    
)



class EmployeeServicesRecruitementInviteResume(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    received_from = models.ForeignKey(RecruitmentManagementCandidateSourcingManageReceiptofResume, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Received from")
    job_link = models.ForeignKey(EmployeeServicesRecruitementCreateRequirement , on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Received from")
    name_of_candidate  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name of Candidate")
    phone_no = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    email_id = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Email Id")
    profile_summary  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Profile Summary")
    resume_received_doc  = models.FileField(upload_to='candidates_resume/%Y/%m/%d/', blank=True, null=True, verbose_name="Resume")
    mode_of_publishing = models.CharField(choices=PUBLISHING_CHOICE  ,default='', max_length=200, blank=True, null=True, verbose_name="Mode of Publishment")
    interview_result_1 = models.CharField(choices=INTERVIEW_RESULT  ,default='', max_length=200, blank=True, null=True, verbose_name="Interview Result")
    interview_date  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Interview Date")
    interview_time  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Interview Time")
    overall_rating  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Overall Rating")
    formalities_completed_on  = models.DateField(blank = True, null = True,  verbose_name = "Formalities Completed on")
    status = models.IntegerField(choices= EMPLOYEE_CANDIDATE_RESUME_STATUS, default=1,  blank=True, null=True, verbose_name="Decision")
    interview_status = models.IntegerField(choices= INTERVIEW_STATUS, default=0,  blank=True, null=True, verbose_name="Resume Status")
    resume_status = models.CharField(choices= RESUME_STATUS_1, default='', max_length=200, blank=True, null=True, verbose_name="Resume Status")
    
    
    interview_committee = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Interview Committee")
    date_of_interview = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = " Date of Interview")
    details_of_interview = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Details of Interview")
    recommendation = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Recommendation")
    
    recommendation_1 = models.CharField(choices=RECOMMENDATION_STATUS_1, default='', blank=True, null=True, max_length=200, verbose_name = "Recommendation")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation offered")
    salary_offered  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Salary offered")
    offer_date  = models.DateField(blank = True, null = True,  verbose_name = "Offer Date")
    document_submission   = models.FileField(upload_to='candidates_upload_document/%Y/%m/%d/', verbose_name="Document", blank=True, null=True)
    date_joining_candition  = models.CharField(default='', blank=True, null=True, max_length=200,  verbose_name = "Date Joining Condition")
    date_of_joining  = models.DateField(blank = True, null = True,  verbose_name = "Date of Joining")
    joining_location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Joining Location", related_name = "joining_location")
    reporting_officer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Reporting Officer")
    offer_letter_date  = models.DateField(blank = True, null = True,  verbose_name = "Offer Letter  Date")
    offer_letter_status = models.IntegerField(choices= OFFER_LETTER_STATUS, default=0,  blank=True, null=True, verbose_name="Interview Status")
    interview_details_status = models.CharField(choices= INTERVIEW_DETAILS, max_length=200 ,default='',  blank=True, null=True, verbose_name="Interview Status")
    interview_of_status = models.CharField(choices= STATUS_OF_INTERVIEW, max_length=200 ,default='Attended',  blank=True, null=True, verbose_name="Interview Status")
    
    place_of_interview  = models.CharField(default='', blank=True, null=True, max_length=200,  verbose_name = " Place Of Interview")
    timing_of_interview = models.CharField(default='', blank=True, null=True, max_length=200,  verbose_name = " Timing Of Interview")
    date_of_interview  = models.CharField(default='', blank=True, null=True, max_length=200,  verbose_name = "Date Of Interview ")
    contact_person = models.CharField(default='', blank=True, null=True, max_length=200,  verbose_name = "Contact Person ")
    comment =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "Comment ")
    document_name = models.CharField(choices= DOCUMNET_NAME, max_length=200 ,default='',  blank=True, null=True, verbose_name=" Document Required")
    
    interview_held =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "Interview Held ")
    cancelled =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "Cancelled ")
    proposed =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "Proposed ")
    new_date =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "New Date ")
    new_time =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "New Time ")
    new_place_of_interview=  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "New Place ")
    new_contact_person =  models.CharField(default='', blank=True, null=True, max_length=800,  verbose_name = "New Contact Person ")
    candidate_shortlist_status = models.CharField(choices= CANDIDATE_SHORTLIST_STATUS, max_length=200 ,default='',  blank=True, null=True, verbose_name=" Status")
    interview_scheduled = models.CharField(choices= INTERVIEW_SCHEDULED_STATUS, max_length=200 ,default='Interview Scheduled',  blank=True, null=True, verbose_name=" Interview Scheduled")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_services_recruitement_invite_resume"
        
###############EmployeeServicesRecruitementPsychometricTest
class EmployeeServicesRecruitementPsychometricTest(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    name_of_candidate  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name of Candidate")
    status = models.IntegerField(choices= EMPLOYEE_CANDIDATE_RESUME_STATUS, default=1,  blank=True, null=True, verbose_name="Mode of Publishing")
    email     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Email Id")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)
    class Meta:
        db_table = "employee_services_recruitement_psychometrictest"
###############

# ************************ Employee Registration 
NAME_SALUTE = (
    ('Mr','Mr'),
    ('Mrs','Mrs'),
    ('Miss','Miss'),
    ('Ms','Ms'),
    ('Dr','Dr'),
    ('CA','CA'),
    ('Er.','Er.'),
    ('Prof','Prof'),
)

MARITAL_STATUS = (
    ('Single','Single'),
    ('Married','Married'),
    ('Separated','Separated'),
   
)
class EmployeeRegistrationUpdateRegistrationPersonalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    employee_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank= False, null=True, related_name = "employee_created_by")
    employee_id  = models.CharField(max_length=200, blank=True, null=True, verbose_name="Employee Id")
    mode_of_sourcing  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Mode of Sourcing")
    
    mode_of_sourcing_1  = models.CharField(choices=PUBLISHING_CHOICE,default='', blank=True, null=True, max_length=200, verbose_name = "Mode of Sourcing")
    photo = models.FileField(upload_to='upload_report/%Y/%m/%d/', blank=True, null=True, verbose_name="Photo")
    type_of_job   = models.ForeignKey(ManagementEmployeeTypeofJob, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Type of Job")
    pay_roll_job   = models.ForeignKey(ManagementEmployeePayrollofJob, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Payroll of")
    name_salute   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name Salute")
    name_salute_1   = models.CharField( choices=NAME_SALUTE ,default='', blank=True, null=True, max_length=200, verbose_name = "Name Salute")
    first_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Employee Name")
    middle_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Middle Name")
    last_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Last Name")
    date_of_birth   =models.DateField(blank = True, null = True, verbose_name = "Date of Birth")
    caste   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Caste")
    religion    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Religion ")
    marital_status     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Marital Status")
    marital_status_1     = models.CharField(choices=MARITAL_STATUS ,default='', blank=True, null=True, max_length=200, verbose_name = "Marital Status")
    mobile_no     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Mobile Number")
    email     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Email Id")
    landline_number      = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Landline Number")
    emergency_number       = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Emergency Number")
    name  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    relationship    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Language Known")
    pan_card   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Pan Card")
    adhar_card   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Adhar Card")
    driving_license    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Driving License")
    language_known    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Language Known")
    language  = models.ForeignKey(ManageLanguage,  on_delete=models.SET_NULL,blank=True, null=True, max_length=200, verbose_name = "Language")
    date_of_anniversary    = models.DateField(blank = True, null = True, verbose_name = "Date of Anniversary")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = "employee_registration_update_registration_personal_details"

class EmployeeRegistrationUpdateRegistrationFamilityDetails(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Employee Id")
    mother_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    mother_dob   = models.DateField(blank = True, null = True, verbose_name = "DOB")
    mother_occupation   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Occupation")
    mother_contact_number   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    father_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    father_dob   = models.DateField(blank = True, null = True, verbose_name = "DOB")
    father_occupation   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Occupation")
    father_contact_number   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    spouse_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    spouse_dob   = models.DateField(blank = True, null = True, verbose_name = "DOB")
    spouse_occupation   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Occupation")
    spouse_contact_number   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_family_details"


class EmployeeRegistrationUpdateRegistrationFamilityChildren(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Employee Id")
    children_name_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    children_dob_1   = models.DateField(blank = True, null = True, verbose_name = "DOB")
    children_occupation_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Occupation")
    children_contact_number_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_family_children"
OTHER_RELATIONSHIP = (
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('Spouse', 'Spouse'),
    ('Daughter', 'Daughter'),
    ('son', 'son'),
    ('Uncle', 'Uncle'),
    ('Friend', 'Friend'),

)

class EmployeeRegistrationUpdateRegistrationFamiliyOtherDetails(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Employee Id")
    other_name_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    other_dob_1   = models.DateField(blank = True, null = True, verbose_name = "DOB")
    other_occupation_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Occupation")
    other_relationship   = models.CharField(choices=OTHER_RELATIONSHIP,  default='', blank=True, null=True, max_length=200, verbose_name = "Other RelationShip")
    other_contact_number_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_family_other_details"


class EmployeeRegistrationUpdateRegistrationMedicalHistory(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    name_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    blood_group_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Blood Group")
    type_of_illness_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Type of Illness")
    result_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Result")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_medical_history"

OWNERSHIP_STATUS = (
    ('Self on','Self on'),
    ('Rented','Rented'),
    ('Family On','Self On'),
)
class EmployeeRegistrationCorrespondenceAddress(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    building   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Building")
    block   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Block")
    sector    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Sector")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="City")
    district   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "District")
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="State")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Country")
    zip_code     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Zip code")
    staying_since = models.DateField(blank = True, null = True, verbose_name = "Staying since")
    ownership     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Ownership")
    ownership_1     = models.CharField(choices=OWNERSHIP_STATUS ,default='', blank=True, null=True, max_length=200, verbose_name = "Ownership")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_correspondance"


class EmployeeRegistrationPermanentAddress(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    building_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Building")
    block_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Block")
    sector_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Sector")
    city_1 = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="City")
    district_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "District")
    state_1 = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="State")
    country_1 = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Country")
    zip_code_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Zip code")
    staying_since_1 = models.DateField(blank = True, null = True, verbose_name = "Staying since")
    ownership_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Ownership")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_parmanent_address"


class EmployeeRegistrationUpdateRegistrationJoiningDetails(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    joining_location   = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Location")
    joining_date_of_joining    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Date of Joining")
    joining_time     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Joining Time")
    joining_grade_offered     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Grade offered")
    joining_next_date_of_increment    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Next Date of Increment")
    joining_department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, null=True, verbose_name="Department")
    joining_designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, null=True, verbose_name="Designation")
    joining_responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL, null=True, verbose_name="Responsibility")
    joining_role = models.ForeignKey(RoleMangement, on_delete=models.SET_NULL, null=True, verbose_name="Role")
    joining_reporting_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Reporting To")
    joining_probation_period  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Probation Period")
    contract_valid_up_to  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Contract Valid Up To")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_registration_joining_detail"


class EmployeeRegistrationUpdateRegistrationJoiningDetailsHistory(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Employee Id")
    current_designation = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Designation")
    new_designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, null=True, verbose_name="New Designation")
    current_department  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Department")
    new_department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, null=True, verbose_name="New Department")
    current_reporting = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Reporting To")
    new_reporting = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="New Reporting To")
    current_responsibilites = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Responsibilit")
    new_responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL, null=True, verbose_name="New Responsibility")
    current_location  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Current Location")
    new_location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "New Location")
    current_role  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Current Role")
    joining_role = models.ForeignKey(RoleMangement, on_delete=models.SET_NULL, null=True, verbose_name="New Role")
    current_salary  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Current Salary")
    new_salary  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="New Salary")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_joining_details_history"


class EmployeeRegistrationUpdateEducationalQualification(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    educational_qualificationcourse_name_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Course Name")
    educational_qualificationstart_date_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Start Date")
    educational_qualificationend_date_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "End Date")
    educational_qualificationmarks_division_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Marks / Division")
    educational_qualificationroll_number_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Roll Number")
    educational_qualificationuniversity_institution_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "University / Institution")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_educational_qualification"


class EmployeeRegistrationUpdateProfessionalJourney(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    professional_journeycompany_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Company")
    professional_journeystart_date_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Start Date")
    professional_journeyend_date_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "End Date")
    professional_journeylast_desgination_1   = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, null=True, verbose_name="Last Designation")
    professional_journeynature_of_duties_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Nature of Duties")
    professional_journeylast_drawn_dalary_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Last Drawn Salary")
    reason_for_leaving_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Reason for Leaving")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_professional_journey"
TAXABILITY_STATUS = (
    ('Yes','Yes'),
    ('No','No'),
)


class EmployeeRegistrationUpdateSalaryStructutre(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    salary_structut_salary_code_1  = models.ForeignKey(ManageSalary, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Salary Code")
    salary_structut_salary_name_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Salary Name")
    salary_structut_salary_frequency_1  = models.IntegerField(choices = FREQUENCY, default=1, blank=True, null=True, verbose_name = "Salary Frequency")
    salary_structut_amount_offered_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Amount offered")
    salary_structut_percentage_value_flag_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Percentage/ Value Flag")
    salary_structut_taxability_1      = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Taxability")
    salary_structut_taxability_status      = models.CharField(choices=TAXABILITY_STATUS ,default='', blank=True, null=True, max_length=200, verbose_name = "Taxability")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_salary_structutre"


class EmployeeRegistrationDeductionAndPerquisites(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    appicablitity_1 = models.IntegerField(choices= YESNO, default=1,  blank=True, null=True, verbose_name="Applicablitity")
    perquisitec_category_1 = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Perquisite Code")
    perquisitec_name_1 = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Perquisite Name")
    perquisite_frequency_1 = models.IntegerField(choices = FREQUENCY, default=1, blank=True, null=True, verbose_name = "Perquisite Frequency")
    percentage_value_flag_1 = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Percentage/ Value Flag")
    perquisite_amount_1 = models.IntegerField(default=0, blank=True, null=True,  verbose_name = "Perquisite Amount")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_deduction_and_perquisites"
class EmployeeRegistrationDeduction(models.Model):
    applicated  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Applicated")
    deduction_code  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Deduction Code")
    deduction_name = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Deduction Name")
    deduction_frequancy = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Deduction Frequancy")
    deduction_ammount = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Deduction Ammount")
    class Meta:
        db_table = "employee_registration_deduction"
class EmployeeRegistrationUpdateBankDetails(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    account_type   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Account Type")
    bank_account_number    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Bank Account Number")
    bank_name    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Bank Name")
    branch     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Branch")
    ifscc_code     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "IFSC Code")
    micr       = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "MICR ")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_registration_bank_details"


class EmployeeRegistrationReferences(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    referencename_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name")
    referencerelationship_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Relationship")
    referencecontact_number_1    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Contact Number")
    referenceemail_id_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Email id")
    referenceaddress_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Address")
    referenceknown_since_1     = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Known since")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_registration_references"

Verification_STATUS = (
    ('Accept', 'Accept'),
    ('Rejected', 'Rejected'),
)
  

class EmployeeRegistrationVerificationReport(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    verification_agency_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name of Report")
    finding_1     = models.CharField( max_length=200, choices= Verification_STATUS, default='',  blank=True, null=True, verbose_name = "Verification Agency Finding ")
    upload_report_1   = models.FileField(upload_to='upload_report/%Y/%m/%d/', verbose_name="Upload Report")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_verification_report"

          
class EmployeeRegistrationDocuments(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    name_of_documents_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Name of Documents")
    upload_1   = models.FileField(upload_to='upload_report/%Y/%m/%d/', verbose_name="Upload")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_registration_documents"


class EmployeeAssetAllocated(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    asset_code_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Asset Code")
    asset_serial_number_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Asset Serial Number")
    asset_name_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Asset Name")
    asset_condition_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Asset Condition")
    asset_location_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Asset Location")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_asset_allocated"


class EmployeeAccessControls(models.Model):
    user_employee  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    official_email_id   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Official Email Id")
    official_contact_number   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Official Contact Number")
    id_card_number   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "ID Card number")
    system_access_id   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "System Access Id")
    attendance_card_number   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Attendance Card Number")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_access_controls"


class EmployeeRegistrationUpdateDepartment(models.Model):
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User Id")
    employee_name   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Employee Name")
    current_designation   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Designation")
    new_designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, null=True, verbose_name="New Designation")
    current_department    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Department")
    new_department  = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, null=True, verbose_name="New Department")
    current_reporting_to = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Current Reporting To")
    new_reporting_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="New Reporting To")
    current_responsibilites   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Responsibilites")
    new_responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL, null=True, verbose_name="New Responsibility")
    current_location   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Location")
    new_location   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "New Location")
    current_salary    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Current Salary")
    new_salary    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "New Salary")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_registration_update_department"


LEAVE_STATUS = (
    (1, "Pending for Approval"),
    (2, "Approved"),
    (3, "Rejected"),
    (4, "Cancel"),
)


# Leaves
class EmployeeLeavesLeaveRequest(models.Model):
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employee Id")
    employee_names   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Employee Name")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    type_of_leave  = models.ForeignKey(HolidaysandLeavesLeaveType, on_delete=models.SET_NULL, blank= False, null=True, verbose_name = "Type of Leave")
    leave_available    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Leave Available")
    start_date    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Start Date")
    end_date    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "End Date")
    total_leave    = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Total Leave")
    explaination    = models.TextField(default='', blank=True, null=True, max_length=200, verbose_name = "Explaination")
    status = models.IntegerField(choices=LEAVE_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_leaves_leave_request"


class EmployeeHRPoliciesUpdatePolicies(models.Model):
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True)
    policy_type  = models.ForeignKey(HRPoliciesPolicyType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Policy Type")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    upload   = models.FileField(upload_to='upload_hr_policies/%Y/%m/%d/', verbose_name="Upload(PDF File Only)")
    effect_date = models.DateTimeField(blank = True, null = True, verbose_name = "Effect Date(Format:2019-08-05)")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.policy_type

    class Meta:
        db_table = "employee_hr_policies_update_policies_model"


class EmployeeHRPoliciesUpdateForm(models.Model):
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True)
    form_type  = models.ForeignKey(PoliciesandFormsManagementHRPolicies, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Form Type")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    upload   = models.FileField(upload_to='upload_hr_policies/%Y/%m/%d/', verbose_name="Upload(PDF File Only)")
    effect_date = models.DateTimeField(blank = True, null = True, verbose_name = "Effect Date")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.form_type

    class Meta:
        db_table = "employee_hr_policies_update_form_model"


class EmployeeHrPoliciesUpdateCirculars(models.Model):
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True)
    circular_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Circular Type")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    upload   = models.FileField(upload_to='upload_hr_policies/%Y/%m/%d/', verbose_name="Upload(PDF File Only)")
    effect_date = models.DateTimeField(blank = True, null = True, verbose_name = "Effect Date")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.circular_type

    class Meta:
        db_table = "employee_hr_policies_update_circulars_model"


CLAIM_STATUS = (
    (1, "Pending"),
    (2, "Approved"),
    (3, "Rejected"),
)

CLAIM_Reimbursement_STATUS = (
        ("Pending", "Pending"),
        ( "Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

# Claim and Reimbursement
class EmployeeClaimandReimbursementSubmitClaims(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employee Id")
    
    employee_names =  models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Employee Name ")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    approved_by  = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True, related_name = "claim_approved_by")
    claim_date_1 = models.DateTimeField(blank = True, null = True, verbose_name = "Claim  Date")
    claim_type_1  = models.ForeignKey(ManageClaimType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Claim Type")
    claim_period_1  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Claim Period")
    claim_details_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Claim Details")
    claim_amount_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Claim Amount")
    claim_restriced_to_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Claim Restriced To")
    comment_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Comment")
    approved_amount_1 = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount Approved")
    upload_1   = models.FileField(upload_to='upload_hr_policies/%Y/%m/%d/', verbose_name="Upload(PDF File Only)")
    date_of_processing = models.DateTimeField(blank = True, null = True, verbose_name = "Date of Processing")
    status = models.CharField( max_length=200,choices=CLAIM_Reimbursement_STATUS, default="",  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_claimand_reimbursement_submit_claims"

class EmployeeClaimandReimbursementSubmitClaimsUpdateStatus(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    submit_claim  = models.OneToOneField(EmployeeClaimandReimbursementSubmitClaims, on_delete=models.CASCADE, blank= False, null=True)
    approved_amount = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount Approved")

    class Meta:
        db_table = "employee_claimand_reimbursement_submit_claims_update_status"



class EmployeeClaimandReimbursementSubmitReimbursement(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employee Id")
    
    employee_names =  models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Employee Name ")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    approved_by  = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True, related_name = "reimbursement_approved_by")
    reimbursement_month_1 = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    reimbursement_type_1 = models.ForeignKey(ManageReimbursement, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Reimbursement Type")
    reimbursement_period_1  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Reimbursement Period")
    amount_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount")
    maximum_limit_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Maximum Limit")
    comment_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Comment")
    upload_1   = models.FileField(upload_to='upload_hr_policies/%Y/%m/%d/', verbose_name="Upload(PDF File Only)")
    status = models.CharField( max_length=200,choices=CLAIM_Reimbursement_STATUS, default='Pending',  blank=True, null=True, verbose_name="Status")
    approved_amount_1   = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount Approved")
    approved_amount = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount Approved")
    
    date_of_processing = models.DateTimeField(blank = True, null = True, verbose_name = "Date of Processing")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_claimand_reimbursement_submit_reimbursement"

class EmployeeClaimandReimbursementSubmitReimbursementUpdateStatus(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    submit_claim  = models.OneToOneField(EmployeeClaimandReimbursementSubmitReimbursement, on_delete=models.CASCADE, blank= False, null=True)
    approved_amount = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount Approved")

    class Meta:
        db_table = "employee_claimand_reimbursement_submit_reimbursement_update_status"

class EmployeePayrollProcessingUpdateAdvances(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    location = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    department = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    month_and_year = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    advance_type = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    recovery_period  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    advance_amount  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    interest_rate   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    total_amount    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    recovery_amount    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    recovery_start_date    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_payroll_processing_update_advances"


class EmployeePayrollProcessingUpdateIncentives(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    location = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    department = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    month_and_year = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    incentive_type  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    incentive_period  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    incentive_amount  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Reimbursement Month")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_payroll_processing_update_incentive"


class EmployeePayrollProcessingUpdateTaxDeclaration(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employee Id")
    
    employee_names  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Employee Name")
    departments = models.CharField(max_length=200, blank=True, null=True, verbose_name="Departments")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Location")
    assessment_year = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Assessment Year")
    tax_declaration_type  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Tax Declaration Type")
    tax_rule  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Tax Rule")
    exemption_claimed  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Exemption Claimed")
    exemption_approved  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Exemption Approved")
    maximum_limit  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=False, verbose_name="Status")
    status1 = models.CharField(max_length=200, choices=CLAIM_Reimbursement_STATUS, default='Pending',  blank=True, null=False, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "employee_payroll_processing_tax_declaration"

####
class EmployeePayrollProcessingUpdateTaxRecovery(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Location")
    departments = models.CharField(max_length=200, blank=True, null=True, verbose_name="Departments")
    assessment_year = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Assessment Year")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employee Id")
    
    employee_names  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Employee Name")
    year_to_date_salary  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Tax Recovery Type")
    annual_salary  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Annual Salary")
    total_tax_payable  =  models.CharField(max_length=200, blank = True, null = True, verbose_name = "Total Tax Payable")
    tax_already_recovered =  models.CharField(max_length=200, blank = True, null = True, verbose_name = "Tax already Recovered")
    recovery_during_current_month =  models.CharField(max_length=200, blank = True, null = True, verbose_name = "Recovery During Current Month")
    total_tax_recovered =  models.CharField(max_length=200, blank = True, null = True, verbose_name = "Total Tax Recovered")
    balance_tax_payable =   models.CharField(max_length=200, blank = True, null = True, verbose_name = "Balance Tax Payable")
    status = models.CharField(max_length=200, choices=CLAIM_Reimbursement_STATUS, default='Pending',  blank=True, null=False, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "employee_payroll_processing_tax_recovery"




class EmployeePayrollProcessingTaxCalculation(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    departments = models.CharField(max_length=200, blank=True, null=True, verbose_name="Department")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Location")
    assessment_year = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Departments")
    year_to_date_salary  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Tax Declaration Type")
    annual_salary  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Tax Rule")
    other_income  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Exemption Claimed")
    total_income  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Exemption Approved")
    exemption  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    deduction  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    taxable_income  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    tax  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    cess   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    total_tax_payable    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    tax_deducted    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    tax_paid    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    balance_tax_payable    = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Maximum Limit")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_payroll_processing_tax_calculation"


class EmployeePayrollProcessingUpdateRecoveries(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    
    employee_names  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Employee Name")
    departments = models.CharField(max_length=200, blank=True, null=True, verbose_name="Department")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Location")
    month_and_year = models.CharField(max_length=200, blank = True, null = True)
    recovery_period   = models.CharField(max_length=200, blank = True, null = True)
    recovery_type  = models.CharField(max_length=200, blank = True, null = True)
    recovery_amount  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Exemption Claimed")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_payroll_processing_update_recoveries"


# Key Responsibility Areas & Targets
class KeyResponsibilityAreasTargetsUpdateKRATargets(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "User Id")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employee Id")
    employee_names  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Employee Name")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    month_and_year = models.DateField(blank = True, null = True, verbose_name = "Month & Year ")
    kra_type   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "KRA Type")
    kra_frequency  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "KRA Frequency")
    kra_details  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "KRA Details")
    kra_fulfilment   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "KRA Fulfilment")
    reporting_officer   = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "Reporting Officer", related_name = "reporting_officer")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "key_responsibility_areas_targets_update_kra_targets"


RESIGNATION_STATUS = (
    (1, "Pending"),
    (2, "Approved"),
    (3, "Full and Final Settlement"),
    (4, "Rejected"),
    (5, "Release"),
)

COMMON_RESIGNATION_STATUS = (
    (1, "Pending"),
    (2, "Inprocess"),
    (3, "Complete"),
)
FINAL_SAL_STATUS = (
    ("Pending", "Pending"),
    
    ( "Setter", "Setter"),
)
class EmployeeExitEmployeeResignation(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "Employee Id")
    employee_id = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "Employee Id")
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    reporting_officer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Reporting Officer", related_name = "reporting_officers")
    resignation_date = models.DateField(blank = True, null = True, verbose_name = "Resignation Date")
    reasons_for_resignation  = models.CharField(max_length=500, blank = True, null = True, verbose_name = "Reasons for Resignation")
    notice_period_applicability = models.IntegerField(choices=YESNO, default=1,  blank=True, null=True, verbose_name="Notice Period Applicability")
    notice_period_required  = models.IntegerField(choices=YESNO, default=0,  blank=True, null=True,  verbose_name = "Notice Period Required")
    notice_period_waived   = models.IntegerField(choices=YESNO, default=0,  blank=True, null=True,  verbose_name = " Notice Period Waived")
    notice_period_to_be_served   = models.IntegerField(default=0,  blank=True, null=True,  verbose_name = "Notice Period to be Served(In days)")
    status = models.IntegerField(choices=RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    notice_pay_deducted = models.IntegerField(choices=YESNO, default=0,  blank=True, null=True, verbose_name="Notice Pay Deducted")
    status_of_assets_allocated = models.IntegerField(choices=COMMON_RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Status of Assets Allocated")
    status_of_responsibility_handover = models.IntegerField(choices=COMMON_RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Status of Responsibility Handover")
    status_of_formalities_completed_status_of_exit_interview  = models.IntegerField(choices=COMMON_RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Status of Formalities completed  Status of Exit Interview")
    status_of_relieving_letters_status_of_full_and_final_settlement  = models.IntegerField(choices=COMMON_RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Status of Relieving Letters  Status of Full and Final Settlement")
    final_salary_status  = models.IntegerField(choices=COMMON_RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Final Salary Status")
    
    final_sal_status  = models.CharField(max_length=200,choices=FINAL_SAL_STATUS, default='',  blank=True, null=True, verbose_name="Final Salary Status")
    net_salary = models.CharField(max_length=200, blank = True, null = True, verbose_name="Net Salary")

    approved_date = models.DateTimeField(blank = True, null = True)
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_exit_employee_resignation"
##
##
class LeaveandHolidaysManagementUpdateLeavesQuota(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "Employee Id")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    first_name  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Name",related_name='first_names')
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    leave_type  = models.ForeignKey(HolidaysandLeavesLeaveType, on_delete=models.SET_NULL, blank= True, null=True, verbose_name = "Leave Type")
    financial_year = models.ForeignKey(ManageFinancialYear, on_delete=models.SET_NULL, blank= True, null=True, verbose_name="Financial Year")
    leave_balance = models.CharField(max_length=200, blank = True, null = True, verbose_name="Total Leave Quota")
    leave_added = models.CharField(max_length=200, blank = True, null = True, verbose_name="Leave Added")
    frequency_of_leave = models.CharField(max_length=200, blank = True, null = True, verbose_name="Frequency of Leave")
    impact_on_salary   = models.IntegerField(choices=YESNO, default=0,  blank=True, null=True,  verbose_name = "Impace on Salary")
    maximum_limit_carry_forward_allowed   = models.CharField(max_length=200, blank = True, null = True,  verbose_name = "Maximum Limit Carry forward Allowed")
    encashment_allowed   = models.IntegerField(choices=YESNO, default=0,  blank=True, null=True,  verbose_name = "Encashment allowed")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "leave_and_holidays_management_leaves"
        unique_together = ('user', 'leave_type',)


class OvertimeManagementUpdateOvertime(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "Employee Id")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    employee_names  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Employee Name")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    month_and_year_date = models.DateField(blank = True, null = True, verbose_name = "Month & Year Date")
    overtime_start = models.CharField(max_length=200, blank = True, null = True, verbose_name="Over Time Start")
    overtime_end = models.CharField(max_length=200, blank = True, null = True, verbose_name="Overtime End")
    total_hours = models.IntegerField(default =0, blank = True, null = True, verbose_name="Total Hours")
    reason = models.TextField(blank = True, null = True, verbose_name="Reason")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "over_time_management_update_over_time"

CLAIM_STATUS = (
    ("Pending", "Pending"),
    ( "Approved", "Approved"),
    ("Rejected", "Rejected"),
)
class TravelClaimManagementTravelConveyanceTravelRequest(models.Model):
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    mode_of_travel  = models.ForeignKey(TravelandClaimTravelManagementModeofTravel, on_delete=models.SET_NULL, blank= True, null=True, verbose_name = "Mode of Travel")
    no_of_days = models.CharField(max_length=200, blank = True, null = True, verbose_name="No of Days")
    travel_start_date =  models.DateField(blank = True, null = True, verbose_name="Travel Start Date")
    travel_end_date =  models.DateField(blank = True, null = True, verbose_name="Travel End Date")
    stay_arrangement = models.IntegerField(choices=YESNO, default=0,  blank=True, null=True, verbose_name="Stay Arrangement")
    total_travel_cost = models.CharField(max_length=200, blank = True, null = True, verbose_name="Total Travel Cost")
    advance_required  = models.CharField(max_length=200, blank = True, null = True, verbose_name="Advance Required")
    reasons_for_travel   = models.CharField(max_length=200, blank = True, null = True, verbose_name="Reasons for Travel")
    status = models.CharField(max_length=200,choices=CLAIM_STATUS, default='Pending',  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "travel_claim_management_travel_conveyance_travel_requests"

REQUEST_STATUS = (
    (1, "Pending"),
    (2, "Processing"),
    (3, "Processed "),
)


REQUEST_EMP_STATUS = (
    ("Pending", "Pending"),
    ("Processing", "Processing"),
    ("Processed", "Processed "),
)

YES_NO =(
    ("YES","YES"),
    ("NO","NO")
)
# Employee Advances 
class EmployeeAdvancesSubmitAdvanceRequest(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "User")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    approved_by   = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True, related_name = "employee_advance_approved_by")
    advance_type_1   = models.ForeignKey(ManagePayRollDefineAdvances, on_delete=models.SET_NULL, blank= True, null=True, verbose_name = "Advance Type")
    advance_amount_1 = models.CharField(max_length=200, blank = True, null = True, verbose_name="Advance Amount")
    recovery_start_from_1 = models.DateField(blank = True, null = True, verbose_name="Recovery Start from")
    recovery_period_1 = models.CharField(max_length=200, blank = True, null = True, verbose_name="Recovery Period")
    justification_1 = models.CharField(max_length=200, blank = True, null = True, verbose_name="Justification")
    status = models.CharField(max_length=200,choices=REQUEST_EMP_STATUS, default='Pending',  blank=True, null=True, verbose_name="Approval Status")
    advance_approved_1 = models.CharField(max_length=200,choices=YES_NO, default="NO",  blank=True, null=True, verbose_name="Advance Approved")
    payment_status  = models.CharField(max_length=200,choices=YES_NO, default="NO",  blank=True, null=True, verbose_name="Payment Status ")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_advances_submit_advance_request"


# Incentive &  Bonus 
class EmployeeAdvancesSubmitIncentiveBonus(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True, verbose_name = "User")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    approved_by   = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True, related_name = "employee_incentive_approved_by")
    incentive_type = models.CharField(max_length=200, blank = True, null = True, verbose_name="Incentive Type")
    incentive_period = models.CharField(max_length=200, blank = True, null = True, verbose_name="Incentive Period")
    incentive_amount = models.CharField(max_length=200, blank = True, null = True, verbose_name="Incentive Amount")
    status = models.CharField(max_length=200,choices=REQUEST_EMP_STATUS, default="Pending",  blank=True, null=True, verbose_name="Approval Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_advances_submit_incentive_bonus"


class ManageProductTrainingSendWishToAttend(models.Model):
    traning_id = models.ForeignKey(ManageKnowledgeProductTraining, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Training")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="User")
    status = models.IntegerField(choices= COMMON_RESIGNATION_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "manage_product_training_send_wish_to_attend"


class PayrollStatutoryDeductions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User")
    deduction_type = models.ForeignKey(ManagePayRollStatutoryDeductions, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Deduction Type")
    employer_contribution = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employer Contribution")
    employee_contribution = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Contribution")
    month_and_year= models.DateField(blank = True, null = True, verbose_name="Month and Year")
    others = models.CharField(max_length=200, blank = True, null = True, verbose_name="Others")
    total_deduction = models.CharField(max_length=200, blank = True, null = True, verbose_name="Total Deduction")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "payroll_statuary_deduction"



class PayrollSalaryVoucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User")
    month_and_year= models.CharField(max_length=200, blank = True, null = True, verbose_name="Month and Year")
    gl_code = models.CharField(max_length=200, blank = True, null = True, verbose_name="GL Code")
    particulars = models.CharField(max_length=200, blank = True, null = True, verbose_name="Particulars")
    debit_amount = models.CharField(max_length=200, blank = True, null = True, verbose_name="Debit Amount")
    credit_amount = models.CharField(max_length=200, blank = True, null = True, verbose_name="Credit Amount")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "payroll_salary_voucher_data"


class PayrollSalaryDisbursement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = "Employee Id")
    
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    month_and_year= models.CharField(max_length=200, blank = True, null = True, verbose_name="Month and Year")
    bank_name = models.CharField(max_length=200, blank = True, null = True, verbose_name="Bank Name")
    ifsc_code = models.CharField(max_length=200, blank = True, null = True, verbose_name="IFSC Code")
    account_number = models.CharField(max_length=200, blank = True, null = True, verbose_name="Account Number")
    amount = models.CharField(max_length=200, blank = True, null = True, verbose_name="Amount")
    mode_of_payment = models.CharField(max_length=200, blank = True, null = True, verbose_name="Mode of Payment")
    date_of_payment  =  models.CharField(max_length=200, blank = True, null = True, verbose_name="Date of Payment")
    status = models.IntegerField(choices=CLAIM_STATUS, default=1,  blank=True, null=True, verbose_name="Status")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "payroll_salary_disbursement"


##
days_in_month = (
    (25,25),
    ( 24,24),
    (23,23),
    (22,22),
)
monthly_off = (
    (8,8),
    ( 6,6),
    (5,5),
    (4,4),
)
working_days = (
    (24,24),
    (23,23),
    (22,22),
    (21,21)
   
)
PAYROLL_STATUS = (
    ("Pending", "Pending"),
    ( "Approved", "Approved"),
    ("Rejected", "Rejected"),
)
class EmployeePayrollProcessed(models.Model):
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    
    month_and_year= models.ForeignKey(EmployeePayrollProcessingUpdateAdvances,on_delete=models.CASCADE, blank = True, null = True, verbose_name="Month and Year")
    employee_id  = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank = True, null = True, verbose_name = "Employee Id",related_name='employee_ids')
    first_name =  models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails, on_delete=models.CASCADE, blank = True, null = True, verbose_name = "Employee Name", related_name='employee_name')
    employee_names = models.CharField(max_length=200, blank = True, null = True, verbose_name="Employee Name")
    days_in_month = models.IntegerField(choices=days_in_month, default="",  blank=True, null=True, verbose_name="Days In Month")
    monthly_off = models.IntegerField(choices=monthly_off, default="",  blank=True, null=True, verbose_name="Month Off")
    working_days  = models.IntegerField(choices=working_days, default="",  blank=True, null=True, verbose_name="Working Days")
    holidays = models.CharField(max_length=200, blank = True, null = True, verbose_name="Holidays")
    leave_balance = models.ForeignKey(LeaveandHolidaysManagementUpdateLeavesQuota,on_delete=models.CASCADE, blank = True, null = True, verbose_name="Total Leave ")
    leave_type  = models.ForeignKey(HolidaysandLeavesLeaveType, on_delete=models.SET_NULL, blank= True, null=True, verbose_name = "Leaves Type")
    leave_without_pay = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="Leave withOut Pay")
    joining_grade_offered = models.ForeignKey(EmployeeRegistrationUpdateRegistrationJoiningDetails,on_delete=models.SET_NULL, blank = True, null = True, verbose_name="Grad")
    pan_card   = models.ForeignKey(EmployeeRegistrationUpdateRegistrationPersonalDetails,on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Pan Card")
    pan_card_1   = models.CharField(max_length=200, blank=True, null=True, verbose_name = "Pan Card")
    
    basic_pay = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="Basic Pay")
    hra_allowances = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="HRA Allowances")
    conveyance = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="Conveyance")
    claim_type   = models.ForeignKey(ManageClaimType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Claim ")
    reimbursement_type_1 = models.ForeignKey(ManageReimbursement, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Reimbursement Type")
    Incentive_1   = models.CharField(max_length=200, blank = True, null = True, verbose_name="Incentive Gross Salary")
    performance_bonus  = models.CharField(max_length=200, blank = True, null = True, verbose_name="Performance Bonus Gross Salary")
    basic_pay  = models.CharField(max_length=200, blank = True, null = True, verbose_name="Basic Pay")
    hra_allowances_1  = models.CharField(max_length=200, blank = True, null = True, verbose_name="HRA Allowances")
    conveyance_1 =  models.CharField(max_length=200, blank = True, null = True, verbose_name="Conveyance")
    claim_amount_1 = models.ForeignKey( EmployeeClaimandReimbursementSubmitClaims, on_delete=models.CASCADE ,blank = True, null = True, verbose_name="Conveyance")
    Reimbursement =	models.CharField(max_length=200, blank = True, null = True, verbose_name="Conveyance")
    incentive_2  =	 models.CharField(max_length=200, blank = True, null = True, verbose_name="Incentive Salary Earned")
    total  = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="Total Gross Salary")
    performance_bonus	=	 models.CharField(max_length=200, blank = True, null = True, verbose_name="Performance Bonus Salary Earned")	 
    total_1	=	 models.CharField(max_length=200 ,blank = True, null = True, verbose_name="Total Salary Earned")
    pf = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="PF Deduction Details")	
    esic = models.CharField(max_length=200, blank = True, null = True, verbose_name="ESIC Deduction Details")
    absent	 = models.CharField(max_length=200, blank = True, null = True, verbose_name="Absent Deduction Details")
    income  = models.CharField(max_length=200, blank = True, null = True, verbose_name="Income Deduction Details")
    tax	 = models.CharField(max_length=200 ,blank = True, null = True, verbose_name="TAX Deduction Details")
    loan_recovery	= models.CharField(max_length=200 ,blank = True, null = True, verbose_name="Loan Recovery Deduction Details")
    total_2	= models.CharField(max_length=200, blank = True, null = True, verbose_name="Total Deduction Details")
    net_salary_payable = models.CharField(max_length=200, blank = True, null = True, verbose_name="Total Salary Earned")
    bank_name = models.CharField(max_length=200, blank = True, null = True, verbose_name="Bank Name")
    ifsc_code = models.CharField(max_length=200, blank = True, null = True, verbose_name="IFSC Code")
    account_number = models.CharField(max_length=200,  blank = True, null = True, verbose_name="Account Number")
    amount = models.CharField(max_length=200  ,blank = True, null = True, verbose_name="Amount")
    mode_of_payment = models.CharField(max_length=200, blank = True, null = True, verbose_name="Mode of Payment")
    date_of_payment  =  models.CharField(max_length=200, blank = True, null = True, verbose_name="Date of Payment")
    status = models.CharField(max_length=200,choices=PAYROLL_STATUS, default="Pending",  blank=True, null=True, verbose_name="Status")
    date_of_processing = models.DateTimeField(blank = True, null = False, verbose_name = "Date of Processing")
    upload = models.FileField(upload_to='documents/%Y/%m/%d/',verbose_name="Template Upload")
    upload_1   = models.FileField(upload_to='upload_report/%Y/%m/%d/', verbose_name="Upload")
    
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "employee_payroll_processed"

   