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

        return current_buy_in - me["bet"]

    def showdown(self, game_state):
        pass

