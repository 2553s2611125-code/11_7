import streamlit as st

st.set_page_config(
    page_title="한끼의 여유",
    page_icon="🍚",
    layout="wide"
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #f7f4f1;
    color: #393333;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #4b3939 !important;
}
.hero {
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(120deg, #eee3dc, #f5efeb);
    border: 1px solid #e5d9d1;
    margin-bottom: 28px;
}
.hero p {
    color: #776564;
    font-size: 16px;
}
.hero h1 {
    color: #493535 !important;
}
.menu-card {
    background: #fffdfb;
    border: 1px solid #e5d9d1;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}
div.stButton > button {
    background-color: #8b6e68;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.5rem 1rem;
}
div.stButton > button:hover {
    background-color: #70544e;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 메뉴 데이터
# -----------------------------
MENUS = [
    {
        "name": "치킨 카레라이스",
        "category": "한식",
        "price": 11000,
        "ingredients": ["닭고기", "쌀", "당근", "감자"],
        "allergens": ["우유"],
        "time": 15
    },
    {
        "name": "크림 파스타",
        "category": "양식",
        "price": 12000,
        "ingredients": ["파스타", "우유", "버섯"],
        "allergens": ["밀", "우유"],
        "time": 20
    },
    {
        "name": "불고기 덮밥",
        "category": "한식",
        "price": 10000,
        "ingredients": ["소고기", "쌀", "양파", "간장"],
        "allergens": ["대두", "밀"],
        "time": 15
    },
    {
        "name": "마르게리타 피자",
        "category": "양식",
        "price": 15000,
        "ingredients": ["밀가루", "치즈", "토마토"],
        "allergens": ["밀", "우유"],
        "time": 25
    },
    {
        "name": "새우 볶음밥",
        "category": "중식",
        "price": 9000,
        "ingredients": ["새우", "쌀", "달걀", "채소"],
        "allergens": ["갑각류", "달걀", "대두"],
        "time": 12
    },
    {
        "name": "두부 채소 덮밥",
        "category": "한식",
        "price": 8500,
        "ingredients": ["두부", "쌀", "애호박", "당근"],
        "allergens": ["대두"],
        "time": 12
    },
    {
        "name": "토마토 달걀 덮밥",
        "category": "한식",
        "price": 7500,
        "ingredients": ["토마토", "달걀", "쌀"],
        "allergens": ["달걀"],
        "time": 10
    },
    {
        "name": "채소 수프와 식빵",
        "category": "간편식",
        "price": 7000,
        "ingredients": ["감자", "당근", "우유", "식빵"],
        "allergens": ["우유", "밀"],
        "time": 15
    },
    {
        "name": "연어 구이 정식",
        "category": "한식",
        "price": 12500,
        "ingredients": ["연어", "쌀", "채소"],
        "allergens": ["생선"],
        "time": 20
    },
    {
        "name": "바나나 오트밀",
        "category": "간편식",
        "price": 5000,
        "ingredients": ["바나나", "귀리", "우유"],
        "allergens": ["우유"],
        "time": 5
    },

    # 새로 추가한 메뉴 9개
    {
        "name": "소고기 채소죽",
        "category": "한식",
        "price": 8000,
        "ingredients": ["소고기", "쌀", "당근", "애호박"],
        "allergens": [],
        "time": 15
    },
    {
        "name": "닭고기 야채볶음밥",
        "category": "한식",
        "price": 9000,
        "ingredients": ["닭고기", "쌀", "당근", "양파"],
        "allergens": [],
        "time": 12
    },
    {
        "name": "감자 치즈전",
        "category": "한식",
        "price": 7000,
        "ingredients": ["감자", "치즈", "달걀"],
        "allergens": ["우유", "달걀"],
        "time": 15
    },
    {
        "name": "고구마 수프",
        "category": "간편식",
        "price": 6000,
        "ingredients": ["고구마", "우유"],
        "allergens": ["우유"],
        "time": 10
    },
    {
        "name": "참치 주먹밥",
        "category": "한식",
        "price": 6500,
        "ingredients": ["참치", "쌀", "김", "마요네즈"],
        "allergens": ["달걀"],
        "time": 10
    },
    {
        "name": "단호박 찜",
        "category": "간편식",
        "price": 5000,
        "ingredients": ["단호박"],
        "allergens": [],
        "time": 10
    },
    {
        "name": "잔치국수",
        "category": "한식",
        "price": 8000,
        "ingredients": ["면", "달걀", "애호박", "육수"],
        "allergens": ["밀", "달걀"],
        "time": 15
    },
    {
        "name": "바나나 팬케이크",
        "category": "디저트",
        "price": 6000,
        "ingredients": ["바나나", "밀가루", "달걀", "우유"],
        "allergens": ["밀", "달걀", "우유"],
        "time": 15
    },
    {
        "name": "사과 요거트볼",
        "category": "디저트",
        "price": 5500,
        "ingredients": ["사과", "플레인 요거트"],
        "allergens": ["우유"],
        "time": 5
    }
]

ALLERGENS = [
    "우유", "달걀", "밀", "대두", "땅콩",
    "견과류", "생선", "갑각류", "참깨"
]

PAGES = [
    "메인 화면",
    "식사 정보 QR",
    "메뉴 추천",
    "메뉴 목록",
    "내 정보",
    "설정"
]


# -----------------------------
# 기본 설정
# -----------------------------
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


def money(number):
    return f"{number:,}원"


def show_menu(menu):
    st.markdown(
        f"""
        <div class="menu-card">
            <h3>{menu['name']}</h3>
            <p>분류: {menu['category']}</p>
            <p>가격: {money(menu['price'])}</p>
            <p>준비 시간: 약 {menu['time']}분</p>
            <p>주요 재료: {', '.join(menu['ingredients'])}</p>
            <p>알레르기 정보: {
                ', '.join(menu['allergens'])
                if menu['allergens'] else '등록된 정보 없음'
            }</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    allergies = st.session_state.child_info["allergies"]
    if st.session_state.alerts and set(allergies) & set(menu["allergens"]):
        st.warning("⚠️ 입력한 알레르기 정보와 겹치는 성분이 있습니다.")


def navigation():
    cols = st.columns(3)

    for i, page in enumerate(PAGES):
        with cols[i % 3]:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()


# -----------------------------
# 상단 메뉴
# -----------------------------
st.title("🍚 아이랑 한끼")
navigation()
st.divider()


# -----------------------------
# 메인 화면
# -----------------------------
if st.session_state.page == "메인 화면":

    st.markdown("""
    <div class="hero">
        <p>👶 한끼의 여유</p>
        <h1>🍚 아이랑 한끼</h1>
        <p>아이도 편하고, 부모도 덜 바쁜 식사 준비 도우미</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("오늘의 식사를 더 편리하게")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥗 식사 정보 QR")
        st.write("메뉴와 재료, 알레르기 관련 정보를 확인해요.")
        if st.button("식사 정보 확인하기", use_container_width=True):
            st.session_state.page = "식사 정보 QR"
            st.rerun()

    with col2:
        st.markdown("### 🍱 메뉴 추천")
        st.write("예산과 준비 시간을 기준으로 메뉴를 살펴봐요.")
        if st.button("메뉴 살펴보기", use_container_width=True):
            st.session_state.page = "메뉴 추천"
            st.rerun()

    st.subheader("메뉴 미리 보기")

    cols = st.columns(3)
    for i, menu in enumerate(MENUS[:3]):
        with cols[i]:
            st.markdown(f"**{menu['name']}**")
            st.write(money(menu["price"]))


# -----------------------------
# 식사 정보 QR
# -----------------------------
elif st.session_state.page == "식사 정보 QR":

    st.header("📱 식사 정보 QR")
    st.write("QR 코드에 연결된 메뉴 정보를 확인하는 예시 화면이에요.")

    code = st.text_input(
        "QR 코드 번호를 입력하세요.",
        placeholder="예: MENU001"
    )

    if st.button("식사 정보 확인", use_container_width=True):

        if code.strip().upper() in ["MENU001", "BABY001", "1234"]:
            menu = MENUS[0]

            st.success("메뉴 정보를 확인했어요!")
            show_menu(menu)

            st.info(
                "알레르기 및 재료 정보는 예시입니다. "
                "실제 주문 전 식당에 정확한 재료와 조리 방법을 확인하세요."
            )

        elif code.strip():
            st.error("등록된 코드가 없어요. 코드를 다시 확인해 주세요.")

        else:
            st.warning("QR 코드 번호를 입력해 주세요.")

    st.caption(
        "현재는 QR 코드 번호를 입력하는 시연 화면이며, "
        "실제 카메라로 QR을 스캔하는 기능은 포함되어 있지 않아요."
    )


# -----------------------------
# 메뉴 추천
# -----------------------------
elif st.session_state.page == "메뉴 추천":

    st.header("🍱 메뉴 추천")
    st.write("예산과 준비 시간을 기준으로 메뉴를 찾아봐요.")

    info = st.session_state.child_info

    st.write(f"현재 예산: {money(info['budget'])}")
    st.write(f"준비 가능 시간: {info['minutes']}분")
    st.write(
        "알레르기 정보: "
        + (", ".join(info["allergies"]) if info["allergies"] else "선택 없음")
    )

    candidates = []

    for menu in MENUS:
        within_budget = menu["price"] <= info["budget"]
        within_time = menu["time"] <= info["minutes"]
        allergy_match = bool(
            set(info["allergies"]) & set(menu["allergens"])
        )

        if within_budget and within_time and not allergy_match:
            candidates.append(menu)

    candidates.sort(key=lambda x: (x["time"], x["price"]))

    if candidates:
        st.success(f"조건에 맞는 메뉴 {len(candidates)}개를 찾았어요.")

        for menu in candidates:
            show_menu(menu)

    else:
        st.warning(
            "현재 조건에 맞는 메뉴가 없어요. "
            "내 정보에서 예산이나 준비 시간을 조정해 보세요."
        )

    st.caption(
        "표시된 결과는 등록된 예시 정보에 따른 것이며, "
        "실제 알레르기 안전성을 보장하지 않아요."
    )


# -----------------------------
# 메뉴 목록
# -----------------------------
elif st.session_state.page == "메뉴 목록":

    st.header("📋 전체 메뉴 목록")

    category = st.selectbox(
        "메뉴 분류",
        ["전체", "한식", "양식", "중식", "간편식", "디저트"]
    )

    keyword = st.text_input("메뉴 이름 검색")

    filtered = []

    for menu in MENUS:
        category_match = (
            category == "전체" or menu["category"] == category
        )
        keyword_match = keyword.strip() in menu["name"]

        if category_match and keyword_match:
            filtered.append(menu)

    st.write(f"검색 결과: {len(filtered)}개")

    if filtered:
        for menu in filtered:
            show_menu(menu)
    else:
        st.info("조건에 맞는 메뉴가 없어요.")


# -----------------------------
# 내 정보
# -----------------------------
elif st.session_state.page == "내 정보":

    st.header("👶 아이 정보 및 식사 조건")
    st.write("아이의 정보와 식사 조건을 입력해 주세요.")

    info = st.session_state.child_info

    with st.form("child_info_form"):

        age = st.selectbox(
            "아이의 연령",
            ["0~6개월", "7~11개월", "12~24개월", "만 2세 이상"],
            index=[
                "0~6개월", "7~11개월",
                "12~24개월", "만 2세 이상"
            ].index(info["age"])
        )

        allergies = st.multiselect(
            "알레르기 유발 성분 선택",
            ALLERGENS,
            default=info["allergies"]
        )

        budget = st.slider(
            "한 끼 예산",
            min_value=5000,
            max_value=20000,
            value=info["budget"],
            step=1000
        )

        minutes = st.slider(
            "준비 가능한 시간",
            min_value=5,
            max_value=60,
            value=info["minutes"],
            step=5
        )

        submitted = st.form_submit_button(
            "정보 저장하기",
            use_container_width=True
        )

        if submitted:
            st.session_state.child_info = {
                "age": age,
                "allergies": allergies,
                "budget": budget,
                "minutes": minutes
            }

            st.success("정보를 저장했어요!")
            st.rerun()

    st.info(
        "알레르기 정보는 메뉴를 확인하기 위한 참고 자료입니다. "
        "실제 음식의 성분은 반드시 식당에 확인해 주세요."
    )


# -----------------------------
# 설정
# -----------------------------
elif st.session_state.page == "설정":

    st.header("⚙️ 설정")

    st.session_state.alerts = st.checkbox(
        "알레르기 주의 안내 표시",
        value=st.session_state.alerts
    )

    st.divider()

    st.subheader("앱 정보")
    st.write("앱 이름: 아이랑 한끼")
    st.write("버전: 1.0")
    st.write("주요 기능: 식사 정보 QR, 메뉴 목록, 식사 조건별 메뉴 찾기")

    st.caption(
        "이 앱은 영유아를 돌보는 부모의 식사 준비를 돕기 위한 "
        "학교 프로젝트용 예시 서비스입니다."
    )


# -----------------------------
# 하단 안내
# -----------------------------
st.divider()

st.caption(
    "아이랑 한끼 · 영유아를 돌보는 부모의 식사 준비를 돕는 앱"
)
