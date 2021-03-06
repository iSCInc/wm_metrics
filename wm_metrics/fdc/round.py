
"""Representation of a FDC round."""


import time
from ..helpers import period


class Round(object):

    """
    FDC Round allows to compute accurate timestamps for start and end of each quarter of the round.

    start and end timestamp are returned as a dictionnary of string { 'start': "...", 'end': "..." }
    """

    QUARTER = [
        {'start': "0101000000", 'end': "0331235959"},
        {'start': "0401000000", 'end': "0630235959"},
        {'start': "0701000000", 'end': "0930235959"},
        {'start': "1001000000", 'end': "1231235959"}
    ]

    def __init__(self, year1, year2, round_number):
        """Constructor.

        Args:
                year1 (int): Year of request of round 1
                year2 (int): Year of request of round 2
                round_number (int): FDC round number,
                        either 1 for round 1 and 2 for round 2

        Raises:
                ValueError: if round is not 1 or 2
        """
        self.year1 = year1
        self.year2 = year2
        if round_number in [1, 2]:
            self.round = round_number
        else:
            raise ValueError(
                "Round number should be either 1 or 2 but is %d" % round_number)

    def quarter(self, quarter):
        """Returns the timestamp of start and end of the quarter.

        Args:
                quarter (int): Number of the quarter (values are between 1 and 4)

        Returns:
                both timestamp of start and end of the quarter as {'start': "XXX", 'end': "YYY"}

        Raises:
                ValueError: if quarter is not in 1..4
        """
        year = self.year2
        index = quarter - 1
        if quarter not in range(1, 5):
            raise ValueError(
                "quarter should be between 1 and 4 but is %d" % quarter)
        if self.round == 2:
            index = (quarter + 1) % 4
            if quarter >= 3:
                year = self.year2 + 1
        return {
            'start': str(year) + Round.QUARTER[index]['start'],
            'end': str(year) + Round.QUARTER[index]['end']}

    def full_period(self):
        """Returns the timestamp of start of the period and the timestamp of end of the period

        Returns:
                both timestamp of start and end of the period as {'start': "XXX", 'end': "YYY"}
        """
        return {
            'start': self.quarter(1)['start'],
            'end': self.quarter(4)['end']
        }

    def _today(self):
        """Returns timestamp of today 0000Z"""
        return time.strftime("%Y%m%d000000", time.gmtime())

    def __repr__(self):
        return "%s-%s round%s" % (self.year1, self.year2, self.round)

    def to_period_for_quarter(self, quarter):
        fdc_period = self.quarter(quarter)
        time_period = period.Period(fdc_period['start'], fdc_period['end'])
        return time_period
