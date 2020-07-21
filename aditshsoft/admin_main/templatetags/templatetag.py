import os
import  uuid
from django import template
from django.db.models import Q
from aditshsoft.common import Getmonthlist
from admin_main.models import *
from hrms_management.models import *
from employee_website.models import *
import datetime
from django.db.models import Sum
from dateutil import relativedelta
import calendar
from math import ceil

register = template.Library()
today = datetime.date.today()
t = []
@register.simple_tag
def get_sub_process_of_approval(process_name):
    get_process_name = DefineProcessAllocation.objects.filter(process_name = process_name)
    return get_process_name

@register.simple_tag
def get_sub_process(process_name):
    get_process_name = DefineProcessAllocation.objects.filter(process_name = process_name)
    return get_process_name
	
@register.simple_tag
def get_month_name(month):
	if month:
		month_list = Getmonthlist.month_list()
		get_month_name = month_list[month - 1][1]
		return get_month_name


@register.simple_tag
def user_value_data_get_user_name(id):
	try:
		user = User.objects.get(id = id)
		return user.name
	except Exception as e:
		return ''


@register.simple_tag
def user_value_data_get_user_designation(id):
	try:
		use = User.objects.get(id = id)
		return use.designation.designation
	except User.CrmOutGoingCallLeadStatus:
		return ''


@register.simple_tag
def user_value_data_get_user_department(id):
	use = User.objects.get(id = id)
	return use.department.department


@register.simple_tag
def user_value_data_get_user_responsibility(id):
	use = User.objects.get(id = id)
	return use.responsibilities.department


@register.simple_tag
def user_value_data_get_user_client_type(id):
	use = AllocationMatrixdLeadAllocation.objects.get(user_id = id)
	return use.client_type.define_client_type


@register.simple_tag
def user_value_data_get_user_client_category(id):
	use = AllocationMatrixdLeadAllocation.objects.get(user_id = id)
	return use.client_category.define_client_category


@register.simple_tag
def user_value_data_get_user_client_product(id):
	use = AllocationMatrixdLeadAllocation.objects.get(user_id = id)
	return use.product.product_name


@register.simple_tag
def user_value_data_get_user_branches(id):
    append_branches = ''
    branches = UserMultipleBranch.objects.filter(user_id =id)
    if branches:
        for bran in branches:
            append_branches += bran.branch_allocated.name_of_branch +','
    return append_branches.strip(',')


@register.simple_tag
def get_time_from_datetime_field(date_time):
	time_format = "%a %b %d %H:%M:%S GMT+05:30 %Y"
	datime = datetime.strptime(date_time, time_format)
	return str(datime.time())


@register.simple_tag
def get_resend_lead_comment(id):
	try:
		data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls_id = id, lead_status = 6)
		return data
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		return  False


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()


@register.simple_tag
def check_permission(request_user, permission):
	if str(request_user.id) in  permission.user_ids.split(',') and str(request_user.department_id) in  permission.department_ids .split(','):
		return True
	else:
		return False


