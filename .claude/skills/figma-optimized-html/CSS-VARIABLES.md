# CSS 변수 규칙 (Design Tokens)

Figma 변수로 자동 변환되는 CSS 변수 체계입니다.

## 1. 변수 명명 규칙

### 계층 구조

```
--{category}-{property}-{variant}
```

| 카테고리 | 예시 |
|----------|------|
| `color` | `--color-primary`, `--color-text-secondary` |
| `space` | `--space-sm`, `--space-md` |
| `font` | `--font-size-lg`, `--font-weight-bold` |
| `radius` | `--radius-md`, `--radius-full` |
| `shadow` | `--shadow-sm`, `--shadow-lg` |
| `blur` | `--blur-sm`, `--blur-md` |
| `transition` | `--transition-fast`, `--transition-normal` |

## 2. Design Tokens 구조

### 기본 토큰 (Primitives)

```css
:root {
  /* ===== Primitive Colors ===== */
  --primitive-gray-50: #fafafa;
  --primitive-gray-100: #f5f5f5;
  --primitive-gray-200: #e5e5e5;
  --primitive-gray-300: #d4d4d4;
  --primitive-gray-400: #a3a3a3;
  --primitive-gray-500: #737373;
  --primitive-gray-600: #525252;
  --primitive-gray-700: #404040;
  --primitive-gray-800: #262626;
  --primitive-gray-900: #171717;

  --primitive-blue-500: #3b82f6;
  --primitive-blue-600: #2563eb;
  --primitive-green-500: #22c55e;
  --primitive-orange-500: #f97316;
  --primitive-red-500: #ef4444;

  /* ===== Primitive Spacing ===== */
  --primitive-space-1: 4px;
  --primitive-space-2: 8px;
  --primitive-space-3: 12px;
  --primitive-space-4: 16px;
  --primitive-space-5: 20px;
  --primitive-space-6: 24px;
  --primitive-space-8: 32px;
  --primitive-space-10: 40px;
  --primitive-space-12: 48px;

  /* ===== Primitive Typography ===== */
  --primitive-font-size-xs: 0.75rem;   /* 12px */
  --primitive-font-size-sm: 0.875rem;  /* 14px */
  --primitive-font-size-md: 1rem;      /* 16px */
  --primitive-font-size-lg: 1.125rem;  /* 18px */
  --primitive-font-size-xl: 1.25rem;   /* 20px */
  --primitive-font-size-2xl: 1.5rem;   /* 24px */
  --primitive-font-size-3xl: 2rem;     /* 32px */

  /* ===== Primitive Radius ===== */
  --primitive-radius-sm: 4px;
  --primitive-radius-md: 8px;
  --primitive-radius-lg: 12px;
  --primitive-radius-xl: 16px;
  --primitive-radius-2xl: 24px;
  --primitive-radius-full: 9999px;
}
```

### 시맨틱 토큰 (Semantic Tokens)

