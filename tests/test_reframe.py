import unittest
from unittest.mock import patch

from app.main import reframe


class ReframeTests(unittest.TestCase):
    def test_reframe_preserves_facts_and_uses_no_research(self):
        original={'objective':'Sales','claims':[{'statement':'A beta was announced','source_id':'S1','quote':'We announce a beta','event_date':'2026-11-14','question':'Old?','implication':'Old'}]}
        model_outputs=[({'moves':[{'index':0,'question':'What would make a partnership useful?','implication':'A partner may help if the beta expands.'}]},{},{}),({'decisions':[{'index':0,'supported':True}]},{},{})]
        with patch('app.main.model_json',side_effect=model_outputs) as model, patch('app.main.post') as search:
            updated=reframe(original,'Partnership')
        self.assertEqual(model.call_count,2)
        search.assert_not_called()
        self.assertEqual(updated['claims'][0]['statement'],original['claims'][0]['statement'])
        self.assertEqual(updated['claims'][0]['question'],'What would make a partnership useful?')
        self.assertEqual(original['claims'][0]['question'],'Old?')

    def test_audit_rejection_keeps_original_move(self):
        original={'objective':'Sales','claims':[{'statement':'A beta was announced','source_id':'S1','quote':'We announce a beta','question':'Original?','implication':'Original'}]}
        outputs=[({'moves':[{'index':0,'question':'Assume a contract?','implication':'Guaranteed spend'}]},{},{}),({'decisions':[{'index':0,'supported':False}]},{},{})]
        with patch('app.main.model_json',side_effect=outputs):
            updated=reframe(original,'Partnership')
        self.assertEqual(updated['claims'][0]['question'],'Original?')


if __name__=='__main__': unittest.main()
