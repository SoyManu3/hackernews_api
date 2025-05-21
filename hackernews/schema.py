import graphene

import links.schema
import users.schema
import graphql_jwt



# ...code

# Add the users.schema.Query
class Query(users.schema.Query, links.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)


class Mutation(users.schema.Mutation, links.schema.Mutation, graphene.ObjectType,):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
