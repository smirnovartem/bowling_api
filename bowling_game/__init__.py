class BowlingGame:
    """
    """
    MAX_FRAME_COUNT = 10
    MAX_PINS = 10

    def __init__(self, num_players=1):
        assert num_players >= 1, 'Invalid number of players'

        self.boards = []
        self.num_players = num_players

        for i in range(0, self.num_players):
            self.boards.append(BowlingScoreBoard())

        self.current_player = 0

        self.started = False
        self.finished = False

    def reset(self):
        for b in self.boards:
            b.reset()
        self.current_player = 0
        self.started = False
        self.finished = False

    def get_dict(self):
        return {'current_player': self.current_player, 'finished': self.finished,
                'scores': list(map(lambda x: x.get_dict(), self.boards))}

    def start(self):
        assert not self.started, 'The game is already started'
        self.started = True

    def add_player(self):
        assert not self.started, 'The game is already started'
        self.num_players += 1
        self.boards.append(BowlingScoreBoard())

    def throw(self, count):
        assert self.started, 'The game is not started'
        assert not self.finished, 'The game is finished'
        assert 0 <= count <= self.MAX_PINS, 'Invalid number of pins knocked down '+str(count)

        frame_finished = self.boards[self.current_player].throw(count)

        if frame_finished:
            self.current_player += 1
            self.current_player = self.current_player % self.num_players

        self.finished = all(map(lambda x: x.finished, self.boards))

        return self.finished


class BowlingScoreBoard:
    """

    """
    def __init__(self):

        self.frames = []
        for i in range(0,BowlingGame.MAX_FRAME_COUNT):
            self.frames.append(BowlingFrame(i == (BowlingGame.MAX_FRAME_COUNT-1)))

        self.current_frame_num = 0
        self.score = 0
        self.finished = False

    def reset(self):
        for f in self.frames:
            f.reset()
        self.current_frame_num = 0
        self.score = 0
        self.finished = False

    def get_dict(self):
        frames_dicts = list(map(lambda x: x.get_dict(), self.frames))
        return {'score': self.score, 'current_frame_num': self.current_frame_num, \
                'frames': frames_dicts, 'finished': self.finished}

    def __str__(self):
        return 'Score: '+str(self.score)+'; Current: '+str(self.current_frame_num)+\
               '; Frames info('+str(list(map(str,self.frames)))+'); Finished: '+str(self.finished)

    def current_score(self):
        return self.score

    def throw(self, count):
        assert 0 <= count <= BowlingGame.MAX_PINS, 'Invalid number of pins knocked down '+str(count)
        assert self.current_frame_num < BowlingGame.MAX_FRAME_COUNT, 'The game is finished'
        assert not self.finished, 'The game is finished'

        frame_finished = self.get_current_frame().throw(count)
        self.score += count
        self.apply_bonus_score(count)

        if self.get_current_frame().finished:
            self.current_frame_num += 1
            if self.current_frame_num >= BowlingGame.MAX_FRAME_COUNT:
                self.finished = True

        return frame_finished

    def get_previous_frame(self, n=1):
        return None if self.current_frame_num <= n-1 else self.frames[self.current_frame_num - n]

    def get_current_frame(self):
        return None if self.current_frame_num >= BowlingGame.MAX_FRAME_COUNT else self.frames[self.current_frame_num]

    def apply_bonus_score(self, count):
        curr_frame = self.get_current_frame()
        prev_frame = self.get_previous_frame()
        
        if prev_frame:
            if curr_frame.throws_done == 1:

                if prev_frame.is_strike_or_spare():
                    prev_frame.score += count
                    self.score += count

                    if prev_frame.is_strike():
                        prev_frame = self.get_previous_frame(2)
                        if prev_frame and prev_frame.is_strike():
                            prev_frame.score += count
                            self.score += count

            elif curr_frame.throws_done == 2:
                if prev_frame.is_strike():
                    prev_frame.score += count
                    self.score += count


class BowlingFrame:
    """A frame in a bowling game
    Attributes:
        throw_scores    A list with number of pins knocked down in the respective try
        score           Total score of the frame
        last_frame      If the frame is the last one in the game
        throws_done     Number of throws done in this frame
        finished        If the frame is finished
    :type last_frame: bool"""
    def __init__(self, last_frame=False):
        self.throw_scores = [0, 0, 0]
        self.score = 0
        self.last_frame = last_frame
        self.throws_done = 0
        self.finished = False

    def reset(self):
        self.throw_scores = [0, 0, 0]
        self.score = 0
        self.throws_done = 0
        self.finished = False

    def get_dict(self):
        return {'score': self.score, 'throw_scores': self.throw_scores if self.last_frame else self.throw_scores[0:2],
                'strike': self.is_strike(), 'spare': self.is_spare(), 'throws_done': self.throws_done}

    def __str__(self):
        return 'Scores: {}; Total: {}; Throws done: {}; Finished: {}; Strike: {}; Spare: {}'\
            .format(self.throw_scores, self.score, self.throws_done,
                    self.finished, self.is_strike(), self.is_spare())

    def is_strike(self):
        return self.throw_scores[0] == BowlingGame.MAX_PINS

    def is_spare(self):
        return not self.is_strike() and self.throws_done > 1 and \
               (self.throw_scores[0] + self.throw_scores[1]) == BowlingGame.MAX_PINS

    def is_strike_or_spare(self):
        return self.is_strike() or self.is_spare()

    def is_last_frame(self):
        return self.last_frame


    def throw(self, count):
        """Throw a ball
        Parameters:
            count   Number of pins knocked down
        :type count: int"""
        count_error_msg = 'Invalid number of pins knocked down: {}'.format(count)
        assert 0 <= count <= BowlingGame.MAX_PINS, count_error_msg
        assert not self.finished, 'Unable to throw during finished frame'

        if self.throws_done == 1 and not self.is_strike():
            assert count <= BowlingGame.MAX_PINS - self.throw_scores[0], count_error_msg

        if self.last_frame and self.throws_done == 2 and \
                self.is_strike() and self.throw_scores[1] < BowlingGame.MAX_PINS:
            assert count <= BowlingGame.MAX_PINS - self.throw_scores[1], count_error_msg

        self.throw_scores[self.throws_done] = count
        self.score += count
        self.throws_done += 1

        finish_ordinary_frame = not self.last_frame and (self.is_strike() or self.throws_done == 2)

        finish_last_frame = self.last_frame and \
                            (not self.is_strike() and not self.is_spare() and self.throws_done == 2 or
                            self.throws_done == 3)

        if finish_ordinary_frame or finish_last_frame:
            self.finished = True

        return self.finished
