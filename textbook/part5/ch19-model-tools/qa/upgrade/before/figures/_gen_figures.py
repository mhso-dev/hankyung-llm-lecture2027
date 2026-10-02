"""Generate topic-specific diagrams from one shared element specification."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _figure import linear, render
HERE = Path(__file__).resolve().parent
SPECS = [
    ('01-tool과-Ch4-함수-재사용-flow', linear([('Ch 4: fetch_orders()', 'code'), ('고정 경로·공개 status', 'code'), ('@tool: 이름·설명·인자', 'tool'), ('invoke로 직접 호출', 'code'), ('조건에 맞는 주문 목록', 'data')], 'Ch 4 함수에 도구 정보를 더한 뒤 invoke로 호출합니다. CSV 경로는 프로그램이 정하고 모델에 공개하는 인자는 status로 제한합니다.')),
    ('02-Pydantic-인자와-반환-스키마-flow', linear([('입력 인자', 'data'), ('Pydantic 입력 검사', 'code'), ('함수 실행', 'tool'), ('반환값 검사', 'code'), ('검사된 주문 결과', 'data')], '입력 형식이 맞는지 확인한 뒤 함수를 실행하고 반환값을 검사합니다. 검사에 실패하면 해당 단계에서 오류가 발생하며 다음 단계로 진행하지 않습니다.')),
    ('03-좋은-도구-이름과-설명-flow', linear([('함수의 실제 역할', 'tool'), ('역할에 맞는 이름', 'code'), ('사용 조건·제외 조건 설명', 'code'), ('모델이 읽는 도구 정보', 'model')], '함수의 실제 역할을 기준으로 이름과 설명을 작성합니다. 모델은 이 정보를 읽고 도구 사용 여부를 판단합니다.')),
    ('04-설명만으로-도구-선택하기-flow', linear([('같은 질문·모델·도구', 'data'), ('설명문만 변경', 'code'), ('모델의 도구 선택', 'model'), ('선택 이름 기록', 'data'), ('정답과 비교: 두 조건 9/9', 'metric')], '설명문을 바꾼 두 조건을 각각 실행하고 도구 선택을 비교합니다. 이번 실행에서는 두 조건 모두 세 질문을 세 번씩 실행한 아홉 응답에서 올바른 도구를 선택했습니다.')),
    ('05-bind_tools와-병렬-호출-flow', linear([('한 번의 사용자 질문', 'data'), ('모델: 두 호출 요청', 'model'), ('프로그램: 요청 목록 순회', 'code'), ('Python에서 도구 순차 실행', 'tool'), ('각 ID에 맞는 ToolMessage', 'data'), ('모델의 최종 답변', 'model')], '모델이 한 응답에 두 호출 요청을 작성해도 Python 실행 방식은 별도로 정합니다. 이 예제는 요청을 순회하며 순차 실행하고 호출 ID에 맞춰 결과를 반환합니다.')),
    ('06-오류와-읽기-쓰기-분리-flow', linear([('사용자 질문·앱 상태', 'data'), ('앱이 공개할 도구 결정', 'code'), ('모델의 도구 호출 요청', 'model'), ('실행 직전 앱 상태 재확인', 'code'), ('허용된 도구 실행', 'tool'), ('결과 또는 오류 메시지', 'data')], '읽기·쓰기 도구의 공개와 실행 권한은 앱 상태로 결정합니다. 모델이 작성한 인자가 앱의 허용 여부를 대신하지 않습니다.')),
]

if __name__ == "__main__":
    for name, spec in SPECS:
        render(HERE, name, spec)
    print(f"generated {len(SPECS)} SVG/Excalidraw pairs")
