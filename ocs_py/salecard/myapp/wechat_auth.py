from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from myapp.models import UserProfile
import jwt
from django.http import JsonResponse
from django.contrib.auth.models import User

def generate_jwt_token(user_id, roles, role):
    # 创建包含用户ID和角色的字典
    payload = {'user_id': user_id, 'roles': roles, 'role':role}
    
    # 使用您的密钥进行签名
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    
    token_str = token.decode('utf-8')
    
    return token_str

def verify_and_decode_token(token, secret_key="your_secret_key"):
    try:
        # 验证并解码JWT令牌
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # 令牌过期
        return None
    except jwt.InvalidTokenError:
        # 无效的令牌
        return None

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
        # 获取JWT令牌
        token = request.META.get('HTTP_AUTHORIZATION')
        print("收到token", token)
        if token:
            try:
                # 解码JWT令牌
                # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
                user_id = payload.get('user_id')
                print("denglu用户id", user_id)

                # 检查用户是否存在
                try:
                    user = User.objects.get(pk=user_id)
                    request.user = user  # 将用户对象添加到请求
                except User.DoesNotExist:
                    pass  # 处理用户不存在的情况

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response
