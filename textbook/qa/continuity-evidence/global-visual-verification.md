# Ch 1~12 최종 시각 검증

2026-09-10 최종 빌드 뒤 Ch 1~12의 챕터 HTML과 `textbook`, `part1`, `part2`, `part3` 인덱스를 Playwright로 검사했다. 각 HTML을 1280px와 390px에서 열고 본문 최소 글자 크기, 대비, 잘림, 페이지 바깥 배치, SVG 경계, 가로 스크롤, 깨진 이미지, 코드 복사, 전체 코드 복사, 내려받는 노트북의 코드 일치를 확인했다.

```text
대상: 16개 디렉터리
HTML: 103개
뷰: 206개(1280px 103개 + 390px 103개)
통과: 206개
실패: 0개
small/contrast/clipped/outside/svgBounds/horizontal/brokenImages/copyErrors/failureErrors: 모두 0
```

각 디렉터리의 `visual-results.json` 수정 시각이 대상 HTML의 가장 늦은 수정 시각보다 뒤인지 확인했다. 16개 보고서가 모두 이 조건을 만족한다. `global-visual-results.json`에는 103개 HTML 각각의 SHA-256과 수정 시각, 두 viewport의 통과 상태, 원본 시각 보고서의 SHA-256을 기록했다. 따라서 집계가 검사 뒤 HTML 변경 전 상태를 가리키는지 다시 확인할 수 있다.

대표 화면은 Ch 4 01절, Ch 12 01절, 전체 교재 인덱스를 1280px와 390px에서 직접 읽었다. 제목·본문·코드·도식·내려받기 링크가 화면 폭 안에 있고, 모바일에서는 내용이 읽는 순서대로 한 열에 배치됐다. 전체 인덱스의 Part 링크와 챕터 목록도 두 화면 폭에서 겹치거나 잘리지 않았다.

세부 기계 판정과 해시는 `textbook/qa/continuity-evidence/global-visual-results.json`, 대표 스크린샷과 디렉터리별 결과는 `textbook/qa/continuity-evidence/visual/`에 있다.

## Ch 7 최종 문장 교정 후 재검증

최종 언어 감사에서 Ch 7 인덱스 소개 문장 한 곳을 교정하고 다시 빌드한 뒤 Ch 7의 HTML 9개를 1280px와 390px에서 재검사했다. 18개 뷰가 모두 통과했고 모든 오류 항목은 0이었다. Ch 7 인덱스 대표 화면을 두 폭에서 직접 읽어 문장 줄바꿈, 목표 목록, 절 목록의 겹침·잘림이 없음을 확인했다. 그 뒤 `global-visual-results.json`을 다시 생성해 최종 Ch 7 HTML·보고서·스크린샷 해시를 포함한 103개 HTML 해시를 갱신했다.
