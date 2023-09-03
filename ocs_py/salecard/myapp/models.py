from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    license_image_url = models.URLField()
    name = models.CharField(max_length=100)
    boss = models.ForeignKey(User, related_name='owned_companies', on_delete=models.CASCADE)
    id_card_front_url = models.URLField()
    id_card_back_url = models.URLField()
    address = models.CharField(max_length=255)
    video_list = models.JSONField(default=list)
    description = models.TextField()
    company_images = models.JSONField(default=list)  # 存储企业图片列表
    is_active = models.BooleanField(default=False)  # 添加激活状态字段，默认为未激活
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Create your models here.
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200)
    wechat_id = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    tiktok_id = models.CharField(max_length=100, blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    card_nums = models.IntegerField(default=3)
    manager = models.ForeignKey(User, related_name='subordinates', null=True, blank=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, related_name='employees',null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    highest_role = models.CharField(max_length=20, default='普通人员')

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.name

def create_roles():
    roles = [
        ("协会会长", 1),
        ("协会经理", 2),
        ("企业老板", 3),
        ("企业经理", 4),
        ("企业销售", 5),
        ("普通人员", 6),
    ]

    for role_name, role_level in roles:
        role, created = Role.objects.get_or_create(name=role_name, level=role_level)
        group, created = Group.objects.get_or_create(name=role_name)
        group.level = role_level
        group.save()
        role.group = group
        role.save()



class Card(models.Model):
    card_code = models.CharField(max_length=12, unique=True)
    hash_value = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_cards', on_delete=models.SET_NULL, null=True)
    salesman = models.ForeignKey(User, related_name='sold_cards', on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(User, related_name='managed_cards', on_delete=models.SET_NULL, null=True)
    boss = models.ForeignKey(User, related_name='bossed_cards', on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, related_name='company_cards', on_delete=models.SET_NULL, null=True)
    video_list = models.JSONField(default=list)  # 使用 JSONField 存储视频列表
    name = models.CharField(max_length=100)
    avatar_url = models.URLField()
    card_style_image_url = models.URLField()
    card_rights = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Application(models.Model):
    # 提交申请的用户
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications_submitted')
    approver = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='applications_approved')
    application_info = models.TextField()
    application_arg = models.CharField(max_length=100, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    application_type = models.CharField(max_length=20, choices=(
        ('注册公司', '注册公司'),
        ('添加员工', '添加员工'),
        ('申请批卡', '申请批卡'),
    ), default='添加员工')

    def __str__(self):
        return f"Application by {self.applicant.username}, Status: {'Approved' if self.is_approved else 'Pending'}"


class HashValue(models.Model):
    id = models.AutoField(primary_key=True)
    hash_value = models.CharField(max_length=12)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.hash_value






