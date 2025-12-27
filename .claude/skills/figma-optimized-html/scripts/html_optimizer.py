#!/usr/bin/env python3
"""
HTML 최적화 검증 스크립트

HTML 파일이 Figma 변환 최적화 규칙을 따르는지 검증하고
개선 사항을 제안합니다.

사용법:
    python html_optimizer.py <html_file>
    python html_optimizer.py liquid-glass.html --fix  # 자동 수정 제안 포함
"""

import sys
import re
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    """검증 이슈"""
    severity: Severity
    rule: str
    message: str
    line: Optional[int] = None
    suggestion: Optional[str] = None


class HTMLOptimizer:
    """HTML 최적화 검증기"""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.issues: list[Issue] = []

    def check_all(self) -> list[Issue]:
        """모든 검증 규칙 실행"""
        self.check_svg_symbols()
        self.check_data_components()
        self.check_css_variables()
        self.check_layout_methods()
        self.check_theme_support()
        self.check_state_attributes()
        self.check_template_usage()
        self.check_class_naming()
        return self.issues

    def check_svg_symbols(self):
        """SVG 심볼 사용 검증"""
        # SVG 태그 찾기
        svg_pattern = r'<svg[^>]*>.*?</svg>'
        svgs = re.findall(svg_pattern, self.content, re.DOTALL)

        # 심볼 정의 확인
        has_symbol_defs = '<symbol' in self.content
        uses_href = 'href="#' in self.content or "xlink:href" in self.content

        # 동일한 SVG 찾기
        svg_hashes = {}
        for svg in svgs:
            normalized = re.sub(r'\s+', ' ', svg).strip()
            if '<symbol' not in normalized:  # 심볼 정의는 제외
                if normalized in svg_hashes:
                    svg_hashes[normalized] += 1
                else:
                    svg_hashes[normalized] = 1

        duplicates = {k: v for k, v in svg_hashes.items() if v > 1}

        if duplicates and not has_symbol_defs:
            self.issues.append(Issue(
                severity=Severity.ERROR,
                rule="svg-symbols",
                message=f"동일한 SVG가 {len(duplicates)}종류 반복됨 (총 {sum(duplicates.values())}개)",
                suggestion="SVG 심볼 시스템 사용: <symbol id='icon-name'> + <use href='#icon-name'/>"
            ))
        elif duplicates and has_symbol_defs:
            self.issues.append(Issue(
                severity=Severity.WARNING,
                rule="svg-symbols",
                message="심볼 정의가 있지만 일부 SVG가 직접 인라인됨",
                suggestion="모든 반복 SVG를 <use> 참조로 변경"
            ))

    def check_data_components(self):
        """data-component 속성 검증"""
        has_data_component = 'data-component=' in self.content

        # 반복 가능한 요소 찾기
        repeated_elements = []
        for pattern, name in [
            (r'<tr[^>]*class', 'table rows'),
            (r'<li[^>]*class', 'list items'),
            (r'<div[^>]*class="[^"]*card', 'cards'),
            (r'<button[^>]*class="[^"]*btn', 'buttons'),
        ]:
            count = len(re.findall(pattern, self.content))
            if count > 3:
                repeated_elements.append((name, count))

        if repeated_elements and not has_data_component:
            self.issues.append(Issue(
                severity=Severity.WARNING,
                rule="data-component",
                message=f"반복 요소 발견: {', '.join([f'{n}({c}개)' for n, c in repeated_elements])}",
                suggestion="반복 요소에 data-component 속성 추가: data-component='card'"
            ))

    def check_css_variables(self):
        """CSS 변수 사용 검증"""
        # :root 블록 확인
        has_root = ':root' in self.content

        if not has_root:
            self.issues.append(Issue(
                severity=Severity.ERROR,
                rule="css-variables",
                message="CSS 변수가 :root에 정의되지 않음",
                suggestion=":root { --color-primary: #3b82f6; --space-md: 16px; ... }"
            ))
            return

        # 변수 정의 확인
        root_match = re.search(r':root\s*\{([^}]+)\}', self.content, re.DOTALL)
        if root_match:
            root_content = root_match.group(1)
            var_count = len(re.findall(r'--[a-zA-Z0-9-]+\s*:', root_content))

            if var_count < 5:
                self.issues.append(Issue(
                    severity=Severity.WARNING,
                    rule="css-variables",
                    message=f"CSS 변수가 부족함 ({var_count}개)",
                    suggestion="색상, 간격, 폰트, 반경 등의 변수 정의 권장"
                ))

            # 카테고리별 변수 확인
            categories = {
                'color': r'--color-|--bg-|--text-',
                'space': r'--space-|--gap-|--padding-',
                'font': r'--font-',
                'radius': r'--radius-',
            }

            for category, pattern in categories.items():
                if not re.search(pattern, root_content):
                    self.issues.append(Issue(
                        severity=Severity.INFO,
                        rule="css-variables",
                        message=f"{category} 관련 CSS 변수 없음",
                        suggestion=f"--{category}-* 변수 정의 권장"
                    ))

    def check_layout_methods(self):
        """레이아웃 방식 검증"""
        # 스타일 태그 내용 추출
        style_content = ""
        style_matches = re.findall(r'<style[^>]*>(.*?)</style>', self.content, re.DOTALL)
        style_content = '\n'.join(style_matches)

        # 인라인 스타일도 확인
        inline_styles = re.findall(r'style="([^"]*)"', self.content)
        all_styles = style_content + '\n'.join(inline_styles)

        # position: absolute 카운트
        absolute_count = len(re.findall(r'position\s*:\s*absolute', all_styles, re.IGNORECASE))
        flexbox_count = len(re.findall(r'display\s*:\s*flex', all_styles, re.IGNORECASE))
        grid_count = len(re.findall(r'display\s*:\s*grid', all_styles, re.IGNORECASE))

        if absolute_count > 10:
            self.issues.append(Issue(
                severity=Severity.ERROR,
                rule="layout",
                message=f"position: absolute 과다 사용 ({absolute_count}개)",
                suggestion="Flexbox/Grid로 변환하여 Auto Layout 호환성 확보"
            ))
        elif absolute_count > 5:
            self.issues.append(Issue(
                severity=Severity.WARNING,
                rule="layout",
                message=f"position: absolute 사용 ({absolute_count}개)",
                suggestion="가능한 Flexbox/Grid로 변환 권장"
            ))

        if flexbox_count + grid_count == 0:
            self.issues.append(Issue(
                severity=Severity.WARNING,
                rule="layout",
                message="Flexbox/Grid 레이아웃 미사용",
                suggestion="Figma Auto Layout 호환을 위해 Flexbox/Grid 사용 권장"
            ))

    def check_theme_support(self):
        """테마 지원 검증"""
        has_theme_attr = 'data-theme=' in self.content
        has_theme_selector = '[data-theme=' in self.content

        if not has_theme_attr:
            self.issues.append(Issue(
                severity=Severity.INFO,
                rule="theme",
                message="테마 속성 없음",
                suggestion="<html data-theme='dark'> 형태로 테마 지원 추가"
            ))

        if not has_theme_selector:
            self.issues.append(Issue(
                severity=Severity.INFO,
                rule="theme",
                message="테마 선택자 없음",
                suggestion="[data-theme='dark'] { ... } 형태로 테마별 스타일 정의"
            ))

    def check_state_attributes(self):
        """상태 속성 검증"""
        # 상태 클래스 사용 확인
        state_classes = re.findall(r'class="[^"]*\b(active|disabled|hover|focus|selected)\b[^"]*"', self.content)

        # data-state 사용 확인
        data_states = re.findall(r'data-state="([^"]*)"', self.content)

        if state_classes and not data_states:
            self.issues.append(Issue(
                severity=Severity.WARNING,
                rule="state-attributes",
                message=f"상태 클래스 사용됨: {', '.join(set(state_classes))}",
                suggestion="data-state 속성으로 변경 권장: data-state='active'"
            ))

    def check_template_usage(self):
        """템플릿 사용 검증"""
        has_template = '<template' in self.content

        # 동적 렌더링 영역 확인 (JavaScript로 채워지는 컨테이너)
        dynamic_containers = re.findall(r'<(tbody|ul|div)[^>]*id="[^"]*"[^>]*>\s*</\1>', self.content)

        if dynamic_containers and not has_template:
            self.issues.append(Issue(
                severity=Severity.INFO,
                rule="template",
                message="동적 컨테이너가 있지만 <template> 미사용",
                suggestion="<template id='item-template'>로 컴포넌트 구조 정의 권장"
            ))

    def check_class_naming(self):
        """클래스 명명 규칙 검증"""
        # 모든 클래스 추출
        classes = re.findall(r'class="([^"]*)"', self.content)
        all_classes = []
        for cls_str in classes:
            all_classes.extend(cls_str.split())

        # BEM 패턴 확인
        bem_pattern = r'^[a-z][a-z0-9]*(__[a-z][a-z0-9]*)?(-{1,2}[a-z][a-z0-9]*)?$'
        non_bem_classes = [c for c in set(all_classes)
                          if not re.match(bem_pattern, c, re.IGNORECASE)
                          and not c.startswith('js-')]

        if len(non_bem_classes) > len(set(all_classes)) * 0.5:
            self.issues.append(Issue(
                severity=Severity.INFO,
                rule="class-naming",
                message="BEM 명명 규칙 미준수 클래스 다수",
                suggestion="block__element--modifier 형태의 명명 규칙 권장"
            ))


