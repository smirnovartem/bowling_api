import random
import json
from bowling_game import BowlingGame


def knock_down_pins(max_pins):
    return random.randint(0, max_pins)


def random_frame_throws(last_frame=False, max_pins=10):
    """
    :type last_frame: bool
    :type max_pins: int
    """
    throws = []
    throws.append(knock_down_pins(max_pins))
    if throws[0] < max_pins:
        throws.append(knock_down_pins(max_pins - throws[0]))
        if last_frame and (throws[0] + throws[1]) == 10:
            throws.append(knock_down_pins(max_pins))
    elif last_frame:
        throws.append(knock_down_pins(max_pins))
        if throws[1] < max_pins:
            throws.append(knock_down_pins(max_pins - throws[1]))
        else:
            throws.append(knock_down_pins(max_pins))

    return throws


# Emulate a predefined game and make sure that scores match
game = BowlingGame()
game.start()
throws = [10, 7, 3, 7, 2, 9, 1, 10, 10, 10, 2, 3, 6, 4, 7, 3, 3]

for cnt in throws:
    game.throw(cnt)

print(json.dumps(game.get_dict()))
assert game.get_dict()['scores'][0]['score'] == 168


# Emulate perfect game and assert that final score is 300
game = BowlingGame()
game.start()

for i in range(0,12):
    game.throw(10)

print(json.dumps(game.get_dict()))
assert game.get_dict()['scores'][0]['score'] == 300


# Play random game
game = BowlingGame(3)
game.add_player()

game.start()

for i in range(0, BowlingGame.MAX_FRAME_COUNT):
    for j in range(0, game.num_players):
        throws = random_frame_throws(i == BowlingGame.MAX_FRAME_COUNT - 1, BowlingGame.MAX_PINS)
        for t in throws:
            game.throw(t)

print(json.dumps(game.get_dict()))
print(game.current_player)
