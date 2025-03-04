""" This module contains all the grapgql mutations """

import graphene

from graphene_django.rest_framework.mutation import SerializerMutation
from graphql import GraphQLError
from .serializers import CommentSerializer, PostSerializer, UserSerializer
from .models import Interaction, User, Post, Comment
from .types import InteractionTypeEnum, InteractionType
from django.db.models import Model


def deleteModel(model: Model, id: graphene.UUID):
    """ Delete the specifies model"""
    try:
        post = model.objects.get(id=id)
        post.delete()
    except Post.DoesNotExist as error:
        raise GraphQLError("Post doest not exist")


class PostMutation(SerializerMutation):
    class Meta:
        serializer_class = PostSerializer

    @classmethod
    def perform_mutate(cls, serialiser, info):
        print(info.context.user)
        return super().perform_mutate(serializer=serialiser, info=info)


class CommentMutation(SerializerMutation):
    class Meta:
        serializer_class = CommentSerializer

    @classmethod
    def perform_mutate(cls, serialiser, info):
        print(info.context.user)
        return super().perform_mutate(serializer=serialiser, info=info)


class UserMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSerializer

    @classmethod
    def perform_mutate(cls, serialiser, info):
        print(info.context.user)
        return super().perform_mutate(serializer=serialiser, info=info)
    

class InteractionMutation(graphene.Mutation):
    """ SerializerMutation does not support a model with choiceField out of the box
        Hence, this is handled manually
    """
    class Arguments:
        user_id = graphene.UUID(required=True)  # The user who interacted
        post_id = graphene.UUID(required=True)  # The post being interacted with
        interaction_type = InteractionTypeEnum() # Either 'like' or 'share'

    interaction = graphene.Field(InteractionType)

    @classmethod
    def mutate(cls, root, info, user_id, post_id, interaction_type):
        try:
            print(info.context.user)
            # Fetch the user and post
            user = User.objects.get(id=user_id)
            post = Post.objects.get(id=post_id)

        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {user_id} does not exist.")
        except Post.DoesNotExist:
            raise GraphQLError(f"Post with ID {post_id} does not exist.")

        # Check if the interaction already exists
        existing_interaction = Interaction.objects.filter(user=user, post=post).first()

        if existing_interaction:
            # Update the existing interaction
            existing_interaction.interaction_type = interaction_type
            existing_interaction.save()
            return InteractionMutation(interaction=existing_interaction)

        else:
            # Create a new interaction
            new_interaction = Interaction(
                user=user,
                post=post,
                interaction_type=interaction_type
            )
            new_interaction.save()
            return InteractionMutation(interaction=new_interaction)


class PostDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True) # The id of the model to delete
    
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        print(info.context.user)
        deleteModel(Post, id=id)


class CommentDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True) # The id of the model to delete
    
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        print(info.context.user)
        deleteModel(Comment, id=id)

class UserDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True) # The id of the model to delete
    
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        print(info.context.user)
        deleteModel(User, id=id)


class InteractionDeleteMutation(graphene.Mutation):
    """ This mutation Deletes a model:
    """
    class Arguments:
        id = graphene.UUID(required=True) # The id of the model to delete
    
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        print(info.context.user)
        deleteModel(Interaction, id=id)

class FeedMutation(graphene.ObjectType):
    create_or_update_post = PostMutation.Field()
    delete_post = PostDeleteMutation.Field()
    create_or_update_comment = CommentMutation.Field()
    delete_comment = CommentDeleteMutation.Field()
    create_or_update_interaction = InteractionMutation.Field()
    # delete_interaction = InteractionDeleteMutation.Field()
    create_or_update_user = UserMutation.Field()
    delete_user = UserDeleteMutation.Field()
