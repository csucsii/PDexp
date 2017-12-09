from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random

class Introduction(Page):
    timeout_seconds = 90
    def is_displayed(self):
        return self.round_number == 1

class Strategy(Page):
    timeout_seconds = 120
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields= ['strategy']

    def before_next_page(self):
        return self.player.in_previous_rounds()


class YourBet(Page):
    def is_displayed(self):
        return self.round_number == 1
    form_model = models.Player
    form_fields = ['er1']

    def before_next_page(self):
        self.player.mystrategy=self.player.in_round(1).strategy

class DecisionWait(Page):

    def before_next_page(self):
        self.player.decision()
        self.player.cooperate_bot = random.choice([False,True])
        self.player.set_payoff()

    def vars_for_template(self):
        return {
            'my_strategy': self.player.get_strategy_display(),
            'my_decision': self.player.decision_label(),
        }




class Results(Page):
    def vars_for_template(self):
        return {
            'my_decision': self.player.get_cooperate_display(),
            'other_player_decision': self.player.get_cooperate_bot_display(),
            'same_choice': self.player.cooperate == self.player.cooperate_bot,
            'round_number': self.round_number
        }

    form_model = models.Player
    form_fields = ['satisfaction']

class Final(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


    form_model = models.Player
    form_fields = ['er2']

page_sequence = [
    Introduction,
    Strategy,
    YourBet,
    DecisionWait,
    Results,
    Final
]



