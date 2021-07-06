from .registry import SchemaRegistry, SchemaMetadata
from mdutils.tools.Table import Table
from mdutils import MdUtils
import io
from io import StringIO
from contextlib import redirect_stdout

import json
from typing import Dict, List
from jsonasobj2 import items, JsonObj, as_dict
from dataclasses import astuple, dataclass, fields

from linkml_runtime.dumpers.dumper_root import Dumper


class MarkdownDumper(Dumper):
    def dump(self, sr: SchemaRegistry, to_file: str) -> None:
        with open(to_file, 'w') as stream:
            stream.write(self.dumps(sr))

    def _get_header_dict(self, pycls) -> Dict:
        h = {}
        for f in fields(pycls):
            # TODO: use metadata
            h[f.name] = f.name
        return h

    def _autoformat(self, text: str) -> str:
        if text.startswith('http'):
            return self._link(text)
        else:
            return text
    def _link(self, url, text: str=None) -> str:
        if text is None:
            text = url
        return f'[{text}]({url})'

class MarkdownTableDumper(MarkdownDumper):

    def dumps(self, sr: SchemaRegistry) -> None:
        h = self._get_header_dict(SchemaMetadata)
        text_list = list(h.values())
        rows = 1
        s: SchemaMetadata
        for s in sr.entries.values():
            print(f'S={s}')
            row = self._create_row(s, h)
            cols = len(row)
            text_list += [str(x) for x in row]
            rows += 1
        table = Table().create_table(columns=cols, rows=rows, text=text_list, text_align='center')
        return str(table)

    def _create_row(self, s: SchemaMetadata, h: dict) -> List[str]:
        row = []
        for k in h.keys():
            v = s.__getattr__(k)
            if v is None:
                v = ''
            row.append(v)
        return row

class MarkdownPageDumper(MarkdownDumper):


    def dumps(self, sr: SchemaRegistry) -> None:
        output = StringIO()
        with redirect_stdout(output):
            print(f'# LinkML Registry Entries\n')
            h = self._get_header_dict(SchemaMetadata)
            s: SchemaMetadata
            for s in sr.entries.values():
                print(f'## {s.name} : {s.title}\n')
                print(f'{s.description}\n')
                text_list = ['key', 'value']
                rows = 1
                for k in h.keys():
                    v = s.__getattr__(k)
                    if v is not None and v != '' and v != []:
                        text_list += [k, self._autoformat(str(v))]
                        rows += 1
                table = Table().create_table(columns=2, rows=rows, text=text_list, text_align='center')
                print(str(table))
        return output.getvalue()

    def _get_header_dict(self, pycls) -> Dict:
        h = {}
        for f in fields(pycls):
            # TODO: use metadata
            h[f.name] = f.name
        return h