@register.simple_tag
def get_status_bulk_data_of_allocated_data(id):
	try:
		get_data = CrmSaveLeadGenerationForm.objects.get(bulk_data_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "Converted in Leads"
	except CrmSaveLeadGenerationForm.DoesNotExist:
		return "Not Converted in Lead"


@register.simple_tag
def get_status_third_party_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__third_party_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(third_party_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_status_referral_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__refe_ral_data_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(refe_ral_data_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_status_online_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__online_lead_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(online_lead_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_status_social_online_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__social_media_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(social_media_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_status_out_going_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__bulk_data_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(bulk_data_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_status_incoming_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__incoming_calls_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(incoming_calls_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_status_field_visits_leads(id):
	try:
		get_data = CrmOutGoingCallLeadStatus.objects.get(out_going_calls__field_visits_id = id)
		return dict(LEAD_STATUS)[get_data.lead_status]
	except CrmOutGoingCallLeadStatus.DoesNotExist:
		try:
			get_data = CrmSaveLeadGenerationForm.objects.get(field_visits_id = id)
			return dict(LEAD_STATUS)[get_data.lead_status] if get_data.lead_status !=0 else "New Leads"
		except CrmSaveLeadGenerationForm.DoesNotExist:
			return "Not Leads"


@register.simple_tag
def get_candidate_joined(department, location):
	try:
		get_joined_jon = EmployeeServicesRecruitementInviteResumemodel.objects.filter(department_id = department,location= location).count()
		return get_joined_jon
	except Exception as e:
		return 0


@register.simple_tag
def get_candidate_balance_vacancies_date_time_year(vacancy_approved, filled_vacancy):
	try:
		return int(vacancy_approved) - filled_vacancy
	except Exception as e:
		return 0


from datetime import datetime, timedelta
@register.simple_tag
def duration_date_of_joining(designation_date_time):
	date1 = today
	time_format = "%Y-%m-%d"
	datime = datetime.strptime(str(designation_date_time), time_format)
	date2 = datime
	diff = relativedelta.relativedelta(date1, date2)
	years = diff.years
	months = diff.months
	days = diff.days
	return ('{} years {} months {} days'.format(years, months, days))


@register.simple_tag
def get_number_of_days_month():
	now = datetime.now()
	return calendar.monthrange(now.year, now.month)[1]


@register.simple_tag
def get_weekly_off_days():
	try:
		get_weekly_days = ManageWorkingDays.objects.filter(is_active = True)
		get_weekly = len(get_weekly_days[0].weekly_off_working_days.split(','))
		return get_weekly
	except:
		return 0


@register.simple_tag
def get_monthly_off_days():
	now = datetime.now()
	day_of_month = calendar.monthrange(now.year, now.month)[1]
	get_weekly_days = ManageWorkingDays.objects.filter(is_active = True)
	get_weekly = len(get_weekly_days[0].weekly_off_working_days.split(','))
	get_total_week_month = ((day_of_month - 1) // 7) * get_weekly
	return get_total_week_month


@register.simple_tag
def get_monthly_holidays_day():
	now = datetime.now()
	get_monthly_holidays_day = ManageHolidays.objects.filter(year =now.year, month = now.month).count()
	return get_monthly_holidays_day


@register.simple_tag
def get_working_days(total_days, weekly_off, monthly_off, holidays):
	return total_days - (monthly_off + holidays)


@register.simple_tag
def days_worked(user_id, total_days):
	now = datetime.now()
	get_user_total_attendance = UserLoginApiLogs.objects.filter( added__month= now.month, added__year = now.year).count()
	result = {
		'get_user_total_attendance': get_user_total_attendance,
		'get_user_total_absent': total_days - get_user_total_attendance
	}
	return result


@register.simple_tag
def get_current_month_approved_leaves(user_id):
	now = datetime.now()
	get_current_month_leave_approved = EmployeeLeavesLeaveRequest.objects.filter(employee_id_id = user_id, status = 2, added__month = now.month)
	result = {
		'total_leaves': get_current_month_leave_approved.count(),
		'get_current_month_leave_approved_type': get_current_month_leave_approved
	}
	return result


@register.simple_tag
def get_current_month_approved_status(user_id):
	try:
		now = datetime.now()
		get_current_month_leave_status = CrmUserLoginApiLogs.objects.filter(user_id = user_id,  added__month = now.month)
		return dict(ATTENDENCE_STATUS)[get_current_month_leave_status[0].attendance_status]
	except:
		return ''

@register.simple_tag
def last_date_of_working(current_date, add_days):
	try:
		d = timedelta(days=int(add_days))
		return current_date + d
	except:
		return ''


@register.simple_tag
def leave_balance(user_id, leave_type, total_leaves):
	try:
		d = EmployeeLeavesLeaveRequest.objects.filter(employee_id_id = user_id, type_of_leave_id = leave_type, status = 2)
		return int(total_leaves) - int(d[0].total_leave)
	except:
		return 0


@register.simple_tag
def get_previous_salary_of_employee(id):
	get_employee_salary = EmployeeRegistrationUpdateSalaryStructutre.objects.filter(user_employee_id = id).order_by('-id')
	if get_employee_salary:
		if get_employee_salary[0].salary_structut_salary_frequency_1 == 1:
			return int(get_employee_salary[0].salary_structut_amount_offered_1) * 12
		else:
			return int(get_employee_salary[0].salary_structut_amount_offered_1) / 12
	return  0


@register.simple_tag
def count_working_time_hours(id):
	now = datetime.now()
	get_employee_salary = OvertimeManagementUpdateOvertime.objects.filter( added__month = now.month).aggregate(Sum('total_hours'))
	return  get_employee_salary['total_hours__sum']


@register.simple_tag
def get_permission_data_from(main_fun, sub_menu_sequence = None):
	if sub_menu_sequence:
		try:
			get_data = UserAccessPermissonModelsPermission.objects.get(main_function= main_fun, sub_menu_sequence = sub_menu_sequence)
			return  get_data
		except:
			return False
	else:
		get_data = UserAccessPermissonModelsPermission.objects.filter(main_function= main_fun).order_by('sub_menu_sequence')
		return get_data



@register.simple_tag
def approval_status_of_requirement(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = EmployeeServicesRecruitementCreateRequirementmodel.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_of_attendance(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = CrmUserLoginApiLogs.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_of_over_time(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = OvertimeManagementUpdateOvertime.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_travel_request(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = TravelClaimManagementTravelConveyanceTravelRequest.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_claim(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = EmployeeClaimandReimbursementSubmitClaims.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_reimbursement(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = EmployeeClaimandReimbursementSubmitReimbursement.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_employee_advance(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = EmployeeAdvancesSubmitAdvanceRequest.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_incentive_bonus(user_id, crt_req_id):
	all_status = []
	try:
		check_blank = EmployeeAdvancesSubmitIncentiveBonus.objects.get(id = crt_req_id)
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except:
		return False


@register.simple_tag
def approval_status_update_policies_circualr(user_id, crt_req_id, list_id):
	all_status = []
	try:
		if list_id == 9:
			check_blank = EmployeeHRPoliciesUpdatePoliciesmodel.objects.get(id = crt_req_id)
		elif list_id == 10:
			check_blank = EmployeeHrPoliciesUpdateCircularsmodel.objects.get(id = crt_req_id)
		elif list_id == 11:
			check_blank = EmployeeHRPoliciesUpdateFormmodel.objects.get(id = crt_req_id)
		elif list_id == 12:
			check_blank = CrmManageProductTrainingModel.objects.get(id = crt_req_id)
		elif list_id == 13:
			check_blank = CrmManageProductPromotionsModel.objects.get(id = crt_req_id)
		elif list_id == 14:
			check_blank = PayrollStatutoryDeductions.objects.get(id = crt_req_id)
		elif list_id == 15:
			check_blank = PayrollSalaryVoucher.objects.get(id = crt_req_id)
		elif list_id == 16:
			check_blank = PayrollSalaryDisbursement.objects.get(id = crt_req_id)
		elif list_id == 17:
			check_blank = EmployeePayrollProcessingUpdateRecoveries.objects.get(id = crt_req_id)
		elif list_id == 18:
			check_blank = EmployeePayrollProcessingUpdateTaxDeclaration.objects.get(id = crt_req_id)
			
		if not check_blank.approval_level_id:
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.all().order_by('approval_level_id')
			else:
				return False
		else:
			data_id = check_blank.approval_level_all_status.split(',')
			get_approval_level = CrmApprovalMatrixMapApprovalLevelWithUsers.objects.filter(user_id = user_id)
			if get_approval_level:
				return get_approval_level[0].crmapprovalmatrixmapapprovallevelwithusersprocesslevel_set.filter(~Q(approval_level_id__in = data_id)).order_by('approval_level_id')
			else:
				return False
	except Exception as e:
		print ("********************", e)
		return False

@register.simple_tag
def get_approval_staus(approval_level):
	level  = approval_level.sequence
	return level




@register.simple_tag
def get_access_of_sub_menu(user_id = None, process_name = None):
    get_process_name = [data.process_name.process_name.strip()+'-'+data.process_name.sub_process_name.strip() for data in LeadAllocationProcessName.objects.filter(lead_allocation__user_id = user_id, process_name__process_name__in = process_name)]
    return get_process_name

@register.simple_tag
def get_access_of_child_menu(user_id = None, process_name = None):
    get_child_process_name = [data.process_name.sub_process_name.strip()+'-'+ str(data.process_name.child_process_name).strip() for data in LeadAllocationProcessName.objects.filter(lead_allocation__user_id = user_id, process_name__process_name__in = process_name)]
    return get_child_process_name



##
@register.simple_tag
def get_sub_process(process_name):
    get_process_incentive = EmployeeAdvancesSubmitIncentiveBonus.objects.all()
    return get_process_incentive
	