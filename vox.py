"""Portable service dispatcher. All paths are relative to this checkout."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['check', 'ima', 'image', 'tts'])
    parser.add_argument('args', nargs=argparse.REMAINDER)
    options = parser.parse_args()
    file = ROOT / '.private/services.json'
    config = json.loads(file.read_text('utf8')) if file.exists() else {}
    if options.command == 'check':
        missing = [x for x in ('node', 'pnpm', 'ffmpeg', 'ffprobe') if not shutil.which(x)]
        print(json.dumps({'missingTools': missing, 'doubaoConfigured': bool(config.get('doubao')),
                          'imageConfigured': bool(config.get('image')),
                          'imaConfigured': bool(config.get('imaClientId') and config.get('imaApiKey')),
                          'checkType': 'local configuration only; no paid API requests'}, indent=2))
        return int(bool(missing))
    env = os.environ.copy()
    if options.command == 'ima':
        if len(options.args) != 2:
            parser.error('ima requires API path and a JSON body file')
        if not config.get('imaClientId') or not config.get('imaApiKey'):
            parser.error('Configure IMA Client ID and API Key first')
        api, bodyfile = options.args
        # This production workflow reads material only.
        import re
        if not re.fullmatch(r'openapi/(get_|list_|search_)[a-z_]+', api):
            parser.error('Only read operations are supported')
        body = json.loads(Path(bodyfile).read_text('utf-8-sig'))
        env.update(IMA_OPENAPI_CLIENTID=config['imaClientId'], IMA_OPENAPI_APIKEY=config['imaApiKey'])
        cmd = ['node', str(ROOT/'services/ima_api.cjs'), api, json.dumps(body, ensure_ascii=False)]
    elif options.command == 'image':
        if not config.get('image'):
            parser.error('Configure FriModel API Key first')
        cmd = [sys.executable, str(ROOT/'services/external_image_channel.py'), *options.args,
               '--key-file', str(ROOT/'.private/image.key')]
    else:
        if not config.get('doubao') or len(options.args) != 2:
            parser.error('tts requires configured Doubao Key, text file and NEW output directory')
        textfile, output = options.args
        if not Path(textfile).is_file() or not Path(textfile).read_text('utf-8-sig').strip():
            parser.error('Narration file is missing or empty')
        target = Path(output).resolve()
        target.mkdir(parents=True, exist_ok=True)
        # Exclusive marker prevents duplicate paid calls, including ambiguous failures.
        with (target/'tts-request.lock').open('x') as lock:
            lock.write('submitted-or-pending; inspect before any retry')
        cmd = ['node', str(ROOT/'work/own-framework/doubao_tts_corrected.mjs'),
               str(ROOT/'.private/doubao.key'), str(target), 'zh_male_liufei_uranus_bigtts',
               'narration-final-raw', '0', str(Path(textfile).resolve())]
    if options.command == 'ima':
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding='utf8')
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            return result.returncode
        response = json.loads(result.stdout)
        print(json.dumps(response, ensure_ascii=False))
        return 0 if response.get('code') == 0 else 1
    return subprocess.run(cmd, env=env).returncode

if __name__ == '__main__':
    raise SystemExit(main())
