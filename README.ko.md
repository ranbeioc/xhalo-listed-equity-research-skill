# XHalo Listed Equity Research Skill — 상장기업 심층 리서치

**출처를 추적·검증할 수 있는 상장기업 분석용 Agent Skill.** 재무제표 품질, 산업 경쟁, 거시경제, 현금흐름, DCF/SOTP 가치평가, 데이터 차트 및 리서치 보고서를 일관된 절차로 작성합니다.

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [English](README.en.md)

> **중요:** `README.md`와 `SKILL.md`만 가져오면 실행되지 않습니다. `references/`, `assets/`, `scripts/`, `examples/`를 포함한 **`listed-equity-research/` 디렉터리 전체**를 설치하세요. 실시간 시세, 유료 증권사 보고서, 거래 실행, 개인별 투자 자문은 제공하지 않습니다.

## 주요 기능

- **기업 심층 분석:** 최근 3~5년 공시 재무제표, 최신 분기 실적, 사업별 경제성, 자본 배분.
- **회계 품질 검증:** 매출 총액/순액 표시, 투자 처분·간주처분 이익, 공정가치 변화, OCI, 일회성 손익과 비GAAP 조정.
- **현금흐름 분석:** CFO, FCFF/FCFE, 운전자본, 설비투자, 리스, 이자, 주식보상(SBC), 자사주 매입과 희석.
- **시장 및 거시경제:** 경쟁사, 점유율, 가격결정력, 가맹점과 고객 ROI, 소비, 고용, 가계 신용, 금리와 환율을 사업 KPI와 연결하고 동일 위험을 중복 반영하지 않음.
- **업종별 가치평가:** DCF, 역DCF, SOTP, 비교기업 멀티플. 은행, 보험, REIT, 광업, 바이오는 업종별 전용 방법 적용.
- **출처 포함 보고서:** 원문 URL, 날짜, 표 위치와 모델 가정을 관리하며, 지원하는 호스트에서 Markdown, HTML, PDF, DOCX, Excel로 문서화.

## 설치

Python 3.9 이상이 필요하며 PNG 차트에는 `matplotlib`가 추가로 필요합니다.

```bash
git clone https://github.com/ranbeioc/xhalo-listed-equity-research-skill.git
cd xhalo-listed-equity-research-skill
python install_listed_equity_research.py --root ~/.agents/skills --test
# Claude Code의 흔한 설치 위치 (실제 환경에 맞게 조정)
python install_listed_equity_research.py --root ~/.claude/skills --test
```

수동 설치도 **`listed-equity-research/` 폴더 전체**를 복사한 뒤 확인합니다.

```bash
python listed-equity-research/scripts/verify_install.py listed-equity-research
python listed-equity-research/scripts/self_test.py
```

## 분석 프롬프트 예시

**메이퇀(3690.HK)**

> `listed-equity-research`를 사용하여 최근 3년 연차보고서와 최신 중간보고서를 검증하라. 배송·가맹점 서비스·직매입 상품 매출을 구분하고 투자처분 손익과 OCI를 영업성과와 분리하라. Douyin, Alibaba, JD와의 경쟁 및 중국 가계 소비·신용을 분석하고 사업별 FCFF/SOTP, 역DCF, 약세/기본/강세 시나리오, 원문 링크와 그래프를 작성하라. 공시되지 않은 부문 수익성은 분석가 추정치로 표시하라.

**Microsoft(MSFT)**

> 클라우드 및 AI 설비투자, 감가상각, ROIC, FCF, 경쟁사 가치평가를 검토하고 역DCF로 현재 주가에 반영된 성장과 영업이익률을 추정하라.

**상장은행**

> 순이자마진, 예금 조달비용, 자산건전성, 대손충당금과 자기자본비율을 분석하고 P/B–ROE 및 잔여이익모형을 우선 적용하라. 일반 제조업의 FCFF 모형을 그대로 적용하지 말라.

## 오프라인 도구

```bash
python listed-equity-research/scripts/new_project.py --company "Example Corp" --ticker DEMO --exchange NASDAQ --output research/demo
python listed-equity-research/scripts/validate_research.py research/demo
python listed-equity-research/scripts/render_charts.py research/demo
python listed-equity-research/scripts/dcf_sotp.py listed-equity-research/assets/valuation.example.json --output research/demo-valuation.json
```

**예시의 가치평가 입력은 가상의 테스트 데이터입니다.** 계산 스크립트가 실제 시세 또는 원문을 자동 수집하거나 검증하는 것은 아닙니다. 전체 Word/PDF/Excel 출력은 호스트의 문서 도구가 있어야 합니다.

## 주의사항

1. 핵심 수치에 원문 URL, 발표일, 보고기간, 통화, 표·페이지 위치를 표시합니다.
2. 공식 공시, 정부 통계, 컨센서스, 증권사 전망, 분석가 추정, 가상 예시를 엄격히 구분합니다.
3. 투자 처분이익은 매출이 아니며 OCI 평가이익도 당기순이익이 아닙니다.
4. SOTP에서 보유 현금, 투자자산, 이연세금, 리스, SBC, 자사주 매입 및 희석을 중복 계상하지 않습니다.
5. 현금흐름과 할인율의 통화·명목/실질 기준을 일치시키고 영구성장과 종말가치 민감도를 공개합니다.
6. 필수 정보가 부족하면 `screen-grade` / `not-decision-ready`로 표시하여 근거 없는 정밀 목표주가를 피합니다.

참조: [SKILL.md](listed-equity-research/SKILL.md) · [설치 가이드](listed-equity-research/INSTALL.md) · [증거 규칙](listed-equity-research/references/evidence.md) · [메이퇀 사례](listed-equity-research/examples/meituan-case-methodology.md).

[기여 방법](CONTRIBUTING.md) · [보안 정책](SECURITY.md) · [MIT 라이선스](LICENSE).
