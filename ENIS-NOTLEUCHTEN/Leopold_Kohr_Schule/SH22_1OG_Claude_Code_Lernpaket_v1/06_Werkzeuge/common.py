from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(rel):
    with (ROOT/rel).open(encoding='utf-8') as f:return json.load(f)
def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def write_report(result,path=None):
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if path:
        p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
    print(text,end='')
