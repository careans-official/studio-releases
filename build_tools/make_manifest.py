"""세 플랫폼 빌드가 끝난 뒤 하나의 업데이트 목록 생성."""
import argparse,json,sys
from pathlib import Path
metadata=json.loads(Path('release_metadata.json').read_text(encoding='utf-8'))
VERSION,PRODUCT,REPOSITORY,TAG_PREFIX=[metadata[key] for key in ['version','product','repository','tag_prefix']]
parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);args=parser.parse_args()
items={}
for path in args.directory.rglob('*.json'):
    try:item=json.loads(path.read_text(encoding='utf-8'))
    except ValueError:continue
    if item.get('platform') in ['windows-x64','macos-x64','macos-arm64']:
        items[item['platform']]={'url':f'https://github.com/{REPOSITORY}/releases/download/{TAG_PREFIX}{VERSION}/{item["filename"]}','sha256':item['sha256'],'entry':item['entry']}
assert set(items)=={'windows-x64','macos-x64','macos-arm64'},items
(args.directory/'v2r-workspace-update.json').write_text(json.dumps({'product':PRODUCT,'version':VERSION,'platforms':items},ensure_ascii=False,indent=2),encoding='utf-8')
