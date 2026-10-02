"""Generate matching editable Excalidraw elements and inline SVG figures."""
from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GREEN, BLUE, YELLOW = '#dcfce7', '#dbeafe', '#fef3c7'
PURPLE, RED = '#ede9fe', '#fee2e2'
FIGURES = {
    '01-cache-flow': ('공통 접두어와 캐시 읽기 계측',
        [('공통 접두어', GREEN), ('모델 호출\n요청 1 · 요청 2', PURPLE), ('일반 입력 ·\ncache read', YELLOW)]),
    '02-batch-flow': ('Batch 입력 파일 검증 범위',
        [('요청 3건', GREEN), ('JSONL 검증', BLUE), ('외부 제출 전\n중단', BLUE)]),
    '03-routing-flow': ('모델 선택과 품질·비용 확인',
        [('고객 요청', GREEN), ('난이도 규칙', BLUE), ('nano · mini', PURPLE), ('품질 · 비용', YELLOW)]),
    '04-rate-limit-flow': ('로컬 429 응답과 재시도',
        [('로컬 429 응답', RED), ('백오프 · 지터', BLUE), ('재시도 후 200', GREEN)]),
    '05-budget-flow': ('대화별 비용 집계와 예산 검사',
        [('호출 기록', GREEN), ('대화별 합계\n· p95', YELLOW), ('예산 가드\n허용 · 차단', BLUE)]),
}


def element(kind, identifier, x, y, width, height, **extra):
    return dict(id=identifier, type=kind, x=x, y=y, width=width, height=height,
                angle=0, strokeColor='#334155', backgroundColor='transparent',
                fillStyle='solid', strokeWidth=2, strokeStyle='solid', roughness=0,
                opacity=100, groupIds=[], frameId=None, roundness=None, seed=1,
                version=1, versionNonce=1, isDeleted=False, boundElements=None,
                updated=1, link=None, locked=False, **extra)


def main():
    for slug, (title, nodes) in FIGURES.items():
        pieces = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 250" role="img" aria-label="'+html.escape(title)+'">',
                  '<rect width="800" height="250" fill="white"/>',
                  '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#334155"/></marker></defs>',
                  f'<text x="400" y="42" text-anchor="middle" font-size="24" fill="#0f172a">{html.escape(title)}</text>']
        elements = []
        positions = [35+i*185 for i in range(len(nodes))]
        if len(nodes)==3:
            positions = [75,325,575]
        elements.append(element('text','title',40,16,720,30,text=title,originalText=title,fontSize=24,fontFamily=2,textAlign='center',verticalAlign='middle',containerId=None,autoResize=False,lineHeight=1.25))
        for index, ((label, color), x) in enumerate(zip(nodes, positions)):
            # The last two operational signals branch from the running app.
            y = 95 if slug != '05-운영신호' or index < 2 else (70 if index==2 else 160)
            if slug=='05-운영신호' and index==3:
                x=positions[2]
            elements.append(element('rectangle',f'box{index}',x,y,155,65))
            elements[-1]['backgroundColor']=color
            elements.append(element('text',f'text{index}',x+5,y+10,145,48,text=label,originalText=label,fontSize=16,fontFamily=2,textAlign='center',verticalAlign='middle',containerId=None,autoResize=False,lineHeight=1.25))
            pieces.append(f'<rect x="{x}" y="{y}" width="155" height="65" rx="10" fill="{color}" stroke="#334155"/>')
            lines=label.split('\n')
            for row, line in enumerate(lines):
                baseline=y+(29 if len(lines)>1 else 38)+row*21
                pieces.append(f'<text x="{x+77.5}" y="{baseline}" text-anchor="middle" font-size="16" fill="#0f172a">{html.escape(line)}</text>')
            if index:
                start_x=positions[index-1]+155
                start_y=127.5
                if slug=='05-운영신호' and index==3:
                    start_x=positions[1]+155
                end_x=x-8
                end_y=y+32.5
                dx,dy=end_x-start_x,end_y-start_y
                elements.append(element('arrow',f'arrow{index}',start_x,start_y,abs(dx),abs(dy),points=[[0,0],[dx,dy]],startBinding=None,endBinding=None,startArrowhead=None,endArrowhead='arrow',elbowed=False))
                pieces.append(f'<path d="M{start_x} {start_y}L{end_x} {end_y}" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#arrow)"/>')
        pieces.append('</svg>')
        (HERE/f'{slug}.svg').write_text(''.join(pieces))
        (HERE/f'{slug}.excalidraw').write_text(json.dumps({'type':'excalidraw','version':2,'source':'https://excalidraw.com','elements':elements,'appState':{'viewBackgroundColor':'#ffffff'},'files':{}},ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
