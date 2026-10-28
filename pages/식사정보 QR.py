
import streamlit as st

st.set_page_config(
    page_title="아이랑 한끼",
    page_icon="🍚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background-color: #fffdf7;}
.block-container {max-width: 1100px; padding-top: 2rem;}
.hero {
    padding: 25px;
    border-radius: 22px;
    background: linear-gradient(110deg, #fff0d8, #edf7e9);
}
.hero h1 {color: #24513e;}
div.stButton > button {
    border-radius: 12px;
    min-height: 2.6rem;
}
</style>
""", unsafe_allow_html=True)

MENUS = [
    {"name":"치킨 카레라이스","category":"한식","price":11000,
     "ingredients":["닭고기","쌀","당근","감자"],"allergens":["우유"],"time":15},
    {"name":"크림 파스타","category":"양식","price":12000,
     "ingredients":["파스타","우유","버섯"],"allergens":["밀","우유"],"time":20},
    {"name":"불고기 덮밥","category":"한식","price":10000,
     "ingredients":["소고기","쌀","양파","간장"],"allergens":["대두","밀"],"time":15},
    {"name":"마르게리타 피자","category":"양식","price":15000,
     "ingredients":["밀가루","치즈","토마토"],"allergens":["밀","우유"],"time":25},
    {"name":"새우 볶음밥","category":"중식","price":9000,
     "ingredients":["새우","쌀","달걀","채소"],"allergens":["갑각류","달걀","대두"],"time":12},
    {"name":"두부 채소 덮밥","category":"한식","price":8500,
     "ingredients":["두부","쌀","애호박","당근"],"allergens":["대두"],"time":12},
    {"name":"토마토 달걀 덮밥","category":"한식","price":7500,
     "ingredients":["토마토","달걀","쌀"],"allergens":["달걀"],"time":10},
    {"name":"채소 수프와 식빵","category":"간편식","price":7000,
     "ingredients":["감자","당근","우유","식빵"],"allergens":["우유","밀"],"time":15},
    {"name":"연어 구이 정식","category":"한식","price":12500,
     "ingredients":["연어","쌀","채소"],"allergens":["생선"],"time":20},
    {"name":"바나나 오트밀","category":"간편식","price":5000,
     "ingredients":["바나나","귀리","우유"],"allergens":["우유"],"time":5},
]

ALLERGENS = [
    "우유", "달걀", "밀", "대두", "땅콩",
    "견과류", "생선", "갑각류", "참깨"
]

PAGES = [
    "메인 화면", "식사 정보 QR", "메뉴 추천",
    "메뉴 목록", "내 정보", "설정"
]

if "page" not in st.session_state:
    st.session_state.page = "메인 화면"

if "child_info" not in st.session_state:
    st.session_state.child_info = {
        "age": "12~24개월",
        "allergies": [],
        "budget": 12000,
        "minutes": 15
    }

if "alerts" not in st.session_state:
    st.session_state.alerts = True

def money(n):
    return f"{n:,}원"

def go(page):
    st.session_state.page = page

st.markdown("""
<div class="hero">
    <p>👶 아이와 함께하는 식사, 조금 더 편리하게</p>
    <h1>🍚 아이랑 한끼</h1>
    <p>아이도 편하고, 부모도 덜 바쁜 식사 준비 도우미</p>
</div>
""", unsafe_allow_html=True)

st.write("### 원하는 기능을 선택하세요")

cols = st.columns(3)

for i, page_name in enumerate(PAGES):
    with cols[i % 3]:
        if st.button(
            page_name,
            key="nav_" + page_name,
            use_container_width=True
        ):
            go(page_name)
            st.rerun()

st.divider()

page = st.session_state.page
info = st.session_state.child_info

if page == "메인 화면":
    st.subheader("오늘도 아이와 함께 든든하게!")
    st.write(
        "아이를 돌보느라 식사를 놓치기 쉬운 부모를 위한 "
        "식사 정보 서비스입니다."
    )

    a, b, c = st.columns(3)
    a.metric("등록 메뉴", f"{len(MENUS)}개")
    b.metric("조리 가능 시간", f"{info['minutes']}분")
    c.metric("한 끼 예산", money(info["budget"]))

    st.info(
        "식사 정보 QR, 메뉴 추천, 메뉴 목록, "
        "아이 정보와 설정을 이용할 수 있어요."
    )

elif page == "식사 정보 QR":
    st.subheader("▦ 식사 정보 QR")
    st.write("메뉴 코드를 입력하여 식사 정보를 확인하세요.")
    st.caption(
        "실제 카메라 스캔이 아닌 코드 입력 방식의 데모입니다."
    )

    code = st.text_input(
        "메뉴 코드",
        placeholder="예: BABY001"
    ).strip().upper()

    if st.button("QR 메뉴 정보 확인", type="primary"):
        if code in ["BABY001", "MENU001", "1234"]:
            st.success("메뉴 정보를 찾았어요!")
            st.markdown("### 🍛 치킨 카레라이스")
            st.write("가격: 11,000원")
            st.write("주요 재료: 닭고기, 쌀, 당근, 감자")
            st.write("예시 알레르기 표기: 우유")
            st.warning(
                "실제 주문 전 식당에 원재료와 "
                "교차접촉 가능성을 확인하세요."
            )
        elif not code:
            st.warning("메뉴 코드를 입력해 주세요.")
        else:
            st.error("등록되지 않은 코드입니다. BABY001을 입력해 보세요.")

elif page == "메뉴 추천":
    st.subheader("✨ 아이와 함께 먹을 메뉴 추천")

    st.write(
        f"예산 {money(info['budget'])} 이하, "
        f"조리 시간 {info['minutes']}분 이내"
    )

    blocked = set(info["allergies"])

    results = [
        m for m in MENUS
        if m["price"] <= info["budget"]
        and m["time"] <= info["minutes"]
        and not blocked.intersection(m["allergens"])
    ]

    if not results:
        st.warning(
            "조건에 맞는 메뉴가 없어요. "
            "내 정보에서 예산이나 시간을 조정해 보세요."
        )
    else:
        for m in sorted(results, key=lambda x: (x["time"], x["price"])):
            with st.container(border=True):
                st.markdown(
                    f"### 🍽️ {m['name']} · {money(m['price'])}"
                )
                st.write(f"예상 조리 시간: {m['time']}분")
                st.write("재료: " + ", ".join(m["ingredients"]))
                st.write("알레르기 표기: " + ", ".join(m["allergens"]))

    st.caption(
        "메뉴 추천은 예시 데이터에 따른 참고 정보입니다. "
        "실제 식품 안전을 보장하지 않습니다."
    )

elif page == "메뉴 목록":
    st.subheader("🍲 전체 메뉴 목록")

    category = st.selectbox(
        "메뉴 분류",
        ["전체", "한식", "양식", "중식", "간편식"]
    )

    query = st.text_input("메뉴 검색", placeholder="음식 이름 입력")

    items = [
        m for m in MENUS
        if (category == "전체" or m["category"] == category)
        and query.strip().lower() in m["name"].lower()
    ]

    if not items:
        st.info("검색 결과가 없습니다.")
    else:
        for m in items:
            with st.container(border=True):
                st.markdown(f"### 🍽️ {m['name']}")
                st.write(f"가격: {money(m['price'])}")
                st.write(f"분류: {m['category']}")
                st.write(f"재료: {', '.join(m['ingredients'])}")
                st.write(f"알레르기: {', '.join(m['allergens'])}")
                st.write(f"예상 조리 시간: {m['time']}분")

                overlap = set(info["allergies"]).intersection(
                    m["allergens"]
                )

                if overlap and st.session_state.alerts:
                    st.error(
                        "⚠️ 등록된 알레르기 성분: "
                        + ", ".join(sorted(overlap))
                    )

elif page == "내 정보":
    st.subheader("👶 아이 정보 및 알레르기 설정")

    with st.form("child_info_form"):
        age_options = [
            "0~6개월", "7~11개월",
            "12~24개월", "만 2세 이상"
        ]

        age = st.selectbox(
            "아이 연령대",
            age_options,
            index=age_options.index(info["age"])
        )

        allergies = st.multiselect(
            "확인할 알레르기 항목",
            ALLERGENS,
            default=info["allergies"]
        )

        budget = st.slider(
            "한 끼 예산",
            5000, 20000,
            int(info["budget"]),
            step=1000
        )

        minutes = st.slider(
            "준비 가능한 시간(분)",
            5, 60,
            int(info["minutes"]),
            step=5
        )

        save = st.form_submit_button(
            "정보 저장",
            type="primary"
        )

    if save:
        st.session_state.child_info = {
            "age": age,
            "allergies": allergies,
            "budget": budget,
            "minutes": minutes
        }
        st.success("정보를 저장했어요!")
        st.rerun()

    if info["allergies"]:
        st.warning(
            "등록된 알레르기: " + ", ".join(info["allergies"])
        )

    st.caption(
        "영유아의 음식은 발달 단계에 맞는지 보호자가 확인하세요. "
        "입력 정보는 영구 저장되지 않을 수 있습니다."
    )

elif page == "설정":
    st.subheader("⚙️ 앱 설정")

    alerts = st.checkbox(
        "알레르기 경고 표시",
        value=st.session_state.alerts
    )

    if st.button("설정 저장", type="primary"):
        st.session_state.alerts = alerts
        st.success("설정을 저장했어요!")

    st.divider()
    st.write("**앱 이름:** 아이랑 한끼")
    st.write("**버전:** 1.0")
    st.write("**주요 기능:** 메뉴 확인, 알레르기 안내, 메뉴 추천")

st.divider()
st.caption("아이랑 한끼 · 영유아를 돌보는 부모의 식사 준비를 돕는 앱")

