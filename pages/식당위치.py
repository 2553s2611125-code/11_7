
import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlencode

# ---------- 기본 설정 ----------
st.set_page_config(
    page_title="아기랑 편한 한 끼",
    page_icon="👶",
    layout="wide",
)

# ---------- 세션 상태 초기화 ----------
if "restaurant_query" not in st.session_state:
    st.session_state["restaurant_query"] = ""

if "restaurant_region" not in st.session_state:
    st.session_state["restaurant_region"] = ""

# ---------- 화면 디자인 ----------
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 1.6rem;
            border-radius: 18px;
            background: linear-gradient(120deg, #fff0e6, #fff8dc);
            margin-bottom: 1.2rem;
        }

        .hero h1 {
            color: #573b2a;
            margin-bottom: 0.5rem;
        }

        .hero p {
            color: #654c3a;
            font-size: 1.05rem;
        }

        .info-card {
            border: 1px solid #eee3d9;
            padding: 1rem;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>👶 아기랑 편한 한 끼</h1>
        <p>아이와 함께 외식하는 부모님을 위한 식당 검색 도우미</p>
        <p>우리 가족에게 맞는 식당을 찾아보고 지도에서 위치를 확인해 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- 검색 조건 ----------
st.subheader("🔎 우리 가족에게 맞는 식당 찾기")

food_options = [
    "전체 음식",
    "한식",
    "국수·면 요리",
    "고기·구이",
    "돈가스·일식",
    "중식",
    "양식·파스타",
    "분식",
    "카페·브런치",
]

food_terms = {
    "전체 음식": "식당",
    "한식": "한식 식당",
    "국수·면 요리": "국수 면 요리 식당",
    "고기·구이": "고기 구이 식당",
    "돈가스·일식": "돈가스 일식 식당",
    "중식": "중식당",
    "양식·파스타": "양식 파스타 식당",
    "분식": "분식집",
    "카페·브런치": "브런치 카페",
}

with st.form("restaurant_search"):
    col1, col2 = st.columns(2)

    with col1:
        region = st.text_input(
            "📍 검색할 지역",
            value="충남 천안시",
            help="예: 천안시 불당동, 천안역 주변, 서울 강남구",
        )

        food = st.selectbox(
            "🍚 먹고 싶은 음식",
            food_options,
        )

    with col2:
        needs = st.multiselect(
            "🍼 중요하게 생각하는 편의시설",
            [
                "아기 의자",
                "유아 메뉴",
                "유모차 이용 편의",
                "주차 가능",
                "넓은 좌석",
                "놀이 공간",
            ],
            help="선택한 조건은 지도 검색어에 반영됩니다. 실제 시설은 식당에 확인하세요.",
        )

        extra = st.text_input(
            "추가 검색어 (선택)",
            placeholder="예: 룸, 조용한 식당, 예약 가능",
        )

    submitted = st.form_submit_button(
        "식당 검색하기",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        if not region.strip():
            st.session_state["restaurant_query"] = ""
            st.session_state["restaurant_region"] = ""
            st.error("검색할 지역을 입력해 주세요.")
        else:
            # 검색어를 만들고 세션 상태에 저장
            search_parts = [
                region.strip(),
                food_terms[food],
                *needs,
                extra.strip(),
            ]

            query = " ".join(
                part for part in search_parts if part
            )

            st.session_state["restaurant_query"] = query
            st.session_state["restaurant_region"] = region.strip()

# ---------- 지도와 검색 결과 ----------
query = st.session_state["restaurant_query"]
saved_region = st.session_state["restaurant_region"]

if query:
    st.divider()
    st.subheader("🗺️ 식당 위치 지도")
    st.write(f"**검색 지역:** {saved_region}")
    st.caption(f"지도 검색어: {query}")

    # Google 지도 검색 URL
    search_url = (
        "https://www.google.com/maps/search/?"
        + urlencode({"api": "1", "query": query})
    )

    # Google 지도 삽입용 URL
    embed_url = (
        "https://maps.google.com/maps?"
        + urlencode({
            "q": query,
            "output": "embed",
        })
    )

    try:
        components.iframe(
            embed_url,
            height=480,
            scrolling=True,
        )
    except Exception:
        st.warning(
            "지도를 화면에 표시하지 못했습니다. "
            "아래 버튼으로 지도에서 검색해 주세요."
        )

    st.link_button(
        "📍 Google 지도에서 식당 목록과 길찾기 보기",
        search_url,
        use_container_width=True,
    )

    st.info(
        "지도에서 식당을 선택하면 주소와 길찾기를 확인할 수 있습니다. "
        "검색 결과와 운영 정보는 지도 서비스에 따라 달라질 수 있습니다."
    )

else:
    st.info(
        "위에서 지역과 음식 종류를 선택한 뒤 "
        "'식당 검색하기'를 누르면 지도 검색 결과가 표시됩니다."
    )

# ---------- 방문 전 체크리스트 ----------
st.divider()
st.subheader("💛 방문 전 확인 체크리스트")

st.caption(
    "방문 전에 직접 확인해 보세요. "
    "체크한 항목은 식당의 실제 시설을 보장하지 않습니다."
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**🍼 아이 편의**")
    st.checkbox("아기 의자 여부 확인", key="check_baby_chair")
    st.checkbox("유아 식기·메뉴 확인", key="check_kids_menu")

with c2:
    st.markdown("**🚗 이동 편의**")
    st.checkbox("주차장 여부 확인", key="check_parking")
    st.checkbox("유모차 진입 가능 여부 확인", key="check_stroller")

with c3:
    st.markdown("**🍽️ 식사 환경**")
    st.checkbox("유아 동반 좌석 확인", key="check_seating")
    st.checkbox("대기 시간·예약 여부 확인", key="check_reservation")

st.caption(
    "※ 이 앱은 지도 검색을 도와주는 도구입니다. "
    "방문 전에 식당에 전화해 아기 의자, 유아 메뉴, "
    "영업시간 등을 확인하세요."
)
