from __future__ import annotations

raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")

import json
from pathlib import Path

HERE = Path(__file__).parent
COLORS = {"blue": "#4F86C6", "purple": "#7C3AED", "green": "#2E8B57",
          "yellow": "#F4B942", "red": "#C94C4C", "ink": "#172033"}

SCENES = {
    "01-역할별-메시지": ([
        (40, 55, 190, 70, "system\n공통 역할", "green"),
        (40, 155, 190, 70, "developer\n과업 제약", "green"),
        (40, 255, 190, 70, "user\n고객 문의", "green"),
        (330, 155, 190, 90, "모델 호출\n역할 규칙 적용", "purple"),
        (620, 155, 200, 90, "응답 원문\n사용량 기록", "yellow"),
    ], [(230,90,330,180),(230,190,330,190),(230,290,330,205),(520,200,620,200)]),
    "02-페르소나-과업-제약": ([
        (35, 55, 165, 70, "고객 문의\n고정 입력", "green"),
        (250, 35, 170, 65, "페르소나\n말투·관점", "blue"),
        (250, 125, 170, 65, "과업\n할 일", "blue"),
        (250, 215, 170, 65, "제약·형식\n지킬 조건", "blue"),
        (500, 115, 165, 90, "모델\n응답 생성", "purple"),
        (735, 115, 155, 90, "원문 평가\n길이·토큰", "yellow"),
    ], [(200,90,500,150),(420,68,500,140),(420,158,500,160),(420,248,500,180),(665,160,735,160)]),
    "03-Few-shot-선택": ([
        (30, 40, 190, 65, "예시 후보 A\n파손 교환", "green"),
        (30, 130, 190, 65, "예시 후보 B\n글꼴 설정", "green"),
        (30, 220, 190, 65, "현재 질문\n텀블러 파손", "green"),
        (300, 105, 180, 90, "예시 선택\n관련성 확인", "blue"),
        (570, 105, 150, 90, "모델 호출", "purple"),
        (790, 95, 150, 110, "필수 값·토큰\n원문 정독", "yellow"),
    ], [(220,72,300,130),(220,162,300,165),(220,252,570,180),(480,150,570,150),(720,150,790,150)]),
    "04-메시지-템플릿": ([
        (25, 65, 210, 80, "ChatPromptTemplate\nsystem + human", "blue"),
        (25, 210, 210, 80, "MessagesPlaceholder\noptional history", "blue"),
        (310, 50, 170, 65, "질문 값", "green"),
        (310, 145, 170, 65, "기록 0개/2개", "green"),
        (310, 240, 170, 65, "형식 값", "green"),
        (560, 125, 170, 100, "완성 메시지\n2개/4개", "blue"),
        (800, 125, 130, 100, "모델", "purple"),
    ], [(235,105,560,150),(235,250,560,200),(480,82,560,150),(480,177,560,175),(480,272,560,200),(730,175,800,175)]),
    "05-reasoning-boundary": ([
        (25, 115, 170, 80, "입력 사실\n주문·파손·규정", "green"),
        (270, 105, 170, 100, "모델 호출\n목표·제약", "purple"),
        (515, 55, 205, 75, "공개 결론\n분류·다음 행동", "blue"),
        (515, 180, 205, 75, "짧은 근거\n입력에서 확인", "blue"),
        (790, 105, 170, 100, "도구 반복 루프\nCh 20 후속", "red"),
    ], [(195,155,270,155),(440,155,515,92),(440,155,515,217),(720,155,790,155)]),
    "06-sample-consensus": ([
        (25, 120, 170, 80, "고정 프롬프트\n동일 조건", "green"),
        (260, 35, 150, 65, "독립 표본 1", "purple"),
        (260, 130, 150, 65, "독립 표본 2", "purple"),
        (260, 225, 150, 65, "독립 표본 3", "purple"),
        (480, 105, 180, 105, "LABEL 형식\n열거형 검사", "blue"),
        (735, 60, 180, 80, "엄격 과반수\n합의 라벨", "yellow"),
        (735, 200, 180, 80, "동률·형식 오류\n합의 없음", "red"),
    ], [(195,160,260,68),(195,160,260,162),(195,160,260,258),(410,68,480,135),(410,162,480,157),(410,258,480,180),(660,140,735,100),(660,175,735,240)]),
    "07-structured-diagnosis": ([
        (20, 35, 180, 60, "간단 JSON 지시", "blue"),
        (20, 125, 180, 60, "필드 이름 지시", "blue"),
        (20, 215, 180, 60, "형식·열거형 지시", "blue"),
        (275, 105, 150, 95, "모델 원문", "purple"),
        (500, 55, 160, 70, "json.loads\n파싱 검사", "yellow"),
        (500, 185, 160, 70, "필드 존재\n내용 정독", "yellow"),
        (740, 105, 190, 95, "진단 기록\n성공 축 분리", "blue"),
    ], [(200,65,275,130),(200,155,275,150),(200,245,275,175),(425,150,500,90),(425,150,500,220),(660,90,740,135),(660,220,740,175)]),
    "08-prompt-version-log": ([
        (20, 40, 190, 75, "v1 기준선", "blue"),
        (20, 140, 190, 75, "v2 제약 추가", "blue"),
        (20, 240, 190, 75, "v3 예시 추가", "blue"),
        (275, 95, 175, 110, "고정 입력·모델\n동일 실행 조건", "green"),
        (520, 95, 155, 110, "모델 호출", "purple"),
        (740, 55, 195, 90, "비교표\n토큰·지연·원문", "yellow"),
        (740, 200, 195, 90, "JSON 기록\n프롬프트·응답", "blue"),
    ], [(210,78,275,120),(210,178,275,150),(210,278,275,180),(450,150,520,150),(675,150,740,100),(675,150,740,245)]),
}


