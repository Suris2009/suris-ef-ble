#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build the beta source/install ZIP with notices and per-file checksums."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {
    '.gitignore', 'README.md', 'LICENSE', 'NOTICE', 'DISCLAIMER.md',
    'UPSTREAM_NOTICE.md', 'THIRD_PARTY_NOTICES.md', 'LICENSE_REVIEW.md',
    'RELEASE_NOTES.md', 'hacs.json', 'suris_ef_ble_0.8.0b1_audit.md',
}
TOP_DIRS = {'custom_components', 'audit', 'verification', 'scripts', '.github'}
EXCLUDED = {'__pycache__', '.pytest_cache', '.ruff_cache', '.git', '.venv'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    component = ROOT / 'custom_components/suris_ef_ble_xboost'
    version = json.loads((component / 'manifest.json').read_text())['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+b\d+', version):
        raise SystemExit('This project release workflow only accepts beta versions.')
    for name in ['LICENSE', 'NOTICE', 'DISCLAIMER.md', 'UPSTREAM_NOTICE.md', 'THIRD_PARTY_NOTICES.md']:
        if (ROOT / name).read_bytes() != (component / name).read_bytes():
            raise SystemExit(f'Missing or inconsistent installed notice: {name}')
    files = []
    for path in sorted(ROOT.rglob('*')):
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED for part in relative.parts):
            continue
        if relative.parts[0] not in TOP_DIRS and str(relative) not in TOP_FILES:
            continue
        if path.is_symlink():
            raise SystemExit(f'Symlinks are not permitted: {relative}')
        if not path.is_file() or path.suffix in {'.pyc', '.pyo'}:
            continue
        if path.name in {'.env', 'secrets.yaml', 'configuration.yaml', 'core.config_entries'}:
            raise SystemExit(f'Private configuration must not be packaged: {relative}')
        files.append((relative.as_posix(), path.read_bytes()))
    sums = ''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n' for name, data in files)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = args.output_dir / f'suris_ef_ble_{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in files + [('SHA256SUMS', sums.encode())]:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 6, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n')
    print(json.dumps({'file': str(archive), 'files': len(files) + 1,
                      'bytes': archive.stat().st_size, 'sha256': digest}))


if __name__ == '__main__':
    main()
