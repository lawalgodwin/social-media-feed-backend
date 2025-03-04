from rest_framework.serializers import ModelSerializer
from .models import Post, Interaction, Comment, User


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class InteractionSerializer(ModelSerializer):
    class Meta:
        model = Interaction
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")