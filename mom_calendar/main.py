"""Main script for adding all the events for when my mom works gcal"""

from __future__ import print_function

import datetime
import pytz

from mom_calendar.working import is_working
from mom_calendar.google_calendar import get_service, TIME_ZONE, CALENDAR_ID


WORK_START_TIME = 17  # 7pm
WORK_SHIFT_LENGTH = 1


def add_event(service, start_work, end_work):
    """Adds an event to Google calendar"""
    los_angeles = pytz.timezone(TIME_ZONE)
    start_work = los_angeles.localize(start_work).isoformat()
    end_work = los_angeles.localize(end_work).isoformat()
    event = {
        'summary': 'Work',
        'location': '',
        'description': '',
        'start': {
            'dateTime': start_work,
            'timeZone': TIME_ZONE,
        },
        'end': {
            'dateTime': end_work,
            'timeZone': TIME_ZONE,
        },
        'recurrence': [],
        'attendees': [],
        'reminders': {
            'useDefault': True,
            'overrides': [],
        },
    }
    print("{} to {}".format(start_work, end_work))
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()



def main():
    """Adds my mom's wor kschedule from 2016 to 2028"""
    service = get_service()

    start_day = datetime.datetime(2016, 1, 1)
    end_day = datetime.datetime(2028, 1, 1)
    counter = 0

    for i in range((end_day - start_day).days):
        work_day = start_day + datetime.timedelta(days=i)
        if not is_working(work_day):
            continue

        counter += 1

        start_work = work_day + datetime.timedelta(hours=WORK_START_TIME)
        end_work = start_work + datetime.timedelta(hours=WORK_SHIFT_LENGTH)
        add_event(service, start_work, end_work)
    print("Added {} events".format(counter))


if __name__ == '__main__':
    main()
