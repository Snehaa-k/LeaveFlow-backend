from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("allists/", views.LeaveApplicationList.as_view(), name="list-leave"),
    path("accept/<int:id>/", views.AcceptLeaveRequest.as_view(), name="leve-accept"),
    path("reject/<int:id>/", views.RejectLeaveRequest.as_view(), name="leave-reject"),
    path("calenderview/", views.DasghbordOverview.as_view(), name="leave-dashbord"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
