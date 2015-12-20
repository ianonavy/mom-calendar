"""Script to fix the times on the Google Calendar events."""

from __future__ import print_function

import datetime
import time

import dateutil.parser

from mom_calendar.google_calendar import get_service, CALENDAR_ID


def main():
    """Updates Google calendar."""
    service = get_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    results = service.events().list(
        calendarId=CALENDAR_ID, timeMin=now, maxResults=10000, singleEvents=True,
        orderBy='startTime').execute()
    events = results.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start_date = event['start'].get('dateTime', event['start'].get('date'))
            original_date = dateutil.parser.parse(start_date).date()
            new_start = datetime.datetime(original_date.year, original_date.month,
                                          original_date.day, 17, 0)
            new_end = new_start + datetime.timedelta(hours=1)
            updated_event = {
                'summary': 'Work',
                'location': '',
                'description': '',
                'recurrence': [],
                'attendees': [],
                'reminders': {
                    'useDefault': True,
                    'overrides': [],
                },
                'start': {
                    'timeZone': event['start'].get('timeZone'),
                    'dateTime': new_start.isoformat()
                },
                'end': {
                    'timeZone': event['start'].get('timeZone'),
                    'dateTime': new_end.isoformat()
                },
            }
            service.events().update(calendarId=CALENDAR_ID, eventId=event['id'],
                                    body=updated_event).execute()
            time.sleep(0.2)  # for rate limiting
            print(updated_event)


if __name__ == '__main__':
    main()
