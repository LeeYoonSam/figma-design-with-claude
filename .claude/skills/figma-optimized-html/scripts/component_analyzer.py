#!/usr/bin/env python3
"""
컴포넌트 분석 스크립트

HTML 파일을 분석하여 Figma 변환 시 발생할 수 있는 중복 요소를 감지하고
최적화 제안을 생성합니다.

사용법:
    python component_analyzer.py <html_file>
    python component_analyzer.py liquid-glass.html
"""

import sys
import re
from collections import Counter, defaultdict
from pathlib import Path
from html.parser import HTMLParser
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SVGInfo:
    """SVG 정보"""
    content: str
    count: int = 1
    locations: list = field(default_factory=list)


@dataclass
class ElementInfo:
    """요소 정보"""
    tag: str
    classes: list
    attributes: dict
    count: int = 1


class HTMLAnalyzer(HTMLParser):
    """HTML 분석 파서"""

    def __init__(self):
        super().__init__()
        self.svg_contents: dict[str, SVGInfo] = {}
        self.elements: list[ElementInfo] = []
        self.class_counter = Counter()
        self.tag_counter = Counter()
        self.data_components = Counter()
        self.current_svg = []
        self.in_svg = False
        self.svg_depth = 0
        self.line_number = 1
        self.position_absolute_count = 0
        self.flexbox_count = 0
        self.grid_count = 0

    def handle_starttag(self, tag: str, attrs: list):
        attrs_dict = dict(attrs)

        # SVG 추적
        if tag == 'svg':
            self.in_svg = True
            self.svg_depth = 1
            self.current_svg = [f'<{tag}']
            for name, value in attrs:
                self.current_svg.append(f' {name}="{value}"')
            self.current_svg.append('>')
        elif self.in_svg:
            self.svg_depth += 1
            self.current_svg.append(f'<{tag}')
            for name, value in attrs:
                self.current_svg.append(f' {name}="{value}"')
            self.current_svg.append('>')

        # 태그 카운트
        self.tag_counter[tag] += 1

        # 클래스 카운트
        if 'class' in attrs_dict:
            classes = attrs_dict['class'].split()
            for cls in classes:
                self.class_counter[cls] += 1

        # data-component 카운트
        if 'data-component' in attrs_dict:
            self.data_components[attrs_dict['data-component']] += 1

        # 스타일 분석
        style = attrs_dict.get('style', '')
        if 'position: absolute' in style or 'position:absolute' in style:
            self.position_absolute_count += 1
        if 'display: flex' in style or 'display:flex' in style:
            self.flexbox_count += 1
        if 'display: grid' in style or 'display:grid' in style:
            self.grid_count += 1

    def handle_endtag(self, tag: str):
        if self.in_svg:
            self.current_svg.append(f'</{tag}>')
            self.svg_depth -= 1
            if self.svg_depth == 0:
                svg_content = ''.join(self.current_svg)
                # 정규화 (공백 제거)
                normalized = re.sub(r'\s+', ' ', svg_content).strip()

                if normalized in self.svg_contents:
                    self.svg_contents[normalized].count += 1
                    self.svg_contents[normalized].locations.append(self.line_number)
                else:
                    self.svg_contents[normalized] = SVGInfo(
                        content=svg_content,
                        count=1,
                        locations=[self.line_number]
                    )
                self.in_svg = False
                self.current_svg = []

    def handle_data(self, data: str):
        if self.in_svg:
            self.current_svg.append(data)
        self.line_number += data.count('\n')


def analyze_css_variables(content: str) -> dict:
    """CSS 변수 분석"""
    # :root 블록 찾기
    root_match = re.search(r':root\s*\{([^}]+)\}', content, re.DOTALL)
    variables = {}

    if root_match:
        root_content = root_match.group(1)
        # CSS 변수 추출
        var_pattern = r'--([a-zA-Z0-9-]+)\s*:\s*([^;]+);'
        for match in re.finditer(var_pattern, root_content):
            variables[f'--{match.group(1)}'] = match.group(2).strip()

    return variables


def analyze_repeated_patterns(content: str) -> list:
    """반복 패턴 분석"""
    patterns = []

    # 동일한 클래스를 가진 연속 요소 찾기
    table_rows = len(re.findall(r'<tr[^>]*>', content))
    list_items = len(re.findall(r'<li[^>]*>', content))
    div_cards = len(re.findall(r'<div[^>]*class="[^"]*card[^"]*"', content))

    if table_rows > 5:
        patterns.append(('table rows', table_rows))
    if list_items > 5:
        patterns.append(('list items', list_items))
    if div_cards > 3:
        patterns.append(('card components', div_cards))

    return patterns


