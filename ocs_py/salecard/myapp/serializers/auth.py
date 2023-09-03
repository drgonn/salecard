from rest_framework import serializers
from myapp.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('wechat_id', 'phone_number')  # 仅接受微信ID和手机号
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)  # 用户名和密码字段

    def create(self, validated_data):
        # 从validated_data中获取wechat_id的值，并用作username
        wechat_id = validated_data['wechat_id']
        phone_number = validated_data['phone_number']
        
        # 创建User记录
        user = User.objects.create(username=wechat_id)
        user.set_password(password)
        user.save()

        # 创建UserProfile记录并关联到User
        profile = UserProfile.objects.create(user=user, wechat_id=wechat_id, phone_number=phone_number)
        
        return user