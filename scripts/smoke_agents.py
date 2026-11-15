"""Live model-route checks with explicitly synthetic evidence, not a research benchmark."""
from app.main import env, plan_research, answer_question
env()
plan=plan_research({'entity_name':'Acme (fictional)','objective':'Partnership discussion'})
print('Planner passed:',len(plan['queries']),'queries,',plan['background_days'],'days',flush=True)
report={'entity':'Acme (fictional)','claims':[{'source_id':'S1','statement':'Acme announced a beta.','quote':'Acme announced a beta on November 14, 2026.','event_date':'2026-11-14'}],'sources':[{'id':'S1','url':'https://example.com','title':'Synthetic test evidence'}]}
result=answer_question(report,'What did Acme announce?')
print('Q&A:',result['answer'],'citations:',len(result['citations']),flush=True)
