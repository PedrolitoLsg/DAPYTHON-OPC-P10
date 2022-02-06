from rest_framework import serializers
from .models import CustomUsers, Projects, Contributors, Issues, Comments


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True}}

    def create_user(self, email, password, first_name=None, last_name=None):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = CustomUsers.objects.create(
            email=email
        )
        if first_name and isinstance(first_name, str):
            user.first_name = first_name
        else:
            user.first_name = ""
        if last_name and isinstance(last_name, str):
            user.last_name = last_name
        else:
            user.last_name = ""
        user.set_password(password)
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type']


class ProjectWithIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'id', 'author_user']
        extra_kwargs = {
            'id': {'read_only': True},
            'author_user': {'read_only': True}
        }


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['role', 'user', 'project', 'id']
        extra_kwargs = {
            'project': {'read_only': True},
            'id': {'read_only': True},
            'role': {'read_only': True}
        }


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            "created_time": {'read_only': True},
            "author_user": {'read_only': True},
            "project": {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['description', 'id', 'issue',
                  'author_user_id', 'created_time']
        extra_kwargs = {
            'id': {'read_only': True},
            'issue': {'read_only': True},
            'author_user_id': {'read_only': True},
            'created_time': {'read_only': True}
        }
