# Changelog

이 프로젝트의 모든 주목할 만한 변경사항은 이 파일에 문서화됩니다.

이 형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 기반으로 하며,
이 프로젝트는 [Semantic Versioning](https://semver.org/lang/ko/)을 준수합니다.

## [Unreleased]
### 추가 예정
- 플러그인 내부 업데이트 확인 기능
- 다국어 지원 (영어)
- 진행 상태 표시 바

### 개선 예정
- 오류 처리 및 사용자 피드백
- 성능 최적화

## [0.1.0] - 2025-11-09
### Added
- 초기 릴리스
- 배치 Shapefile 로딩 기능
  - 여러 하위 폴더에서 동일한 이름의 Shapefile 자동 검색
  - 레이어 자동 생성 및 QGIS 프로젝트에 추가
  - 폴더명 기반 레이어 이름 지정
- 사용자 인터페이스
  - 폴더 선택 대화상자
  - Shapefile 이름 입력 필드
  - 기본 경로 설정
- QGIS 통합
  - 메뉴 항목 추가
  - 툴바 아이콘 추가
- 버전 관리 시스템
  - Semantic Versioning 도입
  - CHANGELOG.md 생성
  - 자동화 스크립트 (bump-version.py, package.py)
  - GitHub Actions CI/CD 설정

### Technical Details
- QGIS 3.0+ 호환
- PyQt5 기반 UI
- Python 3 지원

---

## 변경 유형 설명

- **Added**: 새로운 기능
- **Changed**: 기존 기능의 변경
- **Deprecated**: 곧 제거될 기능
- **Removed**: 제거된 기능
- **Fixed**: 버그 수정
- **Security**: 보안 취약점 수정

---

## 릴리스 링크

<!--
GitHub Releases에서 자동으로 생성됩니다.
예시:
- [0.1.0]: https://github.com/qbong1010/gis_shp-loader/releases/tag/v0.1.0
-->
