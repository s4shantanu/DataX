from .models import UserActivity

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:

        ip = x_forwarded_for.split(',')[0]

    else:

        ip = request.META.get('REMOTE_ADDR')
        
    return ip



def log_user_activity(request, action):

    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            action=action,
            ip_address=get_client_ip(request)
        )