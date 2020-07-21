from __future__ import absolute_import, unicode_literals
from celery import task
from hrms_management.models import *
from employee_website.models import *
from aditshsoft.common import SendMail


@task()
def auto_escalation_resume_receipt():
    get_all_leads_for_verification = EmployeeServicesRecruitementInviteResumemodel.objects.filter(status = 1)
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 1)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



@task()
def auto_escalation_short_listed_resume():
    get_all_leads_for_verification = EmployeeServicesRecruitementInviteResumemodel.objects.filter(status = 2).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 2)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



@task()
def auto_escalation_short_listed_candidates():
    get_all_leads_for_verification = EmployeeServicesRecruitementInviteResumemodel.objects.filter(status = 3, interview_status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 5)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



@task()
def auto_escalation_short_listed_candidates():
    get_all_leads_for_verification = EmployeeServicesRecruitementInviteResumemodel.objects.filter(status = 3, interview_status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 5)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


@task()
def auto_escalation_pending_leave():
    get_all_leads_for_verification = EmployeeLeavesLeaveRequest.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 6)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


@task()
def auto_escalation_attendance_correction():
    get_all_leads_for_verification = CrmUserLoginApiLogs.objects.all().order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 7)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



@task()
def auto_escalation_over_time_status():
    get_all_leads_for_verification = OvertimeManagementUpdateOvertime.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 8)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


@task()
def auto_escalation_travel_request_status():
    get_all_leads_for_verification = TravelClaimManagementTravelConveyanceTravelRequest.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 9)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



@task()
def auto_escalation_claim_status():
    get_all_leads_for_verification = EmployeeClaimandReimbursementSubmitClaims.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 10)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


def auto_escalation_claim_processing_status():
    get_all_leads_for_verification = EmployeeClaimandReimbursementSubmitClaims.objects.filter(status = 2).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 10)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


@task()
def auto_escalation_reimbursement_claim_status():
    get_all_leads_for_verification = EmployeeClaimandReimbursementSubmitReimbursement.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 11)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



def auto_escalation_reimbursement_claim_processing_status():
    get_all_leads_for_verification = EmployeeClaimandReimbursementSubmitReimbursement.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 12)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


@task()
def auto_escalation_employee_advance_status():
    get_all_leads_for_verification = EmployeeAdvancesSubmitAdvanceRequest.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 13)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


def auto_escalation_employee_advance_processing_status():
    get_all_leads_for_verification = EmployeeAdvancesSubmitAdvanceRequest.objects.filter(status = 2).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 14)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')



@task()
def auto_escalation_incentive_bonus_status():
    get_all_leads_for_verification = EmployeeAdvancesSubmitIncentiveBonus.objects.filter(status = 1).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 15)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')


def auto_escalation_incentive_bonus_processing_status():
    get_all_leads_for_verification = EmployeeAdvancesSubmitIncentiveBonus.objects.filter(status = 2).order_by('-id')
    for each_user in get_all_leads_for_verification:
        session_escalation_start_time = NotificationEscalationMatrixDefineTurnAroundTime.objects.get(crmnotificationescalationmatrixdefineturnaroundtimeprocessname__process_name_level_id = 16)
        verfication_updated_date = each_user.updated
        current_date_time = datetime.now()
        get_second = current_date_time - verfication_updated_date.replace(tzinfo=None)
        convert_into_minutes = get_second.seconds / 60
        if convert_into_minutes > float(session_escalation_start_time.tat_in_hours_days):
            get_esclaescalation_user = session_escalation_start_time.crmnotificationescalationmatrixdefineturnaroundtimeescalationuser_set.get(turn_around_id=session_escalation_start_time.id)
            SendMail.mail('Escalation Alert' , get_esclaescalation_user.escalation_user.email, 'Work is not done at given time !!')