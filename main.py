from flask import Flask
from graphene import ObjectType, String, Schema, Field, List, Mutation
from flask_graphql import GraphQLView
import os
from collections import namedtuple


PlayerValueObject = namedtuple('Player', ['id', 'name'])


class Player(ObjectType):
    id = String()
    name = String()


class Query(ObjectType):
    player = Field(Player, id=String(required=True))
    players = List(Player)

    def resolve_player(self, info, id):
        return PlayerValueObject(id=id, name='test')

    def resolve_players(self, info):
        players_list = []
        players_list.append(PlayerValueObject(id='1', name='test'))
        players_list.append(PlayerValueObject(id='2', name='test2'))
        return players_list


class InsertPlayer(Mutation):
    id = String()
    name = String()

    # Getting Parameter
    class Arguments:
        name = String(required=True)

    player = Field(lambda: Player)

    # Insert into Data
    def mutate(root, info, name):
        player = PlayerValueObject(id='3', name='testddd')
        return InsertPlayer(player)


class Mutation(ObjectType):
    insert_player = InsertPlayer.Field()


view_func_cli = GraphQLView.as_view("graphql_cli", schema=Schema(query=Query, mutation=Mutation))
view_func_gui = GraphQLView.as_view("graphql_gui", schema=Schema(query=Query, mutation=Mutation), graphiql=True)


app = Flask(__name__)
app.add_url_rule('/', view_func=view_func_cli)
app.add_url_rule('/graphql', view_func=view_func_gui) # GraphiQLを表示

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # app.run(host="0.0.0.0", port=port, debug=True)
