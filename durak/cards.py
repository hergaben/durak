

DurakCardTuple = namedtuple('DurakCardTuple', ['numeric_rank', 'suit'])

class DurakCard(DurakCardTuple):

    RANKS = ('6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
    SUITS = ('C', 'D', 'H', 'S')

class CardSet(set):
