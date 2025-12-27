# Figma 변환 최적화 규칙

html.to.design 플러그인으로 변환 시 최적의 결과를 얻기 위한 규칙입니다.

## 1. Auto Layout 변환 규칙

### Flexbox → Auto Layout

| CSS | Figma Auto Layout |
|-----|------------------|
| `display: flex` | Auto Layout 활성화 |
| `flex-direction: row` | Horizontal |
| `flex-direction: column` | Vertical |
| `gap: 16px` | Item spacing: 16 |
| `padding: 24px` | Padding: 24 |
| `align-items: center` | Align: Center |
| `justify-content: space-between` | Space between |

### 최적화된 구조

```html
<!-- GOOD: Auto Layout으로 변환됨 -->
<div class="container" style="display: flex; flex-direction: column; gap: 16px; padding: 24px;">
  <div class="item">아이템 1</div>
  <div class="item">아이템 2</div>
</div>

<!-- BAD: Auto Layout 변환 안됨 -->
<div class="container" style="position: relative;">
  <div class="item" style="position: absolute; top: 0;">아이템 1</div>
  <div class="item" style="position: absolute; top: 50px;">아이템 2</div>
</div>
```

### Grid → Auto Layout

```css
/* Grid도 Auto Layout으로 변환 가능 */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
```

## 2. 컴포넌트 인식 패턴

### data-component 속성

html.to.design은 반복되는 구조를 컴포넌트로 인식합니다.

```html
<!-- 명시적 컴포넌트 마킹 -->
<div data-component="card" data-variant="default">
  컨텐츠
</div>

<!-- 반복 요소 마킹 -->
<div class="list">
  <div data-component="list-item">아이템 1</div>
  <div data-component="list-item">아이템 2</div>
  <div data-component="list-item">아이템 3</div>
</div>
```

### Variants 인식

```html
<!-- 같은 data-component, 다른 data-variant → Variants로 그룹화 -->
<button data-component="button" data-variant="primary">Primary</button>
<button data-component="button" data-variant="secondary">Secondary</button>
<button data-component="button" data-variant="ghost">Ghost</button>
```

## 3. 중복 방지 전략

### SVG 심볼 시스템

```html
<!-- 정의 (1번) -->
<svg style="display:none" aria-hidden="true">
  <symbol id="icon-arrow" viewBox="0 0 24 24">
    <path d="M12 5v14M5 12l7-7 7 7"/>
  </symbol>
</svg>

<!-- 사용 (N번) - Figma에서 인스턴스로 인식 -->
<svg class="icon"><use href="#icon-arrow"/></svg>
<svg class="icon"><use href="#icon-arrow"/></svg>
```

### 템플릿 + JavaScript 렌더링

```html
<!-- 템플릿 정의 -->
<template id="row-template">
  <tr data-component="table-row">
    <td class="cell"></td>
  </tr>
</template>

<!-- 빈 컨테이너 (Figma에서 반복 컴포넌트로 표시) -->
<tbody id="table-body">
  <!-- JS로 1-3개만 렌더링해서 컴포넌트 구조 보여주기 -->
</tbody>
```

### 상태 클래스 대신 data 속성

```html
<!-- BAD: 별도 요소로 인식됨 -->
<button class="btn">Default</button>
<button class="btn active">Active</button>
<button class="btn disabled">Disabled</button>

<!-- GOOD: Variants로 그룹화됨 -->
<button class="btn" data-state="default">Default</button>
<button class="btn" data-state="active">Active</button>
<button class="btn" data-state="disabled">Disabled</button>
```

## 4. 스타일 변환 규칙

### 지원되는 CSS 속성

| CSS 속성 | Figma 변환 |
|----------|-----------|
| `background-color` | Fill |
| `border` | Stroke |
| `border-radius` | Corner radius |
| `box-shadow` | Drop shadow |
| `opacity` | Opacity |
| `backdrop-filter: blur()` | Background blur |
| `font-*` | Typography |
| `gap` | Auto Layout spacing |
| `padding` | Auto Layout padding |

### 지원 안되는/제한되는 속성

| CSS 속성 | 해결 방법 |
|----------|----------|
| `position: absolute` | Flexbox로 대체 |
| `transform` | 단순 회전만 지원 |
| `animation` | 무시됨 |
| `::before/::after` | 실제 요소로 대체 |
| `linear-gradient` | 부분 지원 |

## 5. 레이어 구조 최적화

### 명명 규칙

```html
<!-- 클래스명이 레이어명이 됨 -->
<div class="header">              <!-- Layer: header -->
  <h1 class="header__title">      <!-- Layer: header__title -->
    제목
  </h1>
</div>
```

### 그룹화

```html
<!-- data-group으로 그룹 표시 -->
<div data-group="controls">
  <button>버튼 1</button>
  <button>버튼 2</button>
</div>
```

## 6. 반응형 디자인

### 뷰포트별 캡처

html.to.design은 여러 뷰포트 크기로 캡처할 수 있습니다:

```
Desktop: 1440px
Tablet: 768px
Mobile: 375px
```

### 반응형 친화적 구조

```css
/* 비율 기반 레이아웃 */
.container {
  max-width: 1200px;
  width: 100%;
  padding: 0 var(--space-md);
}

/* 유연한 그리드 */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-md);
}
```

## 7. 체크리스트

### 변환 전 확인사항

- [ ] 모든 레이아웃이 Flexbox/Grid 사용
- [ ] position: absolute 최소화
- [ ] SVG가 심볼 시스템 사용
- [ ] 반복 요소에 data-component 속성
- [ ] 상태 변형에 data-state/data-variant 사용
- [ ] CSS 변수가 :root에 정의됨
- [ ] 테마가 [data-theme] 선택자 사용

### 변환 후 확인사항

- [ ] Auto Layout이 올바르게 적용됨
- [ ] 컴포넌트가 그룹화됨
- [ ] 스타일 변수가 생성됨
- [ ] 불필요한 중복 레이어 없음

## 8. 문제 해결

### 빈 프레임으로 변환됨

**원인**: foreignObject 사용 (html-to-image의 toSvg)
**해결**: html.to.design 플러그인 사용 또는 PNG 내보내기

### 컴포넌트가 개별 요소로 분리됨

**원인**: 반복 패턴이 인식되지 않음
**해결**: data-component 속성 추가

### 스타일이 누락됨

**원인**: 인라인 스타일 또는 동적 스타일
**해결**: CSS 클래스로 스타일 정의

### Auto Layout이 적용 안됨

**원인**: position: absolute 또는 float 사용
**해결**: Flexbox/Grid로 변환

## 9. 최적의 워크플로우

```
1. HTML 작성 (이 스킬의 규칙 따름)
       ↓
2. 로컬 서버 실행 (python -m http.server)
       ↓
3. Chrome에서 페이지 열기
       ↓
4. html.to.design 확장으로 캡처
       ↓
5. Figma 플러그인에서 가져오기
   - Import styles: ON
   - Auto layout: ON
   - Generate components: ON
       ↓
6. 컴포넌트 정리 및 변수 확인
```
