from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random

class Introduction(Page):
    timeout_seconds = 100
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields = ['er1']

class Decision(Page):
    form_model = models.Player
    form_fields = ['cooperate']

    def before_next_page(self):
        self.player.cooperate_bot = random.choice([False,True])
        self.player.set_payoff()


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
    Decision,
    Results,
    Final
]



