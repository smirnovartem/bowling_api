from bowling_app import games
from flask_restful import abort


def abort_if_game_not_found(game_id):
    if game_id not in games:
        abort(404, message='Game {} does not exist'.format(game_id))


def throw_ball(game_id, args):
    if args['num_pins'] is None:
        abort(400, message='Number of pins is not specified')
    else:
        num_pins = args['num_pins']
        result = {'game_id': game_id, 'num_pins': num_pins,
                  'started': games[game_id].started}
        try:
            games[game_id].throw(num_pins)
            result['finished'] = games[game_id].finished
            result['current_player'] = games[game_id].current_player
            return result, 200
        except AssertionError as e:
            result['message'] = str(e)
            result['finished'] = games[game_id].finished
            return result, 400


def add_player(game_id, args):
    try:
        games[game_id].add_player()
        return {'game_id': game_id, 'num_players': games[game_id].num_players}, 200
    except AssertionError as e:
        return {'game_id': game_id, 'message': str(e),
                'num_players': games[game_id].num_players,
                'started': games[game_id].started}, 400


def start_game(game_id, args):
    try:
        games[game_id].start()
        return {'game_id': game_id, 'started': games[game_id].started}, 200
    except AssertionError as e:
        return {'game_id': game_id, 'message': str(e),
                'started': games[game_id].started}, 400


game_actions = {'throw': throw_ball, 'add_player': add_player, 'start': start_game}

