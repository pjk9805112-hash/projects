# Chroma v2 - Pro Workflow 개발 계획서

**컨셉: 잠그고 돌리고, 검증하고, 바로 뽑아쓴다.**
단순한 색상 도구를 넘어서 디자이너가 팔레트를 확정하고 개발자에게 전달하기까지의 마지막 10분을 30초로 줄이는 앱. Coolors의 재미 + Figma의 실무성 + Stark의 접근성을 하나로 통합.

---

## 1. 목표 정의
- **Target User:** 브랜드/프로덕트 디자이너, 1인 창업자, 프론트엔드 개발자
- **Core Value:** 팔레트 탐색 → 시스템화 → 접근성 검증 → 개발 전달까지 원스톱 워크플로우 제공

## 2. 4대 핵심 기능 상세 기획

### A. Color Lock & Shuffle [핵심 재미 요소]
- **UX:** 5개 컬러 카드. 각 카드에 자물쇠 아이콘, 스페이스바로 셔플. 드래그앤드롭으로 순서 변경.
- **로직:** 잠금된 색상의 HUE를 유지하고, 잠금 안 된 색상만 HSL 공간에서 ±30도 이내로 조화롭게 랜덤 생성. 완전 랜덤이 아니라 `Analogous`와 `Complementary` 로직을 섞어서 이상한 색이 안 나오게 설계.
- **데이터:** `st.session_state`로 `locked: [bool]*5` 상태 관리.
- **인터랙션:** Spacebar = Shuffle, L = Lock, C = Copy HEX

### B. Light / Dark 10단계 Scale Generator [실무 표준]
- **UX:** 베이스 컬러 1개 선택하면 자동으로 50, 100, 200, 300, 400, 500, 600, 700, 800, 900 스케일 생성. 50은 거의 흰색, 900은 거의 검정에 가깝게.
- **로직:** 단순히 Lightness만 바꾸면 채도가 죽어서 칙해짐. **LCH 색공간** 기반으로 Lightness는 바꾸고 Chroma는 유지하는 방식 필요. Tailwind CSS 방식 참고.
- **출력:** 테이블 뷰 + 각 스케일 hover 시 HEX 복사. 500이 Base Color.

### C. Color Blind Simulator [신뢰도 요소]
- **UX:** 내 팔레트 상단에 토글 버튼 4개 - Original / Deuteranopia(적녹) / Protanopia(적색맹) / Tritanopia(청황색맹)
- **로직:** 라이브러리는 `colorspacious` 또는 Brettel 알고리즘 직접 구현. RGB → LMS 변환 행렬을 이용해 시뮬레이션. 성능을 위해 numpy 벡터 연산.
- **중요 포인트:** 카드 전체가 아니라 텍스트 가독성까지 같이 변해야 하므로, 팔레트 프리뷰와 Contrast Grid에 동시에 적용.
- **검증 기준:** Stark, Sim Daltonism 앱과 시각적 비교 검증.

### D. Export Pro [수익화/락인 요소]
- **지원 포맷 4종:**
  1.  **Figma Variables (JSON)** - Figma에서 바로 import 가능
  2.  **ASE** - Illustrator/Photoshop용 Swatch. `swatch` 라이브러리로 인코딩
  3.  **Tailwind Config** - `colors: { primary: { 50: ..., 900: ... } }` 형태
  4.  **CSS Variables + Style Dictionary용 JSON**
- **UX:** 오른쪽 상단 `Export` 버튼 → 모달에서 포맷 선택 → 미리보기 → 다운로드. 프로처럼 보이려면 포맷별 코드 하이라이트 필수.

---

## 3. 전체 앱 구조 및 기술 스택

```
designer_tools/
├── app.py (메인 라우터, sidebar, session_state 관리)
├── components/
│   ├── palette_card.py (잠금 카드 UI, 드래그앤드롭)
│   ├── scale_generator.py (10단계 생성 로직 - LCH 기반)
│   ├── blind_sim.py (색맹 변환 로직)
│   └── exporter.py (4종 포맷 변환)
├── utils/
│   ├── color_convert.py (HEX/RGB/HSL/LCH 변환 유틸)
│   └── colorblind_matrix.py (Deuter/Protan/Tritan 행렬)
├── requirements.txt
└── assets/
```

**추가 라이브러리:**
- `colorspacious` (색맹 시뮬 + LCH 변환)
- `colour-science` (대안)
- `streamlit-extras` (카드 UI, 버튼 스타일링, 토스트)
- `Pillow` (ASE 생성용)
- `streamlit-keyboard` 또는 `streamlit-shortcuts` (Spacebar 이벤트)

## 4. 개발 로드맵 (총 5일)

### Day 1: 기반 구축 - Lock & Shuffle
- 기존 app.py 리팩토링해서 `session_state`로 팔레트 상태 관리
- Lock & Shuffle UI 프로토타입 완성
- 스페이스바 이벤트는 `streamlit-keyboard` 컴포넌트 활용

### Day 2: Scale Generator
- LCH 기반 10단계 알고리즘 구현, Tailwind와 비교 테스트
- 카드 UI에 스케일 펼치기(Acordion) 기능 추가

### Day 3: Color Blind Simulator
- 3가지 색맹 변환 행렬 구현 및 토글 UI
- Contrast Grid와 연동해서 시뮬레이션 모드에서도 WCAG 점수 재계산

### Day 4: Export Pro
- 4가지 포맷 인코더 구현. ASE가 제일 까다로우니 마지막에 처리
- Figma Variables 포맷은 Figma 공식 문서 기준으로 검증

### Day 5: 폴리싱 & 배포
- 키보드 단축키 (Space: shuffle, C: copy, L: lock)
- 복사 시 토스트 알림, 모바일 반응형 체크
- Streamlit Community Cloud 배포

## 5. 리스크와 해결책

| 리스크 | 해결책 |
| :--- | :--- |
| **ASE 인코딩** | Streamlit에서 직접 바이너리 생성 시 깨질 수 있음 → 대안으로 `.aco`나 `.gpl`도 함께 제공 |
| **색맹 알고리즘 정확도** | 의학적 100% 정확도보다 디자이너 체감용으로 접근, Stark나 Sim Daltonism 앱과 시각적 비교로 검증 |
| **Streamlit의 Spacebar 이벤트** | 네이티브 지원이 약함 → `streamlit-shortcuts` 커스텀 컴포넌트 사용, 버튼으로도 셔플 가능하게 fallback 제공 |
| **LCH 변환 성능** | `colorspacious`는 무거울 수 있음 → `colormath` 경량 라이브러리로 대체 검토 |

## 6. 성공 기준
- 디자이너가 Spacebar 10번 이내에 마음에 드는 팔레트를 찾는다.
- 생성된 10단계 스케일을 Figma에 붙여넣었을 때 바로 디자인 시스템으로 쓸 수 있다.
- 색맹 모드에서도 AA를 통과하는 조합을 5초 안에 찾을 수 있다.

---
*Generated for Chroma v2 - 2026*