def svg_for(boxes, arrows):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 340" role="img">',
             '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#516076"/></marker></defs>',
             '<rect width="980" height="340" rx="18" fill="#F8FAFC"/>']
    for x1,y1,x2,y2 in arrows:
        parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#516076" stroke-width="3" fill="none" marker-end="url(#a)"/>')
    for x,y,w,h,label,color in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{COLORS[color]}" opacity="0.14" stroke="{COLORS[color]}" stroke-width="3"/>')
        lines=label.split("\n")
        start=y+h/2-(len(lines)-1)*12
        for i,line in enumerate(lines):
            parts.append(f'<text x="{x+w/2}" y="{start+i*25}" text-anchor="middle" font-family="sans-serif" font-size="19" font-weight="700" fill="{COLORS["ink"]}">{line}</text>')
    return ''.join(parts)+"</svg>"


def excalidraw_for(boxes, arrows):
    elements = []
    for i,(x,y,w,h,label,color) in enumerate(boxes):
        rid=f"r{i}"
        elements.append({"id":rid,"type":"rectangle","x":x,"y":y,"width":w,"height":h,"strokeColor":COLORS[color],"backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,"roughness":1,"opacity":100,"angle":0,"seed":100+i,"version":1,"versionNonce":200+i,"isDeleted":False,"groupIds":[],"frameId":None,"roundness":{"type":3},"boundElements":[],"updated":1,"link":None,"locked":False})
        elements.append({"id":f"t{i}","type":"text","x":x+12,"y":y+h/2-18,"width":w-24,"height":40,"text":label,"fontSize":19,"fontFamily":1,"textAlign":"center","verticalAlign":"middle","strokeColor":COLORS["ink"],"backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"roughness":1,"opacity":100,"angle":0,"seed":300+i,"version":1,"versionNonce":400+i,"isDeleted":False,"groupIds":[],"frameId":None,"roundness":None,"boundElements":[],"updated":1,"link":None,"locked":False,"containerId":rid,"originalText":label,"autoResize":True,"lineHeight":1.25})
    for i,(x1,y1,x2,y2) in enumerate(arrows):
        elements.append({"id":f"a{i}","type":"arrow","x":x1,"y":y1,"width":x2-x1,"height":y2-y1,"points":[[0,0],[x2-x1,y2-y1]],"lastCommittedPoint":None,"startBinding":None,"endBinding":None,"startArrowhead":None,"endArrowhead":"arrow","strokeColor":"#516076","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,"roughness":1,"opacity":100,"angle":0,"seed":500+i,"version":1,"versionNonce":600+i,"isDeleted":False,"groupIds":[],"frameId":None,"roundness":{"type":2},"boundElements":[],"updated":1,"link":None,"locked":False})
    return {"type":"excalidraw","version":2,"source":"https://excalidraw.com","elements":elements,"appState":{"viewBackgroundColor":"#ffffff"},"files":{}}


for name,(boxes,arrows) in SCENES.items():
    (HERE/f"{name}.svg").write_text(svg_for(boxes,arrows), encoding="utf-8")
    (HERE/f"{name}.excalidraw").write_text(json.dumps(excalidraw_for(boxes,arrows),ensure_ascii=False,indent=2), encoding="utf-8")
    print("wrote", name)
