#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
버전 자동 업데이트 스크립트

이 스크립트는 프로젝트의 버전을 자동으로 증가시킵니다.
Semantic Versioning을 따릅니다: MAJOR.MINOR.PATCH

사용법:
    python bump-version.py major    # 1.0.0 → 2.0.0
    python bump-version.py minor    # 1.0.0 → 1.1.0
    python bump-version.py patch    # 1.0.0 → 1.0.1
"""

import re
import sys
from pathlib import Path
from datetime import datetime


def read_current_version():
    """metadata.txt에서 현재 버전 읽기"""
    metadata_path = Path('metadata.txt')

    if not metadata_path.exists():
        print("❌ metadata.txt 파일을 찾을 수 없습니다.")
        sys.exit(1)

    metadata = metadata_path.read_text(encoding='utf-8')
    match = re.search(r'version=(\d+)\.(\d+)\.(\d+)', metadata)

    if match:
        return tuple(map(int, match.groups()))

    print("❌ metadata.txt에서 버전을 찾을 수 없습니다.")
    print("   형식: version=X.Y.Z")
    sys.exit(1)


def bump_version(version, bump_type):
    """버전 증가"""
    major, minor, patch = version

    if bump_type == 'major':
        return (major + 1, 0, 0)
    elif bump_type == 'minor':
        return (major, minor + 1, 0)
    elif bump_type == 'patch':
        return (major, minor, patch + 1)
    else:
        print(f"❌ 잘못된 bump_type: {bump_type}")
        print("   사용 가능: major, minor, patch")
        sys.exit(1)


def version_to_string(version):
    """버전 튜플을 문자열로 변환"""
    return f"{version[0]}.{version[1]}.{version[2]}"


def update_metadata(old_version, new_version):
    """metadata.txt 업데이트"""
    metadata_path = Path('metadata.txt')
    content = metadata_path.read_text(encoding='utf-8')

    old_str = version_to_string(old_version)
    new_str = version_to_string(new_version)

    updated = content.replace(f'version={old_str}', f'version={new_str}')
    metadata_path.write_text(updated, encoding='utf-8')

    return metadata_path.exists()


def update_init_file(old_version, new_version):
    """__init__.py 업데이트"""
    init_path = Path('__init__.py')

    if not init_path.exists():
        print("⚠  __init__.py 파일을 찾을 수 없습니다.")
        return False

    content = init_path.read_text(encoding='utf-8')

    old_str = version_to_string(old_version)
    new_str = version_to_string(new_version)

    # __version__ 상수가 있으면 업데이트
    if '__version__' in content:
        updated = re.sub(
            r'__version__\s*=\s*["\'][\d.]+["\']',
            f'__version__ = "{new_str}"',
            content
        )
        init_path.write_text(updated, encoding='utf-8')
        return True
    else:
        # 없으면 추가
        lines = content.split('\n')
        # 주석이나 docstring 다음에 추가
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#') and '"""' not in line:
                insert_index = i
                break

        lines.insert(insert_index, f'\n__version__ = "{new_str}"')
        lines.insert(insert_index + 1, f'__version_info__ = {new_version}\n')

        init_path.write_text('\n'.join(lines), encoding='utf-8')
        return True


def update_changelog(new_version):
    """CHANGELOG.md에 새 버전 섹션 추가"""
    changelog_path = Path('CHANGELOG.md')

    if not changelog_path.exists():
        print("⚠  CHANGELOG.md 파일을 찾을 수 없습니다.")
        return False

    content = changelog_path.read_text(encoding='utf-8')
    today = datetime.now().strftime('%Y-%m-%d')
    new_str = version_to_string(new_version)

    # [Unreleased] 섹션 찾기
    unreleased_pattern = r'## \[Unreleased\]'

    if re.search(unreleased_pattern, content):
        # [Unreleased] 다음에 새 버전 섹션 추가
        new_section = f'\n\n## [{new_str}] - {today}\n### Changed\n- 버전 업데이트\n'
        updated = re.sub(
            unreleased_pattern,
            f'## [Unreleased]{new_section}',
            content,
            count=1
        )
        changelog_path.write_text(updated, encoding='utf-8')
        return True
    else:
        print("⚠  CHANGELOG.md에서 [Unreleased] 섹션을 찾을 수 없습니다.")
        return False


def print_summary(old_version, new_version, bump_type):
    """요약 정보 출력"""
    print("\n" + "=" * 50)
    print("  버전 업데이트 완료")
    print("=" * 50)
    print(f"\n유형: {bump_type.upper()}")
    print(f"이전 버전: {version_to_string(old_version)}")
    print(f"새 버전:   {version_to_string(new_version)}")
    print("\n업데이트된 파일:")
    print("  ✓ metadata.txt")
    print("  ✓ __init__.py")
    print("  ✓ CHANGELOG.md")

    new_str = version_to_string(new_version)

    print("\n" + "=" * 50)
    print("  다음 단계")
    print("=" * 50)
    print("\n1. CHANGELOG.md를 편집하여 변경사항을 추가하세요")
    print("\n2. Git에 커밋하고 태그를 생성하세요:")
    print(f"   git add .")
    print(f'   git commit -m "Bump version to {new_str}"')
    print(f'   git tag -a v{new_str} -m "Release v{new_str}"')
    print(f'   git push origin main')
    print(f'   git push origin v{new_str}')
    print("\n3. 플러그인을 패키징하세요:")
    print("   python package.py")
    print("\n" + "=" * 50 + "\n")


def main():
    """메인 함수"""
    # 인수 확인
    if len(sys.argv) != 2 or sys.argv[1] not in ['major', 'minor', 'patch']:
        print("사용법: python bump-version.py [major|minor|patch]")
        print("\n예시:")
        print("  python bump-version.py major    # 주요 버전 증가 (1.0.0 → 2.0.0)")
        print("  python bump-version.py minor    # 부 버전 증가 (1.0.0 → 1.1.0)")
        print("  python bump-version.py patch    # 패치 버전 증가 (1.0.0 → 1.0.1)")
        sys.exit(1)

    bump_type = sys.argv[1]

    # 현재 버전 읽기
    old_version = read_current_version()
    new_version = bump_version(old_version, bump_type)

    old_str = version_to_string(old_version)
    new_str = version_to_string(new_version)

    # 확인
    print(f"\n버전을 {old_str} → {new_str}로 업데이트합니다.")
    print(f"변경 유형: {bump_type.upper()}\n")

    confirm = input("계속하시겠습니까? (y/n): ")

    if confirm.lower() != 'y':
        print("취소되었습니다.")
        sys.exit(0)

    # 파일 업데이트
    print("\n파일 업데이트 중...")

    if update_metadata(old_version, new_version):
        print("  ✓ metadata.txt")
    else:
        print("  ❌ metadata.txt 업데이트 실패")

    if update_init_file(old_version, new_version):
        print("  ✓ __init__.py")
    else:
        print("  ⚠  __init__.py 업데이트 건너뜀")

    if update_changelog(new_version):
        print("  ✓ CHANGELOG.md")
    else:
        print("  ⚠  CHANGELOG.md 업데이트 건너뜀")

    # 요약 출력
    print_summary(old_version, new_version, bump_type)


if __name__ == '__main__':
    main()
