import os
import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.core.mail import EmailMessage
import urllib.parse
from hrms_management.models import *
from django.db.models.functions import Lower
import datetime


def NotificationSendReportingOfficer(sender_id, receiver_id, get_detail):
    # Save Notification To Reporting Officer
    save_notification = ActivityNotification()
    save_notification.sender_id =  sender_id
    save_notification.receiver_id =  receiver_id
    save_notification.body_messages =  get_detail
    save_notification.save()
    return True

class SiteUrl(object):

    ''' Ger secure and unsecure host name'''

    @staticmethod
    def site_url(request):
        if request.is_secure():
            site_url = 'https://'+request.get_host()
        else:
            site_url = 'http://'+request.get_host()
        return site_url


class CommonPagination(object):

    '''Common pagination for all model'''

    @staticmethod
    def paginattion(request, modeldata, pagesize):

        paginator = Paginator(modeldata, pagesize)
        page = request.GET.get('page')
        try:
            querylist = paginator.page(page)
        except PageNotAnInteger:
            querylist = paginator.page(1)
        except EmptyPage:
            querylist = []
        return querylist 


class Getmonthlist(object):

    ''' Common pagination for all model '''

    @staticmethod
    def month_list():
        months_choices = []
        for i in range(1,13):
            months_choices.append((i, datetime.date(2008, i, 1).strftime('%B')))
        return months_choices


class Getyearlist(object):

    '''Common pagination for all model'''

    @staticmethod
    def year_list():
        year_choices = []
        year_list = range(2015, 2031)
        year_choices = [ year for year in year_list]
        return year_choices

class Getyearlist1(object):

    '''Common pagination for all model'''

    @staticmethod
    def year_list():
        year_choices = []
        year_list = range(1950, datetime.datetime.today().year + 1 )
        year_choices = [ year for year in year_list]
        return year_choices


class SaveCsvSheet(object):

    @staticmethod
    def save_file(request, file_name, file_path):
        path = file_path
        if not os.path.exists(path):
            os.makedirs(path)
        destination = open(path + '/' + str(file_name), "wb")
        for chunk in file_name.chunks():
            destination.write(chunk)
        destination.close()


class get_next_week_start_date(object):

    @staticmethod
    def next_weekday(d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)


def time_slots():
    start_time = datetime.time(00, 00)
    end_time = datetime.time(23, 30)
    t = start_time
    while t <= end_time:
        yield t.strftime('%I:%M %p')
        t = (datetime.datetime.combine(datetime.date.today(), t) +
             datetime.timedelta(minutes=15)).time()


class SendMail(object):

    ''' Common Email Setting '''

    @staticmethod
    def mail(subject, email, email_html, multple_receipt = None):
        try:
            if multple_receipt:
                to = multple_receipt
            else:
                to = [email]
            from_email = settings.EMAIL_HOST_USER
            msg = EmailMessage(subject, email_html, to=to, from_email=from_email)
            msg.content_subtype = "html"
            msg.send()
            fail_type = 1
        except:
            fail_type = 0
        return fail_type


class SendSmsNotification(object):

    '''  Mobile Verification  '''

    @staticmethod
    def SendSmsByTwilio(mobileno, message):
        message = urllib.parse.quote(message)
        try:
            baseurl = settings.SMS_BASE_URL+settings.SMS_API_KEY
            url= baseurl+'&sender='+settings.SMS_SENDER_MOBILE+'&to='+mobileno+'&message='+message+'&format=json&promo=1'
            response = requests.get(url)
            if response.status_code == 200 and response.json()['status'] == "AWAITED-DLR":
                return True
            else:
                return False
        except Exception as e:
            return False


class UserPermission(object):

    '''  Mobile Verification  '''

    @staticmethod
    def AddEditPermission(request, main_menu, submenu):
        try:
            user_permi = UserAccessPermissonModelsPermission.objects.get(main_function=main_menu, sub_menu_sequence = submenu)
            user_permi.add = False
            user_permi.edit = False
            user_permi.view = False 
            user_permi.delete = False
            user_permi.save()
        except Exception as e:
            user_permi = UserAccessPermissonModelsPermission()
        return user_permi


def get_all_child(id):
    append_user  = []
    data = User.objects.raw("WITH RECURSIVE subordinates AS (SELECT id from auth_user WHERE id =" +str(id)+ "UNION SELECT e.id from auth_user e INNER JOIN subordinates s ON s.id = e.reporting_to_id) SELECT  * FROM subordinates")
    for p in data:
        append_user.append(p)
    return append_user


class GetAndManageHierarchyOfEmployee(object):

    @staticmethod
    def Employee_list(request):
        append_users = []
        get_all_provided_role = ManageUserMultipleRole.objects.filter(user_id = request.user.id)
        for p in get_all_provided_role:
            if p.user_role.sequence == 1:
                append_users.append(p.user.id)
            elif p.user_role.sequence == 2:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 3:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 4:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 5:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 6:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 7:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 8:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 9:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 10:
                child_user = get_all_child(p.user.id)
                append_users += child_user
            elif p.user_role.sequence == 10:
                child_user = get_all_child(p.user.id)
                append_users += child_user
        return list(dict.fromkeys(append_users))


class SendSmsEmailAndNotification(object):

    ''' Sending Email, SMS and Notification  '''

    @staticmethod
    def send_notification_sms(data = None, action_method = None, send_frm_lead = None):
        get_all_action_lower = TemplateForNotification.objects.annotate(notification_action= Lower('action__notification_action'))
        get_all_action_methd = get_all_action_lower.filter(notification_action = action_method.lower(), is_active = True)
        for data_li in  get_all_action_methd:
            if send_frm_lead is None:
                if data_li.notification_method.notification_method.lower() == "email":
                    receipt_mail = data.email+','+data.reporting_to.email
                    SendMail.mail(data_li.notification_subject, None, data_li.template, receipt_mail.split(','))
                if data_li.notification_method.notification_method.lower() == "sms":
                    SendSmsNotification.SendSmsByTwilio('+91'+str(data.mobile_no), data_li.template)
                if data_li.notification_method.notification_method.lower() == "notification":
                    NotificationSendReportingOfficer(None, data.id, data_li.template)
            else:
                if data_li.notification_method.notification_method.lower() == "email":
                    receipt_mail = str(send_frm_lead['email'])
                    SendMail.mail(data_li.notification_subject, None, data_li.template, receipt_mail.split(','))
                if data_li.notification_method.notification_method.lower() == "sms":
                    SendSmsNotification.SendSmsByTwilio('+91'+str(send_frm_lead['mobile_no']), data_li.template)
                if data_li.notification_method.notification_method.lower() == "notification":
                    NotificationSendReportingOfficer(None, str(send_frm_lead['allocated_to_id']), data_li.template)