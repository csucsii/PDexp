from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'PD1'
    players_per_group = 2
    num_rounds = 2

    instructions_template = 'prisoner/Instructions.html'

    # payoff if 1 player defects and the other cooperates""",
    betray_payoff = c(3)
    betrayed_payoff = c(-1)

    # payoff if both players cooperate or both defect
    both_cooperate_payoff = c(2)
    both_defect_payoff = c(0)


class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):
    def set_payoffs(self):
        self.cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

    er1 = models.IntegerField(min=-15, max=45)
    er2 = models.IntegerField(min=-15, max=45)

class Player(BasePlayer):


    cooperate = models.BooleanField(
        choices=[
            [False, 'Cheat'],
            [True, 'Cooperate']
        ]
    )

    def decision_label(self):
        if self.cooperate:
            return 'cooperate'
        return 'cheat'

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self) -> object:
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

        self.payoff = payoff_matrix[self.cooperate][self.other_player().cooperate]

    satisfaction=models.PositiveIntegerField(min=1, max=10)
