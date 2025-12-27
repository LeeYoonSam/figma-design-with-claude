# 컴포넌트 패턴 가이드

Figma 변환에 최적화된 HTML 컴포넌트 패턴입니다.

## 1. 명명 규칙 (BEM + Data Attributes)

### BEM 구조

```
Block__Element--Modifier
```

```html
<div class="card">                          <!-- Block -->
  <div class="card__header">                <!-- Element -->
    <h3 class="card__title">제목</h3>
  </div>
  <div class="card__body">내용</div>
</div>

<div class="card card--featured">           <!-- Modifier -->
  ...
</div>
```

### Data Attributes 체계

| 속성 | 용도 | 예시 |
|------|------|------|
| `data-component` | 컴포넌트 식별 | `data-component="card"` |
| `data-variant` | 스타일 변형 | `data-variant="glass"` |
| `data-state` | 상태 | `data-state="active"` |
| `data-slot` | 콘텐츠 슬롯 | `data-slot="header"` |
| `data-field` | 데이터 필드 | `data-field="title"` |
| `data-repeat` | 반복 참조 | `data-repeat="list-item"` |

## 2. 반복 컴포넌트 패턴

### 리스트 (List)

```html
<!-- 아이템 템플릿 정의 -->
<template id="list-item-template">
  <div class="list-item" data-component="list-item">
    <span class="list-item__icon" data-slot="icon"></span>
    <span class="list-item__text" data-field="text"></span>
    <span class="list-item__action" data-slot="action"></span>
  </div>
</template>

<!-- 리스트 컨테이너 -->
<div class="list" data-component="list" data-repeat="list-item">
  <!-- JavaScript로 렌더링 -->
</div>
```

```javascript
function renderList(container, items, templateId) {
  const template = document.getElementById(templateId);
  container.innerHTML = '';

  items.forEach(item => {
    const clone = template.content.cloneNode(true);
    Object.entries(item).forEach(([key, value]) => {
      const field = clone.querySelector(`[data-field="${key}"]`);
      if (field) field.textContent = value;
    });
    container.appendChild(clone);
  });
}
```

### 그리드 (Grid)

```html
<template id="grid-card-template">
  <div class="grid-card" data-component="grid-card">
    <img class="grid-card__image" data-field="image" alt="">
    <div class="grid-card__content">
      <h4 class="grid-card__title" data-field="title"></h4>
      <p class="grid-card__desc" data-field="description"></p>
    </div>
  </div>
</template>

<div class="grid" data-component="grid" data-repeat="grid-card">
  <!-- JavaScript로 렌더링 -->
</div>
```

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-md);
}
```

### 테이블 (Table)

```html
<!-- 헤더 셀 템플릿 -->
<template id="table-header-template">
  <th class="table__th" data-component="table-header-cell" data-sortable>
    <span class="table__th-text" data-field="label"></span>
    <svg class="table__sort-icon"><use href="#icon-sort"/></svg>
  </th>
</template>

<!-- 바디 행 템플릿 -->
<template id="table-row-template">
  <tr class="table__row" data-component="table-row">
    <!-- 동적으로 셀 생성 -->
  </tr>
</template>

<!-- 테이블 -->
<div class="table-wrapper" data-component="data-table">
  <table class="table">
    <thead>
      <tr data-component="table-header-row" data-repeat="table-header">
        <!-- JavaScript로 렌더링 -->
      </tr>
    </thead>
    <tbody data-repeat="table-row">
      <!-- JavaScript로 렌더링 -->
    </tbody>
  </table>
</div>
```

## 3. 상태 Variants 패턴

### 버튼 상태

```html
<button class="btn" data-component="button" data-variant="primary" data-state="default">
  기본
</button>
<button class="btn" data-component="button" data-variant="primary" data-state="hover">
  호버
</button>
<button class="btn" data-component="button" data-variant="primary" data-state="active">
  활성
</button>
<button class="btn" data-component="button" data-variant="primary" data-state="disabled" disabled>
  비활성
</button>
```

```css
.btn {
  --btn-bg: var(--color-surface);
  --btn-text: var(--color-text);
  --btn-border: var(--color-border);

  background: var(--btn-bg);
  color: var(--btn-text);
  border: 1px solid var(--btn-border);
}

.btn[data-variant="primary"] {
  --btn-bg: var(--color-primary);
  --btn-text: var(--color-on-primary);
  --btn-border: var(--color-primary);
}

.btn[data-state="hover"],
.btn:hover {
  --btn-bg: var(--color-primary-hover);
}

.btn[data-state="active"],
.btn:active {
  --btn-bg: var(--color-primary-active);
}

