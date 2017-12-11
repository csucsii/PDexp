from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools, random


class Constants(BaseConstants):
    name_in_url = 'PD'
    players_per_group = None
    num_rounds = 3

    instructions_template = 'PD_treatments/Instructions.html'

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

    STRATEGY = ['Nice-guy', 'Nasty-one', 'Grudger', 'Copycat']
    treatments = ['free', 'choice', 'force']


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            if self.session.config.get('treatment'):
                p.vars['treatment'] = self.session.config.get('treatment')
            else:
                treatment = itertools.cycle(Constants.treatments)
            for p in self.session.get_participants():
                p.vars['treatment'] = next(treatment)
                if p.vars['treatment'] == 'force':
                    p.vars['strategy'] = random.choice(Constants.STRATEGY)
        for p in self.get_players():
            p.treatment = p.participant.vars['treatment']
            p.strategy = p.participant.vars.get('strategy')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cooperate = models.BooleanField(choices=Constants.COOPCHOICES)
    cooperate_bot = models.BooleanField(choices=Constants.COOPCHOICES)

    strategy = models.CharField(
        choices=Constants.STRATEGY,
        widget=widgets.RadioSelect()
    )

    er1 = models.IntegerField(min=-7, max=21)
    er2 = models.IntegerField(min=-7, max=21)
    bot_payoff = models.IntegerField()
    satisfaction = models.PositiveIntegerField(min=1, max=10)
    treatment = models.CharField()

    def decision(self):
        # Cooperates in every round
        if self.strategy == 'Nice-guy':
            self.cooperate = True
            return

        # Cheats in every round
        if self.strategy == 'Nasty-one':
            self.cooperate = False
            return

        # Cooperates in Round 1, and keep cooperating until cheated, then cheats in every round
        if self.strategy == 'Grudger':
            if self.round_number == 1:
                self.cooperate = True
                return
            else:
                if self.in_round(self.round_number - 1).cooperate_bot == False:
                    self.cooperate = False
                    return
                self.player.cooperate = self.in_round(self.round_number - 1).cooperate
                return
        # Cooperates in Round 1, then copies the last move of other player
        if self.strategy == 'Copycat':
            if Constants.round_number == 1:
                self.cooperate = True
            else:
                self.cooperate = self.in_round(self.round_number - 1).cooperate_bot

    @property
    def cumulative_payoff(self):
        return sum([p.payoff for p in self.in_all_rounds()])

    @property
    def bot_cumulative_payoff(self):
        return sum([p.bot_payoff for p in self.in_all_rounds()])

    def set_payoffs(self):
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
