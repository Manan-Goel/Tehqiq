from datetime import datetime, timedelta, timezone

from app.main import env, post
import os

env()
today = datetime.now(timezone.utc).date()
result = post('https://api.tavily.com/search', {
    'query': 'OpenAI official announcements',
    'search_depth': 'basic',
    'max_results': 2,
    'start_date': (today - timedelta(days=30)).isoformat(),
    'end_date': today.isoformat(),
    'include_published_date': True,
    'filter_by_published_date': True,
    'include_answer': False,
}, os.environ['TAVILY_API_KEY'])
print({'result_count': len(result.get('results', [])), 'request_id_present': bool(result.get('request_id'))})
if result.get('results'):
    extracted = post('https://api.tavily.com/extract', {
        'urls': [result['results'][0]['url']], 'extract_depth': 'basic'
    }, os.environ['TAVILY_API_KEY'])
    print({'extract_count': len(extracted.get('results', [])), 'failed_count': len(extracted.get('failed_results', []))})
