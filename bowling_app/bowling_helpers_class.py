from bowling_app import games
from bowling_game import BowlingGame
from bowling_app.bowling_helpers_function import abort_if_game_not_found, game_actions
from flask_restful import Resource, abort, reqparse
from werkzeug.exceptions import BadRequest


class NewGame(Resource):
    def post(self):
        keys = list(games.keys())
        game_id = 0 if len(keys) == 0 else max(keys) + 1
        games[game_id] = BowlingGame()
        return {'game_id': game_id}, 201


class GameAction(Resource):
    def get(self, game_id):
        abort_if_game_not_found(game_id)
        return {'game_id': game_id, 'game': games[game_id].get_dict()}, 200

    def put(self, game_id):
        abort_if_game_not_found(game_id)

        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str)
        parser.add_argument('num_pins', type=int)
        try:
            args = parser.parse_args()
            if args['action'] in game_actions:
                return game_actions[args['action']](game_id, args)
            else:
                abort(400, message='No action chosen' if args['action'] is None
                                    else 'Unknown action: {}'.format(args['action']))
        except BadRequest as e:
            abort(400, message=str(e))
