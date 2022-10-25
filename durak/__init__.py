from random import SystemRandom



random = SystemRandom()


class Player(object):

    def __init__(self, name=''):
        self.name = name
        self.cards = None


class Table(list):

    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.given_more = set()

    def give_more(self, cards):
        self.given_more.update(cards)

    def clear(self):
        self[:] = []
        self.given_more = set()


class GameController(object):

    MOVER = 'mover'
    RESPONDER = 'responder'
    PLAYER1 = 'player1'
    PLAYER2 = 'player2'

    class States:
        DEALING = 'dealing'
        MOVING = 'moving'
        RESPONDING = 'responding'
        GIVING_MORE = 'giving_more'

    def __init__(self, player1_name='', player2_name='', log_filename='',
                 overwrite_log=False):
        self._player1 = Player(player1_name)
        self._player2 = Player(player2_name)
        self._winner = None
        self._state = None

        self._log_filename = log_filename
        self._overwrite_log = overwrite_log
        self._logger = GameLogger()
        self._logger_enabled = True

    def start_new_game(self, ignore_winner=True):
        self._deck = list(DurakCard.all())
        random.shuffle(self._deck)
        self._trump = self._deck[-1]

        self._logger.reset()
        if self._logger_enabled:
            self._logger.log_before_game(
                self._player1.name,
                self._player2.name,
                self._deck,
                self._trump
            )

        self._player1.cards = CardSet(cards=self._deck[:6], trump=self._trump)
        self._player2.cards = CardSet(
            cards=self._deck[6:12], trump=self._trump
        )
        self._deck = self._deck[12:]

        if not ignore_winner and self._winner is not None:
            self._to_move = self._winner
        else:
            self._to_move = self._get_first_to_move_by_trump()

        self._winner = None
        self._discarded = []
        self._on_table = Table()

        self._state = self.States.MOVING
        self._no_response = False

        if self._logger_enabled:
            self._logger.log_before_move(
                set(self._player1.cards),
                set(self._player2.cards),
                self.to_move,
                self.deck_count,
            )

        return {
            'player1_cards': CardSet(self._player1.cards, trump=self._trump),
            'player2_cards': CardSet(self._player2.cards, trump=self._trump),
            'trump': DurakCard(self._trump),
        }