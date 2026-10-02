"""Generate topic-specific diagrams from one shared element specification."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _figure import linear, render
HERE = Path(__file__).resolve().parent
SPECS = {'01-흐름': {'size': (620, 510),
           'caption': 'model이 작성한 호출 요청의 유무로 분기합니다. ToolNode 실행 결과는 model에 전달되고, 호출 요청이 없는 응답은 END로 이동합니다.',
           'nodes': [('사용자 질문', 'data', 170, 20, 280, 60),
                     ('model', 'model', 170, 120, 280, 60),
                     ('tools_condition', 'code', 170, 230, 280, 60),
                     ('ToolNode', 'tool', 30, 390, 240, 60),
                     ('END', 'code', 350, 390, 240, 60)],
           'edges': [([(310, 80), (310, 116)],),
                     ([(310, 180), (310, 226)],),
                     ([(230, 290), (150, 290), (150, 386)], ('호출 있음', 10, 318, 130)),
                     ([(390, 290), (470, 290), (470, 386)], ('호출 없음', 485, 318, 120)),
                     ([(30, 420), (12, 420), (12, 150), (166, 150)],)]},
 '02-흐름': None,
 '03-흐름': {'size': (620, 570),
           'caption': 'tick 실행 뒤 종료 조건을 검사합니다. 종료 조건이 거짓이면 tick을 반복합니다. recursion_limit은 그래프 전체 실행의 단계 수를 '
                      '제한하며 END 뒤에 실행하는 노드가 아닙니다.',
           'nodes': [('START', 'code', 170, 20, 280, 60),
                     ('tick: 상태 갱신', 'code', 170, 120, 280, 60),
                     ('종료 조건 확인', 'code', 170, 230, 280, 60),
                     ('END', 'code', 350, 380, 240, 60),
                     ('recursion_limit\n실행 단계 수 제한', 'failure', 130, 475, 360, 70)],
           'edges': [([(310, 80), (310, 116)],),
                     ([(310, 180), (310, 226)],),
                     ([(170, 260), (60, 260), (60, 150), (166, 150)], ('계속', 75, 190, 80)),
                     ([(390, 290), (470, 290), (470, 376)], ('종료', 490, 321, 100))]},
 '04-흐름': {'size': (620, 640),
           'caption': '같은 질문으로 fixed와 agent를 각각 실행합니다. 선택 방식만 달리하고 공통 ToolNode와 답변 노드를 거친 뒤 토큰·전체 지연·반복 변동을 '
                      '비교합니다.',
           'nodes': [('같은 질문·자료', 'data', 170, 20, 280, 60),
                     ('fixed: 코드 선택', 'code', 25, 175, 260, 60),
                     ('agent: 모델 선택', 'model', 335, 175, 260, 60),
                     ('공통 ToolNode', 'tool', 170, 310, 280, 60),
                     ('공통 answer', 'model', 170, 430, 280, 60),
                     ('토큰·전체 지연·반복 변동', 'metric', 130, 550, 360, 60)],
           'edges': [([(230, 80), (155, 80), (155, 171)], ('각각 실행', 0, 105, 140)),
                     ([(390, 80), (465, 80), (465, 171)],),
                     ([(155, 235), (155, 275), (240, 275), (240, 306)],),
                     ([(465, 235), (465, 275), (380, 275), (380, 306)],),
                     ([(310, 370), (310, 426)],),
                     ([(310, 490), (310, 546)],)]}}
SPECS["02-흐름"] = linear([('AIMessage 호출 요청', 'data'), ('ToolNode에서 도구 실행', 'tool'), ('ValueError 발생', 'failure'), ('오류 처리 함수', 'code'), ('오류 ToolMessage', 'failure'), ('모델의 안내 답변', 'model')], 'ToolNode가 도구를 실행하다 ValueError를 만나면 사용자 정의 오류 처리 함수가 오류 내용을 ToolMessage로 바꿉니다. 모델은 이 메시지를 읽고 사용자에게 결과를 설명합니다.')

if __name__ == "__main__":
    for name, spec in SPECS.items():
        render(HERE, name, spec)
    print(f"generated {len(SPECS)} SVG/Excalidraw pairs")
