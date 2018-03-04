#!/usr/bin/env python3

from mmap import mmap, ACCESS_READ
from contextlib import closing
from pathlib import Path
import re

METHOD_RE = re.compile(br'^\.method([a-z ]*) ([^ (]+)\((.*?)\).*\n\s*\.locals \d+$', re.MULTILINE)
PARAM_RE = re.compile(br'\[*(?:L.+?;|[^L])')

def process_dir(path):
    for entry in Path(path).rglob('*.smali'):
        original_path = str(entry)
        print('[-] File name:', original_path)
        with entry.open() as f:
            with closing(mmap(f.fileno(), 0, access=ACCESS_READ)) as smali:
                if re.search(br'\.(?:param|local) ', smali):
                    raise RuntimeError('Parameters are already annotated')
                param_inserts = list(find_methods(smali))
                if not param_inserts:
                    continue
                entry.rename(original_path + '~')
                last_pos = 0
                with open(original_path, 'wb') as output:
                    for offset, params, is_static in param_inserts:
                        output.write(smali[last_pos:offset])
                        wide_offset = 0
                        for n, t in enumerate(params, 0 if is_static else 1):
                            output.write('\n    .param p{0}, "p{0}"    # {1}'.format(n + wide_offset,
                                t.decode('ascii')).encode('ascii'))
                            if t == b'J' or t == b'D':
                                wide_offset += 1
                        last_pos = offset
                    output.write(smali[last_pos:])
        print('[+] Closed', original_path)

def find_methods(smali):
    for method in METHOD_RE.finditer(smali):
        is_static = b'static' in method.group(1)
        print('[-] |- Method:', method.group(2))
        params = PARAM_RE.findall(method.group(3))
        if params:
            yield method.end(), params, is_static

if __name__ == '__main__':
    from sys import argv
    process_dir(argv[1])
