import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from links.models import Link, Vote, Comment
from graphql import GraphQLError
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField

# **1.1 Definición de Tipos (DjangoObjectType)**

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

    user = graphene.Field(UserType)
    created_at = graphene.DateTime()
    

    def resolve_created_at(self, info):
        return self.created_at
    
    
class LinkType(DjangoObjectType):

    class Meta:
        model = Link

    comments = graphene.List(CommentType)

    def resolve_comments(self, info,**kwargs):
        return self.comments.all()



class CountableConnectionBase(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = ('user', 'link')
        filter_fields = ('user', 'link')
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnectionBase





# **1.2 Mutaciones para Crear Link, Vote y Comment**

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    nombre = graphene.String()
    creador = graphene.String()
    plataforma = graphene.String()
    genero = graphene.String()
    fecha_lanzamiento = graphene.Int()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        nombre = graphene.String()
        creador = graphene.String()
        plataforma = graphene.String()
        genero = graphene.String()
        fecha_lanzamiento = graphene.Int()

    def mutate(self, info, url, nombre, creador, plataforma, genero, fecha_lanzamiento):
        user = info.context.user or None

        link = Link(
            url=url,
            nombre=nombre,
            creador=creador,
            plataforma=plataforma,
            genero=genero,
            fecha_lanzamiento=fecha_lanzamiento,
            posted_by=user,
        )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            nombre=link.nombre,
            creador=link.creador,
            plataforma=link.plataforma,
            genero=link.genero,
            fecha_lanzamiento=link.fecha_lanzamiento,
            posted_by=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        link_id = graphene.Int(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, link_id, text):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to comment!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise GraphQLError('Invalid Link!')

        comment = Comment.objects.create(
            user=user,
            link=link,
            text=text
        )

        return CreateComment(comment=comment)


# **2. Query y Resolvers**

class Query(graphene.ObjectType):
    links = graphene.List(
        LinkType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = DjangoFilterConnectionField(VoteType)
    comments = graphene.List(CommentType, link_id=graphene.Int())

    def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Link.objects.all()

        if search:
            filter = (
                Q(url__icontains=search) |
                Q(nombre__icontains=search) |
                Q(creador__icontains=search) |
                Q(plataforma__icontains=search) |
                Q(genero__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]
    
        return qs

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

    def resolve_comments(self, info, link_id, **kwargs):
        return Comment.objects.filter(link_id=link_id)


# **3. Mutation**

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
    create_comment = CreateComment.Field()
