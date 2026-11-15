"""Offline contract tests; no API credentials or network required."""
import os
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from app import main


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(os.environ,{'TEHQIQ_FREE_ONLY':'0'}))
        self.enterContext(patch.object(main,'plan_research',return_value={'queries':['launch','leadership'],'background_days':30,'seconds':90,'reason':'test'}))
        main.METER.set(None)
        self.start = datetime(2026, 10, 16, tzinfo=timezone.utc)
        self.end = datetime(2026, 11, 15, tzinfo=timezone.utc)
        self.sources = [{'id': 'S1', 'content': 'Acme announced a limited beta on November 14.'}]

    def test_unknown_source_and_missing_date_rejected(self):
        raw = {'claims': [
            {'source_id': 'S99', 'quote': 'Acme announced', 'event_date': '2026-11-14'},
            {'source_id': 'S1', 'quote': 'Acme announced', 'event_date': ''},
        ]}
        accepted, rejected = main.check(raw, self.sources, self.start, self.end)
        self.assertEqual(accepted, [])
        self.assertEqual(len(rejected), 2)

    def test_exact_upper_boundary(self):
        raw = {'claims': [{'source_id': 'S1', 'quote': 'Acme announced',
                           'event_date': '2026-11-15T00:00:00+00:00'}]}
        accepted, _ = main.check(raw, self.sources, self.start, self.end)
        self.assertEqual(len(accepted), 1)

    def test_partial_extract_maps_content_by_url(self):
        payloads = []
        def fake_post(url, body, key):
            payloads.append((url, body))
            if url.endswith('/search'):
                return {'results': [{'url': 'https://example.com/one', 'title': 'One', 'published_date': '2026-11-14'},
                                    {'url': 'https://example.com/two', 'title': 'Two', 'published_date': '2026-11-14'}]}
            if url.endswith('/extract'):
                return {'results': [{'url': 'https://example.com/two',
                                     'raw_content': 'Acme announced a limited beta on November 14.'}],
                        'failed_results': [{'url': 'https://example.com/one', 'error': 'Unavailable'}]}
            if 'strict evidence auditor' in body['messages'][0]['content']:
                return {'choices': [{'message': {'content': '{"decisions":[{"index":0,"supported":true,"reason":"Source supports the claim"}]}'}}]}
            return {'choices': [{'message': {'content': '{"claims":[{"statement":"Acme announced a beta","source_id":"S2","quote":"Acme announced a limited beta","date_quote":"November 14","event_date":"2026-11-14","question":"When will it expand?","implication":"May need support"}]}'}}]}

        saved = []
        data = {'entity_name': 'Acme', 'entity_type': 'company',
                'meeting_at': '2026-11-16T10:00:00+05:30', 'timezone': 'Asia/Kolkata'}
        with patch.dict(os.environ, {'TAVILY_API_KEY': 'placeholder', 'BIFROST_MODEL': 'custom/example'}, clear=False), \
             patch.object(main, 'post', side_effect=fake_post), \
             patch.object(main, 'save', side_effect=lambda *a, **kw: saved.append((a, kw))), \
             patch.object(main, 'env'):
            main.run('test-job', data)
        self.assertEqual(saved[-1][0][1], 'complete')
        report = saved[-1][0][2]
        self.assertEqual(len(report['claims']), 1)
        self.assertEqual(report['claims'][0]['source_id'], 'S2')
        self.assertEqual(len(report['sources']), 1)

    def test_bifrost_fallback_payload(self):
        seen = []
        def fake_post(url, body, key):
            seen.append((url, body))
            return {'choices': [{'message': {'content': '{"claims":[]}'}}],
                    'extra_fields': {'routing_info': {'provider': 'backup'}},
                    'usage': {'total_tokens': 12}}
        with patch.dict(os.environ, {'BIFROST_MODEL': 'primary/model',
                                      'BIFROST_FALLBACK_MODEL': 'backup/model'}, clear=False), \
             patch.object(main, 'post', side_effect=fake_post):
            result, route, usage = main.model_json([{'role': 'user', 'content': 'test'}])
        self.assertEqual(seen[0][1]['fallbacks'], ['backup/model'])
        self.assertEqual(route['provider'], 'backup')
        self.assertEqual(usage['total_tokens'], 12)
        self.assertEqual(result, {'claims': []})

    def test_malformed_model_json_raises(self):
        with patch.dict(os.environ, {'BIFROST_MODEL': 'primary/model'}, clear=False), \
             patch.object(main, 'post', return_value={'choices': [{'message': {'content': 'not JSON'}}]}):
            with self.assertRaises(json.JSONDecodeError):
                main.model_json([{'role': 'user', 'content': 'test'}])

    def test_semantic_audit_rejection_excludes_claim(self):
        def fake_post(url, body, key):
            if url.endswith('/search'):
                return {'results': [{'url': 'https://example.com/one', 'title': 'One',
                                     'published_date': '2026-11-14'}]}
            if url.endswith('/extract'):
                return {'results': [{'url': 'https://example.com/one',
                                     'raw_content': 'Acme announced a limited beta on November 14.'}]}
            if 'strict evidence auditor' in body['messages'][0]['content']:
                return {'choices': [{'message': {'content': '{"decisions":[{"index":0,"supported":false,"reason":"Statement overclaims"}]}'}}]}
            return {'choices': [{'message': {'content': '{"claims":[{"statement":"Acme has 1 million users","source_id":"S1","quote":"Acme announced a limited beta","date_quote":"November 14","event_date":"2026-11-14","question":"How many users?","implication":"Could grow"}]}'}}]}
        saved = []
        data = {'entity_name': 'Acme', 'entity_type': 'company',
                'meeting_at': '2026-11-16T10:00:00+05:30', 'timezone': 'Asia/Kolkata'}
        with patch.dict(os.environ, {'TAVILY_API_KEY': 'placeholder', 'BIFROST_MODEL': 'primary/model'}, clear=False), \
             patch.object(main, 'post', side_effect=fake_post), \
             patch.object(main, 'save', side_effect=lambda *a, **kw: saved.append((a, kw))), \
             patch.object(main, 'env'):
            main.run('test-job', data)
        self.assertEqual(saved[-1][0][1], 'complete')
        report = saved[-1][0][2]
        self.assertEqual(report['claims'], [])
        self.assertEqual(report['rejected'][0]['reason'], 'Statement overclaims')


if __name__ == '__main__':
    unittest.main()
