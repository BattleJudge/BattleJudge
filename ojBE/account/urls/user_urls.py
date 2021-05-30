from django.urls import path
from ..views.user_views import (UserRegisterView, UserLoginView,
                                UserUploadAvatar, UserChangePassword,
                                UserResetEmail, GetUserResetPasswordToken,
                                UserResetPassword, GetUserResetEmailToken,
                                GetUsereProfile, )

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('avatar/', UserUploadAvatar.as_view(), name='upload_avatar'),
    path('change_password/', UserChangePassword.as_view(), name='user_change_password'),
    path('reset_pwd_token/', GetUserResetPasswordToken.as_view(), name='user_reset_pwd_token'),
    path('reset_pwd/', UserResetPassword.as_view(), name='user_reset_pws'),
    path('reset_email_token/', GetUserResetEmailToken.as_view(), name='user_reset_email_token'),
    path('reset_email/', UserResetEmail.as_view(), name='user_reset_email'),
    path('profile/', GetUsereProfile.as_view(), name='user_profile'),
]