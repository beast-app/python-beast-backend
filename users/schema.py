from django.contrib.auth import get_user_model

from graphql import GraphQLError
import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    """
    GraphQL User type based on the User model.
    """
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    """
    User queries.
    """
    current_user = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_current_user(self, info):
        """
        Query that returns the authenticated user.
        :param info: Contains the context of the authenticated user.
        :return: Error or user.
        """
        user = info.context.user
        # TODO: Make a helper to check if user is anonymous to reduce boilerplate.
        if user.is_anonymous:
            raise GraphQLError('Not logged in.')
        return user

    def resolve_users(self):
        """
        Query that returns a list of all users.
        TODO: Add pagination & filtering.
        :return: List of all users.
        """
        return get_user_model().objects.all()


class CreateUser(graphene.Mutation):
    """
    GraphQL Mutation that creates users.
    Receives a username, password, and email.
    TODO: Add 3rd party API authentication (e.g. Discord).
    """
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        """
        Creates the user with the given parameters.
        :param info:
        :param username: Username string.
        :param password: Username password.
        :param email: Username email.
        :return: CreateUser call.
        """
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    """
    GraphQL mutation of the users.
    """
    create_user = CreateUser.Field()
