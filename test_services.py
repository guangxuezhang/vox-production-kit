import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import vox

class ServicesTest(unittest.TestCase):
    def test_empty_config_makes_no_request(self):
        with tempfile.TemporaryDirectory() as d, patch.object(vox, 'ROOT', Path(d)), patch.object(vox.subprocess, 'run') as run:
            for command in ('image', 'tts', 'ima'):
                with patch('sys.argv', ['vox.py', command]), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit): vox.main()
            run.assert_not_called()

    def test_ima_write_rejected_and_business_error_propagates(self):
        with tempfile.TemporaryDirectory() as d, patch.object(vox, 'ROOT', Path(d)):
            root = Path(d); (root/'.private').mkdir()
            (root/'.private/services.json').write_text(json.dumps({'imaClientId':'test','imaApiKey':'test'}))
            body=root/'body.json'; body.write_text('{}')
            with patch.object(vox.subprocess, 'run') as run:
                with patch('sys.argv',['vox.py','ima','openapi/delete_doc',str(body)]), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit): vox.main()
                run.assert_not_called()
                run.return_value.returncode=0;run.return_value.stdout='{"code":1,"msg":"denied"}'
                with patch('sys.argv',['vox.py','ima','openapi/list_docs',str(body)]), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(vox.main(),1)

if __name__ == '__main__': unittest.main()
