from rest_framework import serializers
from .models import User, Company, JobListing, JobApplication

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
        raise serializers.ValidationError('Invalid login credentials')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role'] 


class JobListingSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = JobListing
        fields = ['id', 'title','company', 'company_name', 'description', 'requirements', 'location', 'salary', 'created_at', 'is_active'] 
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

        
    def get_company_name(self, obj):
      
        return obj.company.companyname
    

        

class CompanySerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Company
        fields = ['companyname', 'location', 'description', 'owner']
        read_only_fields = ['owner']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job',  'resume', 'cover_letter', 'applied_at', 'status']
        read_only_fields = ['applied_at', 'status']        
