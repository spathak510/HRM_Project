from django.db import models
from hrms_management.models import *



FREQUENCY = (
    (1, "Monthly"),
    (2, "Yearly"),
)

# Create your models here.
class ManageEmployeeReportingStructure(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    reporting_to =  models.CharField(max_length=200, default=None, blank=True, null=True, verbose_name="Reported To")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    role = models.ForeignKey(RoleMangement, on_delete=models.SET_NULL,  null=True, verbose_name="Role")
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_employee_reporting_structure"


class ManageEmployeeId(models.Model):
    employee_id = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Employee Id")
    unique_id = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Sector")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) +'/'+ str(self.employee_id )

    class Meta:
        db_table = "manage_employees_id"


class ManageGrade(models.Model):
    grade_type = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Grade Type")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.grade_type)


    class Meta:
        db_table = "manage_employee_grade"

class ManageSalary(models.Model):
    salary_code = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Salary Code")
    salary_type = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Salary Type")
    salary_frequency  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Salary Frequency")
    measurement  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Measurement")
    taxablility   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Taxablility")
    display_type   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Display Type")
    limit = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Limit")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.salary_code

    class Meta:
        db_table = "manage_employee_salary"

##
class ManageDeductionsStructure(models.Model):
    deduction_category = models.CharField(unique = True, max_length=50, blank=False, null=False, default='', verbose_name="Deduction Category")
    deduction_type = models.CharField(max_length=50, blank=False, null=False, default='', verbose_name="Deduction Type")
    deduction_name  = models.CharField(max_length=10, blank=False, null=False, default='', verbose_name="Deduction Name")
    deduction_amount  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Deduction Amount")
    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    frequency   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Frequency")
    basis_of_calculation = models.CharField(max_length=200, default='',  blank=True, null=True, verbose_name="Basis of Calculation")
    minimum = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Minimum")
    maximum = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum")
    part_of_ctc = models.CharField(max_length=200, default='',  blank=True, null=True, verbose_name="Part of CTC")
    deduction_from_payroll  = models.CharField(max_length=200, default='',  blank=True, null=True, verbose_name="Deduction from Payroll")
    start_date1 = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_deduction_structure"


class ManageOtherIncome(models.Model):
    income_type = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Income Type")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_employee_other_income"


class ManageLanguage(models.Model):
    language  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Language")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_employee_language"


class ManageQualification(models.Model):
    type_of_qualification  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Type of Qualification")
    qualification  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Qualification")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_employee_qualification"


class ManageExpereince(models.Model):
    experience_type  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Experience Type")
    experience  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Experience")
    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_employee_expereince"


class ManageFamily(models.Model):
    relationship  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Relationship")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_employee_family"


# Manage Pay Roll
class ManagePayRollTaxStructure(models.Model):
    assessment_year  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Assessment Year")
    tax_type  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Tax Type")
    minimum  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Minimum")
    maximum  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum")
    tax_rate  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Tax Rate")
    cess_type  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Cess Type")
    cess_rate  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Cess Rate")
    surcharge_rate  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Surcharge Rate")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_pay_roll_tax_structure_model"


class ManagePayRollReimbursement(models.Model):
    reimbursement_type  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Reimbursement Type")
    reimbursement_name  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Reimbursement Name")
    applicable_to  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Applicable to")
    impact_on_tax = models.IntegerField(choices= YESNO, default=1,  blank=True, null=True, verbose_name="Impace On Tax")
    part_of_salary   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Part of Salary")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_pay_roll_reimbursement"


class ManagePayRollExemptedIncome(models.Model):
    income_type  = models.ForeignKey(ManageOtherIncome, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Income Type")
    provision_of_tax_rules  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Provision of Tax Rules")
    maximum_limit  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Maximum Limit")
    criteria  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Criteria")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    end_date   = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_pay_roll_exempted_income"


class ManagePayRollStatutoryDeductions(models.Model):
    deduction_type  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Deduction Type")
    provision_of_rules  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Provision of Rules")
    salary_code  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Salary Code")
    minimum  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Minimum")
    maximum  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum")
    employee_contribution  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Employee Contribution")
    admin_charges  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Admin Charges")
    part_of_ctc  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Part of CTC")
    part_of_taxable_perquisite  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Part of Taxable Perquisite")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    end_date   = models.DateField(blank=True, null=True, verbose_name="End Date")
    description = models.TextField(blank = True, null = True)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.deduction_type

    class Meta:
        db_table = "manage_pay_roll_statutory_deductions"


class ManagePayRollDefineAdvances(models.Model):
    advance_type  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Advance Type")
    minimum_limit  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Minimum Limit")
    maximum_limit  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum Limit")
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grades  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Grades")
    base_rate   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Base Rate")
    interest_rate    = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Interest Rate")
    part_of_ctc    = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Part of CTC")
    taxable     = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Taxable")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    end_date   = models.DateField(blank=True, null=True, verbose_name="End Date")
    description = models.TextField(blank = True, null = True)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.advance_type

    class Meta:
        db_table = "manage_pay_roll_define_advances"


# Holidays and Leaves
class HolidaysandLeavesLeaveType(models.Model):
    short_name   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Short Name")
    leave_name    = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Leave Name")
    leave_type    = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Leave Type")
    applicable_to     = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Applicable to")
    impact_on_salary = models.IntegerField(choices= YESNO, default=1,  blank=True, null=True, verbose_name="Impact on Salary")
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leave_type

    class Meta:
        db_table = "holidays_and_leaves_leave_type"


class HolidaysandLeavesManageLeaveQouta(models.Model):
    short_name   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Short Name")
    leave_name    = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Leave Name")
    leave_type    = models.ForeignKey(HolidaysandLeavesLeaveType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Leave Type")
    applicable_to     = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Applicable to")
    start_month     = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Start Month")
    end_month     = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="End Month")
    maximum_leave_qouta = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum Leave Qouta")
    impact_on_salary = models.IntegerField(choices= YESNO, default=0,  blank=True, null=True, verbose_name="Impact on Salary")
    permission_required = models.IntegerField(choices= YESNO, default=0,  blank=True, null=True, verbose_name="Permission Required")
    authority     = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Authority")
    carried_forward  = models.IntegerField(choices= YESNO, default=0,  blank=True, null=True, verbose_name="Carried Forward")
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    description = models.TextField(blank = True, null = True)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "holidays_and_leaves_manage_leave_qouta"


# Manage Claims
class ManageClaimType(models.Model):
    claim_type   = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Claim Type")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.claim_type

    class Meta:
        db_table = "manage_claim_type"


class ManageClaimsClaimEntitlement(models.Model):
    grade = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Grade")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    claim_type   = models.ForeignKey(ManageClaimType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Claim Type")
    claim_limit = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Claim Limit")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    end_date   = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "holidays_and_leaves_claim_entitlement"

# Travel
class TravelandClaimTravelManagementModeofTravel(models.Model):
    mode_of_travel   = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Mode of Travel")
    description = models.TextField(blank = True, null = True)
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mode_of_travel

    class Meta:
        db_table = "travel_and_claim_travel_management_mode_of_travel"


class TravelandClaimTravelManagementTravelType(models.Model):
    travel_type   = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Travel Type")
    description = models.TextField(blank = True, null = True)
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.travel_type

    class Meta:
        db_table = "travel_and_claim_travel_management_travel_type"


class TravelandClaimTravelManagementTravelPolicy(models.Model):
    policy_name   = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Policy Name")
    mode_of_travel = models.ForeignKey(TravelandClaimTravelManagementModeofTravel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Mode of Travel")
    travel_type = models.ForeignKey(TravelandClaimTravelManagementTravelType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Travel Type")
    description = models.TextField(blank = True, null = True)
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.policy_name

    class Meta:
        db_table = "travel_and_claim_travel_management_travel_policy"


class TravelandClaimTravelManagementManageTravel(models.Model):
    policy_name = models.ForeignKey(TravelandClaimTravelManagementTravelPolicy, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Policy Name")
    travel_name   = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Travel Name")
    entitlement   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Entitlement")
    maximum_limit   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Maximum Limit")
    description = models.TextField(blank = True, null = True)
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.policy_name

    class Meta:
        db_table = "travel_and_claim_travel_management_manage_travel"

# Manage Claims
class ManageReimbursement(models.Model):
    reimbursement_type   = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Reimbursement Type")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reimbursement_type

    class Meta:
        db_table = "manage_reimbursement"


class ManageReimbursementReimbursementEntitilement(models.Model):
    grade = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Grade")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    claim_type   = models.ForeignKey(ManageClaimType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Claim Type")
    claim_limit = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Claim Limit")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    end_date   = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_reimbursement_reimbursement_entitilement"


# ========================
class RecruitementPoliciesEmployeeStrength(models.Model):
    location  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    maximum_employee = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum Employee")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitement_policies_employee_strength"


class RecruitementPoliciesQualification(models.Model):
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    academic_qualification  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Academic Qualification")
    professional_qualification  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Professional Qualification")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitement_policies_qualification"


class RecruitementPoliciesExperience(models.Model):
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    min_experience  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Min Experience")
    max_experience  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Max Experience")
    language_fluency  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Language Fluency")
    other_requirement  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Other Requirement")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitement_policies_experience"


class RecruitementPoliciesManageRecruitmentRules(models.Model):
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    recruitement_rules  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Recruitement Rules")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitement_policies_manage_recruitment_rules"


class PoliciesandFormsManagementHRPolicies(models.Model):
    form_type  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Form Type")
    form_name  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Form Name")
    applicable_to_location  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Applicable to Location")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.form_type)

    class Meta:
        db_table = "policies_and_forms_management_hr_policies_form"


class HRPoliciesPolicyType(models.Model):
    policy_type  = models.CharField(unique = True, max_length=200, blank=False, null=False, default='', verbose_name="Policy Type")
    policy_name  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Policy Name")
    applicable_to_location  = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Applicable to Location")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.policy_type)

    class Meta:
        db_table = "hr_policies_policy_type"


ATTENDENCE_TYPE = (
    (1, 'Bio Matrix'),
    (2, 'Manually'),
    (3, 'By Force'),
    (4, 'Uploaded by Website'),
)

ATTENDENCE_STATUS = (
    (1, 'Pending'),
    (2, 'Accept'),
    (3, 'Reject'),
)


class UserLoginApiLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True, verbose_name = "Employee Id")
    employee_id = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Employee Id")
    employee_names = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Employee Name")
    location  = models.ForeignKey(ManageBranch, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    user_pics = models.ImageField(upload_to = 'user_attendence_pics/', default = '', blank= False, null=True, verbose_name = "Login User Pics")
    logout_user_pics = models.ImageField(upload_to = 'user_attendence_pics/', default = '', blank= False, null=True, verbose_name = "Logout User Pics")
    attendance_type = models.IntegerField(choices= ATTENDENCE_TYPE, default=0,  blank=True, null=True, verbose_name = "Mode of Attendance")
    logout_attendance_type = models.IntegerField(choices= ATTENDENCE_TYPE, default=0,  blank=True, null=True, verbose_name = "Logout Attendance Type")
    address = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Login Location")
    logout_address = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Logout Location")
    latitude = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True)
    logout_latitude = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True)
    logout_longitude = models.DecimalField(max_digits=20, decimal_places=16, null=True, blank=True)
    login_true = models.BooleanField(default=0)
    logout_true = models.BooleanField(default=0)
    logout_true1 = models.BooleanField(default=0)
    notification_send = models.BooleanField(default=0)
    added = models.DateTimeField(auto_now_add=True, verbose_name = "Login  Time")
    login_time = models.DateTimeField(blank = True, null = True, verbose_name = "Login  Time(Format:10:53)")
    logout_time = models.DateTimeField(blank = True, null = True, verbose_name = "Logout Time(10:53)")
    date_field = models.DateField(blank = True, null = True, verbose_name = "Date")
    approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
    approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
    attendance_status = models.IntegerField(choices= ATTENDENCE_STATUS, default=1,  blank=True, null=True, verbose_name = "Attendance Status")
    attendance_correction = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name = "Correction")
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "user_login_api_logs"


