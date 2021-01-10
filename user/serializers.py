from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name',)
        extra_kwargs = {
            "password": {"write_only": True, 'min_length': 4},
        }

    def update(self, instance, validated_data):
        """
        Update a user
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def create(slef, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        return get_user_model().objects.create_user(**validated_data)
