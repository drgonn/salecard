from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from myapp.models import UserProfile

class WechatIdAuthBackend(ModelBackend):
    def authenticate(self, request, wechat_id=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(userprofile__wechat_id=wechat_id)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class WechatIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        wechat_id = request.GET.get('token')  # 从请求中获取wechat_id
        if wechat_id:
            try:
                user_profile = UserProfile.objects.get(wechat_id=wechat_id)
                request.user_profile = user_profile  # 存储用户信息到请求上下文
            except UserProfile.DoesNotExist:
                request.user_profile = None

        response = self.get_response(request)
        return response
