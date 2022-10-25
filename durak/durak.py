import unittest


from durak import Table, GameController
from durak.cards import DurakCard, CardSet


class DurakTest(unittest.TestCase):

    def setUp(self):
        table = Table()
        self.assertTrue(isinstance(table, list))
        self.assertEqual(table.given_more, set())

    def test_give_more_updates_given_more(self):
        table = Table()
        self.assertEqual(table.given_more, set())

        cards = {DurakCard('AH'), DurakCard('6H')}
        table.give_more(cards)

        self.assertEqual(table.given_more, cards)

    def test_clear(self):
        table = Table()
        cards = {DurakCard('AH'), DurakCard('6H')}
        given_more_cards = {DurakCard('AS'), DurakCard('6S')}

        table.extend(cards)
        self.assertItemsEqual(table, cards)
        table.give_more(given_more_cards)
        self.assertEqual(table.given_more, given_more_cards)

        table.clear()

        self.assertEqual(table, [])
        self.assertEqual(table.given_more, set())


class GameControllerTest(unittest.TestCase):

    def test_state(self):
        controller = GameController()
        states = {
            controller.States.MOVING,
            controller.States.RESPONDING,
            controller.States.GIVING_MORE,
            controller.States.DEALING
        }
        for state in states:
            controller._state = state
            self.assertEqual(controller.state, state)

    def test_is_player_first_to_move(self):
        controller = GameController()
        controller._to_move = controller._player1
        self.assertTrue(controller.is_player1_to_move())

        controller._to_move = controller._player2
        self.assertFalse(controller.is_player1_to_move())

    def test_get_enemy_of(self):
        controller = GameController()
        self.assertEqual(
            controller._get_enemy_of(controller._player1), controller._player2
        )
        self.assertEqual(
            controller._get_enemy_of(controller._player2), controller._player1
        )

    def test_to_respond(self):
        controller = GameController()
        controller._to_move = controller._player1
        self.assertEqual(controller._to_respond, controller._player2)

        controller._to_move = controller._player2
        self.assertEqual(controller._to_respond, controller._player1)


    def test_winner_property(self):
        controller = GameController()
        given_list = [controller._player1, controller._player2, None]
        expected_list = [controller.PLAYER1, controller.PLAYER2, None]
        for given, expected in zip(given_list, expected_list):
            controller._winner = given
            self.assertEqual(controller.winner, expected)

