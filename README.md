# Bowling API
This project implements a simple REST API to control bowling games usin [Flask](http://flask.pocoo.org/docs/1.0/) and [Flask-RESTFul](https://flask-restful.readthedocs.io/en/latest/index.html).

## Project contents

* `bowling_game` package implements bowling logic
* `tests/bowling_game_tests.py` contains some unit test for `BowlingGame` class from `bowling_game` package
* `bowling_app` package implements API to create and control bowling games
* `bowling_run.py` is used to run the API server

## Installation and execution
Install the requirements for the project:

```pip install -r requirements.txt```


To run the server execute the following command:

```python bowling_run.py```

After that API is available on `localhost:5000` by default

## Demo
A simple demo that demonstrates an API usage is available on `localhost:5000/demo` (after the server is run) or in [`bowling_app/demo/demo.html`](/bowling_app/demo/demo.html)
It is a simple UI that allows to start bowling games, add players and to specify a number of pins that was knocked down.
The UI in turn requests the game data from the server every two seconds.


## API description
### Create a new game
`POST` request to `/games`.

Successful response is a JSON object: `{"game_id": <game_id>}`.

Example:
```
$ curl http://localhost:5000/games -X POST -v
> POST /games HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.55.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 15
< Access-Control-Allow-Origin: *
< Server: Werkzeug/0.14.1 Python/3.6.2
< Date: Tue, 28 Aug 2018 22:11:07 GMT
<
{"game_id": 0}
* Closing connection 0
```

### Get game standings
`GET` request to `/games/<game_id>`.

A successful response contains the data about the game: total scores and scores in each frame.

Example:
```
$ curl http://localhost:5000/games/0 -v
> GET /games/0 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.55.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 1248
< Access-Control-Allow-Origin: *
< Server: Werkzeug/0.14.1 Python/3.6.2
< Date: Tue, 28 Aug 2018 22:22:12 GMT
<
{"game_id": 0, "game": {"current_player": 0, "finished": false, "scores": [{"score": 0
, "current_frame_num": 0, "frames": [{"score": 0, "throw_scores": [0, 0], "strike": fa
lse, "spare": false, "throws_done": 0, "last_frame": false}, {"score": 0, "throw_score
s": [0, 0], "strike": false, "spare": false, "throws_done": 0, "last_frame": false}, {
"score": 0, "throw_scores": [0, 0], "strike": false, "spare": false, "throws_done": 0,
 "last_frame": false}, {"score": 0, "throw_scores": [0, 0], "strike": false, "spare":
false, "throws_done": 0, "last_frame": false}, {"score": 0, "throw_scores": [0, 0], "s
trike": false, "spare": false, "throws_done": 0, "last_frame": false}, {"score": 0, "t
hrow_scores": [0, 0], "strike": false, "spare": false, "throws_done": 0, "last_frame":
 false}, {"score": 0, "throw_scores": [0, 0], "strike": false, "spare": false, "throws
_done": 0, "last_frame": false}, {"score": 0, "throw_scores": [0, 0], "strike": false,
 "spare": false, "throws_done": 0, "last_frame": false}, {"score": 0, "throw_scores":
[0, 0], "strike": false, "spare": false, "throws_done": 0, "last_frame": false}, {"sco
re": 0, "throw_scores": [0, 0, 0], "strike": false, "spare": false, "throws_done": 0,
"last_frame": true}], "finished": false}]}}
* Closing connection 0
```

### Add a player to the game
`PUT` request to `/games/<game_id>` with request data `action=add_player`.

Example:
```
$ curl http://localhost:5000/games/0 -d "action=add_player" -X PUT
{"game_id": 0, "num_players": 2}
```

### Start the game
`PUT` request to `/games/<game_id>` with request data `action=start`.

Starts the existing game, meaning that no more players can be added and a ball can be thrown.

Example:
```
$ curl http://localhost:5000/games/0 -d "action=start" -X PUT
{"game_id": 0, "started": true}
```

### Send the number of knocked down pins
`PUT` request to `/games/<game_id>` with request data `action=throw&num_pins=<n>`.

Lets the application know that <n> pins were knocked down. <n> is an integer from 0 to 10, and also must no more than a maximum number of pins left after the first throw.

Example:
```
$ curl http://localhost:5000/games/0 -d "action=throw&num_pins=7" -X PUT
{"game_id": 0, "num_pins": 7, "started": true, "finished": false, "current_player": 0}
```
