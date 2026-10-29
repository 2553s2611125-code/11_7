import random
import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="우리끼니 | 오늘의 메뉴 추천",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 메뉴 데이터
# -----------------------------
MENUS = [
    {
        "name": "소고기 채소죽",
        "description": "부드러운 식감으로 아침이나 가벼운 식사에 잘 어울려요.",
        "time": 20,
        "ingredients": ["소고기", "쌀", "당근", "애호박"],
        "difficulty": "쉬움",
        "meal_type": "아침",
        "menu_type": "죽",
        "steps": ["소고기와 채소를 잘게 다져요.", "냄비에 재료와 불린 쌀을 넣어요.", "물을 넣고 쌀이 충분히 익을 때까지 끓여요."],
    },
    {
        "name": "닭고기 채소볶음밥",
        "description": "닭고기와 여러 채소를 한 번에 준비할 수 있는 메뉴예요.",
        "time": 20,
        "ingredients": ["닭고기", "밥", "당근", "양파"],
        "difficulty": "쉬움",
        "meal_type": "점심",
        "menu_type": "밥",
        "steps": ["닭고기와 채소를 잘게 썰어요.", "팬에 닭고기를 충분히 익혀요.", "채소와 밥을 넣고 골고루 볶아요."],
    },
    {
        "name": "두부 달걀찜",
        "description": "두부와 달걀을 활용해 부드럽게 만들 수 있어요.",
        "time": 15,
        "ingredients": ["두부", "달걀"],
        "difficulty": "쉬움",
        "meal_type": "저녁",
        "menu_type": "찜",
        "steps": ["두부를 곱게 으깨요.", "달걀을 풀어 두부와 섞어요.", "그릇에 담아 속까지 익도록 쪄요."],
    },
    {
        "name": "감자 당근 수프",
        "description": "감자와 당근을 익혀 부드럽게 갈아 만드는 수프예요.",
        "time": 25,
        "ingredients": ["감자", "당근", "우유"],
        "difficulty": "보통",
        "meal_type": "아침",
        "menu_type": "수프",
        "steps": ["감자와 당근을 작게 썰어요.", "재료가 부드러워질 때까지 삶아요.", "우유를 넣고 곱게 갈아 한 번 더 끓여요."],
    },
    {
        "name": "애호박 된장국",
        "description": "애호박을 활용한 따뜻한 국 메뉴예요.",
        "time": 20,
        "ingredients": ["애호박", "두부", "된장"],
        "difficulty": "쉬움",
        "meal_type": "저녁",
        "menu_type": "국",
        "steps": ["애호박과 두부를 먹기 좋은 크기로 썰어요.", "물을 끓이고 된장을 소량 풀어요.", "재료를 넣고 충분히 익혀요."],
    },
    {
        "name": "연어 채소덮밥",
        "description": "연어와 채소를 밥 위에 올려 간편하게 준비해요.",
        "time": 25,
        "ingredients": ["연어", "밥", "브로콜리", "당근"],
        "difficulty": "보통",
        "meal_type": "점심",
        "menu_type": "밥",
        "steps": ["연어의 가시를 꼼꼼히 확인해요.", "연어와 채소를 각각 충분히 익혀요.", "밥 위에 재료를 올려요."],
    },
    {
        "name": "소고기 미역국",
        "description": "소고기와 미역으로 만드는 익숙한 국 메뉴예요.",
        "time": 30,
        "ingredients": ["소고기", "미역"],
        "difficulty": "보통",
        "meal_type": "저녁",
        "menu_type": "국",
        "steps": ["미역을 불려 잘게 잘라요.", "소고기와 미역을 냄비에서 볶아요.", "물을 넣고 재료가 부드러워질 때까지 끓여요."],
    },
    {
        "name": "단호박 수프",
        "description": "단호박을 익혀 부드럽게 즐기는 메뉴예요.",
        "time": 20,
        "ingredients": ["단호박", "우유"],
        "difficulty": "쉬움",
        "meal_type": "아침",
        "menu_type": "수프",
        "steps": ["단호박의 씨를 제거하고 잘라요.", "단호박을 푹 익혀요.", "우유와 함께 갈아 부드럽게 끓여요."],
    },
    {
        "name": "두부 채소전",
        "description": "두부와 채소를 섞어 노릇하게 익히는 메뉴예요.",
        "time": 20,
        "ingredients": ["두부", "당근", "애호박", "달걀"],
        "difficulty": "보통",
        "meal_type": "점심",
        "menu_type": "전",
        "steps": ["두부의 물기를 빼고 으깨요.", "다진 채소와 달걀을 섞어요.", "작은 크기로 빚어 속까지 익혀요."],
    },
    {
        "name": "닭고기 감자조림",
        "description": "닭고기와 감자를 함께 익혀 만드는 반찬이에요.",
        "time": 30,
        "ingredients": ["닭고기", "감자", "당근"],
        "difficulty": "보통",
        "meal_type": "저녁",
        "menu_type": "조림",
        "steps": ["닭고기와 채소를 작은 크기로 썰어요.", "냄비에 재료와 물을 넣어요.", "양념을 조절하고 재료가 충분히 익을 때까지 조려요."],
    },
    {
        "name": "브로콜리 달걀볶음",
        "description": "간단한 재료로 빠르게 준비할 수 있는 메뉴예요.",
        "time": 15,
        "ingredients": ["브로콜리", "달걀"],
        "difficulty": "쉬움",
        "meal_type": "아침",
        "menu_type": "볶음",
        "steps": ["브로콜리를 작게 잘라 충분히 익혀요.", "달걀을 풀어 팬에서 익혀요.", "브로콜리를 넣고 함께 볶아요."],
    },
    {
        "name": "새우 채소죽",
        "description": "새우와 채소를 넣어 끓이는 부드러운 죽이에요.",
        "time": 25,
        "ingredients": ["새우", "쌀", "당근", "애호박"],
        "difficulty": "보통",
        "meal_type": "아침",
        "menu_type": "죽",
        "steps": ["새우를 손질하고 잘게 다져요.", "채소와 불린 쌀을 냄비에 넣어요.", "물을 넣고 재료가 충분히 익도록 끓여요."],
    },
    {
        "name": "토마토 달걀볶음",
        "description": "토마토와 달걀을 함께 익히는 간단한 메뉴예요.",
        "time": 15,
        "ingredients": ["토마토", "달걀"],
        "difficulty": "쉬움",
        "meal_type": "점심",
        "menu_type": "볶음",
        "steps": ["토마토를 작게 썰어요.", "달걀을 풀어 부드럽게 익혀요.", "토마토를 넣고 재료가 충분히 익도록 볶아요."],
    },
    {
        "name": "소고기 채소주먹밥",
        "description": "밥과 고기, 채소를 한입 크기로 뭉쳐 준비해요.",
        "time": 20,
        "ingredients": ["소고기", "밥", "당근", "김"],
        "difficulty": "쉬움",
        "meal_type": "점심",
        "menu_type": "밥",
        "steps": ["소고기와 당근을 잘게 다져 충분히 익혀요.", "밥과 재료를 골고루 섞어요.", "먹기 편한 크기로 뭉쳐요."],
    },
    {
        "name": "양배추 감자수프",
        "description": "양배추와 감자를 익혀 부드럽게 만든 수프예요.",
        "time": 25,
        "ingredients": ["양배추", "감자", "우유"],
        "difficulty": "보통",
        "meal_type": "저녁",
        "menu_type": "수프",
        "steps": ["양배추와 감자를 잘게 썰어요.", "냄비에서 재료를 충분히 익혀요.", "우유를 넣고 원하는 식감으로 갈아요."],
    },
    {
        "name": "두부 버섯덮밥",
        "description": "두부와 버섯을 활용해 만드는 간단한 한 그릇 메뉴예요.",
        "time": 20,
        "ingredients": ["두부", "버섯", "밥", "양파"],
        "difficulty": "쉬움",
        "meal_type": "저녁",
        "menu_type": "밥",
        "steps": ["두부와 버섯, 양파를 작게 썰어요.", "팬에서 양파와 버섯을 익혀요.", "두부를 넣고 충분히 익힌 뒤 밥 위에 올려요."],
    },
    {
        "name": "바나나 오트밀",
        "description": "오트밀과 바나나를 활용한 간단한 아침 메뉴예요.",
        "time": 10,
        "ingredients": ["오트밀", "바나나", "우유"],
        "difficulty": "쉬움",
        "meal_type": "아침",
        "menu_type": "죽",
        "steps": ["오트밀과 우유를 냄비에 넣어요.", "약한 불에서 부드럽게 끓여요.", "바나나를 으깨 넣고 잘 섞어요."],
    },
    {
        "name": "고구마 으깬 샐러드",
        "description": "익힌 고구마를 으깨 간단하게 준비할 수 있어요.",
        "time": 20,
        "ingredients": ["고구마", "요거트"],
        "difficulty": "쉬움",
        "meal_type": "간식",
        "menu_type": "샐러드",
        "steps": ["고구마를 부드럽게 익혀요.", "껍질을 제거하고 곱게 으깨요.", "플레인 요거트를 소량 넣고 섞어요."],
    },
    {
        "name": "채소 달걀국",
        "description": "채소와 달걀을 넣어 빠르게 끓이는 국이에요.",
        "time": 15,
        "ingredients": ["달걀", "당근", "애호박"],
        "difficulty": "쉬움",
        "meal_type": "저녁",
        "menu_type": "국",
        "steps": ["당근과 애호박을 잘게 썰어요.", "물을 끓여 채소를 충분히 익혀요.", "풀어 둔 달걀을 넣고 익혀요."],
    },
]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "recommended_menu" not in st.session_state:
    st.session_state.recommended_menu = None

