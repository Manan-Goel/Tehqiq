import json
import os
import time
from urllib.request import Request, urlopen

base = os.getenv('TEHQIQ_BASE_URL', 'http://127.0.0.1:8002')
meeting = {'entity_name': 'OpenAI', 'entity_type': 'company', 'meeting_at': '2026-11-16T10:00:00+05:30', 'timezone': 'Asia/Kolkata', 'objective': 'Partnership discussion'}
request = Request(base + '/api/briefings', json.dumps(meeting).encode(), {'Content-Type': 'application/json'}, method='POST')
with urlopen(request, timeout=5) as response:
    job = json.load(response)['job_id']
previous = None
for _ in range(100):
    time.sleep(1.5)
    with urlopen(base + '/api/jobs/' + job, timeout=5) as response:
        result = json.load(response)
    if result['state'] != previous:
        print('stage:', result['state'], flush=True)
        previous = result['state']
    if result['state'] in ('complete', 'failed'):
        if result['state'] == 'complete':
            report = result['report']
            print({'claim_count': len(report.get('claims', [])), 'rejected_count': len(report.get('rejected', [])), 'sources': len(report.get('sources', [])), 'trace': report.get('trace')}, flush=True)
        else:
            print('error:', result.get('error'), flush=True)
        break
