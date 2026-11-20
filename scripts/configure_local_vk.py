"""Create a one-day Bifrost key limited to free OpenRouter models and Gemini fallback."""
import json
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parent.parent
config_path = root / 'bifrost/config.json'
env_path = root / '.env'
settings = {}
for line in env_path.read_text(encoding='utf-8-sig').splitlines():
    if '=' in line and not line.startswith('#'):
        name, value = line.split('=', 1)
        settings[name.strip()] = value.strip()
gemini_enabled = settings.get('TEHQIQ_GEMINI_FREE_TIER_CONFIRMED') == '1'
con = sqlite3.connect(root / 'bifrost/config.db')
rows = con.execute("SELECT key_id FROM config_keys WHERE provider='openrouter' AND enabled=1").fetchall()
gemini_rows = con.execute("SELECT key_id FROM config_keys WHERE provider='gemini' AND enabled=1").fetchall()
if len(rows) != 1:
    raise RuntimeError('Expected exactly one enabled OpenRouter provider key')
if gemini_enabled and len(gemini_rows) != 1:
    raise RuntimeError('Expected exactly one enabled Gemini provider key; start Bifrost once after adding GEMINI_API_KEY')
provider_key_id = rows[0][0]
gemini_key_id = gemini_rows[0][0] if gemini_rows else None
if not provider_key_id:
    raise RuntimeError('OpenRouter provider key ID unavailable')
config = json.loads(config_path.read_text(encoding='utf-8-sig'))
if 'openrouter' not in config['providers'] or gemini_enabled and 'gemini' not in config['providers']:
    raise RuntimeError('Unexpected provider configuration; refusing to create key')
secret = 'sk-bf-' + secrets.token_hex(24)
config['governance'] = {'virtual_keys': [{
    'id': 'vk-tehqiq-local', 'name': 'tehqiq-local',
    'value': 'env.BIFROST_API_KEY', 'is_active': True,
    'disable_content_logging': True,
    'expires_at': (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    'provider_configs': [{
        'provider': 'openrouter',
        'allowed_models': ['inclusionai/ling-3.2-flash:free','google/gemma-4-26b-a4b-it:free'],
        'key_ids': [provider_key_id],
    }],
}]}
if gemini_enabled:
    config['governance']['virtual_keys'][0]['provider_configs'].append({
        'provider': 'gemini',
        'allowed_models': ['gemini-3.8-flash'],
        'key_ids': [gemini_key_id],
    })
lines = [line for line in env_path.read_text(encoding='utf-8-sig').splitlines() if not line.startswith('BIFROST_API_KEY=')]
lines.append('BIFROST_API_KEY=' + secret)
role_models={
    'BIFROST_PLANNER_MODEL':'openrouter/inclusionai/ling-3.2-flash:free',
    'BIFROST_DRAFT_MODEL':'openrouter/google/gemma-4-26b-a4b-it:free',
    'BIFROST_AUDIT_MODEL':'openrouter/inclusionai/ling-3.2-flash:free',
    'BIFROST_QA_MODEL':'openrouter/google/gemma-4-26b-a4b-it:free',
    'BIFROST_PLANNER_FALLBACK_MODEL':'openrouter/google/gemma-4-26b-a4b-it:free',
    'BIFROST_DRAFT_FALLBACK_MODEL':'openrouter/inclusionai/ling-3.2-flash:free',
    'BIFROST_AUDIT_FALLBACK_MODEL':'openrouter/google/gemma-4-26b-a4b-it:free',
    'BIFROST_QA_FALLBACK_MODEL':'openrouter/inclusionai/ling-3.2-flash:free',
    'BIFROST_GEMINI_FALLBACK_MODEL':'gemini/gemini-3.8-flash' if gemini_enabled else '',
}
for name,value in role_models.items():
    lines=[line for line in lines if not line.startswith(name+'=')]
    lines.append(name+'='+value)
env_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
config_path.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
print('Configured a one-day key for two OpenRouter free models'+(' plus Gemini Free Tier fallback.' if gemini_enabled else '. Gemini is disabled until Free Tier billing status is confirmed.'))
