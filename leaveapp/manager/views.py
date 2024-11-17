from django.shortcuts import render
from rest_framework import status, permissions
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import generics
from django.core.mail import send_mail
from employe.models import Leaveapplication, CustomUser
from employe.serializers import LeaveApplicationSerializer, UserLeaveSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser



# Create your views here.
class LeaveApplicationList(APIView):
    def get(self, request):
        leave_applications = Leaveapplication.objects.all()
        serializer = LeaveApplicationSerializer(leave_applications, many=True)
        return Response(serializer.data)


class AcceptLeaveRequest(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, id, *args, **kwargs):

        try:
            form = Leaveapplication.objects.get(id=id)
            user = CustomUser.objects.get(email=form.user.email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "email is not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        form.status = "accepted"
        form.save()

        return Response({"status": "Accepted"}, status=status.HTTP_200_OK)


class RejectLeaveRequest(APIView):

    permission_classes = [IsAdminUser] 
    def post(self, request, id, *args, **kwargs):

        try:
            form = Leaveapplication.objects.get(id=id)
            user = CustomUser.objects.get(email=form.user.email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "email is not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        reason = request.data.get("reason")

        form.status = "rejected"
        form.save()

        subject = "Leave Application Rejected"
        message = f"Dear {user.username},\n\nYour leave application has been rejected for the following reason:\n\n{reason}\n\nIf you have any questions, please contact the HR department."
        from_email = "worldmagical491@gmail.com"
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({"status": "rejected"}, status=status.HTTP_200_OK)


class DasghbordOverview(generics.ListAPIView):
    queryset = (
        CustomUser.objects.prefetch_related("leave_applications")
        .exclude(is_superuser=True)
        .all()
    )

    serializer_class = UserLeaveSerializer

    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)

        total_employees = CustomUser.objects.exclude(is_superuser=True).count()

        total_pending_approvals = Leaveapplication.objects.filter(
            status="pending"
        ).count()

        response.data = {
            "total_employees": total_employees,
            "total_pending_approvals": total_pending_approvals,
            "users": response.data,
        }

        return response
