import graphene
import channels_graphql_ws

from graphql import GraphQLError
from graphene_django import DjangoObjectType

from django.db.models import Q
from users.schema import UserType
from .models import Clip, ClipVote


class ClipType(DjangoObjectType):
    """
    GraphQL Clip type based on the Clip model.
    Additionally, it contains clip_votes_count which returns the total amount of votes.
    """
    class Meta:
        model = Clip
    clip_votes = graphene.AbstractType()
    clip_votes_count = graphene.Int()

    def resolve_votes(self, info):
        """
        Resolves the related votes of the clip.
        :return: List of related votes.
        """
        return Clip.objects.get(pk=self.id).clip_votes

    def resolve_clip_votes_count(self, info):
        """
        Resolves the related votes of the clip.
        :return: List of clip votes count.
        """
        return Clip.objects.get(pk=self.id).clip_votes.count()


class ClipVoteType(DjangoObjectType):
    """
    GraphQL ClipVote type based on the Clip model.
    """
    class Meta:
        model = ClipVote


class Query(graphene.ObjectType):
    """
    GraphQL querry of clips and clip votes.
    The clips query accepts search filtering and pagination.
    """
    clips = graphene.List(
        ClipType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    votes = graphene.List(ClipVoteType)

    def resolve_clips(self, info, search=None, first=None, skip=None, **kwargs):
        """
        Resolves clips depending on the parameters.
        :param search: Filters by URL or description.
        :param first: Selects the first N number of links.
        :param skip: Skips the first N number of links
        :return: Clips List.
        """
        if search:
            qs_filter = (
                Q(url_icontains=search) |
                Q(description_icontains=search)
            )
            qs = Clip.objects.filter(qs_filter)
        else:
            qs = Clip.objects.all()
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

    def resolve_votes(self, info, **kwargs):
        """
        Resolves clip votes.
        :return: Clip votes list.
        TODO: Add filtering by user or votes if necessary.
        """
        return ClipVote.objects.all()


class CreateClip(graphene.Mutation):
    """
    GraphQL Mutation that creates clips.
    Receives a url, and description.
    """
    id = graphene.ID()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user
        # TODO: Make a helper to check if user is anonymous to reduce boilerplate.
        if user.is_anonymous:
            raise GraphQLError('Not logged in.')
        clip = Clip(
            url=url,
            description=description,
            posted_by=user,
        )
        clip.save()
        print("CreateClipVote: ClipsSubscription.on_new_clip?")
        ClipsSubscription.new_clip()
        return CreateClip(
            id=clip.id,
            url=clip.url,
            description=clip.description,
            posted_by=clip.posted_by
        )


class CreateClipVote(graphene.Mutation):
    """
    GraphQL Mutation that creates clip votes.
    Receives a clip to relate.
    """
    user = graphene.Field(UserType)
    clip = graphene.Field(ClipType)

    class Arguments:
        clip_id = graphene.ID()

    def mutate(self, info, clip_id):
        user = info.context.user
        # TODO: Make a helper to check if user is anonymous to reduce boilerplate.
        if user.is_anonymous:
            raise GraphQLError('Not logged in.')
        # Checking if the voted clip is valid:
        clip = Clip.objects.get(pk=clip_id)
        if not clip:
            raise GraphQLError('Invalid clip.')
        # Checking if the user already voted on this clip:
        clip_vote = ClipVote.objects.filter(user=user, clip=clip_id).first()
        if clip_vote:
            raise GraphQLError('User already voted for this clip.')
        # Creating clip:
        ClipVote.objects.create(
            user=user,
            clip=clip,
        )
        return CreateClipVote(user=user, clip=clip)


class Mutation(graphene.ObjectType):
    """
    GraphQL mutation of the clips & clip votes.
    """
    create_clip = CreateClip.Field()
    create_clip_vote = CreateClipVote.Field()


class ClipsSubscription(channels_graphql_ws.Subscription):
    """Simple GraphQL subscription."""

    # Subscription payload.
    event = graphene.String()

    # class Arguments:
    #     """That is how subscription arguments are defined."""
    #     arg1 = graphene.String()

    def subscribe(root, info):
        """Called when user subscribes."""
        print('ClipsSubscription: Subscribing to group42...')
        # Return the list of subscription group names.
        return ['group42']

    def publish(payload, info):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        event = payload["event"]
        print(f'ClipsSubscription: Hello? {event}')
        return ClipsSubscription(event=event)

    @classmethod
    def new_clip(cls):
        """Auxiliary function to send subscription notifications.
        It is generally a good idea to encapsulate broadcast invocation
        inside auxiliary class methods inside the subscription class.
        That allows to consider a structure of the `payload` as an
        implementation details.
        """
        cls.broadcast(
            # Subscription group to notify clients in.
            group='group42',
            # Dict delivered to the `publish` method.
            payload={
                'event': 'New clip was created',
            },
        )


class Subscription(graphene.ObjectType):
    """Root GraphQL subscription."""
    on_new_clip = ClipsSubscription.Field()
