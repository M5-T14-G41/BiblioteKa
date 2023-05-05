from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import User


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=120,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered."
            )
        ],
    )
    password = serializers.CharField(max_length=120, write_only=True)
    is_employee = serializers.BooleanField(default=False, allow_null=True)
    is_banned = serializers.BooleanField(default=False, allow_null=False)

    class Meta:
        model = User
        fields = ['id', 'email','username', 'password', 'is_superuser', 'is_employee', 'is_banned']
        read_only_fields = ['id']
        write_only_fields = ['is_superuser']

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def create(self, validated_data):
        if validated_data["is_employee"]:
            validated_data["is_superuser"] = True
        else:
            validated_data["is_superuser"] = False
        create_user = User.objects.create_user(**validated_data)
        return create_user

    def __str__(self):
        return f"Name {self.username} é id: [{self.id}]"