# -----------------------------
# 깔끔한 디자인
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background-color: #F7F8F6;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E7EAE5;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: #FFFFFF;
        border: 1px solid #E7EAE5;
        border-radius: 16px;
        padding: 28px 30px;
        margin-bottom: 24px;
    }

    .hero-label {
        color: #68816D;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #202820;
        font-size: 29px;
        font-weight: 700;
        line-height: 1.4;
        margin: 0 0 8px 0;
    }

    .hero-description {
        color: #70776F;
        font-size: 14px;
        line-height: 1.7;
        margin: 0;
    }

    .menu-card {
        background: #FFFFFF;
        border: 1px solid #E7EAE5;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .menu-name {
        color: #26342A;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .menu-description {
        color: #737A72;
        font-size: 13px;
        line-height: 1.6;
        margin-bottom: 14px;
    }

    .menu-meta {
        color: #566558;
        font-size: 12px;
        line-height: 2;
    }

    .section-title {
        color: #26342A;
        font-size: 20px;
        font-weight: 700;
        margin: 18px 0 12px 0;
    }

    div.stButton > button {
        border-radius: 9px;
        border: 1px solid #D9E2D8;
        font-weight: 600;
        min-height: 42px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #617B65;
        border-color: #617B65;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #4E6852;
        border-color: #4E6852;
        color: white;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E7EAE5;
        padding: 14px;
        border-radius: 12px;
    }

    h1, h2, h3 {
        color: #26342A;
    }

    .footer {
        color: #8A9189;
        font-size: 12px;
        text-align: center;
        padding-top: 28px;
    }
    </style>

    <div class="hero">
        <div class="hero-label">URIKKINI · DAILY MENU</div>
        <div class="hero-title">오늘의 식사, 우리끼니</div>
        <p class="hero-description">
            바쁜 육아 중에도 식사 준비를 조금 더 쉽게.<br>
            조리 시간과 재료에 맞는 메뉴를 찾아보세요.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 사이드바 필터
