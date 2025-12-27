---
name: figma-optimized-html
description: Figma 디자인 가이드 변환에 최적화된 HTML/CSS 코드 생성. 웹페이지, UI 컴포넌트, 대시보드, 디자인 시스템 구현 시 자동 적용. HTML, CSS, 컴포넌트, 레이아웃, 스타일 작성 요청 시 사용.
---

# Figma 최적화 HTML/CSS 생성 스킬

Figma 디자인 가이드로 변환 시 중복 컴포넌트를 최소화하고, 효율적인 디자인 시스템을 생성하는 코드를 작성합니다.

## 핵심 원칙

### 1. 컴포넌트 재사용 (Component Reusability)

**반복 요소는 절대 복사하지 않습니다.**

```html
<!-- BAD: 동일한 SVG 16번 반복 -->
<th><svg>...</svg> Name</th>
<th><svg>...</svg> Score</th>

<!-- GOOD: SVG 심볼로 정의 후 참조 -->
<svg style="display:none">
  <symbol id="icon-sort" viewBox="0 0 24 24">
    <path d="M12 5v14M5 12l7-7 7 7"/>
  </symbol>
</svg>
<th><svg class="icon"><use href="#icon-sort"/></svg> Name</th>
<th><svg class="icon"><use href="#icon-sort"/></svg> Score</th>
```

### 2. 상태 기반 스타일링 (State-based Styling)

**상태는 data 속성으로 관리합니다.**

```html
<!-- BAD: 별도 클래스로 상태 관리 -->
<button class="btn">Default</button>
<button class="btn btn-active">Active</button>

<!-- GOOD: data 속성으로 상태 관리 -->
<button class="btn" data-state="default">Default</button>
<button class="btn" data-state="active">Active</button>
```

```css
.btn { --btn-bg: var(--color-surface); }
.btn[data-state="active"] { --btn-bg: var(--color-primary); }
```

### 3. 컴포넌트 마커 (Component Markers)

**Figma가 인식할 수 있도록 컴포넌트를 마킹합니다.**

```html
<div data-component="card" data-variant="glass">
  <div data-slot="header">제목</div>
  <div data-slot="body">내용</div>
</div>
```

### 4. 템플릿 기반 반복 (Template-based Repetition)

**리스트/그리드는 하나의 템플릿으로 정의합니다.**

```html
<!-- 템플릿 정의 (Figma에서 컴포넌트로 인식) -->
<template id="list-item-template" data-component="list-item">
  <div class="list-item">
    <span data-field="title"></span>
    <span data-field="value"></span>
  </div>
</template>

<!-- 컨테이너 (Auto Layout으로 변환) -->
<div class="list" data-component="list" data-repeat="list-item">
  <!-- JavaScript로 렌더링 -->
</div>
```

## 코드 작성 워크플로우

### Step 1: 요구사항 분석

사용자 요청을 분석하여 다음을 파악합니다:
- 필요한 컴포넌트 목록
- 반복되는 패턴
- 상태 변화가 필요한 요소
- 데이터 구조

### Step 2: 컴포넌트 설계

[COMPONENT-PATTERNS.md](COMPONENT-PATTERNS.md) 참조하여:
- 컴포넌트 계층 구조 설계
- 재사용 가능한 단위 식별
- Variants 정의

### Step 3: Design Tokens 정의

[CSS-VARIABLES.md](CSS-VARIABLES.md) 참조하여:
- 색상, 간격, 타이포그래피 변수 정의
- 테마 지원 구조 설계

### Step 4: HTML 구조 작성

[FIGMA-CONVERSION-RULES.md](FIGMA-CONVERSION-RULES.md) 참조하여:
- Auto Layout 친화적 구조 사용
- 컴포넌트 마커 추가
- SVG 심볼 시스템 적용

### Step 5: 검증

```bash
python .claude/skills/figma-optimized-html/scripts/component_analyzer.py 파일명.html
python .claude/skills/figma-optimized-html/scripts/html_optimizer.py 파일명.html
```

## 필수 체크리스트

코드 작성 완료 후 반드시 확인:

- [ ] 동일한 SVG가 2번 이상 반복되지 않음 (심볼 사용)
- [ ] 반복 요소에 `data-component` 속성 있음
- [ ] 상태 변화는 `data-state` 또는 `data-variant`로 관리
- [ ] CSS 변수가 `:root`에 정의됨
- [ ] Flexbox/Grid 레이아웃 사용 (position absolute 최소화)
- [ ] 테마 지원 (`[data-theme]` 선택자)

## 참조 문서

- [컴포넌트 패턴](COMPONENT-PATTERNS.md)
- [CSS 변수 규칙](CSS-VARIABLES.md)
- [Figma 변환 규칙](FIGMA-CONVERSION-RULES.md)

## 예제

### 카드 컴포넌트

```html
<div class="card" data-component="card" data-variant="glass">
  <div class="card__header" data-slot="header">
    <h3 class="card__title">제목</h3>
  </div>
  <div class="card__body" data-slot="body">
    내용
  </div>
</div>
```

### 테이블 컴포넌트

```html
<!-- 아이콘 심볼 정의 -->
<svg style="display:none">
  <symbol id="icon-sort" viewBox="0 0 24 24">
    <path d="M12 5v14M5 12l7-7 7 7"/>
  </symbol>
</svg>

<!-- 테이블 -->
<div class="table-wrapper" data-component="data-table">
  <table>
    <thead>
      <tr data-component="table-header-row">
        <th data-sortable="true">
          Name <svg class="icon"><use href="#icon-sort"/></svg>
        </th>
      </tr>
    </thead>
    <tbody data-repeat="table-row">
      <!-- 템플릿 기반 렌더링 -->
    </tbody>
  </table>
</div>
```
