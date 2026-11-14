from urllib.error import HTTPError

from app.main import env, model_json

env()
try:
    body, route, usage = model_json([{'role': 'user', 'content': 'Reply with only this JSON object: {"ok":true}'}])
    print({'body': body, 'route': route, 'usage': usage})
except HTTPError as error:
    print('Gateway HTTP status:', error.code)
    print(error.read().decode()[:1000])
    raise SystemExit(1)