def generate_report(issues: list[Issue], filepath: str) -> str:
    """검증 리포트 생성"""
    report = []
    report.append("=" * 60)
    report.append(f"HTML 최적화 검증 리포트: {filepath}")
    report.append("=" * 60)
    report.append("")

    errors = [i for i in issues if i.severity == Severity.ERROR]
    warnings = [i for i in issues if i.severity == Severity.WARNING]
    infos = [i for i in issues if i.severity == Severity.INFO]

    report.append(f"총 이슈: {len(issues)}개")
    report.append(f"  - 오류: {len(errors)}개")
    report.append(f"  - 경고: {len(warnings)}개")
    report.append(f"  - 정보: {len(infos)}개")
    report.append("")

    if errors:
        report.append("## 오류 (필수 수정)")
        report.append("-" * 40)
        for issue in errors:
            report.append(f"❌ [{issue.rule}] {issue.message}")
            if issue.suggestion:
                report.append(f"   💡 {issue.suggestion}")
            report.append("")

    if warnings:
        report.append("## 경고 (권장 수정)")
        report.append("-" * 40)
        for issue in warnings:
            report.append(f"⚠️  [{issue.rule}] {issue.message}")
            if issue.suggestion:
                report.append(f"   💡 {issue.suggestion}")
            report.append("")

    if infos:
        report.append("## 정보 (선택 개선)")
        report.append("-" * 40)
        for issue in infos:
            report.append(f"ℹ️  [{issue.rule}] {issue.message}")
            if issue.suggestion:
                report.append(f"   💡 {issue.suggestion}")
            report.append("")

    # 결과 요약
    report.append("## 결과")
    report.append("-" * 40)
    if not errors and not warnings:
        report.append("✅ Figma 변환 준비 완료!")
    elif not errors:
        report.append("⚠️  경고 사항 확인 후 변환 가능")
    else:
        report.append("❌ 오류 수정 필요")

    report.append("")
    report.append("=" * 60)

    return "\n".join(report)


