from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("register/", views.RegisterationApi.as_view(), name="register"),
    path("verification/", views.VerifyOtp.as_view(), name="verification"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("leaveapply/", views.LeaveApply.as_view(), name="leave"),
    path("leavelists/", views.ListLeave.as_view(), name="lists-leave"),
    path("editleave/<int:id>/", views.EditLeave.as_view(), name="edit-leave"),
    path("deleteleave/<int:id>/", views.leavedelete.as_view(), name="edit-leave"),
    path("profileupload/", views.ProfileImageUpload.as_view(), name="upload-image"),
    path("profileview/", views.ProfileImageGet.as_view(), name="profile-view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
