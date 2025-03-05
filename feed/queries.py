""" This module contains all the graphql queries """

import graphene
from graphql import GraphQLError
from .types import InteractionType, PostType, CommentType, UserType, InteractionTypeEnum
from .models import Interaction, Post, Comment, User
from .permissions import check_permission


class FeedQuery(graphene.ObjectType):
    all_interactions = graphene.List(InteractionType)
    interactions_by_type = graphene.List(InteractionType, interaction_type=InteractionTypeEnum())

    all_posts = graphene.List(PostType)
    posts_by_user = graphene.List(PostType, user_id=graphene.UUID(required=True))
    most_liked_posts = graphene.Field(PostType)

    all_comments = graphene.List(CommentType)
    comments_by_post = graphene.List(CommentType, post_id=graphene.UUID(required=True))

    all_users = graphene.List(UserType)
    user_by_email = graphene.Field(UserType, email=graphene.String(required=True))

    def resolve_all_interactions(root, info):
        # We can easily optimize query count in the resolve method
        print(info.context.user)
        return Interaction.objects.prefetch_related("post").all()
    
    def resolve_interactions_by_type(self, info, interaction_type=None):
        # Filter interactions by type if interaction_type is provided
        print(info.context.user)
        if interaction_type:
            print(interaction_type)
            return Interaction.objects.filter(interaction_type=interaction_type)
        else:
            return Interaction.objects.all()

    def resolve_all_posts(root, info):
        # We can easily optimize query count in the resolve method
        return Post.objects.prefetch_related("comments").all()

    def resolve_posts_by_user(root, info, user_id):
        user = info.context.user
        check_permission(user, Post)
        try:
            return Post.objects.filter(user=user_id)
        except Exception as exception:
            raise exception
    
    def resolve_most_liked_posts(self, info):
        pass

    def resolve_all_comments(root, info):
        # We can easily optimize query count in the resolve method
        return Comment.objects.prefetch_related("post").all()

    def resolve_comments_by_post(root, info, post_id):
        try:
            return Comment.objects.filter(post=post_id)
        except Exception as exception:
            raise exception

    def resolve_all_users(root, info):
        # We can easily optimize query count in the resolve method
        return User.objects.all()

    def resolve_user_by_email(root, info, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist as exception:
            raise GraphQLError("User does not exist")