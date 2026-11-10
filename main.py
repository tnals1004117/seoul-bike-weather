
import streamlit as st
import pandas as pd
from ucimlrepo import fetch_ucirepo

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="따릉이 날씨 예측 연구소",
    page_icon="🚲",
    layout="wide"
)

st.title("🚲 따릉이 날씨 예측 연구소")
st.caption("날씨에 따른 서울시 공공자전거 대여량 분석 및 예측")

st.divider()

# -------------------------
# 데이터 불러오기
# -------------------------
@st.cache_data(ttl=3600)
def load_data():
    bike = fetch_ucirepo(id=560)

    features = bike.data.features
    targets = bike.data.targets

    df = pd.concat([features, targets], axis=1)

    return df

st.header("1. 데이터 수집")

st.write("""
UCI Machine Learning Repository에서 제공하는
서울시 공공자전거 대여량 데이터를 불러옵니다.
""")

with st.spinner("데이터를 불러오는 중입니다..."):
    try:
        df = load_data()
        st.success("데이터 수집에 성공했습니다!")

    except Exception as e:
        st.error("데이터를 불러오지 못했습니다.")
        st.exception(e)
        st.stop()

# -------------------------
# 데이터 기본 정보
# -------------------------
st.header("2. 데이터 기본 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 데이터 수", f"{len(df):,}개")

with col2:
    st.metric("전체 열 개수", f"{len(df.columns)}개")

with col3:
    st.metric(
        "전체 결측치",
        f"{df.isnull().sum().sum():,}개"
    )

st.divider()

# -------------------------
# 데이터 열 확인
# -------------------------
st.header("3. 데이터 열 확인")

column_info = pd.DataFrame({
    "열 이름": df.columns,
    "데이터 종류": [
        str(df[col].dtype) for col in df.columns
    ],
    "결측치 개수": [
        df[col].isnull().sum() for col in df.columns
    ]
})

st.dataframe(
    column_info,
    use_container_width=True,
    hide_index=True
)

# -------------------------
# 데이터 미리보기
# -------------------------
st.header("4. 데이터 미리보기")

st.write("수집한 데이터의 처음 10개 행입니다.")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)

# -------------------------
# 결측치 확인
# -------------------------
st.header("5. 결측치 확인")

missing = pd.DataFrame({
    "열 이름": df.columns,
    "결측치 개수": [
        df[col].isnull().sum() for col in df.columns
    ]
})

st.dataframe(
    missing,
    use_container_width=True,
    hide_index=True
)

if df.isnull().sum().sum() == 0:
    st.success("결측치가 없습니다.")
else:
    st.warning("결측치가 있는 열을 확인해야 합니다.")

# -------------------------
# CSV 다운로드
# -------------------------
st.divider()

st.header("6. 데이터 다운로드")

csv = df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="📥 원본 데이터 CSV 다운로드",
    data=csv,
    file_name="bike_weather_raw.csv",
    mime="text/csv"
)

st.info("""
다음 단계에서는 날짜, 시간, 날씨 등의 데이터를 분석하고
날씨와 따릉이 대여량 사이의 관계를 그래프로 살펴봅니다.
""")
