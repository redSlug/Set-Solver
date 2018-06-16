
import argparse, random
from itertools import combinations, product


STANDARD_FEATURES = [['red', 'green', 'purple'], ['1', '2', '3'], ['diamond', 'squiggle', 'oval'], ['solid', 'stripe', 'outline']]
DEFAULT_CARD_COUNT = 12

class Game:
    def __init__(self, card_count=DEFAULT_CARD_COUNT, cards_input=None):
        """
        Initializes game instance. Generates random card_count random cards
        if cards_input is not provided. Otherwise, generates cards from
        cards_input.

        :param cards_count: amount of cards from which to search for sets
        :param cards: list of cards, each card is represented by a tuple
        """
        self.features = self.get_features(cards_input) if cards_input else STANDARD_FEATURES
        self.dimensions = len(self.features)
        self.cards = self.generate_cards(cards_input) if cards_input else self.generate_random_cards(card_count)

    @staticmethod
    def get_features(cards_input):
        """
        Generates features using cards input
        :param cards_input:
        :return:
        """
        a = [c.split() for c in list(c.strip() for c in cards_input.split(','))]

        if sum(1 for v in a if len(v) is len(a[0])) is not len(a):
            raise Exception('Invalid input, cards differ in dimension count')

        features = [list() for _ in range(len(a[0]))]
        for row in a:
            for i, item in enumerate(row):
                if item not in features[i]:
                    features[i].append(item)
        return features

    def generate_cards(self, cards_input):
        """
        Generates cards from valid user input.

        :param cards_input: Comma delimited string representing cards visible in a set game.
            for example, 'purple 2 diamond solid, red 2 squiggle stripe'
        :return: a list of tuples of integers corresponding to features and
            representing cards in a set game
        """
        return [self.generate_card(card.strip()) for card in cards_input.split(',')]

    def generate_card(self, card_input):
        """
        Generates a card from valid user input.

        :param card_input: Space delimited string representing a visible card in a set game.
            for example, 'purple 2 diamond solid'
        :return: tuple of integers representing the card, corresponding to features indices
        """
        return tuple(self.features[i].index(feature) for i, feature in enumerate(card_input.split()))

    def generate_random_cards(self, cards_count):
        """
        Generates random cards that would appear face up on the table in a game
        of Set. First generates the deck, shuffles the deck, then picks
        cards_count cards from the deck

        :param cards_count: amount of cards to be generated
        :return: list of cards
        """
        values_per_dimension = len(self.features[0])
        deck = list(product(list(range(values_per_dimension)), repeat=self.dimensions))
        random.shuffle(deck)
        return [deck.pop() for _ in range(cards_count)]

    def find_sets(self, cards_per_set):
        """
        Finds all the sets in cards. Each set is represented by a tuple of
        integers representing the index of each card in that set.

        :param cards_per_set:
        :return: sets
        """
        def is_set(cards):
            """
            A set consists of n cards in which each feature or value
            associated with a dimension is EITHER the same on each card OR is
            different on each card.

            :param cards: collection of n cards
            :return: whether the cards are considered a set
            """
            for d in range(self.dimensions):
                dimension_values = [c[d] for c in cards]

                if sum(1 for v in dimension_values if v is cards[0][d]) == len(cards):
                    # all values in dimension are same
                    continue

                if len(dimension_values) is len(set(dimension_values)):
                    # all values in dimension are different
                    continue

                return False
            return True

        if len(set(self.cards)) is not len(self.cards):
            raise Exception('Invalid input, cards differ in dimension count')

        sets = [c for c in combinations(self.cards, cards_per_set) if is_set(c)]
        sets_by_index = list()
        for s in sets:
            sets_by_index.append([self.cards.index(c) for c in s])
        return sets_by_index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find indices of the sets in the game of Set.')
    parser.add_argument('-c', '--cards', type=str, help='Comma and space delimited string, for example "red 2 squiggle outline cold, red 2 diamond stripe warm, red 2 oval solid hot" or "0 0, 1 1"')
    parser.add_argument('-a', '--amount', type=int, help='Amount of cards in a set; default is 3')

    args = parser.parse_args()
    g = Game(cards_input=args.cards if args.cards else None)
    print("cards=", g.cards)
    sets = g.find_sets(cards_per_set=args.amount if args.amount else 3)
    print("sets_by_index=", sets)
