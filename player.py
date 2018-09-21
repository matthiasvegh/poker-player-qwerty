from __future__ import print_function

import sys

class Player:
    VERSION = "Default Python calling player"

    def convertCardsToString(self, cards):
        cardList = []

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
        if have_one_pair(game_state):
            print("have one pair")

        return current_buy_in - me["bet"]

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

        return False

    def showdown(self, game_state):
        pass

