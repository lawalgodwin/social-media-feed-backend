from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Interaction, Comment, User


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = fields = ("id", "content",)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content")


class InteractionSerializer(ModelSerializer):
    class Meta:
        model = Interaction
        fields = "__all__"


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password")
