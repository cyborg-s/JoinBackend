from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField
from join_BE.models import Tasks, Contacts, Subtask, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ContactSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = PhoneNumberSerializerField()

    def create(self, validated_data):
        return Contacts.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'status']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'assigned_to',
                  'due_date', 'prio', 'category', 'PositionID', 'subtasks']

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        task = Tasks.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if subtasks_data is not None:
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    reapeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'reapeated_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['reapeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")

        return data

    def create(self, validated_data):
        validated_data.pop('reapeated_password')
        first_name = validated_data.pop('first_name')
        email = validated_data['email']

        username = email
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=first_name
        )

        profile = UserProfile.objects.create(user=user)
        print(">>> PROFILE CREATED:", profile)

        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "Ungültige E-Mail oder Passwort.", code='authorization')

        attrs['user'] = user
        return attrs
