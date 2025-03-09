""" This module contains all the grapgql mutations """

import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from graphql import GraphQLError
from .serializers import CommentSerializer, PostSerializer
from .models import Interaction, User, Post, Comment
from .types import CommentType, InteractionTypeEnum, InteractionType, PostType, UserType
from django.db.models import Model
import graphql_jwt
from .permissions import check_is_logged_in, check_permission, is_staff


def deleteModel(model: Model, id: graphene.UUID):
    """ Delete the specifies model"""
    try:
        instance = model.objects.get(id=id)
        instance.delete()
    except Post.DoesNotExist:
        raise GraphQLError("model doest not exist")


class PostMutation(SerializerMutation):
    class Meta:
        serializer_class = PostSerializer
        model_operations = ['update']
        lookup_field = 'id'

    @classmethod
    def perform_mutate(cls, serialiser, info):
        user = info.context.user
        check_permission(user, Post)
        return super().perform_mutate(serializer=serialiser, info=info)


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)

    def mutate(self, info, content):
        user = info.context.user
        try:
            check_is_logged_in(user=user)
            post = Post(content=content, user=user)
            post.save()
            return CreatePost(post=post)
        except Exception as error:
            return CreatePost(post=error)


class CommentMutation(SerializerMutation):
    comment = graphene.Field(CommentType)

    class Meta:
        serializer_class = CommentSerializer

    @classmethod
    def perform_mutate(cls, serialiser, info, **kwargs):
        user = info.context.user
        try:
            check_permission(user=user, model=Comment)
            return super().perform_mutate(serialiser, info, **kwargs)
        except GraphQLError:
            return cls(comment=None)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.UUID(required=True)
        parent_comment_id = graphene.UUID()

    def mutate(self, info, content, post_id, parent_comment_id=None):
        user = info.context.user
        try:
            # Find the associated post
            post = Post.objects.get(id=post_id)
            #  Find the parent comment
            parent_comment = None
            comment = None
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                comment = Comment(content=content, user=user, post=post, parent_comment=parent_comment)
                comment.save()
            else:
                comment = Comment(content=content, user=user, post=post)
                print("executed else block")
                comment.save()
            print(comment.parent_comment)
            return CreateComment(comment=comment)
        except Exception:
            return CreateComment(comment=None)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, password, first_name, last_name, email):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class InteractionMutation(graphene.Mutation):
    """ SerializerMutation does not support a model with choiceField out of the box
        Hence, this is handled manually
    """
    class Arguments:
        # user_id = graphene.UUID(required=True)  # The user who interacted
        post_id = graphene.UUID(required=True)  # The post being interacted with
        interaction_type = InteractionTypeEnum()  # Either 'like' or 'share'

    interaction = graphene.Field(InteractionType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        check_is_logged_in(user)
        try:
            # Fetch the user and post
            user = User.objects.get(id=user.id)
            post = Post.objects.get(id=kwargs.get("post_id"))

        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {kwargs.get("user_id")} does not exist.")
        except Post.DoesNotExist:
            raise GraphQLError(f"Post with ID {kwargs.get("post_id")} does not exist.")

        # Create a new interaction
        try:
            new_interaction = Interaction(
                user=user,
                post=post,
                interaction_type=kwargs.get("interaction_type")
            )
            new_interaction.save()
            print(new_interaction.interaction_type)
            if new_interaction.interaction_type == InteractionTypeEnum.LIKE:
                post.likes_count += 1
            else:
                post.shares_count += 1
            post.save()
            return InteractionMutation(interaction=new_interaction)
        except Exception as error:
            return InteractionMutation(interaction=error)


class PostDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """

    class Arguments:
        id = graphene.UUID(required=True)  # The id of the model to delete

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        user = info.context.user
        try:
            check_permission(user, Post)
            deleteModel(Post, id=id)
            return cls(success=True)
        except GraphQLError:
            return cls(success=False)


class CommentDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True)  # The id of the model to delete

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        user = info.context.user
        try:
            check_permission(user=user, model=Comment)
            deleteModel(Comment, id=id)
            return cls(success=True)
        except GraphQLError:
            return cls(success=False)


class UserDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True)  # The id of the model to delete

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if is_staff(info.context.user):
            try:
                deleteModel(User, id=id)
                return cls(success=True)
            except GraphQLError:
                return cls(success=False)


class InteractionDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True)  # The id of the model to delete

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        print(info.context.user)
        try:
            deleteModel(Interaction, id=id)
            return cls(success=True)
        except GraphQLError:
            return cls(success=False)


class FeedMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = PostMutation.Field()
    delete_post = PostDeleteMutation.Field()
    update_comment = CommentMutation.Field()
    create_comment = CreateComment.Field()
    delete_comment = CommentDeleteMutation.Field()
    create_or_update_interaction = InteractionMutation.Field()
    # delete_interaction = InteractionDeleteMutation.Field()
    create_user = CreateUser.Field()
    delete_user = UserDeleteMutation.Field()


class AuthMutation(graphene.ObjectType):
    sign_in = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
