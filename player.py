from __future__ import print_function
import requests
import json

class Player:
    VERSION = "Default Python calling player"

    def get_ranking(self, cards):
        response = requests.get('http://rainman.leanpoker.org/rank?cards=' + json.dumps(cards))
        print("Ranking: " + response.text)
        return json.loads(response.text)

    def get_table_ranking(self, game_state):
        cards = self.get_communal_cards(game_state)
        return self.get_ranking(cards)


    def get_cards_ranking(self, game_state):
        cards = self.get_my_hand(game_state)
        return self.get_ranking(cards)


    def log(self, game_state):
        me = game_state["players"][game_state["in_action"]]
        print("Game id: %s" % (game_state["game_id"]))
        print("Round: %d" % (game_state["round"]))
        print("  Buy in: %d" % (game_state["current_buy_in"]))
        print("  My bet: %d" % (me["bet"]))
        print("  Hands: ")
        for card in me["hole_cards"]:
            print("      %s:%s" % (card["suit"], card["rank"]))
        print("  Community: ")
        for card in game_state["community_cards"]:
            print("      %s:%s" % (card["suit"], card["rank"]))

    def betRequest(self, game_state):
        current_buy_in = game_state["current_buy_in"]
        me = game_state["players"][game_state["in_action"]]

        if self.have_one_pair(game_state):
            print("have one pair")
            print("current probability: ", self.get_probability_of_hand(1))


        my_bet = 0
        bet_needed = current_buy_in - me["bet"]

        if len(self.get_communal_cards(game_state)) == 0:
            if self.have_one_pair(game_state) and \
                    self.get_lowest_value_card(game_state) >= 10:
                my_bet = bet_needed + 3 * self.get_blind_bet(game_state)
                print('Raising pre-flop (high-pair)')
            elif self.have_one_pair(game_state):
                my_bet = bet_needed
            elif current_buy_in < me["stack"] * 0.4 and \
                    self.get_lowest_value_card(game_state) >= 10:
                my_bet = bet_needed
                print('Calling pre-flop (high-cards)')
            elif current_buy_in < me["stack"] * 0.2 and \
                    self.get_highest_value_card(game_state) == 14:
                my_bet = bet_needed
                print('Calling pre-flop (high-card)')
            elif current_buy_in < me["stack"] * 0.1:
                my_bet = bet_needed
                print('Calling pre-flop (cheap)')
            elif 3 * self.get_blind_bet(game_state) >= me["stack"]:
                my_bet = bet_needed
                print('Calling pre-flop (dying)')
            else:
                print("Folding pre-flop")
        else:
            hand_rank = self.get_cards_ranking(game_state)["rank"]
            table_rank = self.get_estimated_table_rank(game_state)
            rank = hand_rank - table_rank

            if rank > 3:
                my_bet = me["stack"]
                print("All-in rank delta 4")
            elif rank > 1:
                my_bet = int(me["stack"] / 2)
                print("Half-in rank delta 2")
            elif rank == 1:
                my_bet = 1
                if bet_needed == 0:
                    my_bet = game_state["minimum_raise"]
                    print("Raising post-flop")
                else:
                    print("Calling rank delta 1")
            elif rank == 0:
                my_bet = 0
                print("Folding post-flop")
            if my_bet < bet_needed and my_bet != 0:
                my_bet = bet_needed

        my_bet = min(me["stack"], my_bet)

        print("My bet: %d" % (my_bet))

        return my_bet

    def get_my_hand(self, game_state):
        return self.get_my_cards(game_state) + \
                self.get_communal_cards(game_state)

    def get_my_cards(self, game_state):
        me = game_state["players"][game_state["in_action"]]
        my_cards = me["hole_cards"]
        return my_cards

    def get_communal_cards(self, game_state):
        return game_state["community_cards"]

    def is_pair_among_cards(self, cards):
        ranks = [card["rank"] for card in cards]
        rank_counts = [ranks.count(rank) for rank in set(ranks)]
        if max(rank_counts) == 2:
            return True

    def have_one_pair(self, game_state):
        my_hand = self.get_my_hand(game_state)
        return self.is_pair_among_cards(my_hand)

    def has_table_one_pair(self, game_state):
        table_cards = self.get_communal_cards(game_state)
        return self.is_pair_among_cards(table_cards)

    def have_royal_flush(self, game_state):
        return False

    def get_probability_of_hand(self, rank_id):

        probabilities = {
            0: 1/(1+0.995), # No pair
            1: 1/(1+1.37),  # One pair
            2: 1/(1+20),    # Two pairs
            3: 1/(1+46.3),  # Three of a kind
            4: 1/(1+254),   # Straight
            5: 1/(1+508),   # Flush
            6: 1/(1+693),   # Full House
            7: 1/(1+4165),  # Four of a kind
            8: 1/(1+72192)  # Straight Flush
        }

        return probabilities[rank_id]

    def get_numeric_value_of_card(self, card):
        """Get value of card

        >>> Player().get_numeric_value_of_card({"rank": "4"})
        4
        >>> Player().get_numeric_value_of_card({"rank": "A"})
        14
        >>> Player().get_numeric_value_of_card({"rank": "Q"})
        12
        """
        try:
            return int(card["rank"])
        except ValueError as e:
            values = {
                "J": 11,
                "Q": 12,
                "K": 13,
                "A": 14
            }
            return values[card["rank"]]

    def get_lowest_value_card(self, game_state):
        values = [self.get_numeric_value_of_card(card)
                for card in self.get_my_cards(game_state)]
        return min(values)

    def get_highest_value_card(self, game_state):
        values = [self.get_numeric_value_of_card(card)
                for card in self.get_my_cards(game_state)]
        return max(values)

    def get_blind_bet(self, game_state):
        return 2 * game_state["small_blind"]

    def get_estimated_table_rank(self, game_state):
        if self.has_table_one_pair(game_state):
            return 1
        if len(self.get_communal_cards(game_state)) == 5:
            table_ranking = self.get_table_ranking(game_state)
        return 0

    def showdown(self, game_state):
        pass



if __name__ == "__main__":
    import doctest
    doctest.testmod()
