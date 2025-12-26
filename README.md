# Figma Design with Claude

Claude를 사용하여 웹 디자인을 생성하고 Figma 디자인 가이드로 변환하는 프로젝트

## 개요

이 프로젝트는 Claude AI를 활용하여 웹페이지 디자인을 생성하고, 이를 Figma 컴포넌트 기반 디자인 시스템으로 변환하는 워크플로우를 제공합니다.

---

## 1. Figma 변환을 위한 최적화된 웹페이지 만들기

### 1.1 Design Tokens 사용

CSS 변수로 디자인 토큰을 정의하면 Figma에서 자동으로 스타일 변수로 변환됩니다.

```css
:root {
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;

  /* Typography */
  --font-size-sm: 0.875rem;
  --font-size-md: 1rem;
  --font-size-lg: 1.25rem;

  /* Colors */
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --accent-primary: #ff6b35;

  /* Border Radius */
  --radius-sm: 12px;
  --radius-md: 20px;
  --radius-lg: 28px;
}
```

### 1.2 테마 지원 (다크/라이트 모드)

`data-theme` 속성을 사용하여 테마별 스타일을 분리합니다.

```css
[data-theme="dark"] {
  --glass-bg: rgba(20, 20, 25, 0.6);
  --text-primary: #ffffff;
}

[data-theme="light"] {
  --glass-bg: rgba(255, 255, 255, 0.6);
  --text-primary: #1a1a2e;
}
```

### 1.3 컴포넌트 구조화

Figma 컴포넌트로 변환하기 좋은 HTML 구조:

```html
<!-- 명확한 클래스명으로 컴포넌트 식별 -->
<div class="card glass-card">
  <div class="card-header">...</div>
  <div class="card-body">...</div>
</div>

<!-- 상태 변화는 클래스로 표현 (hover variants 생성) -->
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary active">Active</button>
```

### 1.4 Auto Layout 친화적 스타일

Flexbox와 Grid를 사용하면 Figma Auto Layout으로 자동 변환됩니다.

```css
.container {
  display: flex;
  flex-direction: column;
  gap: 16px;  /* Figma의 spacing으로 변환 */
  padding: 24px;
}
```

### 1.5 권장 사항

| 항목 | 권장 | 비권장 |
|------|------|--------|
| 단위 | `px`, `rem` | `vh`, `vw`, `%` (복잡한 계산) |
| 레이아웃 | Flexbox, Grid | Position absolute |
| 색상 | CSS 변수 | 하드코딩된 값 |
| 폰트 | 시스템 폰트, Google Fonts | 로컬 커스텀 폰트 |

---

## 2. HTML을 Figma 디자인 가이드로 변환하기

### 2.1 필요한 도구

1. **Figma 플러그인**: [html.to.design](https://www.figma.com/community/plugin/1159123024924461424)
2. **Chrome 확장**: [html.to.design Extension](https://chromewebstore.google.com/detail/htmltodesign/ldnheaepmnmbjjjahokphckbpgciiaed)

### 2.2 변환 프로세스

#### Step 1: 로컬 서버 실행

```bash
cd /path/to/project
python3 -m http.server 8080
```

#### Step 2: Chrome에서 페이지 열기

```
http://localhost:8080/liquid-glass.html
```

#### Step 3: 페이지 캡처

1. Chrome 상단의 확장 프로그램 아이콘 클릭
2. **html.to.design** 선택
3. 캡처 완료 후 **"Send to Figma"** 클릭

#### Step 4: Figma에서 가져오기

1. Figma에서 새 파일 생성
2. 우클릭 → **Plugins** → **html.to.design**
3. **"Receive"** 탭에서 가져오기

### 2.3 가져오기 옵션

| 옵션 | 설명 | 권장 |
|------|------|------|
| Import styles | CSS 스타일을 Figma 변수로 변환 | O |
| Auto layout | Flexbox/Grid를 Auto Layout으로 변환 | O |
| Generate components | 반복 요소를 컴포넌트로 생성 | O |
| Include hover states | hover 상태를 variants로 생성 | O |

### 2.4 변환 후 정리 작업

1. **컴포넌트 정리**: 생성된 컴포넌트 이름 정리 및 그룹화
2. **스타일 확인**: 색상, 타이포그래피 변수 검토
3. **Auto Layout 조정**: 패딩, 간격 미세 조정
4. **반응형 설정**: 필요시 Constraints 설정

---

## 3. 프로젝트 구조

```
figma-design-with-claude/
├── README.md              # 프로젝트 문서
├── liquid-glass.html      # Liquid Glass 디자인 예제
└── .claude/
    └── plans/             # Claude 작업 계획 파일
```

---

## 4. 디자인 가이드 예제

### 포함된 컴포넌트

- **Glass Card**: 투명 배경의 카드 컴포넌트
- **Filter Buttons**: 활성/비활성 상태 variants
- **Data Table**: 정렬 가능한 테이블
- **Search Box**: 검색 입력 필드
- **Theme Toggle**: 다크/라이트 모드 전환

### 디자인 토큰

- **Colors**: Primary, Secondary, Accent, Team colors
- **Typography**: Font sizes (xs ~ 2xl)
- **Spacing**: 4px 기반 스케일 (xs ~ 2xl)
- **Border Radius**: sm, md, lg, full
- **Transitions**: fast, normal, slow

---

## 5. 문제 해결

### SVG 내보내기가 Figma에서 빈 프레임으로 나타남

**원인**: `html-to-image` 라이브러리의 `toSvg()`는 `foreignObject`를 사용하는데, Figma는 이를 지원하지 않음

**해결**: PNG로 내보내기 (`toPng()` 사용) 또는 html.to.design 플러그인 사용

### 폰트가 다르게 보임

**원인**: 시스템에 해당 폰트가 설치되지 않음

**해결**: 웹 폰트(Google Fonts) 사용 또는 시스템 폰트 스택 사용

### Auto Layout이 제대로 적용되지 않음

**원인**: 복잡한 position absolute 레이아웃

**해결**: Flexbox/Grid 기반으로 레이아웃 재구성

---

## 6. 참고 자료

- [html.to.design 공식 문서](https://html.to.design/home/)
- [Figma Variables](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
- [Figma Auto Layout](https://help.figma.com/hc/en-us/articles/5731482952599-Using-auto-layout)

---

## 라이선스

MIT License
