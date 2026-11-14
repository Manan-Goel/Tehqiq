"""Show public claim/source summaries from the latest completed local job."""
import json
import sqlite3
from pathlib import Path

database = Path(__file__).resolve().parent.parent / 'tehqiq.db'
con = sqlite3.connect(database)
row = con.execute("SELECT report FROM jobs WHERE state='complete' AND report IS NOT NULL ORDER BY rowid DESC LIMIT 1").fetchone()
if not row:
    raise SystemExit('No completed report')
report = json.loads(row[0])
print('ENTITY:', report['entity'])
for claim in report['claims']:
    print('CLAIM:', claim['event_date'], claim['source_id'], claim['statement'])
    print('QUOTE:', claim['quote'][:400])
    print('ASK:', claim['question'])
for source in report['sources']:
    print('SOURCE:', source['id'], source['title'], source['published_date'], source['url'])