def generate_json_report(issues: list[Issue], filepath: str) -> str:
    """JSON 형식 리포트 생성"""
    return json.dumps({
        "file": filepath,
        "issues": [
            {
                "severity": issue.severity.value,
                "rule": issue.rule,
                "message": issue.message,
                "line": issue.line,
                "suggestion": issue.suggestion
            }
            for issue in issues
        ],
        "summary": {
            "errors": len([i for i in issues if i.severity == Severity.ERROR]),
            "warnings": len([i for i in issues if i.severity == Severity.WARNING]),
            "infos": len([i for i in issues if i.severity == Severity.INFO]),
        }
    }, indent=2, ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print("사용법: python html_optimizer.py <html_file> [--json]")
        print("예시: python html_optimizer.py liquid-glass.html")
        print("      python html_optimizer.py liquid-glass.html --json")
        sys.exit(1)

    filepath = sys.argv[1]
    json_output = '--json' in sys.argv

    path = Path(filepath)
    if not path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {filepath}")
        sys.exit(1)

    content = path.read_text(encoding='utf-8')

    optimizer = HTMLOptimizer(content)
    issues = optimizer.check_all()

    if json_output:
        print(generate_json_report(issues, filepath))
    else:
        print(generate_report(issues, filepath))

    # 오류가 있으면 exit code 1
    errors = [i for i in issues if i.severity == Severity.ERROR]
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
