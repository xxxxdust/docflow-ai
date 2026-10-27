"""Build a self-contained standard or WorkBuddy skill ZIP without editing sources."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'organize-search-documents'


def build(target, out):
    source = ROOT / 'skills' / NAME
    out.mkdir(parents=True, exist_ok=True)
    archive = out / ('docflow-' + target + '-0.1.0.zip')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(source.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            content = path.read_bytes()
            if path.name == 'SKILL.md' and target == 'workbuddy':
                text = content.decode('utf-8')
                meta = '\ndisplay_name: 文档整理与检索\ndisplay_name_en: Document Organization and Search\ndescription_zh: 整理并检索本地文档，生成带出处的证据包。\ndescription_en: Index local documents and export source-grounded evidence.\nversion: 0.1.0\nauthor: DocFlow AI contributors\n'
                text = text.replace('\n---\n', meta + '---\n', 1)
                content = text.encode('utf-8')
            z.writestr(NAME + '/' + path.relative_to(source).as_posix(), content)
        z.write(ROOT / 'requirements.txt', NAME + '/requirements.txt')
        z.write(ROOT / 'LICENSE', NAME + '/LICENSE')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['standard', 'workbuddy'], default='standard')
    parser.add_argument('--out', type=Path, default=ROOT / 'dist')
    a = parser.parse_args()
    print(build(a.target, a.out))
