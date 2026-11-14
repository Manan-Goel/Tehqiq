import unittest
from datetime import datetime, timezone

from app.main import check, window


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.meeting, self.start, self.end = window(
            {'meeting_at': '2026-11-16T10:00:00+05:30'},
            datetime(2026, 11, 15, tzinfo=timezone.utc),
        )
        self.sources = [{'id': 'S1', 'content': 'Northstar announced a private beta on November 14.'}]

    def claim(self, **changes):
        value = {'statement': 'Private beta announced', 'source_id': 'S1',
                 'quote': 'Northstar announced a private beta', 'event_date': '2026-11-14',
                 'implication': 'May need support', 'question': 'What is the expansion plan?'}
        value.update(changes)
        return value

    def test_valid_excerpt_and_date(self):
        accepted, rejected = check({'claims': [self.claim()]}, self.sources, self.start, self.end)
        self.assertEqual(len(accepted), 1)
        self.assertFalse(rejected)

    def test_invented_excerpt_and_old_event_rejected(self):
        accepted, rejected = check({'claims': [self.claim(quote='Northstar has paying customers'),
                                                self.claim(event_date='2026-10-01')]}, self.sources, self.start, self.end)
        self.assertFalse(accepted)
        self.assertEqual(len(rejected), 2)

    def test_future_window_not_started(self):
        with self.assertRaises(ValueError):
            window({'meeting_at': '2027-01-01T10:00:00+05:30'},
                   datetime(2026, 11, 15, tzinfo=timezone.utc))


if __name__ == '__main__':
    unittest.main()
