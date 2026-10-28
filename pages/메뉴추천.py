
import streamlit as st
import random

st.set_page_config(
    page_title="오늘 뭐 먹지? 🍓",
    page_icon="🍓",
    layout="wide",
)

# -----------------------------
# 메뉴 데이터
# -----------------------------
MENUS = [
    {
        "name": "계란볶음밥", "emoji": "🍳", "time": 10,
        "difficulty": "쉬움", "meals": ["아침", "점심", "저녁"],
        "category": "간편식",
        "ingredients": ["밥", "계란", "대파", "당근"],
        "description": "냉장고 속 재료로 뚝딱 만드는 한 끼",
        "steps": ["대파와 당근을 잘게 썰어요.", "팬에 채소를 볶아요.", "밥과 계란을 넣고 골고루 볶아요."],
    },
    {
        "name": "두부덮밥", "emoji": "🍚", "time": 15,
        "difficulty": "쉬움", "meals": ["점심", "저녁"],
        "category": "한식",
        "ingredients": ["밥", "두부", "양파", "대파"],
        "description": "부드러운 두부로 만드는 든든한 덮밥",
        "steps": ["두부와 양파를 썰어요.", "팬에 양파와 두부를 익혀요.", "밥 위에 올려 완성해요."],
    },
    {
        "name": "참치마요덮밥", "emoji": "🥣", "time": 10,
        "difficulty": "쉬움", "meals": ["점심", "저녁"],
        "category": "간편식",
        "ingredients": ["밥", "참치", "계란", "마요네즈"],
        "description": "재료가 간단해서 준비하기 편해요",
        "steps": ["참치의 기름을 빼요.", "계란을 익혀요.", "밥 위에 참치와 계란을 올리고 마요네즈를 곁들여요."],
    },
    {
        "name": "간장계란밥", "emoji": "🍳", "time": 5,
        "difficulty": "쉬움", "meals": ["아침", "점심", "저녁"],
        "category": "간편식",
        "ingredients": ["밥", "계란", "간장", "참기름"],
        "description": "바쁜 날 가장 간단하게 준비하는 메뉴",
        "steps": ["계란을 프라이해요.", "따뜻한 밥 위에 올려요.", "간장과 참기름을 기호에 맞게 곁들여요."],
    },
    {
        "name": "계란국", "emoji": "🍲", "time": 10,
        "difficulty": "쉬움", "meals": ["아침", "점심", "저녁"],
        "category": "국·찌개",
        "ingredients": ["계란", "대파", "육수"],
        "description": "밥과 함께 먹기 좋은 따뜻한 국",
        "steps": ["육수를 끓여요.", "풀어 둔 계란을 천천히 넣어요.", "대파를 넣고 충분히 익혀요."],
    },
    {
        "name": "두부된장찌개", "emoji": "🍲", "time": 20,
        "difficulty": "보통", "meals": ["점심", "저녁"],
        "category": "국·찌개",
        "ingredients": ["두부", "된장", "애호박", "양파", "대파"],
        "description": "구수하게 즐기는 집밥 메뉴",
        "steps": ["채소와 두부를 썰어요.", "물에 된장을 풀고 채소를 넣어요.", "두부를 넣고 재료가 익을 때까지 끓여요."],
    },
    {
        "name": "김치볶음밥", "emoji": "🍚", "time": 15,
        "difficulty": "쉬움", "meals": ["점심", "저녁"],
        "category": "한식",
        "ingredients": ["밥", "김치", "계란", "대파"],
        "description": "익은 김치로 간단히 만드는 볶음밥",
        "steps": ["김치와 대파를 썰어요.", "팬에 김치와 대파를 볶아요.", "밥을 넣고 볶은 뒤 원하면 계란을 곁들여요."],
    },
    {
        "name": "야채계란말이", "emoji": "🥚", "time": 15,
        "difficulty": "보통", "meals": ["아침", "점심", "저녁"],
        "category": "한식",
        "ingredients": ["계란", "당근", "대파"],
        "description": "채소를 함께 먹기 좋은 반찬",
        "steps": ["당근과 대파를 잘게 썰어요.", "계란에 채소를 섞어요.", "팬에 얇게 부어 말아가며 충분히 익혀요."],
    },
    {
        "name": "토마토 파스타", "emoji": "🍝", "time": 20,
        "difficulty": "보통", "meals": ["점심", "저녁"],
        "category": "양식",
        "ingredients": ["파스타면", "토마토소스", "마늘", "양파"],
        "description": "한 접시로 즐기는 간편한 양식",
        "steps": ["파스타면을 삶아요.", "팬에 마늘과 양파를 볶고 소스를 넣어요.", "면을 넣고 소스와 섞어요."],
    },
    {
        "name": "크림 파스타", "emoji": "🍝", "time": 20,
        "difficulty": "보통", "meals": ["점심", "저녁"],
        "category": "양식",
        "ingredients": ["파스타면", "생크림", "우유", "마늘"],
        "description": "부드러운 소스로 만드는 파스타",
        "steps": ["파스타면을 삶아요.", "팬에 마늘을 볶고 생크림과 우유를 넣어요.", "면을 넣고 소스가 어우러지도록 익혀요."],
    },
    {
        "name": "야채볶음우동", "emoji": "🍜", "time": 15,
        "difficulty": "쉬움", "meals": ["점심", "저녁"],
        "category": "일식",
        "ingredients": ["우동면", "양배추", "당근", "양파", "간장"],
        "description": "채소와 면을 한 번에 먹는 메뉴",
        "steps": ["채소를 썰어요.", "팬에 채소와 우동면을 볶아요.", "간장으로 간을 맞춰요."],
    },
    {
        "name": "참치주먹밥", "emoji": "🍙", "time": 10,
        "difficulty": "쉬움", "meals": ["아침", "점심", "간식"],
        "category": "간편식",
        "ingredients": ["밥", "참치", "김", "참기름"],
        "description": "한입 크기로 만들어 먹기 편해요",
        "steps": ["참치의 기름을 빼요.", "밥에 참치와 잘게 부순 김을 섞어요.", "한입 크기로 뭉쳐요."],
    },
    {
        "name": "감자수프", "emoji": "🥣", "time": 25,
        "difficulty": "보통", "meals": ["아침", "점심", "간식"],
        "category": "양식",
        "ingredients": ["감자", "양파", "우유", "버터"],
        "description": "부드럽고 따뜻하게 먹기 좋은 수프",
        "steps": ["감자와 양파를 작게 썰어요.", "버터에 양파를 볶고 감자와 물을 넣어 익혀요.", "감자를 으깨고 우유를 넣어 끓여요."],
    },
    {
        "name": "소고기채소볶음", "emoji": "🥩", "time": 20,
        "difficulty": "보통", "meals": ["점심", "저녁"],
        "category": "한식",
        "ingredients": ["소고기", "양파", "당근", "대파"],
        "description": "고기와 채소를 함께 준비하는 반찬",
        "steps": ["고기와 채소를 썰어요.", "팬에 소고기를 충분히 익혀요.", "채소를 넣고 함께 볶아요."],
    },
    {
        "name": "닭가슴살 샐러드", "emoji": "🥗", "time": 15,
        "difficulty": "쉬움", "meals": ["점심", "저녁"],
        "category": "양식",
        "ingredients": ["닭가슴살", "양상추", "토마토", "오이"],
        "description": "채소와 단백질을 함께 챙기는 메뉴",
        "steps": ["채소를 씻어 먹기 좋게 썰어요.", "닭가슴살을 속까지 충분히 익혀요.", "접시에 담고 드레싱을 곁들여요."],
    },
    {
        "name": "프렌치토스트", "emoji": "🍞", "time": 10,
        "difficulty": "쉬움", "meals": ["아침", "간식"],
        "category": "양식",
        "ingredients": ["식빵", "계란", "우유", "버터"],
        "description": "아침이나 간식으로 좋은 토스트",
        "steps": ["계란과 우유를 섞어요.", "식빵을 적셔요.", "버터를 두른 팬에서 양면을 노릇하게 익혀요."],
    },
    {
        "name": "바나나 요거트", "emoji": "🍌", "time": 5,
        "difficulty": "쉬움", "meals": ["아침", "간식"],
        "category": "간편식",
        "ingredients": ["바나나", "요거트", "견과류"],
        "description": "불을 사용하지 않고 준비하는 간식",
        "steps": ["바나나를 먹기 좋게 썰어요.", "요거트에 바나나를 올려요.", "원하면 잘게 부순 견과류를 곁들여요."],
    },
    {
        "name": "김치콩나물국", "emoji": "🍲", "time": 20,
        "difficulty": "보통", "meals": ["아침", "점심", "저녁"],
        "category": "국·찌개",
        "ingredients": ["김치", "콩나물", "대파", "육수"],
        "description": "밥과 곁들이기 좋은 국물 메뉴",
        "steps": ["김치를 먹기 좋게 썰어요.", "육수에 김치를 넣고 끓여요.", "콩나물을 충분히 익히고 대파를 넣어요."],
    },
    {
        "name": "두부구이", "emoji": "🍽️", "time": 10,
        "difficulty": "쉬움", "meals": ["아침", "점심", "저녁"],
        "category": "한식",
        "ingredients": ["두부", "간장", "대파"],
        "description": "재료가 적고 조리 과정이 간단한 반찬",
        "steps": ["두부의 물기를 제거해요.", "팬에 두부를 앞뒤로 구워요.", "잘게 썬 대파와 간장을 곁들여요."],
    },
    {
        "name": "고구마와 우유", "emoji": "🍠", "time": 15,
        "difficulty": "쉬움", "meals": ["아침", "간식"],
        "category": "간편식",
        "ingredients": ["고구마", "우유"],
        "description": "간단하게 준비할 수 있는 메뉴",
        "steps": ["고구마를 깨끗이 씻어요.", "전자레인지나 찜기로 속까지 익혀요.", "우유와 함께 먹어요."],
    },
]

