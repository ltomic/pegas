import json

from pegas.settings import (
    BASE_DIR
    )

info_error = {'memory': -1, 'time': -1}
argv_lang = json.load(open('info/run.json', 'r'))
info_lang = json.load(open('info/lang.json', 'r'))
verdicts = json.load(open('info/verdicts.json', 'r'))
args_judge = ['schroot', '-c', 'chroot:trusty', 
              '--directory', '.', './bin/run_code']

path = {'code': 'lark/sandbox/code',
        'checker': 'lark/sandbox/checker',
        'input': 'lark/sandbox/tests/in',
        'usage': 'lark/sandbox/info.json',
        'error': 'lark/sandbox/errors',
        'ans': 'lark/sandbox/ans',
        }
