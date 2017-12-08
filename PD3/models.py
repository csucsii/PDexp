from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools


class Constants(BaseConstants):
    name_in_url = 'PD3'
    players_per_group = None
    num_rounds = 3

    instructions_template = 'PD3/Instructions.html'

    # payoff if 1 player defects and the other cooperates""",
    betray_payoff = c(3)
    betrayed_payoff = c(-1)

    # payoff if both players cooperate or both defect
    both_cooperate_payoff = c(2)
    both_defect_payoff = c(0)

    COOPCHOICES = [
        [False, 'Cheat'],
        [True, 'Cooperate']
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            expgroup = itertools.cycle(['free', 'choice', 'force'])
            for p in self.get_participants():
                p.expgroup = next(expgroup)


class Group(BaseGroup):
    ...


class Player(BasePlayer):
    cooperate = models.BooleanField(choices=Constants.COOPCHOICES)
    cooperate_bot = models.BooleanField(choices=Constants.COOPCHOICES)

    er1 = models.IntegerField(min=-7, max=21)
    er2 = models.IntegerField(min=-7, max=21)
    bot_payoff= models.IntegerField()
    @property
    def cumulative_payoff(self):
        return sum([p.payoff for p in self.in_all_rounds()])

    @property
    def bot_cumulative_payoff(self):
        return sum([p.bot_payoff for p in self.in_all_rounds()])

    def other_player(self):
        return self.cooperate_bot

    def set_payoff(self):
        payoff_matrix = {
            True:
                {
                    True: Constants.both_cooperate_payoff,
                    False: Constants.betrayed_payoff
                },
            False:
                {
                    True: Constants.betray_payoff,
                    False: Constants.both_defect_payoff
                }
        }

        self.payoff = payoff_matrix[self.cooperate][self.cooperate_bot]
        self.bot_payoff = payoff_matrix[self.cooperate_bot][self.cooperate]

    satisfaction = models.PositiveIntegerField(min=1, max=10)