# -----------------------------
st.sidebar.title("메뉴 조건")
st.sidebar.caption("원하는 조건을 선택해 주세요.")

time_options = {
    "전체": 999,
    "10분 이내": 10,
    "15분 이내": 15,
    "20분 이내": 20,
    "30분 이내": 30,
}

selected_time = st.sidebar.selectbox(
    "조리 시간",
    list(time_options.keys()),
)

all_ingredients = sorted({
    ingredient
    for menu in MENUS
    for ingredient in menu["ingredients"]
})

selected_ingredients = st.sidebar.multiselect(
    "사용할 수 있는 재료",
    all_ingredients,
    help="선택한 재료가 모두 포함된 메뉴를 찾습니다.",
)

ingredient_match = st.sidebar.checkbox(
    "선택한 재료가 모두 포함된 메뉴만 보기",
    value=True,
)

selected_difficulty = st.sidebar.selectbox(
    "조리 난이도",
    ["전체", "쉬움", "보통"],
)

selected_meal_type = st.sidebar.selectbox(
    "식사 시간",
    ["전체", "아침", "점심", "저녁", "간식"],
)

all_menu_types = sorted({menu["menu_type"] for menu in MENUS})
selected_menu_type = st.sidebar.selectbox(
    "메뉴 종류",
    ["전체"] + all_menu_types,
)

