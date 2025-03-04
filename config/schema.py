import graphene
from graphene import Schema
from feed import queries
from feed.mutations import FeedMutation

class Query(queries.FeedQuery, graphene.ObjectType):
    """ This is the root query """
    pass


class Mutation(FeedMutation, graphene.ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)