```css
:root {
  /* ===== Semantic Spacing ===== */
  --space-xs: var(--primitive-space-1);   /* 4px */
  --space-sm: var(--primitive-space-2);   /* 8px */
  --space-md: var(--primitive-space-4);   /* 16px */
  --space-lg: var(--primitive-space-6);   /* 24px */
  --space-xl: var(--primitive-space-8);   /* 32px */
  --space-2xl: var(--primitive-space-12); /* 48px */

  /* ===== Semantic Typography ===== */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-xs: var(--primitive-font-size-xs);
  --font-size-sm: var(--primitive-font-size-sm);
  --font-size-md: var(--primitive-font-size-md);
  --font-size-lg: var(--primitive-font-size-lg);
  --font-size-xl: var(--primitive-font-size-xl);
  --font-size-2xl: var(--primitive-font-size-2xl);

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* ===== Semantic Radius ===== */
  --radius-sm: var(--primitive-radius-md);   /* 8px */
  --radius-md: var(--primitive-radius-lg);   /* 12px */
  --radius-lg: var(--primitive-radius-xl);   /* 16px */
  --radius-full: var(--primitive-radius-full);

  /* ===== Effects ===== */
  --blur-sm: 8px;
  --blur-md: 16px;
  --blur-lg: 24px;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

  /* ===== Transitions ===== */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

## 3. 테마 시스템

### 다크 테마

```css
[data-theme="dark"] {
  /* ===== Surface Colors ===== */
  --color-bg: #0a0a0a;
  --color-surface: #171717;
  --color-surface-elevated: #262626;

  /* ===== Text Colors ===== */
  --color-text: #ffffff;
  --color-text-secondary: rgba(255, 255, 255, 0.7);
  --color-text-muted: rgba(255, 255, 255, 0.5);

  /* ===== Border Colors ===== */
  --color-border: rgba(255, 255, 255, 0.1);
  --color-border-strong: rgba(255, 255, 255, 0.2);

  /* ===== Brand Colors ===== */
  --color-primary: var(--primitive-blue-500);
  --color-primary-hover: var(--primitive-blue-600);
  --color-on-primary: #ffffff;

  --color-accent: var(--primitive-orange-500);
  --color-success: var(--primitive-green-500);
  --color-error: var(--primitive-red-500);

  /* ===== Glass Effect ===== */
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-bg-hover: rgba(255, 255, 255, 0.08);
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-shadow: rgba(0, 0, 0, 0.3);
}
```

### 라이트 테마

```css
[data-theme="light"] {
  /* ===== Surface Colors ===== */
  --color-bg: #ffffff;
  --color-surface: #f5f5f5;
  --color-surface-elevated: #ffffff;

  /* ===== Text Colors ===== */
  --color-text: #171717;
  --color-text-secondary: rgba(0, 0, 0, 0.7);
  --color-text-muted: rgba(0, 0, 0, 0.5);

  /* ===== Border Colors ===== */
  --color-border: rgba(0, 0, 0, 0.1);
  --color-border-strong: rgba(0, 0, 0, 0.2);

  /* ===== Brand Colors ===== */
  --color-primary: var(--primitive-blue-600);
  --color-primary-hover: var(--primitive-blue-500);
  --color-on-primary: #ffffff;

  --color-accent: var(--primitive-orange-500);
  --color-success: var(--primitive-green-500);
  --color-error: var(--primitive-red-500);

  /* ===== Glass Effect ===== */
  --glass-bg: rgba(255, 255, 255, 0.7);
  --glass-bg-hover: rgba(255, 255, 255, 0.85);
  --glass-border: rgba(0, 0, 0, 0.1);
  --glass-shadow: rgba(0, 0, 0, 0.1);
}
```

## 4. 컴포넌트 변수

### 컴포넌트별 로컬 변수

```css
/* 버튼 */
.btn {
  --btn-height: 40px;
  --btn-padding-x: var(--space-md);
  --btn-padding-y: var(--space-sm);
  --btn-font-size: var(--font-size-sm);
  --btn-radius: var(--radius-md);
  --btn-bg: var(--color-surface);
  --btn-text: var(--color-text);
  --btn-border: var(--color-border);
}

/* 카드 */
.card {
  --card-padding: var(--space-lg);
  --card-radius: var(--radius-lg);
  --card-bg: var(--color-surface);
  --card-border: var(--color-border);
  --card-shadow: var(--shadow-sm);
}

/* 입력 필드 */
.input {
  --input-height: 44px;
  --input-padding-x: var(--space-md);
  --input-font-size: var(--font-size-md);
  --input-radius: var(--radius-md);
  --input-bg: var(--color-surface);
  --input-border: var(--color-border);
}

/* 테이블 */
.table {
  --table-header-bg: var(--color-surface);
  --table-row-bg: transparent;
  --table-row-hover-bg: var(--color-surface);
  --table-border: var(--color-border);
  --table-cell-padding: var(--space-sm) var(--space-md);
}
```

## 5. Figma 변수 매핑

### 자동 변환되는 변수

| CSS 변수 | Figma 변수 타입 |
|----------|----------------|
| `--color-*` | Color |
| `--space-*` | Number |
| `--font-size-*` | Number |
| `--radius-*` | Number |
| `--shadow-*` | Effect |

### 변환 최적화 팁

1. **변수명 일관성**: kebab-case 사용
2. **계층 구조**: primitive → semantic → component
3. **테마 분리**: `[data-theme]` 선택자 사용
4. **단위 통일**: px 또는 rem 일관 사용

## 6. 사용 예시

```css
.glass-card {
  /* 컴포넌트 변수 정의 */
  --card-blur: var(--blur-lg);

  /* 변수 사용 */
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--card-radius);
  padding: var(--card-padding);
  backdrop-filter: blur(var(--card-blur));
  box-shadow: 0 8px 32px var(--glass-shadow);

  /* 트랜지션 */
  transition:
    background var(--transition-normal),
    border-color var(--transition-normal);
}

.glass-card:hover {
  background: var(--glass-bg-hover);
  border-color: var(--glass-border);
}
```
