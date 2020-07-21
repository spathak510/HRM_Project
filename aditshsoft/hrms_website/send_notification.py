from hrms_management.models import *
# from crm_api.models import *



def NotificationSendReportingOfficer(sender_id, receiver_id, get_detail):
	# Save Notification To Reporting Officer
	save_notification = AllUserActivityNotification()
	save_notification.sender_id =  sender_id
	save_notification.receiver_id =  receiver_id
	save_notification.body_messages =  get_detail
	save_notification.save()
	return True