def generate_report(analyzer: HTMLAnalyzer, css_vars: dict, patterns: list, filepath: str) -> str:
    """분석 리포트 생성"""
    report = []
    report.append("=" * 60)
    report.append(f"Figma 최적화 분석 리포트: {filepath}")
    report.append("=" * 60)
    report.append("")

    # 1. 중복 SVG 분석
    report.append("## 1. 중복 SVG 분석")
    report.append("-" * 40)

    duplicate_svgs = [(k, v) for k, v in analyzer.svg_contents.items() if v.count > 1]
    if duplicate_svgs:
        report.append(f"⚠️  중복된 SVG: {len(duplicate_svgs)}개 발견")
        report.append("")
        for svg_hash, info in sorted(duplicate_svgs, key=lambda x: -x[1].count):
            report.append(f"  - {info.count}번 반복")
            preview = info.content[:80] + "..." if len(info.content) > 80 else info.content
            report.append(f"    미리보기: {preview}")
            report.append("")
        report.append("  💡 해결: SVG 심볼 시스템 사용 (<symbol> + <use>)")
    else:
        report.append("✅ 중복 SVG 없음")
    report.append("")

    # 2. 반복 패턴 분석
    report.append("## 2. 반복 패턴 분석")
    report.append("-" * 40)

    if patterns:
        for pattern_name, count in patterns:
            report.append(f"  - {pattern_name}: {count}개")
        report.append("")
        report.append("  💡 해결: <template> 기반 렌더링 또는 data-component 속성 사용")
    else:
        report.append("✅ 과도한 반복 패턴 없음")
    report.append("")

    # 3. data-component 사용 현황
    report.append("## 3. data-component 사용 현황")
    report.append("-" * 40)

    if analyzer.data_components:
        report.append("✅ data-component 속성 사용 중:")
        for comp, count in analyzer.data_components.most_common(10):
            report.append(f"  - {comp}: {count}개")
    else:
        report.append("⚠️  data-component 속성 없음")
        report.append("  💡 반복 요소에 data-component 속성 추가 권장")
    report.append("")

    # 4. 레이아웃 방식 분석
    report.append("## 4. 레이아웃 방식 분석")
    report.append("-" * 40)

    report.append(f"  - Flexbox 사용: {analyzer.flexbox_count}개")
    report.append(f"  - Grid 사용: {analyzer.grid_count}개")
    report.append(f"  - Position absolute: {analyzer.position_absolute_count}개")

    if analyzer.position_absolute_count > 5:
        report.append("")
        report.append("  ⚠️  position: absolute 과다 사용")
        report.append("  💡 Flexbox/Grid로 변환 권장 (Auto Layout 호환성)")
    report.append("")

    # 5. CSS 변수 분석
    report.append("## 5. CSS 변수 분석")
    report.append("-" * 40)

    if css_vars:
        color_vars = [v for v in css_vars if 'color' in v.lower() or v.startswith('--bg') or v.startswith('--text')]
        space_vars = [v for v in css_vars if 'space' in v.lower() or 'gap' in v.lower() or 'padding' in v.lower()]
        font_vars = [v for v in css_vars if 'font' in v.lower()]

        report.append(f"✅ CSS 변수 정의됨: {len(css_vars)}개")
        report.append(f"  - 색상 관련: {len(color_vars)}개")
        report.append(f"  - 간격 관련: {len(space_vars)}개")
        report.append(f"  - 폰트 관련: {len(font_vars)}개")
    else:
        report.append("⚠️  :root에 CSS 변수 없음")
        report.append("  💡 Design Tokens을 CSS 변수로 정의 권장")
    report.append("")

    # 6. 최적화 점수
    report.append("## 6. Figma 최적화 점수")
    report.append("-" * 40)

    score = 100
    issues = []

    # 중복 SVG 감점
    if duplicate_svgs:
        penalty = min(len(duplicate_svgs) * 5, 20)
        score -= penalty
        issues.append(f"중복 SVG (-{penalty}점)")

    # position absolute 감점
    if analyzer.position_absolute_count > 5:
        penalty = min(analyzer.position_absolute_count, 15)
        score -= penalty
        issues.append(f"position absolute 과다 (-{penalty}점)")

    # data-component 미사용 감점
    if not analyzer.data_components:
        score -= 15
        issues.append("data-component 미사용 (-15점)")

    # CSS 변수 미사용 감점
    if not css_vars:
        score -= 10
        issues.append("CSS 변수 미사용 (-10점)")

    report.append(f"  점수: {score}/100")
    if issues:
        report.append("  감점 항목:")
        for issue in issues:
            report.append(f"    - {issue}")
    report.append("")

    # 7. 권장 사항
    report.append("## 7. 권장 사항")
    report.append("-" * 40)

    if score >= 80:
        report.append("✅ Figma 변환 준비 완료!")
    elif score >= 60:
        report.append("⚠️  일부 최적화 필요")
    else:
        report.append("❌ 상당한 최적화 필요")

    report.append("")
    report.append("권장 조치:")
    if duplicate_svgs:
        report.append("  1. SVG 심볼 시스템 적용")
    if analyzer.position_absolute_count > 5:
        report.append("  2. Flexbox/Grid 레이아웃으로 변환")
    if not analyzer.data_components:
        report.append("  3. 반복 요소에 data-component 속성 추가")
    if not css_vars:
        report.append("  4. Design Tokens을 CSS 변수로 정의")

    report.append("")
    report.append("=" * 60)

    return "\n".join(report)


def main():
    if len(sys.argv) < 2:
        print("사용법: python component_analyzer.py <html_file>")
        print("예시: python component_analyzer.py liquid-glass.html")
        sys.exit(1)

    filepath = sys.argv[1]
    path = Path(filepath)

    if not path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {filepath}")
        sys.exit(1)

    content = path.read_text(encoding='utf-8')

    # HTML 분석
    analyzer = HTMLAnalyzer()
    analyzer.feed(content)

    # CSS 변수 분석
    css_vars = analyze_css_variables(content)

    # 반복 패턴 분석
    patterns = analyze_repeated_patterns(content)

    # 리포트 생성
    report = generate_report(analyzer, css_vars, patterns, filepath)
    print(report)


if __name__ == "__main__":
    main()
