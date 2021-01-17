from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name',)

        # These fields are displayed but not editable and have to be a part of 'fields' tuple
        read_only_fields = ('id',)
        
        # These fields are only editable (not displayed) and have to be a part of 'fields' tuple
        extra_kwargs = {
            "password": {"write_only": True, 'min_length': 4}
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


class AuthTokenSerializer(serializers.Serializer):
    """
    Get token for the user
    """
    email = serializers.EmailField(
        required=True,
        max_length=150
    )
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