.btn[data-state="disabled"],
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### 토글 그룹

```html
<div class="toggle-group" data-component="toggle-group">
  <button class="toggle-btn" data-component="toggle-button" data-state="default">
    옵션 1
  </button>
  <button class="toggle-btn" data-component="toggle-button" data-state="active">
    옵션 2
  </button>
  <button class="toggle-btn" data-component="toggle-button" data-state="default">
    옵션 3
  </button>
</div>
```

### 입력 필드 상태

```html
<div class="input-wrapper" data-component="text-input" data-state="default">
  <label class="input-label">라벨</label>
  <input class="input-field" type="text" placeholder="입력...">
</div>

<div class="input-wrapper" data-component="text-input" data-state="focus">
  <label class="input-label">라벨</label>
  <input class="input-field" type="text" value="입력 중...">
</div>

<div class="input-wrapper" data-component="text-input" data-state="error">
  <label class="input-label">라벨</label>
  <input class="input-field" type="text" value="잘못된 입력">
  <span class="input-error">오류 메시지</span>
</div>
```

## 4. 아이콘 심볼 시스템

### SVG 심볼 정의

```html
<!-- 페이지 상단에 숨겨진 SVG 정의 -->
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <defs>
    <!-- 정렬 아이콘 -->
    <symbol id="icon-sort" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 5v14M5 12l7-7 7 7"/>
    </symbol>

    <!-- 검색 아이콘 -->
    <symbol id="icon-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="11" cy="11" r="8"/>
      <path d="m21 21-4.3-4.3"/>
    </symbol>

    <!-- 닫기 아이콘 -->
    <symbol id="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M18 6L6 18M6 6l12 12"/>
    </symbol>

    <!-- 체크 아이콘 -->
    <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="20 6 9 17 4 12"/>
    </symbol>

    <!-- 화살표 아이콘 -->
    <symbol id="icon-chevron-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="6 9 12 15 18 9"/>
    </symbol>
  </defs>
</svg>
```

### 아이콘 사용

```html
<!-- 기본 사용 -->
<svg class="icon" aria-hidden="true">
  <use href="#icon-search"/>
</svg>

<!-- 크기 변형 -->
<svg class="icon icon--sm"><use href="#icon-search"/></svg>
<svg class="icon icon--md"><use href="#icon-search"/></svg>
<svg class="icon icon--lg"><use href="#icon-search"/></svg>
```

```css
.icon {
  width: 1em;
  height: 1em;
  fill: none;
  stroke: currentColor;
}

.icon--sm { width: 16px; height: 16px; }
.icon--md { width: 24px; height: 24px; }
.icon--lg { width: 32px; height: 32px; }
```

## 5. 모달/오버레이 패턴

```html
<div class="modal-overlay" data-component="modal" data-state="closed">
  <div class="modal" data-variant="default">
    <div class="modal__header" data-slot="header">
      <h3 class="modal__title">모달 제목</h3>
      <button class="modal__close" aria-label="닫기">
        <svg class="icon"><use href="#icon-close"/></svg>
      </button>
    </div>
    <div class="modal__body" data-slot="body">
      모달 내용
    </div>
    <div class="modal__footer" data-slot="footer">
      <button class="btn" data-variant="secondary">취소</button>
      <button class="btn" data-variant="primary">확인</button>
    </div>
  </div>
</div>
```

## 6. 카드 컴포넌트 패턴

```html
<div class="card" data-component="card" data-variant="default">
  <div class="card__media" data-slot="media">
    <img src="image.jpg" alt="설명">
  </div>
  <div class="card__content">
    <div class="card__header" data-slot="header">
      <h3 class="card__title" data-field="title">카드 제목</h3>
      <span class="card__badge" data-field="badge">NEW</span>
    </div>
    <div class="card__body" data-slot="body">
      <p class="card__text" data-field="description">카드 설명 텍스트</p>
    </div>
    <div class="card__footer" data-slot="footer">
      <button class="card__action">액션</button>
    </div>
  </div>
</div>
```

### 카드 Variants

```css
.card {
  --card-bg: var(--color-surface);
  --card-border: var(--color-border);
  --card-shadow: var(--shadow-sm);
}

.card[data-variant="glass"] {
  --card-bg: var(--glass-bg);
  --card-border: var(--glass-border);
  backdrop-filter: blur(var(--blur-md));
}

.card[data-variant="elevated"] {
  --card-shadow: var(--shadow-lg);
  --card-border: transparent;
}

.card[data-variant="outlined"] {
  --card-bg: transparent;
  --card-shadow: none;
}
```
