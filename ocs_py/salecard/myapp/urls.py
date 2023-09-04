from django.urls import path
from myapp.views import views
from myapp.views.views import UserRegistrationView
from myapp.views import drf

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('register', UserRegistrationView.as_view(), name='user-registration'),
    path('user_info', views.get_user_info, name='get_user_info'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('upload_video', views.upload_video, name='upload_video'),
    path('company/list', views.company_list, name='company_list'),
    path('company/detail/<int:company_id>', views.company_detail, name='company_detail'),
    path('company/create', views.create_company, name='create_company'),
    path('drf/company/list/', drf.CompanyList.as_view(), name='company-list'),
    path('drf/company/detail/<int:pk>/', drf.CompanyDetail.as_view(), name='company-detail'),
    path('drf/company/create/', drf.CompanyCreate.as_view(), name='company-create'),
    path('company/update/<int:company_id>', views.update_company, name='update_company'),
    path('invite_to_company', views.invite_to_company, name='invite_to_company'),
    path('invite/<int:company_id>/<int:inviter_id>', views.submit_invitation, name='submit_invitation'),
    path('view_applications/', views.view_applications, name='view_applications'),
    path('approve_application/<int:application_id>/', views.approve_application, name='approve_application'),
    path('activate_card/', views.activate_card, name='activate_card'),
    path('send_card/', views.send_card, name='send_card'),
    path('switch_role/', views.switch_role, name='switch_role'),
    path('apply_for_cards/', views.apply_for_cards, name='apply_for_cards'),
    path('card_details/<str:card_code>/', views.get_card_details, name='get_card_details'),
    path('wechat_login', views.wechat_login, name='wechat_login'),
]
