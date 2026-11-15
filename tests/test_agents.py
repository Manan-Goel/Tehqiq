import os
import unittest
from unittest.mock import patch
from app import main

class AgentTests(unittest.TestCase):
    def setUp(self): main.METER.set(None)

    def test_planner_clamps_unbounded_work(self):
        with patch.object(main,'agent',return_value=({'queries':['a','b','c','d','e'],'background_days':999,'seconds':999},{},{})):
            plan=main.plan_research({'entity_name':'Acme'})
        self.assertEqual(len(plan['queries']),4)
        self.assertEqual(plan['background_days'],180)
        self.assertEqual(plan['seconds'],90)

    def test_paid_model_blocked_before_network(self):
        with patch.dict(os.environ,{'BIFROST_MODEL':'openrouter/paid','TEHQIQ_FREE_ONLY':'1'}), patch.object(main,'post') as network:
            with self.assertRaises(ValueError): main.model_json([])
        network.assert_not_called()

    def test_qa_unknown_citation_cannot_escape(self):
        report={'entity':'Acme','claims':[{'source_id':'S1','quote':'Beta'}],'sources':[{'id':'S1'}]}
        with patch.object(main,'agent',return_value=({'answer':'Invented answer','source_ids':['S99']},{},{})):
            answer=main.answer_question(report,'Any contract?')
        self.assertEqual(answer['citations'],[])
        self.assertNotIn('Invented',answer['answer'])

    def test_qa_requires_audit_and_returns_source(self):
        report={'entity':'Acme','claims':[{'source_id':'S1','quote':'Beta'}],'sources':[{'id':'S1','url':'https://example.com'}]}
        with patch.object(main,'agent',side_effect=[({'answer':'Beta announced.','source_ids':['S1']},{},{}),({'supported':True},{},{})]):
            result=main.answer_question(report,'What changed?')
        self.assertEqual(result['citations'][0]['id'],'S1')

    def test_context_budget_rejects_before_network(self):
        with patch.dict(os.environ,{'BIFROST_MODEL':'openrouter/openrouter/free'}),patch.object(main,'post') as network:
            with self.assertRaises(ValueError): main.model_json([{'content':'x'*18001}])
        network.assert_not_called()
