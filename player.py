from __future__ import print_function

class Player:
    VERSION = "Default Python calling player"

    def betRequest(self, game_state):
        current_buy_in = game_state.current_buy_in
        me = game_state.players[game_state.in_action]
        print('To call, would need to bet:', current_buy_in - me.bet)

        return current_buy_in - me.bet

    def showdown(self, game_state):
        pass