class RecruitmentManagementRecruitmentPlanningEmployeeStrength(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    maximum_employee = models.IntegerField(default=0,  blank=True, null=True, verbose_name = "Maximum Employee")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_recruitment_planning_employee_strength"


class RecruitmentManagementRecruitmentPlanningQualification(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    academic_qualification = models.CharField(default='',  blank=True, null=True, max_length = 250,verbose_name = "Academic Qualification")
    personal_qualification = models.CharField(default='',  blank=True, null=True, max_length = 250,verbose_name = "Professional Qualification")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_recruitment_planning_qualification"


class RecruitmentManagementRecruitmentPlanningExperience(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    min_experience = models.CharField(default='',  blank=True, null=True, max_length = 250,verbose_name = "Min Experience")
    max_experience = models.CharField(default='',  blank=True, null=True, max_length = 250,verbose_name = "Max Experience")
    language_fluency = models.CharField(default='',  blank=True, null=True, max_length = 250,verbose_name = "Language Fluency")
    other_requirement = models.CharField(default='',  blank=True, null=True, max_length = 250,verbose_name = "Other Requirement")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_recruitment_planning_expirence"


class RecruitmentManagementRecruitmentPlanningManageRecruitmentRules(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    recruitement_rules = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Recruitement Rules")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_recruitment_planning_recruitment_rules"


class RecruitmentManagementCandidateSourcingManageJobPublishment(models.Model):
    publishment_type = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Publishment type")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.publishment_type

    class Meta:
        db_table = "recruitment_management_candidate_sourcing_manage_job_publishment"


class RecruitmentManagementCandidateSourcingManageReceiptofResume(models.Model):
    mode_of_resume_receipt = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Mode of Resume Receipt")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mode_of_resume_receipt

    class Meta:
        db_table = "recruitment_management_candidate_sourcing_manage_receipt_of_resume"


# 55  		 	

class RecruitmentManagementInterveiwProcessScreeningLevel(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    desigantion = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Desigantion  ")
    screening_Process = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Screening Process  ")
    sequencing_of_process = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Sequencing of Process")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.screening_Process
    
    class Meta:
        db_table = "recruitment_management_interveiw_process_screening_level"

#66   
class RecruitmentManagementInterveiwProcessManageInterviewProcess(models.Model):
    mode_of_interview = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Mode of interview")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_interveiw_process_manage_interview_process"


class RecruitmentManagementInterveiwProcessScorecard(models.Model):
    resume_screen_level = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name="Resume  Screen Level")
    maximum_score = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Maximum Score")
    passing_score = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Passing Score")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_interveiw_process_scorecard"


class RecruitmentManagementInterveiwManageCandidateShortlistingAuthority(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    resume_screen_level = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name="Resume  Screen Level")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_interview_manage_candidate_shortlisting_authority"


class RecruitmentManagementInterveiwManageSelectionProcess(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    resume_screen_level = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name="Resume  Screen Level")
    maximum_score = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Maximum Score")
    passing_score = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Passing Score")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recruitment_management_interview_manage_selection_process"


class ManagementEmployeeTypeofJob(models.Model):
    name = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Name")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "management_employee_type_of_job"


class ManagementEmployeePayrollofJob(models.Model):
    name = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Name")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "management_employee_pay_roll_of_job"


# Knowledge and Training
class KnowledgeandTrainingUpdateDocuments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    document_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Document Type")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    subject  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Subject")
    upload   = models.FileField(upload_to='knowleage_traninig/%Y/%m/%d/', verbose_name="Upload(PDF File Only)")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.document_type

    class Meta:
        db_table = "knowledgeand_training_update_documents"


class KnowledgeandTrainingUpdatePromotions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    promotion_product  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Promotion Product")
    promotion_details  = models.TextField(default='', blank=True, null=True, max_length=200, verbose_name="Promotion Details")
    promotion_period  = models.TextField(default='', blank=True, null=True, max_length=200, verbose_name="Promotion Period")
    location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "knowledgeand_training_update_pramotions"


class KnowledgeandTrainingKnowledgeSharing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
    documents_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Documents Type")
    subject  = models.TextField(default='', blank=True, null=True, max_length=200, verbose_name="Subject")
    status  = models.IntegerField(choices= ATTENDENCE_STATUS , default=1, blank=True, null=True,  verbose_name="Status")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "knowledgeand_training_knowledge_sharing"


# On boarding & Exit Management
class OnboardingExitRemunerationManagement(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    salary_code  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Salary Code")
    salary_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Salary Type")
    salary_frequency  = models.IntegerField(choices = FREQUENCY, default=1, blank=True, null=True, verbose_name = "Salary Frequency")
    amount  = models.IntegerField(default=0, blank=True, null=True, verbose_name = "Amount")
    deduction_category  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Deduction Category")
    deduction_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Deduction type")
    deduction_name  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Deduction Name")
    deduction_frequency  = models.IntegerField(choices = FREQUENCY, default=1, blank=True, null=True, verbose_name="Deduction Frequency")
    deduction_amount  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Deduction Amount")   
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "onboarding_exit_remuneration_management"


# Registration Management

class RegistrationManagementEmploymentType(models.Model):
    employment_type  = models.CharField(unique = True, default='', blank=True, null=True, max_length=200, verbose_name="Employment Type")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.employment_type

    class Meta:
        db_table = "registration_management_employment_type"



class RegistrationManagementPayrollType(models.Model):
    payroll_type  = models.CharField(unique = True, default='', blank=True, null=True, max_length=200, verbose_name="Payroll Type")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.payroll_type

    class Meta:
        db_table = "registration_management_payroll_type"


class RegistrationManagementPayrollAgency(models.Model):
    employment_type  =models.ForeignKey(RegistrationManagementEmploymentType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Employment Type")
    payroll_type  =models.ForeignKey(RegistrationManagementPayrollType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Payroll Type")
    payroll_agency  = models.CharField(unique = True, default='', blank=True, null=True, max_length=200, verbose_name="Payroll Agency")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.payroll_agency

    class Meta:
        db_table = "registration_management_payroll_agency"


class RegistrationManagementKeyResponsibilityAreas(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    kra_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="KRA Type")
    kra_details  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="KRA Details")
    kra_frequency  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="KRA Frequency")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "registration_management_key_responsibility_areas"


# Exit Management 
class ExitManagementExitType(models.Model):
    exit_type   = models.CharField(unique = True, default='', blank=True, null=True, max_length=200, verbose_name="Exit Type")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.exit_type

    class Meta:
        db_table = "exit_management_exit_type"


class ExitManagementNoticePeriod(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    notice_period_in_days = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Notice Period in Days")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.employment_type

    class Meta:
        db_table = "exit_management_notice_period"


class ExitManagementFinalSettlement(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    final_settlement_days = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Final Settlement Days")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.department

    class Meta:
        db_table = "exit_management_final_settlement_days"


class ExitManagementExitInterview(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    interview_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Interview type")
    requirement_type  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Requirement Type")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.interview_type

    class Meta:
        db_table = "exit_management_exit_interview"



class AssetManagementAssetsType(models.Model):
    assets_type   = models.CharField(unique = True, default='', blank=True, null=True, max_length=50, verbose_name="Assets Type")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.assets_type

    class Meta:
        db_table = "asset_management_assets_type"


class AssetManagementManageAssets(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    assets_type = models.ForeignKey(AssetManagementAssetsType, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assets Type")
    assets_details  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Assets Details")
    assets_number   = models.CharField(default='', blank=True, null=True, max_length=50, verbose_name="Assets Number")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "asset_management_manage_assets"



class AssetManagementAllocationPolicy(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    assets_type = models.ForeignKey(AssetManagementAssetsType, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Assets Type")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "asset_management_allocation_policy"


# Performance & Appraisal Management 
class PerformanceAppraisalPerformanceManagementTargets(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    responsibilities = models.ForeignKey(ManageResponsibility, on_delete=models.SET_NULL,  null=True, verbose_name="Responsibility")
    role = models.ForeignKey(RoleMangement, on_delete=models.SET_NULL,  null=True, verbose_name="Role")
    kra_type   = models.CharField(unique = True, max_length=200, blank = True, null = True, verbose_name = "KRA Target Type")
    kra_frequency  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "KRA Frequency")
    target = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Target")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.kra_type

    class Meta:
        db_table = "performance_appraisal_performance_management_targets"


class PerformanceAppraisalPerformanceManagementIncentive(models.Model):
    incentive_type   = models.CharField( unique = True, max_length=200, blank = True, null = True, verbose_name = "Incentive Type")
    incentive_name  = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Incentive Name")
    incentive_frequency = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Incentive Frequency")
    basis_of_incentive = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Basis of Incentives")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.incentive_type

    class Meta:
        db_table = "performance_appraisal_performance_management_incentive"


class PerformanceAppraisalManagePerformanceIncentive(models.Model):
    incentive_type = models.ForeignKey(PerformanceAppraisalPerformanceManagementIncentive, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Incentive Type")
    incentive_frequency = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Incentive Frequency")
    target_fulfilment   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Target Fulfilment")
    incentive_amount   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Incentive Amount")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_management_performance_incentive"



class PerformanceAppraisalManagementAppraisalFrequency(models.Model):
    appraisal_frequency   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Appraisal Frequency")
    cut_off_date = models.CharField(max_length=200, blank = True, null = True, verbose_name="Cut off Date")
    description = models.CharField(max_length=200, blank = True, null = True, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_management_appraisal_frequency"


class PerformanceAppraisalManagementCrossDepartment(models.Model):
    main_department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Main Department")
    cross_department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Cross Departments", related_name = "cross_departments")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_management_cross_department"



class PerformanceAppraisalRatingWeightage(models.Model):
    appraising_person = models.CharField(max_length=200, blank = True, null = True, verbose_name="Appraising Person") 
    maximum_weightage = models.CharField(max_length=200, blank = True, null = True, verbose_name="Maximum Weightage") 
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_rating_weightage"



class PerformanceAppraisalRatingManageRating(models.Model):
    weightage_range = models.CharField(max_length=200, blank = True, null = True, verbose_name="Weightage Range") 
    rating = models.CharField(max_length=200, blank = True, null = True, verbose_name="Rating") 
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.rating
    class Meta:
        db_table = "performance_appraisal_rating_manage_rating"



class PerformanceAppraisalAppraisalCommittee(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    no_of_members    = models.CharField(unique = True, max_length=200, blank = True, null = True, verbose_name = "No of Members")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)


    class Meta:
        db_table = "performance_appraisal_appraisal_committee"


# -------------------------
class PerformanceAppraisalAppraisalBenefitsDefineChangeinGrade(models.Model):
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    no_of_grades = models.CharField(max_length=200, blank = True, null = True, verbose_name="No of  Grades")
    description  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_appraisal_benefits_change_in_grade"


class PerformanceAppraisalBenefitsManageGradeChange(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    rating = models.CharField(max_length=200, blank = True, null = True, verbose_name="Rating")
    no_of_grades = models.CharField(max_length=200, blank = True, null = True, verbose_name="No of  Grades")
    new_grades = models.CharField(max_length=200, blank = True, null = True, verbose_name="New Grades")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_benefits_manage_grade_change"



class PerformanceAppraisalBenefitsDefineIncrement(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    rating = models.CharField(max_length=200, blank = True, null = True, verbose_name="Rating")
    increment  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Increment")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)



    class Meta:
        db_table = "performance_appraisal_benefits_define_increment"


class PerformanceAppraisalBenefitsAppraisalIncentive(models.Model):
    location = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    rating = models.CharField(max_length=200, blank = True, null = True, verbose_name="Rating")
    incentive_type = models.ForeignKey(PerformanceAppraisalPerformanceManagementIncentive, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Incentive Type")
    amount  = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="Amount")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "performance_appraisal_benefits_appraisal_incentive"
#######
class RecruitmentManagePsychometricTest(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    desigantion = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Desigantion  ")
    test_required  = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Test Required ")
    test_type = models.CharField(unique = True,default='',  blank=True, null=True, max_length = 250, verbose_name = "Test Type")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")

    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.test_required)
    class Meta:
        db_table = "recruitment_manage_psychometric_test"


##managetestresult  Department	Desigantion	Test Type	minimum_points	maximum_points	passing_points	threshhold_limit	Desctiption
class RecruitmentManageTestResult(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    desigantion = models.ForeignKey(RecruitmentManagementInterveiwProcessScreeningLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Desigantion  ")
    # test_required  = models.CharField(unique = True, default='',  blank=True, null=True, max_length = 250, verbose_name = "Test Required ")
    test_type = models.ForeignKey(RecruitmentManagePsychometricTest, on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Test Type")
    minimum_points = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Minimum Points")
    maximum_points = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Maximum Points")
    passing_points = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Passing Points")
    threshhold_limit = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Threshhold Limit")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")

    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.threshhold_limit)
    class Meta:
        db_table = "recruitment_manage_test_result"


###############


########99 Department	Desigantion	Authority Type	Designation	Department	Description

class Recruitmentapprovingauthority(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    authority_type = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Authority Type")
    # department = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Department")
    # designation = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Designation")

    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")
    start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.authority_type
    class Meta:
        db_table = "recruitment_approving_authority"


##grade1
class ManageSalaryRange(models.Model):
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    designation   = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    start_salary  = models.IntegerField(default=0,  blank=True, null=True, verbose_name=" Salary Range")
    maximum_salary = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum Salary")
    description = models.TextField(blank = True, null = True)
    start_date  = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active  = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.grade


    class Meta:
        db_table = "manage_employee_salary_range"


class ManagePayRollDeductions(models.Model):
    deduction_type = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Deduction Type")
    nature_of_deduction   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Nature of Deduction")
    tax_exempted   = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name="Tax Exempted")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    minimum  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Minimum")
    maximum  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum")
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_pay_roll_deductions"
###########Updateadvancetype
class Updateadvancetype(models.Model):
    advance_type  = models.ForeignKey(ManagePayRollDefineAdvances, on_delete=models.SET_NULL, blank=True, null=True, default='', verbose_name="Advance Type")
    description = models.TextField(blank = True, null = True)
    # start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.advance_type

    class Meta:
        db_table = "update_advance_type"

###########advance entitlement
class AdvanceEntitlement(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    advance_type  = models.ForeignKey(ManagePayRollDefineAdvances, on_delete=models.SET_NULL, blank=True, null=True, default='', verbose_name="Advance Type")
    maximum_amount  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum Amount")
    interest_required  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Interest Required")
    rate_of_nterest  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Rate of Interest")

    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    no_of_installments  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="No of Installments")
    
    description = models.TextField(blank = True, null = True)
    # start_date   = models.DateField(blank=True, null=True, verbose_name="Start Date")
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

   

    class Meta:
        db_table = "advance_entitlement"

#########  UpdateOther Deductions

class UpdateOtherDeductions(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    maximum_limit  = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Maximum Limit")
    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    description = models.TextField(blank = True, null = True)
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.maximum_limit)
    class Meta:
        db_table = "update_other_deductions"


# Performance & Appraisal Management   

class PerformanceAppraisalUpdateIncentiveType(models.Model):
    inventive_type = models.CharField(unique = True, max_length=200, blank = True, null = True,  verbose_name="Inventive Type")
    frequency_of_incentive   = models.CharField(unique = True, max_length=200, blank = True, null = True, verbose_name = "Frequency of Incentive")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
   
    description = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.inventive_type

    class Meta:
        db_table = "performance_appraisal_updateIncentive_type"

##PerformanceAppraisalUpdateBonus  Bonus Type	Frequency of Bonus	Description

class PerformanceAppraisalUpdateBonus(models.Model):
    bonus_type = models.CharField(unique = True, max_length=200, blank = True, null = True,  verbose_name="Bonus Type")
    frequency_of_bonus   = models.CharField(unique = True, max_length=200, blank = True, null = True, verbose_name = "Frequency of Bonus")
   
    description = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.bonus_type

    class Meta:
        db_table = "performance_appraisal_updatebonus"
##PerformanceAppraisalManageBonus

class PerformanceAppraisalManageBonus(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    bonus_type = models.ForeignKey(PerformanceAppraisalUpdateBonus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Bonus Type")
    frequency_of_bonus   = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Frequency of Bonus")
    maximum_limit   = models.ForeignKey(UpdateOtherDeductions, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Maximum Limit")
    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    description = models.CharField(max_length=200, blank = True, null = True, verbose_name = "Description")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.department

    class Meta:
        db_table = "performance_appraisal_managebonus"

## UpdateExitApprovalAuthority
class UpdateExitApprovalAuthority(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    authority_type = models.ForeignKey(Recruitmentapprovingauthority ,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Authority Type")
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Designation")
    exit_type   = models.ForeignKey(ExitManagementExitType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Exit Type")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
   
    def __str__(self):
        return self.authority_type
    class Meta:
        db_table = "update_exit_approval_authority"
       
## UpdateAppraisalProcessType
class UpdateAppraisalProcessType(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    appraisal_process_type = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = " Appraisal Process Type")  
    
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "update_appraisal_process_type"

### UpdatePyschometricTest
class UpdatePyschometricTest(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    grade = models.ForeignKey(ManageGrade, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Grade")
    test_required = models.ForeignKey(RecruitmentManagePsychometricTest, on_delete=models.SET_NULL, blank=True, null=True, verbose_name = " Appraisal Process Type")  
    test_type = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Test Type")
    minimum_points = models.IntegerField(default=0,  blank=True, null=True, verbose_name = "Minimum Points")
    maximum_points = models.IntegerField(default=0,  blank=True, null=True, verbose_name = "Maximum Points")
    threshhold_limit = models.ForeignKey(RecruitmentManageTestResult, on_delete=models.CASCADE, blank=True, null=True, verbose_name = "Threshhold Limit")
    passing_points = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Passing Points")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "update_pyschometric_test"
#Update Appraisal Benefit Type

class UpdateAppraisalBenefitType(models.Model):
    appraisal_benefit_type = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Appraisal Benefit Type")
    # description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "update_appraisal_benefit_type"
  
##ManageGradeChange
class ManageGradeChange(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    rating = models.ForeignKey(PerformanceAppraisalRatingManageRating,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Rating")
    new_grade = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "New Grade")
    existing_grade = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Existing Grade")
    applicable_from = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Applicable From")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)
    class Meta:
        db_table = "manage_grade_change"
    
##ManageIncrements   
class ManageIncrements(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    rating = models.ForeignKey(PerformanceAppraisalRatingManageRating,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Rating")
    increment_amount = models.IntegerField(default='',  blank=True, null=True,  verbose_name = " Increment Amount")
    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    applicable_from = models.ForeignKey(ManageGradeChange,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Applicable From")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.increment_amount)
    class Meta:
        db_table = "manage_increments"
    
###########ManageAppraisalIncentive

class ManageAppraisalIncentive(models.Model):
    department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
    designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
    rating = models.ForeignKey(PerformanceAppraisalRatingManageRating,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Rating")
    increment_amount = models.ForeignKey(ManageIncrements,on_delete=models.SET_NULL, blank=True, null=True,  verbose_name = " Increment Amount")
    unit_value   = models.ForeignKey(UnitValue, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Unit Value")
    applicable_from = models.ForeignKey(ManageGradeChange,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Applicable From")
    description = models.CharField(default='',  blank=True, null=True, max_length = 250, verbose_name = "Description")  
    is_active = models.BooleanField(default=1, verbose_name="Is Active")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "manage_appraisal_incentive"
   
