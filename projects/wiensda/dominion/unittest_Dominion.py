from projects.wiensda.dominion import Dominion
from projects.wiensda.dominion import testUtility as tU


class TestActionCard:

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
        # data setup
        self.setUp()
        testPlayerSam = Dominion.Player("Sam")
        testCard = Dominion.Action_card("Woodcutter",1,1,1,1,1)
        testPlayerSam.hand.append(testCard)

        assert(testCard in testPlayerSam.hand)
        assert(testCard not in testPlayerSam.played)

        # call the use function
        testCard.use(testPlayerSam, self.trash)

        assert(testCard not in testPlayerSam.hand)
        assert(testCard in testPlayerSam.played)


    def test_augment(self):
        # data setup
        self.setUp()
        testPlayerSam = Dominion.Player("Sam")
        originalHandLen = len(testPlayerSam.hand)
        samPreAugActions = 1
        samPreAugBuys = 1
        samPreAugPurse = 0
        testPlayerSam.actions = samPreAugActions
        testPlayerSam.buys = samPreAugBuys
        testPlayerSam.purse = samPreAugPurse

        numActions = 2
        numBuys = 3
        numCoins = 4
        numCards = 2
        testCard = Dominion.Action_card("Woodcutter", 1, numActions,numCards,numBuys,numCoins)


        # Call the function
        testCard.augment(testPlayerSam)

        assert (testPlayerSam.actions == samPreAugActions + numActions)
        assert (testPlayerSam.buys == samPreAugBuys + numBuys)
        assert (testPlayerSam.purse == samPreAugPurse + numCoins)
        assert (len(testPlayerSam.hand) == (originalHandLen + numCards))

class TestPlayer:

    def test_action_balance(self):
        #Initialize Data
        testPlayerJenn = Dominion.Player("Jenn")
        originalStackSize = len(testPlayerJenn.stack())

        # run function and assert return
        assert (testPlayerJenn.action_balance() == 0)

        # Modify Jenn's card lists and assert
        testPlayerJenn.deck.append(Dominion.Woodcutter())     # Woodcutters have no actions
        assert (testPlayerJenn.action_balance() == 70*(-1)/(originalStackSize + 1))

        # Modify Jenn's card lists and assert again
        testPlayerJenn.deck.append(Dominion.Festival())             # Festival's have 2 actions
        testPlayerJenn.deck.append(Dominion.Festival())             # Festival's have 2 actions
        assert (testPlayerJenn.action_balance() == 70*(-1+1+1)/(originalStackSize + 3))


    def test_calcpoints(self):
        #Initialize Data
        testPlayerJenn = Dominion.Player("Jenn")

        # Test 1: 3 victory points in the beginning (three Estate cards)
        initPoints = testPlayerJenn.calcpoints()
        assert(initPoints == 3)

        # Test 2: Correct calculation from plain victory cards
        testPlayerJenn.deck.append(Dominion.Estate())       # Estate have 1 VP
        testPlayerJenn.deck.append(Dominion.Duchy())        # Duchy have 3 VP
        testPlayerJenn.deck.append(Dominion.Duchy())        # Duchy have 3 VP
        testPlayerJenn.deck.append(Dominion.Province())     # Province have 6 VP

        plainCardPoints = testPlayerJenn.calcpoints()
        assert(plainCardPoints == (3 + (1+3+3+6)))

        # Test 2: Correct calculation with addition of Gardens cards
        testPlayerJenn.deck.append(Dominion.Gardens())      # Gardens have 0 VP, but for each Gardens, the player..
        testPlayerJenn.deck.append(Dominion.Gardens())      # ... receives 1 VP for every 10 cards she has.

        fullCardPoints = testPlayerJenn.calcpoints()
        assert(fullCardPoints == (3 + (1+3+3+6) + (2*(len(testPlayerJenn.stack())//10))))



    def test_draw(self):
        #Initialize Data
        bill = Dominion.Player("Bill")
        originalHandLen = len(bill.hand)

        # Test 1a: Default Destination Hand
        bill.draw()
        assert(len(bill.hand) == originalHandLen + 1)

        # Test 1b: Custom Destination
        bill.hand.pop()     # remove previously added card
        metalBucket = []
        bill.draw(metalBucket)
        assert(len(bill.hand) == originalHandLen)
        assert(len(metalBucket) == 1)

        #Test 2: Deck starts empty -> proper shuffling of discard
        bill.discard = bill.deck
        bill.deck = []
        assert(len(bill.discard) > 0)
        assert(len(bill.deck) == 0)
        assert(len(bill.hand) == originalHandLen)
        bill.draw()
        assert(len(bill.discard) == 0)
        assert(len(bill.deck) > 0)
        assert(len(bill.hand) == (originalHandLen + 1))


        #Test 3: Empty draw and discard produces no card in hand
        bill.hand.pop()     # remove previously added card
        bill.discard = []
        bill.deck = []
        assert(len(bill.discard) == 0)
        assert(len(bill.deck) == 0)
        assert(len(bill.hand) == originalHandLen)
        bill.draw()
        assert(len(bill.discard) == 0)
        assert(len(bill.deck) == 0)
        assert(len(bill.hand) == originalHandLen)




    def test_cardsummary(self):
        #Initialize Data
        lisa = Dominion.Player("Lisa")

        # Test initial summary
        summary = lisa.cardsummary()
        assert(len(summary) == 3)
        assert('Copper' in summary)
        assert(summary['Copper'] == 7)
        assert('Estate' in summary)
        assert(summary['Estate'] == 3)
        assert('VICTORY POINTS' in summary)
        assert(summary['VICTORY POINTS'] == 3)

        # Test addition of two card types
        lisa.deck.append(Dominion.Woodcutter())
        lisa.deck.append(Dominion.Province())
        summary = lisa.cardsummary()

        assert (len(summary) == 5)
        assert ('Copper' in summary)
        assert (summary['Copper'] == 7)
        assert ('Estate' in summary)
        assert (summary['Estate'] == 3)
        assert ('Province' in summary)
        assert (summary['Province'] == 1)
        assert ('Woodcutter' in summary)
        assert (summary['Woodcutter'] == 1)
        assert ('VICTORY POINTS' in summary)
        assert (summary['VICTORY POINTS'] == 3 + 6)



class TestGameOver:

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



    def test_gameOver(self):
        # Initialize Data
        self.setUp()

        # Test initial setup
        assert (len(self.supply['Province']) > 0)
        gameOverResult = Dominion.gameover(self.supply)
        assert (gameOverResult is False)

        # Test when all provinces depleted
        self.supply['Province'] = []
        assert (len(self.supply['Province']) == 0)
        gameOverResult = Dominion.gameover(self.supply)
        assert (gameOverResult is True)

        # Test when Provinces exist, but 3 stacks depleted
        self.setUp()
        self.supply["Silver"] = []      # 1st stack depleted
        self.supply["Estate"] = []      # 2nd stack depleted
        assert (len(self.supply['Province']) > 0)
        gameOverResult = Dominion.gameover(self.supply)
        assert (gameOverResult is False)
        self.supply["Curse"] = []       # 3rd stack depleted
        gameOverResult = Dominion.gameover(self.supply)
        assert (gameOverResult is True)


