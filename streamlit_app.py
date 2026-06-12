import streamlit as st

# 1. 앱 제목 및 설정
st.title("💧 수분 섭취 추적기 (Water Tracker)")
st.write("하루 목표를 설정하고 마신 물의 양을 기록해 보세요!")

# 2. 고정된 목표치 설정
GOAL = 2000

# 3. 데이터 유지를 위한 세션 상태(session_state) 초기화
if "water" not in st.session_state:
    st.session_state.water = []
if "total" not in st.session_state:
    st.session_state.total = 0

# 4. 사용자 입력 위젯 (음수 입력 방지를 위해 min_value=0 설정)
n = st.number_input(
    "물의 양을 입력하세요 (ml 단위)",
    min_value=0,
    max_value=2000,
    value=250,
    step=50,
)

# 5. 버튼 레이아웃
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ 물 섭취 기록하기", use_container_width=True):
        if n > 0:
            st.session_state.water.append(n)
            st.session_state.total += n
            st.success(f"성공적으로 기록되었습니다! (+{n}ml)")
        elif n == 0:
            st.warning("0ml는 기록되지 않습니다. 숫자를 변경해 주세요.")
        else:
            st.error("잘못된 입력입니다.")

with col2:
    if st.button("🔄 기록 초기화", use_container_width=True):
        st.session_state.water = []
        st.session_state.total = 0
        st.rerun()  # 화면 새로고침

# 안전한 구분선 추가
st.divider()

# 6. 결과 출력 및 대시보드 시각화
st.subheader("📊 오늘의 수분 섭취 현황")

left_col, right_col = st.columns(2)
with left_col:
    st.metric(
        label="지금까지 마신 물의 총량", value=f"{st.session_state.total} / {GOAL} ml"
    )
with right_col:
    remaining = GOAL - st.session_state.total
    st.metric(
        label="남은 목표량",
        value=f"{max(0, remaining)} ml",
        delta=f"-{n}ml" if n > 0 else None,
    )

# 7. 목표 달성 여부 판별
if GOAL <= st.session_state.total:
    st.balloons()  # 축하 풍선 이펙트 🎉
    st.success(f"🏆 목표 달성! 오늘 총 {st.session_state.total}ml의 물을 마셨습니다.")
else:
    st.info(f"💪 목표 달성까지 {remaining}ml 남았습니다. 힘내세요!")

# 8. 상세 기록 목록 표시
if st.session_state.water:
    st.write("**상세 섭취 기록 목록:**")
    st.dataframe(
        st.session_state.water,
        column_config={"value": "마신 양 (ml)"},
        use_container_width=True,
    )
    