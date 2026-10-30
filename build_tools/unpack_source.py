"""GitHub Actions 내부에서만 보호된 빌드 소스 풀기."""
import io,os,zipfile
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
payload=Path('v2r-source.enc').read_bytes();assert payload[:8]==b'V2RSRC1\n'
key=bytes.fromhex(os.environ['V2R_BUILD_SOURCE_KEY']);source=AESGCM(key).decrypt(payload[8:20],payload[20:],b'careans-v2r-source')
root=Path('app').resolve();root.mkdir(exist_ok=True)
with zipfile.ZipFile(io.BytesIO(source)) as archive:
    assert len(archive.infolist())<300 and sum(x.file_size for x in archive.infolist())<10_000_000
    for item in archive.infolist():
        name=item.filename.replace('\\','/');assert not name.startswith('/') and ':' not in name and '..' not in name.split('/')
    archive.extractall(root)
print('빌드 소스 준비 완료')
