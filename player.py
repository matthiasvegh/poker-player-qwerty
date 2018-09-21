from __future__ import print_function
import sys

class Player:
    VERSION = "Default Python calling player"

    def betRequest(self, game_state):
        print('hello world')
        print('hello world stderr', file=sys.stderr)
        current_buy_in = game_state["current_buy_in"]
        me = game_state["players"][game_state["in_action"]
        print('To call, would need to bet:', current_buy_in - me.bet)

        return current_buy_in - me.bet

    def showdown(self, game_state):
        pass