st.sidebar.divider()
st.sidebar.caption("필터를 변경하면 조건에 맞는 메뉴가 표시됩니다.")

# -----------------------------
# 메뉴 필터링
# -----------------------------
filtered_menus = []

for menu in MENUS:
    if menu["time"] > time_options[selected_time]:
        continue

    if selected_difficulty != "전체" and menu["difficulty"] != selected_difficulty:
        continue

    if selected_meal_type != "전체" and menu["meal_type"] != selected_meal_type:
        continue

    if selected_menu_type != "전체" and menu["menu_type"] != selected_menu_type:
        continue

    if selected_ingredients:
        menu_ingredients = set(menu["ingredients"])
        selected_set = set(selected_ingredients)

        if ingredient_match and not selected_set.issubset(menu_ingredients):
            continue

        if not ingredient_match and not selected_set.intersection(menu_ingredients):
            continue

    filtered_menus.append(menu)

# -----------------------------
# 상단 통계
# -----------------------------
metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("추천 가능한 메뉴", f"{len(filtered_menus)}개")

with metric2:
    st.metric("등록된 메뉴", f"{len(MENUS)}개")

with metric3:
    st.metric("즐겨찾기", f"{len(st.session_state.favorites)}개")

# -----------------------------
# 메뉴 추천
# -----------------------------
st.markdown('<div class="section-title">메뉴 추천</div>', unsafe_allow_html=True)
st.caption("선택한 조건에 맞는 메뉴를 확인하거나, 메뉴 하나를 무작위로 추천받을 수 있어요.")

recommend_col, reset_col = st.columns([2, 1])

with recommend_col:
    if st.button("오늘의 메뉴 추천받기", type="primary", use_container_width=True):
        if filtered_menus:
            st.session_state.recommended_menu = random.choice(filtered_menus)
        else:
            st.session_state.recommended_menu = None

with reset_col:
    if st.button("추천 초기화", use_container_width=True):
        st.session_state.recommended_menu = None

if st.session_state.recommended_menu:
    recommended = st.session_state.recommended_menu

    # 현재 필터 조건에 맞지 않는 메뉴가 남아 있으면 추천 표시를 해제
    if recommended not in filtered_menus:
        st.session_state.recommended_menu = None
    else:
        st.success(f"오늘의 추천 메뉴는 **{recommended['name']}** 입니다.")

        with st.container(border=True):
            st.subheader(recommended["name"])
            st.write(recommended["description"])
            st.write(
                f"**조리 시간:** 약 {recommended['time']}분  ·  "
                f"**난이도:** {recommended['difficulty']}"
            )
            st.write("**재료:** " + ", ".join(recommended["ingredients"]))

            with st.expander("만드는 방법"):
                for index, step in enumerate(recommended["steps"], start=1):
                    st.write(f"{index}. {step}")

            if recommended["name"] not in st.session_state.favorites:
                if st.button(
                    "즐겨찾기에 추가",
                    key=f"recommend_fav_{recommended['name']}",
                ):
                    st.session_state.favorites.append(recommended["name"])
                    st.rerun()
            else:
                st.caption("이미 즐겨찾기에 추가된 메뉴예요.")