ALL_INGREDIENTS = sorted({
    ingredient
    for menu in MENUS
    for ingredient in menu["ingredients"]
})

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #FFF9F5;
    color: #514641;
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #75534D !important;
}
.hero {
    background: linear-gradient(135deg, #FFE6EB, #FFF0D9 58%, #E5F4E8);
    border: 2px solid #FFFFFF;
    border-radius: 26px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 5px 18px #E8C9C333;
}
.hero h1 {
    font-size: 2.3rem;
    color: #9B5969 !important;
    margin: 8px 0 12px 0;
}
.hero p {
    color: #795D58;
    line-height: 1.8;
    margin: 0;
}
.sticker {
    font-size: 2rem;
}
.tag {
    display: inline-block;
    background: #FFFFFFB8;
    color: #A35E72;
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 0.82rem;
    margin-top: 10px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #F4E3DD;
    border-radius: 20px;
    box-shadow: 0 4px 14px #DCC4B51A;
}
div.stButton > button {
    border-radius: 14px;
    border: 1px solid #F0D5D9;
    background: #FFF0F2;
    color: #965C68;
    font-weight: 600;
}
div.stButton > button:hover {
    border-color: #E9AAB9;
    background: #FFE1E8;
    color: #814858;
}
div.stButton > button[kind="primary"],
div.stFormSubmitButton > button {
    background: #E99BAC;
    border: none;
    color: white;
    border-radius: 15px;
    font-weight: 700;
    min-height: 44px;
}
div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button:hover {
    background: #D98196;
    color: white;
}
div[data-baseweb="select"] > div {
    border-radius: 12px;
    border-color: #EBD8D1;
}
div[data-testid="stExpander"] {
    background: #FFFAF8;
    border: 1px solid #F2E3DD;
    border-radius: 13px;
}
div[data-testid="stCaptionContainer"] {
    color: #9B8580;
}
hr {
    border-color: #F0DFD8;
}
@media (max-width: 640px) {
    .hero { padding: 22px 18px; }
    .hero h1 { font-size: 1.8rem; }
}
</style>

<div class="hero">
    <div class="sticker">🧸 🍓 🥣</div>
    <div class="tag">♡ 육아맘 · 육아대디를 위한 레시피 ♡</div>
    <h1>오늘 뭐 먹지? 🌷</h1>
    <p>아가 돌보느라 바쁜 하루에도</p>
    <p><b>내 밥은 맛있고 간편하게!</b> 🍚</p>
    <p>냉장고 속 재료로 오늘의 메뉴를 찾아봐요.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 세션 상태
# -----------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "filters" not in st.session_state:
    st.session_state.filters = {
        "max_time": 20,
        "meal_type": "전체",
        "difficulty": "전체",
        "menu_type": "전체",
        "ingredients": [],
        "strict_ingredients": False,
    }

if "recommendation_seed" not in st.session_state:
    st.session_state.recommendation_seed = 0

# -----------------------------
# 화면 탭
# -----------------------------
tab_recommend, tab_favorites = st.tabs(
    ["🍓 메뉴 추천", "💗 나의 레시피 북"]
)

# -----------------------------
# 메뉴 추천
# -----------------------------
with tab_recommend:
    st.subheader("🌷 어떤 메뉴가 필요하세요?")
    st.caption("오늘의 상황을 골라주면 맛있는 메뉴를 찾아줄게요 ♡")

    with st.form("menu_filter_form"):
        left, right = st.columns(2)

        with left:
            max_time = st.selectbox(
                "⏰ 요리 가능 시간",
                [10, 20, 30],
                index=1,
                format_func=lambda x: f"{x}분 이내",
            )
            meal_type = st.selectbox(
                "🍚 식사 종류",
                ["전체", "아침", "점심", "저녁", "간식"],
            )
            difficulty = st.selectbox(
                "👩‍🍳 조리 난이도",
                ["전체", "쉬움", "보통"],
            )

        with right:
            menu_type = st.selectbox(
                "🥗 메뉴 종류",
                ["전체", "한식", "양식", "일식", "간편식", "국·찌개"],
            )
            ingredients = st.multiselect(
                "🧺 집에 있는 재료",
                ALL_INGREDIENTS,
                placeholder="재료를 여러 개 선택해 보세요",
            )
            strict_ingredients = st.checkbox(
                "선택한 재료만으로 만들 수 있는 메뉴 우선",
                value=False,
            )

        submitted = st.form_submit_button(
            "🍓 내 조건으로 메뉴 찾기",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        st.session_state.filters = {
            "max_time": max_time,
            "meal_type": meal_type,
            "difficulty": difficulty,
            "menu_type": menu_type,
            "ingredients": ingredients,
            "strict_ingredients": strict_ingredients,
        }
        st.session_state.recommendation_seed += 1

    filters = st.session_state.filters
    results = []

    try:
        for menu in MENUS:
            if menu["time"] > filters["max_time"]:
                continue

            if (
                filters["meal_type"] != "전체"
                and filters["meal_type"] not in menu["meals"]
            ):
                continue

            if (
                filters["difficulty"] != "전체"
                and menu["difficulty"] != filters["difficulty"]
            ):
                continue

            if (
                filters["menu_type"] != "전체"
                and menu["category"] != filters["menu_type"]
            ):
                continue

            selected = filters["ingredients"]
            matched = [
                item for item in selected
                if item in menu["ingredients"]
            ]

            if selected and not matched:
                continue

            missing = [
                item for item in menu["ingredients"]
                if item not in selected
            ] if selected else []

            results.append({
                **menu,
                "matched_count": len(matched),
                "missing": missing,
            })

        if filters["ingredients"]:
            results.sort(
                key=lambda item: (
                    len(item["missing"]),
                    -item["matched_count"],
                    item["time"],
                )
            )
        else:
            results.sort(key=lambda item: (item["time"], item["name"]))

        if filters["strict_ingredients"] and filters["ingredients"]:
            exact = [item for item in results if not item["missing"]]
            results = exact

        if results:
            random_seed = st.session_state.recommendation_seed
            if random_seed:
                random.Random(random_seed).shuffle(results)

            st.markdown("---")
            st.subheader(f"💗 오늘의 추천 메뉴 ({len(results)}개)")
            st.caption("마음에 드는 메뉴를 저장해 두세요!")

            for start in range(0, len(results), 2):
                columns = st.columns(2)

                for column, menu in zip(columns, results[start:start + 2]):
                    with column:
                        with st.container(border=True):
                            st.markdown(f"### {menu['emoji']} {menu['name']}")
                            st.caption(f"🍓 {menu['description']}")

                            st.markdown(
                                f"⏱️ **{menu['time']}분**　"
                                f"🌼 **{menu['difficulty']}**"
                            )
                            st.caption(f"🍽️ 메뉴 종류: {menu['category']}")

                            if filters["meal_type"] == "전체":
                                st.caption(
                                    "추천 식사: " + ", ".join(menu["meals"])
                                )

                            if filters["ingredients"]:
                                if menu["missing"]:
                                    st.caption(
                                        "🧺 추가로 필요한 재료: "
                                        + ", ".join(menu["missing"])
                                    )
                                else:
                                    st.caption("💚 선택한 재료로 만들 수 있어요!")

                            with st.expander("🥣 재료와 만드는 방법"):
                                st.markdown("**필요한 재료**")
                                st.write(", ".join(menu["ingredients"]))
                                st.markdown("**만드는 방법**")
                                for number, step in enumerate(menu["steps"], 1):
                                    st.write(f"{number}. {step}")

                            if menu["name"] in st.session_state.favorites:
                                if st.button(
                                    "💗 저장됨 · 취소하기",
                                    key=f"remove_{menu['name']}",
                                    use_container_width=True,
                                ):
                                    st.session_state.favorites.remove(menu["name"])
                                    st.rerun()
                            else:
                                if st.button(
                                    "♡ 메뉴 저장하기",
                                    key=f"save_{menu['name']}",
                                    use_container_width=True,
                                ):
                                    st.session_state.favorites.append(menu["name"])
                                    st.rerun()

            if st.button("🔄 같은 조건으로 다시 추천받기"):
                st.session_state.recommendation_seed += 1
                st.rerun()

        else:
            st.warning(
                "앗, 조건에 맞는 메뉴가 없어요 🥺 "
                "요리 시간을 늘리거나 재료 조건을 줄여 보세요!"
            )

    except Exception as error:
        st.error("메뉴를 불러오지 못했어요. 조건을 다시 선택해 주세요.")
        st.caption(f"오류 확인용: {error}")

# -----------------------------
# 즐겨찾기
# -----------------------------
with tab_favorites:
    st.subheader("💗 나의 레시피 북")
    st.caption("마음에 드는 메뉴를 모아두고 언제든 확인해요 ♡")

    favorite_menus = [
        menu for menu in MENUS
        if menu["name"] in st.session_state.favorites
    ]

    if not favorite_menus:
        st.info("아직 저장한 메뉴가 없어요 🍓 메뉴 카드에서 하트를 눌러 보세요!")
    else:
        for menu in favorite_menus:
            with st.container(border=True):
                st.markdown(f"### {menu['emoji']} {menu['name']}")
                st.caption(
                    f"⏱️ {menu['time']}분　·　"
                    f"🌼 {menu['difficulty']}　·　"
                    f"🍽️ {menu['category']}"
                )
                st.write("🧺 재료: " + ", ".join(menu["ingredients"]))

                with st.expander("🥣 만드는 방법 보기"):
                    for number, step in enumerate(menu["steps"], 1):
                        st.write(f"{number}. {step}")

                if st.button(
                    "♡ 저장 목록에서 빼기",
                    key=f"favorite_remove_{menu['name']}",
                ):
                    st.session_state.favorites.remove(menu["name"])
                    st.rerun()

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#B49A91;'>"
    "🌷 오늘도 나를 위한 한 끼, 잊지 말기 ♡<br>"
    "조리시간은 예상치이며, 알레르기와 식재료 상태를 확인해 주세요."
    "</div>",
    unsafe_allow_html=True,
)
