from bowling_app import bowling_api
from bowling_app.bowling_helpers_class import NewGame, GameAction

bowling_api.add_resource(NewGame, '/games')
bowling_api.add_resource(GameAction, '/games/<int:game_id>')
