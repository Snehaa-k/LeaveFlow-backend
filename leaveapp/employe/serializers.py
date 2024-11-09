from rest_framework import serializers
from .models import CustomUser,Leaveapplication,Userprofile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password','username','is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        
       
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.generate_otp()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password) 
        return super().update(instance, validated_data)
    
class LeaveApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Leaveapplication
        fields = ['id', 'leave_type', 'start_date','end_date','reason','document','status','username','email']
    document = serializers.FileField(required=False)

class UserLeaveSerializer(serializers.ModelSerializer):
    leaves = LeaveApplicationSerializer(many=True, source='leave_applications')  

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'leaves']


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Userprofile
        fields = ['profile_image',"email",'username']
