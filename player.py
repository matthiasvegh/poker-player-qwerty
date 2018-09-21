from __future__ import print_function
import requests
import json

class Player:
    VERSION = "Default Python calling player"

    def get_cards_ranking(self, game_state):
        cards = self.get_my_hand(game_state)
        cards += self.get_communal_cards(game_state)
        response = requests.get('http://rainman.leanpoker.org/rank?cards=' + json.dumps(cards))
        print("Ranking: " + response.text)
        return json.loads(response.text)


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

        self.log(game_state)
        if self.have_one_pair(game_state):
            print("have one pair")
            print("current probability: ", self.get_probability_of_hand(1))


        my_bet = 0

        if len(self.get_communal_cards(game_state)) == 0:
            if self.have_one_pair(game_state):
                my_bet = current_buy_in - me["bet"]
        else:
            ranking = self.get_cards_ranking(game_state)
            if ranking["rank"] > 0:
                my_bet = current_buy_in - me["bet"]

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

    def have_one_pair(self, game_state):
        my_hand = self.get_my_hand(game_state)
        ranks = [card["rank"] for card in my_hand]
        rank_counts = [ranks.count(rank) for rank in set(ranks)]
        if max(rank_counts) == 2:
            return True

        return False

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

    def showdown(self, game_state):
        pass

