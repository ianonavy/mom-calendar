"""
week is even => sat, sun off
week is odd => sat, sun on
alternate three day weekend with mon & fri =>

work three days a week
must work exactly two days in a row:
    mon => tue
    mon & tue => not wed
    not mon & tue => wed
    not mon & not tue & not wed => not thu
    tue & wed => not thu
    tue & not wed => not thu
    not tue & wed => thu
    not thu & not fri => sat
    sat => not fri
week % 4 == 1 => mon

"""

import datetime
import itertools

from constraint import Problem


MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6



def week_even_weekend_off(work_week, week_number):
    """Ensures not working on even weeks"""
    if week_number % 2 == 0:
        return not work_week[SAT] and not work_week[SUN]
    else:
        return work_week[SAT] and work_week[SUN]


def alternate_fri_mon(work_week, week_number):
    """Ensures alternating fri/mon for three day weekends

    Ensures that the 0th week (mon-sun) is a fri, sat, sun off week.
    Ensures that the 3rd week (mon-sun) is a sat, sun, mon off week.
    """
    if week_number % 4 == 0:
        if not work_week[FRI]:
            return False
    if week_number % 4 == 1:
        if work_week[MON]:
            return False
    if week_number % 4 == 2:
        if work_week[FRI]:
            return False
    elif week_number % 4 == 3:
        if not work_week[MON]:
            return False
    return True


def work_three_days_a_week(work_week, week_number):
    """Ensures that sun-sat weeks always include exactly 3 days

    (should either be 2 or 4 days on a mon-sunday week)
    """
    return len([day for day in work_week if day]) in (2, 4)


def work_two_days_in_row(work_week, week_number):
    """Ensures working no more than two days in a row

    Could probably be generalized to simpler rules, but meh
    """
    if work_week[MON] and not work_week[TUE]:
        return False
    if work_week[MON] and work_week[TUE] and work_week[WED]:
        return False
    if not work_week[MON] and work_week[TUE] and not work_week[WED]:
        return False
    if not work_week[MON] and not work_week[TUE] and not work_week[WED] and not work_week[THU]:
        return False
    if work_week[TUE] and work_week[WED] and work_week[THU]:
        return False
    if not work_week[TUE] and work_week[WED] and not work_week[THU]:
        return False
    if work_week[TUE] and not work_week[WED] and work_week[THU]:
        return False
    if not work_week[THU] and not work_week[FRI] and not work_week[SAT]:
        return False
    if work_week[SAT] and work_week[FRI]:
        return False
    return True


def no_off_four_days_in_row(work_week, week_number):
    """Ensures that we're not off four days in a row across weeks"""
    if week_number % 4 == 1 and not work_week[MON] and not work_week[TUE]:
        return False
    return True


def work_cycle():
    """Produces the 28-day working cycle as a list of booleans"""
    possibilities = list(itertools.product([True, False], repeat=7))
    variables = ("work week", "week number")
    problem = Problem()
    problem.addVariable("work week", possibilities)
    problem.addVariable("week number", [0, 1, 2, 3])
    problem.addConstraint(week_even_weekend_off, variables)
    problem.addConstraint(alternate_fri_mon, variables)
    problem.addConstraint(work_three_days_a_week, variables)
    problem.addConstraint(work_two_days_in_row, variables)
    problem.addConstraint(no_off_four_days_in_row, variables)
    solutions = sorted(problem.getSolutions(),
                       key=lambda solution: solution['week number'])
    return itertools.chain(*[sol['work week'] for sol in solutions])


EPOCH = datetime.datetime(2015, 11, 30)


def is_working(day):
    """Computes whether mom is working on a given day"""
    diff = (day - EPOCH).days % 28
    return list(work_cycle())[diff]
