from hrms_management.models import *
from django.db.models import Q
from django.db.models import Max, Count


def UserDataAllocationContextProcessor(request):
	context = {}
	if request.user.is_authenticated:
		get_all_user_permission = UserAccessPermissonModelsPermission.objects.filter(user_id = request.user.id)
		get_all_user_permission1 = UserAccessPermissonModelsPermission.objects.values('main_function').annotate(Count('main_function')).filter(user_id = request.user.id).order_by('sequence')
		get_all_user_by_function_level = UserAccessPermissonModelsPermission.objects.values('function_level').annotate(Max('function_level')).filter(user_id = request.user.id)
		context = {
			'get_all_user_permission' : get_all_user_permission,
			'get_all_user_permission1': get_all_user_permission1,
			'get_all_user_by_function_level': get_all_user_by_function_level,
			'working_days': WORKINGDAYS1,
			'notification_type': NotificationType.objects.filter(is_active  = 1),
			'notification_listing': ActivityNotification.objects.filter(receiver_id = request.user.id ,is_read = False).order_by('-id'),
			'user_userdesignation': ManageDesignation.objects.filter(is_active = True).order_by('-id')
		}
	return context