# -----------------------------
# 메뉴 목록
# -----------------------------
st.divider()
st.markdown('<div class="section-title">조건에 맞는 메뉴</div>', unsafe_allow_html=True)

if not filtered_menus:
    st.warning(
        "선택한 조건에 맞는 메뉴가 없어요. "
        "조리 시간을 늘리거나 재료 조건을 줄여 보세요."
    )
else:
    st.caption(f"총 {len(filtered_menus)}개의 메뉴를 찾았어요.")

    for menu in filtered_menus:
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.markdown(
                    f'<div class="menu-name">{menu["name"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="menu-description">{menu["description"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="menu-meta">'
                    f'조리 시간 약 {menu["time"]}분　|　'
                    f'난이도 {menu["difficulty"]}<br>'
                    f'식사 {menu["meal_type"]}　|　'
                    f'종류 {menu["menu_type"]}<br>'
                    f'재료: {", ".join(menu["ingredients"])}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with right:
                is_favorite = menu["name"] in st.session_state.favorites

                button_label = "★ 즐겨찾기" if is_favorite else "☆ 즐겨찾기"

                if st.button(
                    button_label,
                    key=f"favorite_{menu['name']}",
                    use_container_width=True,
                ):
                    if is_favorite:
                        st.session_state.favorites.remove(menu["name"])
                    else:
                        st.session_state.favorites.append(menu["name"])
                    st.rerun()

                with st.expander("만드는 방법"):
                    for index, step in enumerate(menu["steps"], start=1):
                        st.write(f"{index}. {step}")

# -----------------------------
# 즐겨찾기
# -----------------------------
st.divider()
st.markdown('<div class="section-title">즐겨찾기 메뉴</div>', unsafe_allow_html=True)

if not st.session_state.favorites:
    st.info("아직 즐겨찾기에 추가한 메뉴가 없어요.")
else:
    favorite_menus = [
        menu for menu in MENUS
        if menu["name"] in st.session_state.favorites
    ]

    for menu in favorite_menus:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{menu['name']}**")
                st.caption(
                    f"약 {menu['time']}분 · {menu['difficulty']} · "
                    f"{menu['menu_type']}"
                )

            with col2:
                if st.button(
                    "삭제",
                    key=f"remove_{menu['name']}",
                    use_container_width=True,
                ):
                    st.session_state.favorites.remove(menu["name"])
                    st.rerun()

# -----------------------------
# 안내 및 푸터
# -----------------------------
st.divider()

with st.expander("이용 전 확인해 주세요"):
    st.write(
        "이 앱은 메뉴 아이디어를 제공하기 위한 서비스입니다. "
        "영유아에게 제공할 때는 아이의 월령과 발달 상태에 맞게 "
        "재료의 크기와 식감을 조절해 주세요."
    )
    st.write(
        "달걀, 우유, 밀, 생선, 갑각류 등 알레르기를 일으킬 수 있는 "
        "재료는 아이의 알레르기 여부를 확인한 뒤 사용하세요. "
        "고기와 생선, 달걀은 충분히 익혀 주세요."
    )
    st.write(
        "메뉴에 표시된 조리 시간은 예상 시간이며, "
        "재료 손질이나 조리 환경에 따라 달라질 수 있습니다."
    )

st.markdown(
    '<div class="footer">우리끼니 · 매일의 식사를 조금 더 편하게</div>',
    unsafe_allow_html=True,
)
