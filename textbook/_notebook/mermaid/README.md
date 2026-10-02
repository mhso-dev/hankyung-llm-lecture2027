# Mermaid 도식 렌더 준비

`QUALITY-UPGRADE.md` §5-3의 Mermaid 도식을 SVG·PNG로 만드는 도구입니다. 원본은 챕터 `figures/{NN}-{순번}-{이름}.mmd`입니다.

## 한 번만 준비 (Cowork Linux 샌드박스, 2026-09-15 확인)

마운트 폴더에는 설치하지 않고 `/tmp`에 둡니다. 약 1.1GB가 필요합니다.

```bash
mkdir -p /tmp/mmd && cd /tmp/mmd
export npm_config_cache=/tmp/npm-cache PUPPETEER_CACHE_DIR=/tmp/pptr-cache
npm install --no-audit --no-fund @mermaid-js/mermaid-cli@11.17.0
rm -rf /tmp/npm-cache
# Chromium 이 libXdamage.so.1 을 찾지 못하면
mkdir -p /tmp/libs && cd /tmp/libs && apt-get download libxdamage1 && dpkg-deb -x libxdamage1_*.deb root
```

## 렌더

```bash
export PUPPETEER_CACHE_DIR=/tmp/pptr-cache
export LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu   # x86_64 환경이면 x86_64-linux-gnu
python3 textbook/_notebook/mermaid/render_mermaid.py textbook/part6/ch22-middleware
```

- `.mmd` 안의 `%% classes` 한 줄은 의미 색 classDef(`flow`·`model`·`tool`·`measure`·`fail`)로 바뀝니다.
- SVG는 그림마다 다른 id를 가지므로 한 페이지에 여러 장을 넣어도 스타일이 섞이지 않습니다.
- 원본과 설정이 바뀌지 않았으면 다시 렌더하지 않습니다(`.render.json`). 전부 다시 만들려면 `--force`.
- 교재 본문에는 `{{mermaid:이름|대체 텍스트|캡션}}`으로 넣습니다. 노트북에는 PNG를 셀 첨부로 넣습니다.
