from django.urls import path
from ..views.admin_views import (AdminGetUserInfoList, AdminGetUserInfoByUsername, 
                                AdminUpdateUserInfo, AdminManagerUser, )

urlpatterns = [
    path('user_info/', AdminGetUserInfoList.as_view(), name='user_info'),
    path('user_info_by_username/', AdminGetUserInfoByUsername.as_view(), name='user_info_by_name'),
    path('update_user_info/', AdminUpdateUserInfo.as_view(), name='update_user_info'),
    path('user/', AdminManagerUser.as_view(), name='user'),
]