"""Interactive local credential setup. Never prints secrets."""
from pathlib import Path
import getpass
import json

root = Path(__file__).resolve().parent
private = root / '.private'
private.mkdir(exist_ok=True, mode=0o700)
config = private / 'services.json'
values = json.loads(config.read_text('utf8')) if config.exists() else {}
fields = [('doubao', 'Doubao API Key'), ('image', 'FriModel API Key'),
          ('imaClientId', 'IMA Client ID (optional)'), ('imaApiKey', 'IMA API Key (optional)')]
for key, label in fields:
    value = getpass.getpass(label + ' [Enter keeps existing]: ').strip()
    if value:
        values[key] = value
config.write_text(json.dumps(values), encoding='utf8')
config.chmod(0o600)
for key in ('doubao', 'image'):
    if values.get(key):
        file = private / (key + '.key')
        file.write_text(values[key], encoding='utf8')
        file.chmod(0o600)
print('Saved locally in .private. Run python vox.py check.')
