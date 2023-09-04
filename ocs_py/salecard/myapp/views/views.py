from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# 模型
from myapp.models import UserProfile,Role, Company, Application, HashValue, Card
from myapp.form import CompanyForm
from myapp.wechat_auth import generate_jwt_token, verify_and_decode_token

from myapp.serializers.auth import UserRegistrationSerializer,UserProfileSerializer
from django.http import JsonResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import hashlib
from datetime import datetime
import os
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def hello_world(request):
    return JsonResponse({'message': 'Hello, World!'})

class UserRegistrationView(APIView):
    def post(self, request):
        # 获取提交的数据
        wechat_id = request.data.get('wechat_id')
        phone_number = request.data.get('phone_number')

        if not wechat_id or not phone_number:
            return JsonResponse({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否已存在具有相同wechat_id的用户
        if User.objects.filter(username=wechat_id).exists():
            return JsonResponse({'error': 'User with this WeChat ID already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建用户
        role = Role.objects.get(name='普通人员')
        group = Group.objects.get(name='普通人员')
        user = User.objects.create_user(username=wechat_id)
        user.groups.add(group)
        for _ in range(3):
            # 创建卡片并设置user字段为注册的用户
            card = Card(user=user)
            card.save()


        # 创建关联的UserProfile记录
        UserProfile.objects.create(user=user, wechat_id=wechat_id, phone_number=phone_number)

        return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('success_url')  # 重定向到登录成功后的页面
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
@login_required
def get_user_info(request):
    # user_profile = request.user_profile
    # print(user_profile)
    user = request.user
    print(user)

        # 用户已登录，可以获取用户信息
    user_info = {
        'id': user.userprofile.user.id,
        'name': user.userprofile.name,
        'card_nums': user.userprofile.card_nums,
        # 'role': user.userprofile.user.groups.first().name,
        'role': user.userprofile.role.name,
    }
    return JsonResponse({'user_info': user_info})


@csrf_exempt
def generate_unique_filename(file):
    # 生成文件哈希码并作为文件名
    file_hash = hashlib.md5(file.read()).hexdigest()[:12]
    file_extension = os.path.splitext(file.name)[-1]
    return f"{file_hash}{file_extension}"

@csrf_exempt
def upload_image(request):
    print(request.method)
    print(request.FILES)
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_name = generate_unique_filename(image)
        # 构建静态资源文件路径
        static_path = os.path.join(settings.STATIC_DIR, 'images', image_name)

        # 将上传的图片保存到静态资源文件夹中
        with open(static_path, 'wb') as file:
            for chunk in image.chunks():
                file.write(chunk)

        # 返回图片的 URL 地址
        domain = 'http://fpi.3p3.top'
        image_url = os.path.join(settings.STATIC_URL, 'images', image_name)
        image_url = domain + image_url
        return JsonResponse({'image_url': image_url})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def company_list(request):
    # 获取查询参数，如果提供了激活状态参数，则筛选企业
    is_active = request.GET.get('is_active')
    companies = Company.objects.all()

    if is_active:
        companies = companies.filter(is_active=is_active)

    # 分页
    page_number = request.GET.get('page', 1)
    per_page = 10  # 每页显示的企业数量
    paginator = Paginator(companies, per_page)
    page = paginator.page(page_number)

    # 构建企业列表
    company_list = []
    for company in page:
        company_info = {
            'id': company.id,
            'name': company.name,
            'is_active': company.is_active,
            # 其他企业信息字段...
        }
        company_list.append(company_info)

    return JsonResponse({'companies': company_list, 'total_pages': paginator.num_pages})

@csrf_exempt
def company_detail(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
        company_info = {
            'id': company.id,
            'name': company.name,
            'is_active': company.is_active,
            # 其他企业信息字段...
        }
        return JsonResponse({'company': company_info})
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)

@csrf_exempt
def create_company(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        company_name = json_data.get('name')
        print(company_name)


            # 创建申请对象
            # application = Application(
            #     applicant=applicant,
            #     application_type=application_type,
            #     application_info=f'申请注册公司，公司ID：{company_id}',
            #     application_arg=str(company_id),
            # )
            # application.save()

        return JsonResponse({'message': 'Company created successfully',
            #  'company_id': company.id
             })
        # else:
        #     errors = form.errors.as_json()
        #     return JsonResponse({'error': errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# @login_required
    """
    企业老板的用户账号可以修改自己的企业内容，除了激活状态不能修改之外。
协会经理可以修改企业的激活状态。
    """
@require_POST
@csrf_exempt
def update_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)


        # 检查用户权限
        if request.user == company.boss:
            # 企业老板可以修改企业信息（除激活状态以外的字段）
            company.name = request.POST.get('name', company.name)
            company.license_image_url = request.POST.get('license_image_url', company.license_image_url)
            company.id_card_front_url = request.POST.get('id_card_front_url', company.id_card_front_url)
            company.id_card_back_url = request.POST.get('id_card_back_url', company.id_card_back_url)
            company.address = request.POST.get('address', company.address)
            company.video_list = request.POST.get('video_list', company.video_list)
            company.description = request.POST.get('description', company.description)
            company.save()
            return JsonResponse({'message': 'Company information updated successfully'})
        elif request.user.groups.filter(name='协会经理').exists():
            # 协会经理可以修改激活状态
            is_active = request.POST.get('is_active')
            if is_active is not None:
                company.is_active = is_active
                company.save()
                return JsonResponse({'message': 'Company activation status updated successfully'})
            else:
                return JsonResponse({'error': 'Invalid request'}, status=400)
        else:
            # 其他用户没有权限修改企业信息
            return JsonResponse({'error': 'Permission denied'}, status=403)

    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)


"""返回邀请加入企业的邀请链接
链接的接口里面含有公司id，邀请人的id，这两者是当前用户的，只有普通用户之上的用户可以请求此接口。
此链接前缀为
http://fpi.3p3.top/api"""
@csrf_exempt
def invite_to_company(request):
    # 验证用户权限，只有普通用户之上的用户可以访问
    if not request.user.groups.filter(name__in=['协会会长', '协会经理', '企业老板', '企业经理']).exists():
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # 获取当前用户的公司ID和用户ID
    company_id = request.user.userprofile.company.id
    inviter_id = request.user.id

    # 构建邀请链接
    invite_link = f"http://fpi.3p3.top/api/invite/{company_id}/{inviter_id}"

    return JsonResponse({'invite_link': invite_link})



"""
户提交用户的wechat_id，和用户id到此接口http://fpi.3p3.top/api/invite/{company_id}/{inviter_id}
成功后会创建一个申请，记录申请人审批人，申请信息等。
"""
@csrf_exempt
def submit_invitation(request, company_id, inviter_id):
    # 验证请求方法为POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    # 获取用户提交的wechat_id
    wechat_id = request.POST.get('wechat_id')
    if not wechat_id:
        return JsonResponse({'error': 'Missing wechat_id'}, status=400)

    # 获取申请人和审批人
    applicant = User.objects.get(id=inviter_id)
    company = applicant.userprofile.company
    approver = company.boss  

    # 创建申请记录
    application_info = f"Invitation to join company {company_id}. Wechat ID: {wechat_id}"
    application = Application.objects.create(
        applicant=applicant,
        approver=approver,
        company=company,
        application_info=application_info,
    )

    return JsonResponse({'message': 'Invitation submitted successfully', 'application_id': application.id})


"""用户查看自己的申请表列表，需要分页，当用户是属于企业时，提交参数企业申请，可以产看企业ID和审批人ID为自己的申请。此举需要自身是销售角色之上的用户。"""
@csrf_exempt
def view_applications(request):
    # 获取当前用户
    current_user = request.user

    # 根据角色筛选申请
    if current_user.groups.filter(name='销售').exists() and current_user.userprofile.manager:
        # 如果用户是销售及以上角色，并且有上级用户，筛选属于自己和上级用户企业的申请
        applications = Application.objects.filter(
            company_id__in=[current_user.userprofile.company.id, current_user.userprofile.manager.userprofile.company.id],
            approver_id=current_user.id
        ).order_by('-created_at')
    elif current_user.groups.filter(name='销售').exists():
        # 如果用户是销售及以上角色，但没有上级用户，筛选属于自己企业的申请
        applications = Application.objects.filter(
            company_id=current_user.userprofile.company.id,
            approver_id=current_user.id
        ).order_by('-created_at')
    else:
        # 如果用户不是销售及以上角色，返回空列表
        applications = []

    # 分页
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(applications, per_page)
    
    try:
        applications_page = paginator.page(page)
    except EmptyPage:
        applications_page = paginator.page(paginator.num_pages)

    # 构建返回数据
    application_list = []
    for application in applications_page:
        application_data = {
            'id': application.id,
            'applicant_id': application.applicant.id,
            'applicant_username': application.applicant.username,
            'application_info': application.application_info,
            'is_approved': application.is_approved,
            'created_at': application.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        application_list.append(application_data)

    return JsonResponse({'applications': application_list, 'total_pages': paginator.num_pages})


"""对自己为审批人的申请表批准，修改is_approved为true，此举需要自身是销售角色之上的用户。
如果是注册公司申请类型，通过申请对象里面的application_arg获取company对象，改变公司激活状态。
如果是申请获取卡片,通过申请对象里面的application_arg获取卡片数量，创建申请数量的Card，用户和boss都是老板，company是老板的公司。
"""
@csrf_exempt
def approve_application(request, application_id):
    # 获取当前用户
    current_user = request.user

    # 验证用户角色，确保用户是销售角色之上的用户
    if not current_user.groups.filter(name__in=['协会经理', '企业老板', '企业经理']).exists():
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # 获取申请对象
    application = Application.objects.get(id=application_id)

    # 验证用户是否是审批人
    if application.approver != current_user:
        return JsonResponse({'error': 'You are not the approver of this application'}, status=403)

    # 开启事务
    with transaction.atomic():
        # 更新申请表属性
        application.is_approved = True
        application.save()
                # 根据申请类型处理不同情况
        if application.application_type == '注册公司':
            # 获取公司对象
            try:
                company_id = int(application.application_arg)
                company = Company.objects.get(id=company_id)
            except (ValueError, Company.DoesNotExist):
                return JsonResponse({'error': 'Invalid company ID'}, status=400)

            # 修改公司激活状态
            company.is_active = True
            company.save()
        elif application.application_type == '申请批卡':
            # 获取申请数量
            try:
                card_count = int(application.application_arg)
            except ValueError:
                return JsonResponse({'error': 'Invalid card count'}, status=400)

            # 创建申请数量的卡片
            for _ in range(card_count):
                card = Card(
                    user=current_user,
                    boss=current_user,
                    company=current_user.userprofile.company,
                )
                card.save()
        elif application.application_type == '添加员工':
            # 更新申请人的角色、企业ID和上级用户
            applicant = application.applicant
            current_role = applicant.groups.first()
            if current_role:
                # 获取当前角色的下一个角色名称，这里假设角色名称是有序的，例如：销售、企业销售、企业经理、企业老板
                roles = ['销售', '企业销售', '企业经理', '企业老板']
                next_role = roles[roles.index(current_role.name) - 1]

                # 更新申请人的角色
                try:
                    next_group = Group.objects.get(name=next_role)
                    applicant.groups.clear()
                    applicant.groups.add(next_group)
                except Group.DoesNotExist:
                    pass

            # 更新申请人的企业ID和上级用户
            applicant.userprofile.company = application.company
            applicant.userprofile.manager = current_user
            applicant.userprofile.save()

    return JsonResponse({'message': 'Application approved successfully'})

"""
用户激活名片，用户的card_nums有额度的时候可以编辑名片码，
填写姓名，头像地址，企业名称，名片专属名称，然后点击激活，
激活后还要插入hash_value从HashValue表中取出created_at时间最近的，
然后再使用取出的这个hash_value通过hash算法再生成一个12位hash_value插入HashValue表，最后创建此card成功。
"""
@csrf_exempt
def activate_card(request):
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        # 检查用户是否有足够的卡片额度
        if user_profile.card_nums <= 0:
            return JsonResponse({'error': 'Insufficient card balance'}, status=400)

        # 获取用户提交的信息
        name = request.POST.get('name')
        avatar_url = request.POST.get('avatar_url')
        company_name = request.POST.get('company_name')
        exclusive_name = request.POST.get('exclusive_name')

        # 创建新的名片
        new_card = Card(
            user=user,
            name=name,
            avatar_url=avatar_url,
            company_name=company_name,
            exclusive_name=exclusive_name,
        )
        new_card.save()

        # 更新用户的名片额度
        user_profile.card_nums -= 1
        user_profile.save()

        # 从 HashValue 表中获取最新的 hash 值
        latest_hash_value = HashValue.objects.latest('created_at').hash_value

        # 使用 hash 算法生成新的 12 位 hash 值
        new_hash_value = generate_new_hash(latest_hash_value)

        # 创建新的 hash 值并保存到 HashValue 表中
        new_hash = HashValue(hash_value=new_hash_value)
        new_hash.save()

        return JsonResponse({'message': 'Card activated successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_new_hash(old_hash):
    now = datetime.now()
    random_string = '1234567890abcdefghijklmnopqrstvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return hashlib.md5((old_hash + random_string).encode()).hexdigest()[:12]

"""
当用户手上的card里面user为自己并且企业ID和自己的企业ID相同的card数量大于0时，可以将自己的卡片发给自己的员工（也就是角色下一级用户），提交员工的用户id和卡片数量，之后这些卡的user将会变成员工的user，sender将会变成发送者用户，然后根据自己与员工的角色分别设置boss，manager，salesman的用户id，
"""
@csrf_exempt
def send_card(request):
    if request.method == 'POST':
        sender = request.user
        sender_profile = UserProfile.objects.get(user=sender)

        # 获取员工的用户id和卡片数量
        employee_id = request.POST.get('employee_id')
        card_count = int(request.POST.get('card_count', 0))

        # 检查 sender 是否拥有足够的卡片
        if sender_profile.card_nums < card_count:
            return JsonResponse({'error': 'Insufficient card balance'}, status=400)

        # 获取员工对象
        employee = User.objects.get(id=employee_id)
        employee_profile = UserProfile.objects.get(user=employee)

        # 检查 sender 是否有权限发送卡片给员工（例如，只能给下一级角色发送）
        if not is_allowed_to_send(sender, employee):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        # 获取 sender 手上的卡片
        sender_cards = Card.objects.filter(user=sender, company=sender_profile.company)[:card_count]

        # 更新卡片信息并分配给员工
        for card in sender_cards:
            card.user = employee
            card.sender = sender
            card.save()

            # 更新卡片的 boss、manager 和 salesman
            if employee_profile.company == sender_profile.company:
                card.boss = employee
                card.manager = sender
            else:
                card.boss = sender
                card.manager = None  # 员工不再有上级
            card.salesman = None  # 员工不再是销售
            card.save()


        # 更新 sender 的卡片额度
        sender_profile.card_nums -= card_count
        sender_profile.save()

        return JsonResponse({'message': f'{card_count} card(s) sent successfully to employee {employee.username}'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def is_allowed_to_send(sender, employee):
    # 编写逻辑来验证 sender 是否有权限发送卡片给 employee
    # 这里你可以根据权限规则来编写逻辑
    return True  # 暂时返回 True，需要根据具体规则来实现


"""
户可以切换最高角色范围内的角色，
企业内的3种角色：1. 企业老板2.企业经理；3.企业销售

老板可以切换企业经理或企业销售身份；企业经理可以切换企业销售身份；企业销售不能做切换
"""

# @login_required
@csrf_exempt
def switch_role(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile

        # 获取要切换的角色
        new_role = request.POST.get('new_role')

        # 检查要切换的角色是否在最高角色范围内
        if not is_valid_role(user_profile.highest_role, new_role):
            return JsonResponse({'error': 'Invalid role switch request'}, status=400)

        # 更新用户的角色
        user_profile.highest_role = new_role
        user_profile.save()

        return JsonResponse({'message': f'Role switched to {new_role} successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def is_valid_role(highest_role, new_role):
    # 编写逻辑来验证是否可以切换到新角色，根据角色规则来定义
    # 例如，老板可以切换到企业经理或企业销售，企业经理只能切换到企业销售
    if highest_role == '企业老板':
        return new_role in ['企业经理', '企业销售']
    elif highest_role == '企业经理':
        return new_role == '企业销售'
    else:
        return False  # 企业销售不能做切换

"""
企业老板向协会申请获得卡申请的接口
企业老板用户有权限可以向提交协会申请，提交申请数量即可
接口中创建一个申请，申请类型是申请批卡，申请批卡是用户自己，application_arg是数量
"""
# @login_required
@csrf_exempt
def apply_for_cards(request):
    if request.method == 'POST':
        user = request.user

        # 检查用户是否是企业老板，可以根据角色规则来判断
        if not is_company_owner(user):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        # 获取申请的数量
        card_count = int(request.POST.get('card_count', 0))

        # 创建申请对象
        application_type = '申请批卡'
        application_info = f'申请批卡，数量：{card_count}'
        application_arg = str(card_count)

        application = Application(
            applicant=user,
            application_type=application_type,
            application_info=application_info,
            application_arg=application_arg,
        )
        application.save()

        return JsonResponse({'message': 'Card application submitted successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def is_company_owner(user):
    # 编写逻辑来验证用户是否是企业老板，根据角色规则来定义
    return True  



@csrf_exempt
def get_card_details(request, card_code):
    try:
        card = Card.objects.select_related('company', 'user').get(card_code=card_code)
        
        # 构建卡片详情的响应数据
        card_details = {
            'card_code': card.card_code,
            'company': {
                'id': card.company.id,
                'name': card.company.name,
                # 其他公司字段
            },
            'user': {
                'id': card.user.id,
                'name': card.user.userprofile.name,
                # 其他用户字段
            },
            # 其他卡片字段
        }

        return JsonResponse({'card_details': card_details})
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Card not found'}, status=404)


@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        # 获取上传的视频文件
        video_file = request.FILES['video']

        # 生成视频文件名（使用哈希码）
        video_name = generate_video_name(video_file)

        # 构建视频保存路径
        video_path = os.path.join(settings.STATIC_DIR, 'videos', video_name)

        # 保存视频文件到指定路径
        with open(video_path, 'wb') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        domain = 'http://fpi.3p3.top'
        video_url = os.path.join(settings.STATIC_URL, 'images', image_name)
        video_url = domain + video_url
        return JsonResponse({'video_url': video_url})
        # return JsonResponse({'message': 'Video uploaded successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_video_name(video_file):
    # 生成哈希码（可以使用不同的哈希算法）
    hasher = hashlib.sha256()
    for chunk in video_file.chunks():
        hasher.update(chunk)
    
    # 使用哈希码的一部分作为文件名
    hash_part = hasher.hexdigest()[:12]

    # 获取文件扩展名
    _, extension = os.path.splitext(video_file.name)

    # 组合哈希码和扩展名作为文件名
    video_name = f'{hash_part}{extension}'

    return video_name



@csrf_exempt
def wechat_login(request):
    if request.method == 'POST':
        # 从POST请求中获取微信小程序发送的code
        json_data = json.loads(request.body.decode('utf-8'))
        code= json_data.get("code")
        print("code",code)
        # 向微信服务器发送code以获取用户的unionID等信息
        response = get_wechat_user_info(code)
        print(response)
        # response = {'session_key': '0nIb4FqCbbPXNiOzSVkrCg==', 'openid': 'ox2bR5D44QC4oi_tUy71oAXp7wEs'}

        # 处理微信服务器的响应
        if response.get('errcode'):
            return JsonResponse({'error': 'WeChat authentication failed',"detail":response.get('errmsg')}, status=400)


        # 从响应中获取unionID
        open_id = response.get('openid')
        # open_id = 'wwww3registeredregisteredregisteredregregisterergisteredregistered3233www'

        print("open id",open_id)

        # 检查是否已存在具有相同unionID的用户，如果不存在则创建新用户
        # user, created = User.objects.get_or_create(username=open_id)
        # print("用户创建结果",user,created)
        if User.objects.filter(username=open_id).exists():
            user = User.objects.filter(username=open_id).first()
            group_names = user.groups.values_list('name', flat=True).all()
            group_names = [i for i in group_names]
            role_name = user.userprofile.role.name
            token =  generate_jwt_token(user.id, group_names,role_name)

            test = verify_and_decode_token(token)
            print("已存在用户",test)
            print(user.userprofile.role)
            return JsonResponse({
                'message': 'Login successful',
                'user_id': user.id,"token":token,
                "roles":group_names,
                "role": user.userprofile.role.name,
            })

        # 创建用户
        role = Role.objects.get(name='普通人员')
        group = Group.objects.get(name='普通人员')
        user = User.objects.create_user(username=open_id)
        print("tianj group")
        user.groups.add(group)
        for _ in range(3):
            # 创建卡片并设置user字段为注册的用户
            card = Card(user=user)
            card.save()
        print("card save")
        # 创建关联的UserProfile记录
        UserProfile.objects.create(user=user, wechat_id=open_id, role=role)
        print("userfpofile")


        return JsonResponse({
                'message': 'Login successful',
                'user_id': user.id,"token":token,
                "roles":group_names,
                # "role": user.userprofile.role.name,
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_wechat_user_info(code):
    # 向微信服务器发送请求以获取用户信息
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': 'wx3b66399b629ecb67',  # 小程序的AppID
        'secret': '440e1f31159ffd0b910a85b2aaf37859',  # 小程序的App Secret
        'js_code': code,
        'grant_type': 'authorization_code',
    }

    response = requests.get(url, params=params)
    return json.loads(response.text)
