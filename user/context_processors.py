from .models import UserProfile

def user_balance(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'user_balance': profile.balance}
        except UserProfile.DoesNotExist:
            return {'user_balance': 0.0}
    return {}
