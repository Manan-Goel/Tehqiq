"""Print non-secret IDs from the local Bifrost config database."""
import sqlite3
from pathlib import Path

db = Path(__file__).resolve().parent.parent / 'bifrost/config.db'
con = sqlite3.connect(db)
for table in ('config_providers', 'config_keys'):
    columns = [row[1] for row in con.execute(f'PRAGMA table_info({table})')]
    print(table, columns)
    safe = [name for name in columns if name.lower() in ('id', 'name', 'provider', 'provider_id', 'provider_name', 'key_id')]
    if safe:
        print(con.execute(f'SELECT {", ".join(safe)} FROM {table} LIMIT 10').fetchall())
