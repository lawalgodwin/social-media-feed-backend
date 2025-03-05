from django.db.models import Model
from django.shortcuts import get_object_or_404
from graphql import GraphQLError

def check_permission(user, model: Model):
    if not user.is_authenticated:
        raise GraphQLError("You must sign in before interacting with a post")
    if model.user != user and not user.is_staff:
        raise GraphQLError("Permission denied")

def check_is_owner(user, model: Model):
    if model.user != user and not user.is_staff:
        raise GraphQLError("Permission denied")
    return True

def check_is_logged_in(user, model: Model):
    if not user.is_authenticated:
        raise GraphQLError("You must sign in before interacting with a post")
    return True

def is_staff(user):
    return user.is_staff