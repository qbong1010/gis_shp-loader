# 버전 관리 빠른 시작 가이드

이 가이드는 GIS SHP Loader의 버전 관리 시스템을 빠르게 시작할 수 있도록 도와줍니다.

## 📦 첫 릴리스 만들기 (v1.0.0)

현재 프로젝트는 v0.1.0 상태입니다. 첫 정식 릴리스를 만들려면:

```bash
# 1. CHANGELOG.md 업데이트
# [Unreleased] 섹션에 변경사항 추가

# 2. 버전을 1.0.0으로 증가
python bump-version.py major  # 0.1.0 → 1.0.0

# 3. 플러그인 패키징 (선택사항 - 테스트용)
python package.py

# 4. Git에 커밋
git add .
git commit -m "Release v1.0.0"

# 5. 태그 생성
git tag -a v1.0.0 -m "Release v1.0.0"

# 6. 푸시 (GitHub Actions가 자동으로 릴리스 생성)
git push origin claude/plan-versioning-strategy-011CUx8bmb43pugB4LNu9Lrx
git push origin v1.0.0
```

## 🔄 일상적인 버전 업데이트

### 버그 수정 릴리스 (Patch)

```bash
python bump-version.py patch  # 1.0.0 → 1.0.1
git add .
git commit -m "Bump version to 1.0.1"
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin main
git push origin v1.0.1
```

### 새 기능 릴리스 (Minor)

```bash
python bump-version.py minor  # 1.0.1 → 1.1.0
git add .
git commit -m "Bump version to 1.1.0"
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main
git push origin v1.1.0
```

### 주요 변경 릴리스 (Major)

```bash
python bump-version.py major  # 1.1.0 → 2.0.0
git add .
git commit -m "Bump version to 2.0.0"
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin main
git push origin v2.0.0
```

## 📝 CHANGELOG.md 작성 팁

릴리스 전에 항상 CHANGELOG.md를 업데이트하세요:

```markdown
## [Unreleased]
### Added
- 새로 추가된 기능

### Changed
- 변경된 기능

### Fixed
- 수정된 버그
```

## 🤖 자동화된 것들

태그를 푸시하면 GitHub Actions가 자동으로:

1. ✅ 버전 번호 검증 (metadata.txt와 태그 일치 확인)
2. 📦 플러그인 ZIP 파일 생성
3. 📄 CHANGELOG에서 릴리스 노트 추출
4. 🚀 GitHub Release 생성
5. 📎 ZIP 파일 첨부

## 🎯 체크리스트

릴리스하기 전에 확인:

- [ ] CHANGELOG.md 업데이트 완료
- [ ] 모든 변경사항 커밋 완료
- [ ] 로컬에서 테스트 완료
- [ ] bump-version.py 실행 완료
- [ ] 버전 번호가 올바른지 확인

## 🛠️ 유용한 명령어

```bash
# 현재 버전 확인
grep "version=" metadata.txt

# 최근 태그 확인
git tag -l

# 태그 삭제 (실수한 경우)
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# ZIP 파일 테스트
python package.py
unzip -l gis_shp_loader.*.zip
```

## ❓ 문제 해결

### 버전이 맞지 않는 경우

```bash
# 수동으로 metadata.txt 수정
vim metadata.txt  # version=X.Y.Z

# __init__.py도 수정
vim __init__.py   # __version__ = "X.Y.Z"
```

### GitHub Actions 실패

1. GitHub에서 Actions 탭 확인
2. 실패 로그 확인
3. 버전 불일치가 주 원인인 경우가 많음

### 태그를 다시 만들어야 하는 경우

```bash
# 로컬 태그 삭제
git tag -d v1.0.0

# 원격 태그 삭제
git push origin :refs/tags/v1.0.0

# 새로 태그 생성
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## 📚 더 자세한 정보

- [VERSIONING_STRATEGY.md](VERSIONING_STRATEGY.md) - 전체 전략 문서
- [CHANGELOG.md](CHANGELOG.md) - 변경 이력
- [README.md](README.md) - 프로젝트 정보
