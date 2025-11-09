# GIS SHP Loader

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/qbong1010/gis_shp-loader/releases)
[![QGIS](https://img.shields.io/badge/QGIS-3.0+-green.svg)](https://qgis.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

이 QGIS 플러그인은 여러 폴더에서 동일한 이름의 Shapefile(.shp)을 일괄적으로 로드하는 기능을 제공합니다.

## 기능

- 지정된 상위 폴더 내의 모든 하위 폴더에서 동일한 이름의 Shapefile 파일을 일괄 로드
- 로드된 레이어는 폴더명_파일명 형식으로 표시됨
- 사용자 인터페이스를 통해 상위 폴더와 로드할 파일명 지정 가능

## 설치 방법

1. QGIS 플러그인 디렉토리에 이 플러그인을 복사합니다.
   (일반적으로 `C:\Users\[사용자명]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`)
2. QGIS를 재시작하거나 플러그인 관리자에서 플러그인을 활성화합니다.

## 사용 방법

1. QGIS 상단 메뉴 또는 툴바에서 "SHP 파일 로더" 아이콘을 클릭합니다.
2. 대화 상자에서 다음 정보를 입력합니다:
   - 상위 폴더 경로 (예: `C:\Users\dohwa\Desktop\경기_남양주시`)
   - 로드할 Shapefile 이름 (예: `A0010000.shp`)
3. "확인" 버튼을 클릭하면 자동으로 모든 하위 폴더에서 지정된 파일을 찾아 로드합니다.
4. 로드 완료 후 작업 결과가 메시지 상자로 표시됩니다.

## 사용 예시

폴더 구조:
```
C:\Users\dohwa\Desktop\경기_남양주시\
  ├─ 37701096\
  │    └─ A0010000.shp
  ├─ 37701097\
  │    └─ A0010000.shp
  └─ 37701098\
       └─ A0010000.shp
```

위와 같은 구조에서 플러그인을 실행하면 각 폴더의 `A0010000.shp` 파일이 `37701096_A0010000`, `37701097_A0010000`, `37701098_A0010000` 등의 레이어 이름으로 QGIS에 로드됩니다.

## 버전 정보

현재 버전: **0.1.0**

전체 변경 이력은 [CHANGELOG.md](CHANGELOG.md)를 참조하세요.

### 최신 릴리스 다운로드

최신 버전은 [GitHub Releases](https://github.com/qbong1010/gis_shp-loader/releases)에서 다운로드할 수 있습니다.

## 요구사항

- QGIS 3.0 이상
- Python 3.6 이상

## 개발 가이드

### 버전 업데이트

이 프로젝트는 [Semantic Versioning](https://semver.org/lang/ko/)을 따릅니다.

```bash
# 버전 증가 (major/minor/patch)
python bump-version.py minor

# 변경사항 커밋
git add .
git commit -m "Bump version to X.Y.Z"

# 태그 생성 및 푸시
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

### 플러그인 패키징

```bash
# ZIP 파일 생성
python package.py

# 생성된 파일: gis_shp_loader.X.Y.Z.zip
```

### 릴리스 프로세스

1. `CHANGELOG.md` 업데이트
2. 버전 번호 증가: `python bump-version.py [major|minor|patch]`
3. 변경사항 커밋 및 태그 생성
4. GitHub에 푸시하면 자동으로 릴리스 생성 (GitHub Actions)

자세한 내용은 [VERSIONING_STRATEGY.md](VERSIONING_STRATEGY.md)를 참조하세요.

## 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

1. 이 저장소를 Fork합니다
2. Feature 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 문의

버그를 발견하거나 기능을 제안하고 싶으시면 [GitHub Issues](https://github.com/qbong1010/gis_shp-loader/issues)에 등록해주세요.

## 크레딧

개발: QGIS User

---

**Note**: 이 플러그인은 대량의 Shapefile을 폴더별로 구성하여 작업하는 GIS 전문가를 위해 개발되었습니다. 