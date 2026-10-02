# 2026-09-29 Ch 29 01절 품질 개선: 옛 도식(NN-흐름.svg·.excalidraw·.caption.md 열둘)을 만드는 옛 생성기입니다.
# 개선본 그림은 절마다 figures/NN-k-이름.mmd(Mermaid)와 삽화 PNG가 대신합니다(QUALITY-UPGRADE.md §5·§8).
# 이 파일을 실행하면 옛 그림을 다시 쓰려 하므로, 아래 줄에서 실행을 막습니다. 옮기기(mv -n)는 챕터 마감 몫입니다.
"""Ch29 개념 도식을 SVG와 Excalidraw JSON으로 생성합니다."""
raise SystemExit("옛 Ch 29 도식 생성기입니다. 개선본 그림은 figures/NN-k-이름.mmd와 삽화 PNG를 쓰세요.")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))
from _figure import linear, render

HERE = Path(__file__).resolve().parent
SPECS = {
    "01-흐름": linear([("고정 예시 궤적", "code"), ("Final Response", "metric"), ("Single step", "metric"), ("Trajectory", "metric")], "코드로 만든 한 예시 궤적을 최종 응답, 한 단계, 전체 궤적의 세 수준에서 평가합니다."),
    "02-흐름": linear([("기준 궤적", "data"), ("strict", "code"), ("unordered", "code"), ("subset", "code"), ("superset", "code")], "strict는 순서까지 같아야 하고 unordered는 순서를 무시합니다. subset과 superset은 실제 호출과 기준 호출의 포함 관계를 검사합니다."),
    "03-흐름": linear([("고정 예시 궤적", "code"), ("평가 루브릭", "data"), ("LLM judge", "model"), ("점수·설명", "metric")], "LLM judge는 코드로 만든 예시 궤적과 루브릭을 함께 읽고 점수와 설명을 반환합니다."),
    "04-흐름": linear([("Ch18 실제 출력", "data"), ("공통 열 변환", "code"), ("스텝·도구·토큰", "metric"), ("지연·비용 p95", "metric")], "Ch18 워크플로우 기록과 에이전트 궤적을 공통 운영 열로 변환해 분포를 비교합니다."),
}
if __name__ == "__main__":
    for name, spec in SPECS.items():
        render(HERE, name, spec)
    print("generated", len(SPECS))
