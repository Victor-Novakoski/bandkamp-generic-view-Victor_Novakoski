from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.set_password(validated_data["password"])
        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "validators": [UniqueValidator(queryset=User.objects.all())]
                },
            "username": {
                "validators": [
                    UniqueValidator(
                        User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
        }
