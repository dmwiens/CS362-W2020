from projects.wiensda.dominion import Dominion
from projects.wiensda.dominion import testUtility as tU


class TestCard:

    def setUp(self):
        # data setup
        self.player_names = tU.getPlayerNames()
        self.nV = tU.getNumberOfVictoryCards(len(self.player_names))
        self.nC = tU.getNumberOfCurses(len(self.player_names))
        self.box = tU.getFullBox(self.nV)
        self.supply_order = tU.getSupplyOrder()
        self.supply = tU.getSupplyFromBox(self.box, len(self.player_names), self.nV, self.nC)
        self.players = tU.getPlayers(self.player_names)
        self.trash = []

    def test_react(self):
        assert False


class TestActionCard:

    def test_init(self):

        for i in range(-100, 100):

            # initialize the variables ((self,name,cost,actions,cards,buys,coins))
            name = "Woodcutter"
            cost = i
            actions = i
            cards = i
            buys = i
            coins = i

            # instantiate the Action Card object
            card = Dominion.Action_card(name, cost, actions, cards, buys, coins)

            # verify that the class variables have the expected values
            assert (card.name == name)
            assert (card.cost == cost)
            assert (card.actions == actions)
            assert (card.cards == cards)
            assert (card.buys == buys)
            assert (card.coins == coins)

    def test_use(self):
        assert False

    def test_augment(self):
        assert False


class TestPlayer:

    def test_action_balance(self):
        assert False

    def test_calcpoints(self):
        assert False

    def test_draw(self):
        assert False

    def test_cardsummary(self):
        assert False


def test_gameOver():
    assert False

