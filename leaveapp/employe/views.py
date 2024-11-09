from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import generics
from django.core.mail import send_mail
from .serializers import  UserLeaveSerializer, UserSerializer,LeaveApplicationSerializer,ProfileSerializer
from .models import CustomUser,Leaveapplication,Userprofile
from rest_framework.parsers import MultiPartParser






# Create your views here.


class RegisterationApi(APIView):
    print("hello")
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({"message": "User created successfully. OTP sent.",
                             "user": user_data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOtp(APIView):
    def post(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = CustomUser.objects.get(email= email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.is_verified = True
            user.otp = ''
            user.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        
        else: 
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomTokenObtainPairView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"emailfail{email}")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found or invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        
        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.is_superuser == False:

        
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            },status=status.HTTP_200_OK)
        else:
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'admin': UserSerializer(user).data
            },status=status.HTTP_200_OK)
        

class LeaveApply(APIView):
    def post(self, request):
        user = request.user.id
        try:
            employe = CustomUser.objects.get(id=user)
        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        document = request.FILES.get('document', None)
        data = request.data.copy()
        if document:
            data['document'] = document
        serializer = LeaveApplicationSerializer(data=data)
        if serializer.is_valid():
            leave_application = serializer.save(user=employe)  
            user_data = LeaveApplicationSerializer(leave_application).data
            return Response({
                "message": "Leave application created successfully.",
                "user": user_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListLeave(APIView):
    def get(self, request):
        user = request.user.id
        try:
            leave = Leaveapplication.objects.filter(user=user)
        except Leaveapplication.DoesNotExist:
            return Response({'error': 'No leave applications found for this user'}, status=status.HTTP_404_NOT_FOUND)
        
        
        leave_data = [] 
        for application in leave:
            leave_data.append({
                'id': application.id,
                'leave_type': application.leave_type,
                'start_date': application.start_date,
                'end_date': application.end_date,
                'reason': application.reason,
                'status':application.status,
                'document': application.document.url if application.document else None  
            })

        return Response({"leave": leave_data}, status=status.HTTP_200_OK)
    

class EditLeave(APIView):
    def post(self, request,id, *args, **kwargs):
        user_id = request.user.id
        print(id,"id")
        try:
            leave, created = Leaveapplication.objects.get_or_create(id = id)
        except Leaveapplication.DoesNotExist:
            return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)
        
        leave_type = request.data.get('leave_type')
        print(leave_type)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        reason = request.data.get('reason')
        
        leave.leave_type = leave_type
        leave.start_date = start_date
        leave.end_date = end_date
        leave.reason = reason
        

        image_file = request.FILES.get('document', None)
        if image_file:
            leave.document = image_file

        leave.save()

        
        if created:
            message = "leave created"
        else:
            message = "leave edited sucussfully"
        
        return Response({"message": message}, status=status.HTTP_200_OK)
    

class leavedelete(APIView):
    def delete(self, request, id):
        user = request.user
        print(f"Attempting to delete leave with ID: {id}")
        
        try:
            leave = Leaveapplication.objects.get(id=id, user=user)
            leave.delete()
            return Response({'message': 'Leave application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Leaveapplication.DoesNotExist:
            return Response({'error': 'Leave application not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
        


class LeaveApplicationList(APIView):
    def get(self, request):
        leave_applications = Leaveapplication.objects.all()
        serializer = LeaveApplicationSerializer(leave_applications, many=True)
        return Response(serializer.data)



class AcceptLeaveRequest(APIView):
  
    # permission_classes = [IsAuthenticated]
    def post(self, request, id, *args, **kwargs):
        
        try:
            form = Leaveapplication.objects.get(id=id)
            user = CustomUser.objects.get(email = form.user.email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        form.status = "accepted"
        form.save()
        
        return Response({'status': 'Accepted'}, status=status.HTTP_200_OK)
    

class RejectLeaveRequest(APIView):
  
    # permission_classes = [IsAuthenticated]
    def post(self, request, id, *args, **kwargs):

        
        try:
            form = Leaveapplication.objects.get(id=id)
            user = CustomUser.objects.get(email = form.user.email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        reason = request.data.get('reason')

        form.status = "rejected"
        form.save()

        subject = "Leave Application Rejected"
        message = f"Dear {user.username},\n\nYour leave application has been rejected for the following reason:\n\n{reason}\n\nIf you have any questions, please contact the HR department."
        from_email = "worldmagical491@gmail.com" 
        recipient_list = [user.email]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
    

class DasghbordOverview(generics.ListAPIView):
    queryset = CustomUser.objects.prefetch_related('leave_applications').exclude(is_superuser=True).all()

    serializer_class = UserLeaveSerializer
    
    def list(self, request, *args, **kwargs):
       
        response = super().list(request, *args, **kwargs)
        
        total_employees = CustomUser.objects.exclude(is_superuser=True).count()
        
        total_pending_approvals = Leaveapplication.objects.filter(status="pending").count()
        
        response.data = {
            "total_employees": total_employees,
            "total_pending_approvals": total_pending_approvals,
            "users": response.data 
        }
        
        return response




class ProfileImageUpload(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            user = CustomUser.objects.get(id = user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            userprofile = Userprofile.objects.get(user_id=user_id)
            created = False
        except Userprofile.DoesNotExist:
            userprofile = None
            created = True

        
        if userprofile:
            userprofile.profile_image = image_file
            userprofile.save()
        
        else:
            userprofile = Userprofile.objects.create(user_id=user_id, profile_image=image_file)
        
        return Response({"message":"success"}, status=status.HTTP_201_CREATED)


class ProfileImageGet(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            userprofile = Userprofile.objects.get(user_id=user_id)
        except Userprofile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)
