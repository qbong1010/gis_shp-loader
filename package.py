#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QGIS 플러그인 패키징 스크립트

이 스크립트는 QGIS 플러그인을 배포 가능한 ZIP 파일로 패키징합니다.
QGIS 플러그인 저장소 및 수동 설치에 사용할 수 있습니다.

사용법:
    python package.py
"""

import zipfile
import shutil
import re
from pathlib import Path
from datetime import datetime


def get_version():
    """metadata.txt에서 버전 읽기"""
    metadata_path = Path('metadata.txt')

    if not metadata_path.exists():
        print("❌ metadata.txt 파일을 찾을 수 없습니다.")
        return "unknown"

    metadata = metadata_path.read_text(encoding='utf-8')
    match = re.search(r'version=(\d+\.\d+\.\d+)', metadata)

    if match:
        return match.group(1)

    print("⚠  metadata.txt에서 버전을 찾을 수 없습니다. 'unknown' 사용")
    return "unknown"


def get_plugin_name():
    """metadata.txt에서 플러그인 이름 읽기"""
    metadata_path = Path('metadata.txt')

    if not metadata_path.exists():
        return "gis_shp_loader"

    metadata = metadata_path.read_text(encoding='utf-8')
    match = re.search(r'name=(.+)', metadata)

    if match:
        # 공백을 언더스코어로, 소문자로 변환
        name = match.group(1).strip()
        return re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()

    return "gis_shp_loader"


def get_files_to_include():
    """패키징에 포함할 파일 목록"""
    # 필수 파일
    required_files = [
        '__init__.py',
        'metadata.txt',
    ]

    # 선택적 파일 (있으면 포함)
    optional_files = [
        'gis_shp_loader.py',
        'gis_shp_loader_dialog.py',
        'icon.png',
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
    ]

    # UI 파일들
    ui_files = list(Path('.').glob('*.ui'))

    # 리소스 파일들
    resource_files = list(Path('.').glob('resources.qrc'))
    resource_files.extend(Path('.').glob('resources/*.png'))
    resource_files.extend(Path('.').glob('resources/*.svg'))

    files = []

    # 필수 파일 확인
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 필수 파일 누락: {file}")
            return None
        files.append(file)

    # 선택적 파일 추가
    for file in optional_files:
        if Path(file).exists():
            files.append(file)

    # UI 파일 추가
    for file in ui_files:
        files.append(str(file))

    # 리소스 파일 추가
    for file in resource_files:
        files.append(str(file))

    return files


def get_exclude_patterns():
    """제외할 파일 패턴"""
    return [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        '.gitignore',
        '.github',
        '*.zip',
        'package.py',
        'bump-version.py',
        '.vscode',
        '.idea',
        '*.tmp',
        '*.log',
        'test_*',
        'tests/',
        '.pytest_cache',
        'VERSIONING_STRATEGY.md',
    ]


def should_exclude(file_path, exclude_patterns):
    """파일이 제외 패턴에 해당하는지 확인"""
    file_str = str(file_path)

    for pattern in exclude_patterns:
        if pattern.endswith('/'):
            # 디렉토리 패턴
            if pattern[:-1] in file_str:
                return True
        elif '*' in pattern:
            # 와일드카드 패턴
            import fnmatch
            if fnmatch.fnmatch(file_str, pattern):
                return True
        else:
            # 정확한 매치
            if pattern in file_str:
                return True

    return False


def create_plugin_zip():
    """플러그인 ZIP 파일 생성"""
    version = get_version()
    plugin_name = get_plugin_name()
    zip_filename = f"{plugin_name}.{version}.zip"

    print("\n" + "=" * 60)
    print("  QGIS 플러그인 패키징")
    print("=" * 60)
    print(f"\n플러그인: {plugin_name}")
    print(f"버전:     {version}")
    print(f"파일명:   {zip_filename}")
    print(f"날짜:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 포함할 파일 가져오기
    files_to_include = get_files_to_include()

    if files_to_include is None:
        print("\n❌ 패키징 실패: 필수 파일이 누락되었습니다.")
        return None

    exclude_patterns = get_exclude_patterns()

    print("\n포함할 파일:")

    # ZIP 파일 생성
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            file_path = Path(file)

            if should_exclude(file_path, exclude_patterns):
                print(f"  ⊘ {file} (제외됨)")
                continue

            if file_path.exists():
                # ZIP 내부 경로: plugin_name/file
                arcname = f"{plugin_name}/{file}"
                zipf.write(file, arcname)
                file_size = file_path.stat().st_size
                print(f"  ✓ {file:<30} ({file_size:>8,} bytes)")
            else:
                print(f"  ⚠ {file:<30} (파일 없음)")

    # ZIP 파일 정보
    zip_path = Path(zip_filename)
    if zip_path.exists():
        zip_size = zip_path.stat().st_size

        print("\n" + "=" * 60)
        print("  패키징 완료")
        print("=" * 60)
        print(f"\n생성된 파일: {zip_filename}")
        print(f"파일 크기:   {zip_size:,} bytes ({zip_size / 1024:.2f} KB)")

        # ZIP 내용 검증
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            file_count = len(zipf.namelist())
            print(f"포함된 파일: {file_count}개")

        print("\n" + "=" * 60)
        print("  설치 방법")
        print("=" * 60)
        print("\n1. QGIS 플러그인 관리자:")
        print("   - 플러그인 → 플러그인 관리 및 설치")
        print("   - ZIP에서 설치 탭")
        print(f"   - {zip_filename} 선택")
        print("\n2. 수동 설치:")
        print("   - 플러그인 디렉토리로 ZIP 압축 해제")
        print("   - Windows: %APPDATA%\\QGIS\\QGIS3\\profiles\\default\\python\\plugins")
        print("   - Linux: ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
        print("   - macOS: ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins")
        print("\n3. GitHub Release:")
        print("   - GitHub Releases 페이지에 업로드")
        print(f"   - 사용자가 다운로드하여 설치")
        print("\n" + "=" * 60 + "\n")

        return zip_filename
    else:
        print("\n❌ ZIP 파일 생성 실패")
        return None


def verify_package(zip_filename):
    """패키지 무결성 검증"""
    if not Path(zip_filename).exists():
        return False

    print("\n패키지 검증 중...")

    try:
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            # ZIP 파일 무결성 테스트
            bad_file = zipf.testzip()

            if bad_file is not None:
                print(f"❌ 손상된 파일 발견: {bad_file}")
                return False

            # 필수 파일 존재 확인
            namelist = zipf.namelist()
            plugin_name = get_plugin_name()

            required_in_zip = [
                f"{plugin_name}/__init__.py",
                f"{plugin_name}/metadata.txt",
            ]

            for required_file in required_in_zip:
                if required_file not in namelist:
                    print(f"❌ 필수 파일 누락: {required_file}")
                    return False

            print("✓ 패키지 검증 완료 - 문제 없음")
            return True

    except zipfile.BadZipFile:
        print("❌ 잘못된 ZIP 파일")
        return False
    except Exception as e:
        print(f"❌ 검증 실패: {e}")
        return False


def main():
    """메인 함수"""
    # 현재 디렉토리 확인
    if not Path('metadata.txt').exists():
        print("❌ 오류: 플러그인 루트 디렉토리에서 실행해주세요.")
        print("   metadata.txt 파일이 필요합니다.")
        return 1

    # ZIP 파일 생성
    zip_filename = create_plugin_zip()

    if zip_filename is None:
        return 1

    # 패키지 검증
    if not verify_package(zip_filename):
        print("\n⚠  경고: 패키지 검증에 문제가 있습니다.")
        print("   ZIP 파일을 확인해주세요.")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
