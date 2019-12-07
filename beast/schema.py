from promise import Promise

import graphene
import graphql_jwt
import channels_graphql_ws

import users.schema
import clips.schema


class Query(
    users.schema.Query,
    clips.schema.Query,
):
    """
    Root Query composing queries per model.
    """
    pass


class Mutation(
    users.schema.Mutation,
    clips.schema.Mutation,
    graphene.ObjectType
):
    """
    Root Mutation composing mutations per model & JWT resolvers.
    """
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Subscription(
    clips.schema.Subscription,
):
    """
    Root Query composing queries per model.
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
introspect = schema.introspect()

# ----------------------------------------------------------- GRAPHQL WEBSOCKET CONSUMER


def demo_middleware(next_middleware, root, info, *args, **kwds):
    """Demo GraphQL middleware.
    For more information read:
    https://docs.graphene-python.org/en/latest/execution/middleware/#middleware
    """
    result = next_middleware(root, info, **args)
    if info.operation.operation == 'subscription' and isinstance(result, Promise):
        return result.get()
    return result


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    async def on_connect(self, payload):
        """Handle WebSocket connection event."""

        # Use auxiliary Channels function `get_user` to replace an
        # instance of `channels.auth.UserLazyObject` with a native
        # Django user object (user model instance or `AnonymousUser`)
        # It is not necessary, but it helps to keep resolver code
        # simpler. Cause in both HTTP/WebSocket requests they can use
        # `info.context.user`, but not a wrapper. For example objects of
        # type Graphene Django type `DjangoObjectType` does not accept
        # `channels.auth.UserLazyObject` instances.
        # https://github.com/datadvance/DjangoChannelsGraphqlWs/issues/23
        # self.scope["user"] = await channels.auth.get_user(self.scope)
        print("New client connected!")

    schema = schema
    # middleware = [demo_middleware]
