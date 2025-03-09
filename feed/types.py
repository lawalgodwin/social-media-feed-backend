import graphene
from graphene_django import DjangoObjectType

from feed.models import User, Post, Comment, Interaction


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"


class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction
        fields = "__all__"


class InteractionTypeEnum(graphene.Enum):
    LIKE = "like"
    SHARE = "share"
