"""Create a one-day local Bifrost key for the OpenRouter free router only."""
import json
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parent.parent
config_path = root / 'bifrost/config.json'
env_path = root / '.env'
con = sqlite3.connect(root / 'bifrost/config.db')
rows = con.execute("SELECT key_id FROM config_keys WHERE provider='openrouter' AND enabled=1").fetchall()
if len(rows) != 1:
    raise RuntimeError('Expected exactly one enabled OpenRouter provider key')
provider_key_id = rows[0][0]
if not provider_key_id:
    raise RuntimeError('OpenRouter provider key ID unavailable')
config = json.loads(config_path.read_text(encoding='utf-8-sig'))
if set(config['providers']) != {'openrouter'}:
    raise RuntimeError('Unexpected provider configuration; refusing to create key')
secret = 'sk-bf-' + secrets.token_hex(24)
config['governance'] = {'virtual_keys': [{
    'id': 'vk-tehqiq-local', 'name': 'tehqiq-local',
    'value': 'env.BIFROST_API_KEY', 'is_active': True,
    'disable_content_logging': True,
    'expires_at': (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    'provider_configs': [{
        'provider': 'openrouter',
        'allowed_models': ['openrouter/free'],
        'key_ids': [provider_key_id],
    }],
}]}
lines = [line for line in env_path.read_text(encoding='utf-8-sig').splitlines() if not line.startswith('BIFROST_API_KEY=')]
lines.append('BIFROST_API_KEY=' + secret)
env_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
config_path.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
print('Configured one-day local key for the configured OpenRouter key and openrouter/free only.')
