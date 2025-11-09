# GIS SHP Loader - 버전 관리 및 업그레이드 전략

## 📋 목차
1. [개요](#개요)
2. [버전 관리 전략](#버전-관리-전략)
3. [버전 업데이트 프로세스](#버전-업데이트-프로세스)
4. [클라이언트 업그레이드 메커니즘](#클라이언트-업그레이드-메커니즘)
5. [배포 전략](#배포-전략)
6. [구현 로드맵](#구현-로드맵)

---

## 개요

### 현재 상태
- **버전**: 0.1 (초기 개발 단계)
- **프로젝트 타입**: QGIS 3.0+ 플러그인
- **배포 방식**: 수동 설치
- **버전 관리**: 기본적 (metadata.txt만 존재)

### 목표
- **체계적인 버전 관리** 시스템 구축
- **자동화된 릴리스** 프로세스 확립
- **사용자 친화적 업그레이드** 경험 제공
- **투명한 변경 이력** 관리

---

## 버전 관리 전략

### 1. Semantic Versioning (유의적 버전)

**형식**: `MAJOR.MINOR.PATCH` (예: 1.2.3)

```
MAJOR: 주요 버전 (호환성이 깨지는 변경)
  - QGIS API 대규모 변경
  - 플러그인 구조 전면 개편
  - 이전 버전과 호환되지 않는 변경

MINOR: 부 버전 (기능 추가)
  - 새로운 기능 추가
  - 기존 기능 향상
  - 하위 호환성 유지

PATCH: 패치 버전 (버그 수정)
  - 버그 수정
  - 성능 개선
  - 문서 업데이트
```

### 2. 버전 정보 관리 위치

#### A. `metadata.txt` (필수 - QGIS 표준)
```ini
[general]
name=GIS SHP Loader
qgisMinimumVersion=3.0
qgisMaximumVersion=3.99
version=1.0.0
author=QGIS User
email=developer@example.com
description=여러 폴더에서 동일한 이름의 shapefile을 로드하는 플러그인
about=이 플러그인은 지정된 이름의 Shapefile을 여러 하위 폴더에서 일괄 로드합니다.
tracker=https://github.com/qbong1010/gis_shp-loader/issues
repository=https://github.com/qbong1010/gis_shp-loader
homepage=https://github.com/qbong1010/gis_shp-loader
changelog=CHANGELOG.md 참조
tags=shapefile, batch, loader, GIS
category=Vector
icon=icon.png
experimental=False
deprecated=False
```

#### B. `__init__.py` (버전 상수)
```python
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
```

#### C. `CHANGELOG.md` (변경 이력)
```markdown
# Changelog

## [Unreleased]
### Added
- 새로운 기능 목록

## [1.0.0] - 2025-11-09
### Added
- 초기 릴리스
- 배치 Shapefile 로딩 기능
```

#### D. Git Tags (릴리스 마킹)
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
```

### 3. 개발 브랜치 전략

```
main (또는 master)
  ├── develop (개발 브랜치)
  │     ├── feature/새기능명
  │     └── fix/버그수정명
  └── release/v1.0.0 (릴리스 준비)
```

**브랜치 규칙**:
- `main`: 안정화된 릴리스만
- `develop`: 개발 중인 최신 코드
- `feature/*`: 새 기능 개발
- `fix/*`: 버그 수정
- `release/*`: 릴리스 준비

---

## 버전 업데이트 프로세스

### 1. 자동화 도구: `bump-version.py`

새 파일 생성 추천:

```python
#!/usr/bin/env python3
"""
버전 자동 업데이트 스크립트
사용법: python bump-version.py [major|minor|patch]
"""

import re
import sys
from pathlib import Path

def read_current_version():
    """metadata.txt에서 현재 버전 읽기"""
    metadata = Path('metadata.txt').read_text(encoding='utf-8')
    match = re.search(r'version=(\d+)\.(\d+)\.(\d+)', metadata)
    if match:
        return tuple(map(int, match.groups()))
    raise ValueError("버전을 찾을 수 없습니다")

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
        raise ValueError("bump_type은 major, minor, patch 중 하나여야 합니다")

def update_files(old_version, new_version):
    """모든 파일의 버전 업데이트"""
    old_str = f"{old_version[0]}.{old_version[1]}.{old_version[2]}"
    new_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"

    files_to_update = [
        'metadata.txt',
        '__init__.py',
        'README.md'
    ]

    for file_path in files_to_update:
        path = Path(file_path)
        if path.exists():
            content = path.read_text(encoding='utf-8')
            updated = content.replace(old_str, new_str)
            path.write_text(updated, encoding='utf-8')
            print(f"✓ {file_path} 업데이트: {old_str} → {new_str}")

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['major', 'minor', 'patch']:
        print("사용법: python bump-version.py [major|minor|patch]")
        sys.exit(1)

    bump_type = sys.argv[1]
    old_version = read_current_version()
    new_version = bump_version(old_version, bump_type)

    print(f"버전 업데이트: {'.'.join(map(str, old_version))} → {'.'.join(map(str, new_version))}")

    confirm = input("계속하시겠습니까? (y/n): ")
    if confirm.lower() == 'y':
        update_files(old_version, new_version)
        print(f"\n다음 단계:")
        print(f"1. git add .")
        print(f"2. git commit -m 'Bump version to {'.'.join(map(str, new_version))}'")
        print(f"3. git tag -a v{'.'.join(map(str, new_version))} -m 'Release v{'.'.join(map(str, new_version))}'")
    else:
        print("취소되었습니다")
```

### 2. 릴리스 체크리스트

#### 릴리스 준비
- [ ] 모든 기능 개발 완료
- [ ] 코드 리뷰 완료
- [ ] 테스트 통과 (수동/자동)
- [ ] CHANGELOG.md 업데이트
- [ ] README.md 업데이트
- [ ] 버전 번호 결정 (Semantic Versioning)

#### 버전 업데이트
```bash
# 1. 버전 자동 증가
python bump-version.py minor  # 또는 major/patch

# 2. 변경사항 커밋
git add .
git commit -m "Bump version to 1.1.0"

# 3. Git 태그 생성
git tag -a v1.1.0 -m "Release version 1.1.0"

# 4. 원격 저장소에 푸시
git push origin main
git push origin v1.1.0
```

#### 패키징 및 배포
```bash
# 5. 플러그인 ZIP 생성
python package.py  # (아래 참조)

# 6. GitHub Release 생성
# GitHub UI 또는 gh CLI 사용

# 7. QGIS 플러그인 저장소 업로드 (선택)
```

---

## 클라이언트 업그레이드 메커니즘

### 1. QGIS 기본 플러그인 관리자 활용

**장점**:
- QGIS에 내장된 업데이트 확인 기능
- 사용자에게 친숙한 UI
- 자동 업데이트 알림

**설정 방법**:

#### A. 플러그인 저장소 등록

**공식 QGIS 플러그인 저장소**: https://plugins.qgis.org/

등록 절차:
1. https://plugins.qgis.org/ 계정 생성
2. 플러그인 업로드 (ZIP 파일)
3. metadata.txt 검증
4. 승인 대기

#### B. 사설 플러그인 저장소 구축

조직 내부용 또는 베타 테스트용:

```xml
<!-- plugins.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<plugins>
  <pyqgis_plugin name="GIS SHP Loader" version="1.0.0">
    <description>여러 폴더에서 동일한 이름의 shapefile을 로드하는 플러그인</description>
    <about>배치 Shapefile 로딩 도구</about>
    <version>1.0.0</version>
    <qgis_minimum_version>3.0</qgis_minimum_version>
    <homepage>https://github.com/qbong1010/gis_shp-loader</homepage>
    <file_name>gis_shp_loader.1.0.0.zip</file_name>
    <icon>https://example.com/icon.png</icon>
    <author_name>QGIS User</author_name>
    <download_url>https://github.com/qbong1010/gis_shp-loader/releases/download/v1.0.0/gis_shp_loader.zip</download_url>
    <uploaded_by>developer</uploaded_by>
    <create_date>2025-11-09</create_date>
    <update_date>2025-11-09</update_date>
    <experimental>False</experimental>
    <deprecated>False</deprecated>
    <tracker>https://github.com/qbong1010/gis_shp-loader/issues</tracker>
    <repository>https://github.com/qbong1010/gis_shp-loader</repository>
    <tags>shapefile,batch,loader</tags>
  </pyqgis_plugin>
</plugins>
```

**호스팅 옵션**:
- GitHub Pages (무료)
- AWS S3 + CloudFront
- 자체 웹 서버

### 2. 플러그인 내부 업데이트 확인 기능

`gis_shp_loader.py`에 추가:

```python
import urllib.request
import json
from packaging import version

class GisSHPLoader:
    # 기존 코드...

    def check_for_updates(self):
        """GitHub API를 통한 최신 버전 확인"""
        try:
            url = "https://api.github.com/repos/qbong1010/gis_shp-loader/releases/latest"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data['tag_name'].lstrip('v')
                current_version = "0.1"  # metadata에서 읽어오기

                if version.parse(latest_version) > version.parse(current_version):
                    self.show_update_notification(latest_version, data['html_url'])
        except Exception as e:
            # 조용히 실패 (인터넷 연결 없을 수 있음)
            pass

    def show_update_notification(self, new_version, download_url):
        """업데이트 알림 표시"""
        from qgis.PyQt.QtWidgets import QMessageBox

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("업데이트 가능")
        msg.setText(f"GIS SHP Loader의 새 버전이 있습니다!")
        msg.setInformativeText(
            f"현재 버전: {self.get_current_version()}\n"
            f"최신 버전: {new_version}\n\n"
            f"업데이트하시겠습니까?"
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            import webbrowser
            webbrowser.open(download_url)

    def initGui(self):
        # 기존 코드...

        # 플러그인 로드 시 업데이트 확인 (백그라운드)
        from qgis.PyQt.QtCore import QTimer
        QTimer.singleShot(2000, self.check_for_updates)  # 2초 후 확인
```

### 3. 사용자 업그레이드 프로세스

#### 방법 1: QGIS 플러그인 관리자 (권장)

1. QGIS 메뉴: `플러그인 → 플러그인 관리 및 설치`
2. `설치된 플러그인` 탭에서 "GIS SHP Loader" 확인
3. 업데이트 가능 시 `업그레이드` 버튼 클릭
4. QGIS 재시작

#### 방법 2: 수동 설치

1. GitHub Releases 페이지 방문
2. 최신 `.zip` 파일 다운로드
3. QGIS 메뉴: `플러그인 → 플러그인 관리 및 설치 → ZIP에서 설치`
4. 다운로드한 ZIP 파일 선택
5. QGIS 재시작

#### 방법 3: 명령줄 (고급 사용자)

```bash
# 플러그인 디렉토리로 이동
cd %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins

# 기존 플러그인 삭제
rmdir /s gis_shp-loader

# 새 버전 다운로드 및 압축 해제
curl -L https://github.com/qbong1010/gis_shp-loader/releases/latest/download/gis_shp_loader.zip -o gis_shp_loader.zip
unzip gis_shp_loader.zip
del gis_shp_loader.zip
```

---

## 배포 전략

### 1. 패키징 자동화

`package.py` 스크립트 생성:

```python
#!/usr/bin/env python3
"""
QGIS 플러그인 패키징 스크립트
사용법: python package.py
"""

import zipfile
import shutil
from pathlib import Path
import re

def get_version():
    """metadata.txt에서 버전 읽기"""
    metadata = Path('metadata.txt').read_text(encoding='utf-8')
    match = re.search(r'version=(\d+\.\d+\.\d+)', metadata)
    return match.group(1) if match else "unknown"

def create_plugin_zip():
    """플러그인 ZIP 파일 생성"""
    version = get_version()
    plugin_name = "gis_shp_loader"
    zip_filename = f"{plugin_name}.{version}.zip"

    # 포함할 파일 목록
    include_files = [
        '__init__.py',
        'gis_shp_loader.py',
        'gis_shp_loader_dialog.py',
        'metadata.txt',
        'icon.png',
        'README.md',
        'LICENSE'
    ]

    # 제외할 패턴
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '.git',
        '.gitignore',
        '*.zip',
        'package.py',
        'bump-version.py'
    ]

    print(f"패키징 중: {plugin_name} v{version}")

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in include_files:
            if Path(file).exists():
                zipf.write(file, f"{plugin_name}/{file}")
                print(f"  ✓ {file}")
            else:
                print(f"  ⚠ {file} (없음)")

    print(f"\n생성 완료: {zip_filename}")
    print(f"크기: {Path(zip_filename).stat().st_size / 1024:.2f} KB")
    return zip_filename

if __name__ == '__main__':
    create_plugin_zip()
```

### 2. GitHub Actions CI/CD

`.github/workflows/release.yml` 생성:

```yaml
name: Release Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Get version from tag
      id: get_version
      run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

    - name: Package plugin
      run: python package.py

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: gis_shp_loader.*.zip
        body_path: CHANGELOG.md
        draft: false
        prerelease: false
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Upload to QGIS Plugin Repository
      if: success()
      run: |
        # QGIS 플러그인 저장소 업로드 스크립트
        # (선택사항 - API 키 필요)
        echo "수동 업로드 필요: https://plugins.qgis.org/"
```

### 3. 릴리스 채널

#### Stable (안정 버전)
- `main` 브랜치의 태그된 릴리스
- 철저한 테스트 완료
- 일반 사용자용

#### Beta (베타 버전)
- `develop` 브랜치의 태그된 릴리스
- 기능 테스트 중
- 얼리 어답터용
- metadata.txt에 `experimental=True` 설정

#### Nightly (개발 버전)
- `develop` 브랜치의 최신 커밋
- 자동 빌드
- 개발자 전용

---

## 구현 로드맵

### Phase 1: 기본 인프라 (1-2주)

**우선순위: 높음**

- [ ] **버전 관리 시스템 구축**
  - [ ] `CHANGELOG.md` 생성
  - [ ] `__init__.py`에 버전 상수 추가
  - [ ] `metadata.txt` 완성 (repository, tracker URL 등)

- [ ] **자동화 스크립트 작성**
  - [ ] `bump-version.py` 구현
  - [ ] `package.py` 구현
  - [ ] 사용 문서화

- [ ] **Git 브랜치 전략 수립**
  - [ ] `main`, `develop` 브랜치 생성
  - [ ] 브랜치 보호 규칙 설정
  - [ ] 커밋 메시지 컨벤션 정의

### Phase 2: 배포 자동화 (2-3주)

**우선순위: 중간**

- [ ] **GitHub Actions 설정**
  - [ ] 릴리스 자동화 워크플로우
  - [ ] 테스트 자동화 (optional)
  - [ ] 코드 품질 검사

- [ ] **릴리스 프로세스 확립**
  - [ ] GitHub Releases 템플릿 작성
  - [ ] 릴리스 노트 자동 생성
  - [ ] ZIP 파일 자동 첨부

### Phase 3: 업데이트 메커니즘 (3-4주)

**우선순위: 낮음 (선택)**

- [ ] **플러그인 내부 업데이트 확인**
  - [ ] GitHub API 연동
  - [ ] 버전 비교 로직
  - [ ] 사용자 알림 UI

- [ ] **플러그인 저장소 설정**
  - [ ] QGIS 공식 저장소 등록 (또는)
  - [ ] 사설 저장소 구축 (GitHub Pages)

### Phase 4: 품질 개선 (지속적)

**우선순위: 낮음**

- [ ] **테스트 작성**
  - [ ] 단위 테스트 (pytest)
  - [ ] 통합 테스트
  - [ ] QGIS 플러그인 테스트 프레임워크

- [ ] **문서화**
  - [ ] 사용자 매뉴얼 (한국어/영어)
  - [ ] API 문서
  - [ ] 개발자 가이드

- [ ] **사용자 피드백 수집**
  - [ ] GitHub Issues 템플릿
  - [ ] 사용 통계 (선택)
  - [ ] 사용자 설문

---

## 빠른 시작 가이드

### 첫 정식 릴리스 (v1.0.0) 준비

```bash
# 1. 문서 준비
echo "# Changelog\n\n## [1.0.0] - 2025-11-09\n### Added\n- 초기 릴리스" > CHANGELOG.md

# 2. metadata.txt 업데이트
# repository, tracker, homepage URL 추가

# 3. 버전을 1.0.0으로 설정
python bump-version.py  # 수동으로 1.0.0 설정

# 4. 패키징
python package.py

# 5. Git 커밋 및 태그
git add .
git commit -m "Release v1.0.0"
git tag -a v1.0.0 -m "First stable release"
git push origin main
git push origin v1.0.0

# 6. GitHub Release 생성
# GitHub UI에서 수동 생성 또는:
gh release create v1.0.0 gis_shp_loader.1.0.0.zip \
  --title "GIS SHP Loader v1.0.0" \
  --notes-file CHANGELOG.md
```

---

## 참고 자료

### QGIS 플러그인 개발
- [QGIS Plugin Development Guide](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/plugins/index.html)
- [QGIS Plugin Repository](https://plugins.qgis.org/)
- [Plugin Metadata Reference](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/plugins/metadata.html)

### 버전 관리
- [Semantic Versioning](https://semver.org/lang/ko/)
- [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

### 자동화
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Packaging](https://packaging.python.org/)

---

## 결론

이 문서는 GIS SHP Loader 플러그인의 체계적인 버전 관리와 사용자 친화적인 업그레이드 프로세스를 위한 포괄적인 전략을 제시합니다.

**핵심 원칙**:
1. **투명성**: 모든 변경사항을 명확히 문서화
2. **자동화**: 수동 작업 최소화로 오류 방지
3. **사용자 중심**: 쉬운 업그레이드 경험 제공
4. **표준 준수**: QGIS 및 업계 모범 사례 따르기

**다음 단계**: [구현 로드맵](#구현-로드맵) Phase 1부터 시작하세요.
