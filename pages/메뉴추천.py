
import streamlit as st
import random

st.set_page_config(
    page_title="오늘뭐먹지? | 육아 부모 메뉴추천",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 메뉴 데이터
# -----------------------------
MENUS = [
    {
        "name": "계란볶음밥",
        "emoji": "🍳",
        "time": 10,
        "difficulty": "쉬움",
        "meals": ["아침", "점심", "저녁"],
        "category": "간편식",
        "ingredients": ["밥", "계란", "대파", "당근"],
        "steps": ["대파와 당근을 잘게 썬다.", "팬에 재료를 볶는다.", "밥과 계란을 넣고 골고루 볶는다."],
        "description": "냉장고 속 재료로 빠르게 만드는 한 끼",
    },
    {
        "name": "두부덮밥",
        "emoji": "🍚",
        "time": 15,
        "difficulty": "쉬움",
        "meals": ["점심", "저녁"],
        "category": "한식",
        "ingredients": ["밥", "두부", "양파", "대파"],
        "steps": ["두부와 양파를 먹기 좋은 크기로 썬다.", "팬에 양파와 두부를 익힌다.", "밥 위에 올려 완성한다."],
        "description": "부드러운 두부로 만드는 간단한 덮밥",
    },
    {
        "name": "참치마요덮밥",
        "emoji": "🥣",
        "time": 10,
        "difficulty": "쉬움",
        "meals": ["점심", "저녁"],
        "category": "간편식",
        "ingredients": ["밥", "참치", "계란", "마요네즈"],
        "steps": ["참치의 기름을 뺀다.", "계란을 익혀 준비한다.", "밥 위에 참치와 계란을 올리고 마요네즈를 곁들인다."],
        "description": "재료가 간단하고 준비 시간이 짧은 메뉴",
    },
    {
        "name": "계란국",
        "emoji": "🍲",
        "time": 10,
        "difficulty": "쉬움",
        "meals": ["아침", "점심", "저녁"],
        "category": "국·찌개",
        "ingredients": ["계란", "대파", "육수"],
        "steps": ["육수를 끓인다.", "풀어 놓은 계란을 천천히 넣는다.", "대파를 넣고 익힌다."],
        "description": "밥과 함께 먹기 좋은 따뜻한 국",
    },
    {
        "name": "두부된장찌개",
        "emoji": "🍲",
        "time": 20,
        "difficulty": "보통",
        "meals": ["점심", "저녁"],
        "category": "국·찌개",
        "ingredients": ["두부", "된장", "애호박", "양파", "대파"],
        "steps": ["채소와 두부를 썬다.", "물에 된장을 풀고 채소를 넣는다.", "두부를 넣고 재료가 익을 때까지 끓인다."],
        "description": "집밥으로 즐기기 좋은 구수한 찌개",
    },
    {
        "name": "김치볶음밥",
        "emoji": "🍚",
        "time": 15,
        "difficulty": "쉬움",
        "meals": ["점심", "저녁"],
        "category": "한식",
        "ingredients": ["밥", "김치", "계란", "대파"],
        "steps": ["김치와 대파를 썬다.", "팬에 김치와 대파를 볶는다.", "밥을 넣어 볶고 원하면 계란을 곁들인다."],
        "description": "익은 김치로 간단히 만드는 볶음밥",
    },
    {
        "name": "간장계란밥",
        "emoji": "🍳",
        "time": 5,
        "difficulty": "쉬움",
        "meals": ["아침", "점심", "저녁"],
        "category": "간편식",
        "ingredients": ["밥", "계란", "간장", "참기름"],
        "steps": ["계란을 프라이한다.", "따뜻한 밥 위에 계란을 올린다.", "간장과 참기름을 기호에 맞게 곁들인다."],
        "description": "시간이 부족할 때 활용하기 좋은 기본 메뉴",
    },
    {
        "name": "야채계란말이",
        "emoji": "🥚",
        "time": 15,
        "difficulty": "보통",
        "meals": ["아침", "점심", "저녁"],
        "category": "한식",
        "ingredients": ["계란", "당근", "대파"],
        "steps": ["당근과 대파를 잘게 썬다.", "계란에 채소를 섞는다.", "팬에 얇게 부어 말아가며 익힌다."],
        "description": "채소를 함께 먹기 좋은 반찬",
    },
    {
        "name": "토마토 파스타",
        "emoji": "🍝",
        "time": 20,
        "difficulty": "보통",
        "meals": ["점심", "저녁"],
        "category": "양식",
        "ingredients": ["파스타면", "토마토소스", "마늘", "양파"],
        "steps": ["파스타면을 삶는다.", "팬에 마늘과 양파를 볶고 소스를 넣는다.", "면을 넣어 소스와 섞는다."],
        "description": "한 접시로 즐기는 간편한 양식",
    },
    {
        "name": "크림 파스타",
        "emoji": "🍝",
        "time": 20,
        "difficulty": "보통",
        "meals": ["점심", "저녁"],
        "category": "양식",
        "ingredients": ["파스타면", "생크림", "우유", "마늘"],
        "steps": ["파스타면을 삶는다.", "팬에 마늘을 볶고 생크림과 우유를 넣는다.", "면을 넣고 소스가 어우러지도록 익힌다."],
        "description": "부드러운 소스로 만드는 파스타",
    },
    {
        "name": "야채볶음우동",
        "emoji": "🍜",
        "time": 15,
        "difficulty": "쉬움",
        "meals": ["점심", "저녁"],
        "category": "일식",
        "ingredients": ["우동면", "양배추", "당근", "양파", "간장"],
        "steps": ["채소를 썬다.", "팬에 채소와 우동면을 볶는다.", "간장으로 간을 맞춘다."],
        "description": "채소와 면을 한 번에 먹는 메뉴",
    },
    {
        "name": "참치주먹밥",
        "emoji": "🍙",
        "time": 10,
        "difficulty": "쉬움",
        "meals": ["아침", "점심", "간식"],
        "category": "간편식",
        "ingredients": ["밥", "참치", "김", "참기름"],
        "steps": ["참치의 기름을 뺀다.", "밥에 참치와 잘게 부순 김을 섞는다.", "한입 크기로 뭉친다."],
        "description": "먹기 편하고 준비가 간단한 주먹밥",
    },
    {
        "name": "감자수프",
        "emoji": "🥣",
        "time": 25,
        "difficulty": "보통",
        "meals": ["아침", "점심", "간식"],
        "category": "양식",
        "ingredients": ["감자", "양파", "우유", "버터"],
        "steps": ["감자와 양파를 작게 썬다.", "버터에 양파를 볶고 감자와 물을 넣어 익힌다.", "감자를 으깨고 우유를 넣어 끓인다."],
        "description": "부드럽고 따뜻하게 먹기 좋은 수프",
    },
    {
        "name": "소고기채소볶음",
        "emoji": "🥩",
        "time": 20,
        "difficulty": "보통",
        "meals": ["점심", "저녁"],
        "category": "한식",
        "ingredients": ["소고기", "양파", "당근", "대파"],
        "steps": ["고기와 채소를 먹기 좋은 크기로 썬다.", "팬에 고기를 충분히 익힌다.", "채소를 넣어 함께 볶는다."],
        "description": "고기와 채소를 함께 준비하는 반찬",
    },
    {
        "name": "닭가슴살 샐러드",
        "emoji": "🥗",
        "time": 15,
        "difficulty": "쉬움",
        "meals": ["점심", "저녁"],
        "category": "양식",
        "ingredients": ["닭가슴살", "양상추", "토마토", "오이"],
        "steps": ["채소를 씻어 먹기 좋게 썬다.", "닭가슴살을 속까지 충분히 익힌다.", "접시에 담고 드레싱을 곁들인다."],
        "description": "채소와 단백질을 함께 챙기는 메뉴",
    },
    {
        "name": "프렌치토스트",
        "emoji": "🍞",
        "time": 10,
        "difficulty": "쉬움",
        "meals": ["아침", "간식"],
        "category": "양식",
        "ingredients": ["식빵", "계란", "우유", "버터"],
        "steps": ["계란과 우유를 섞는다.", "식빵을 적셔 준비한다.", "버터를 두른 팬에서 양면을 노릇하게 익힌다."],
        "description": "아침이나 간식으로 좋은 간단한 토스트",
    },
    {
        "name": "바나나 요거트",
        "emoji": "🍌",
        "time": 5,
        "difficulty": "쉬움",
        "meals": ["아침", "간식"],
        "category": "간편식",
        "ingredients": ["바나나", "요거트", "견과류"],
        "steps": ["바나나를 먹기 좋게 썬다.", "요거트에 바나나를 올린다.", "원하면 잘게 부순 견과류를 곁들인다."],
        "description": "불을 사용하지 않고 준비하는 간식",
    },
    {
        "name": "김치콩나물국",
        "emoji": "🍲",
        "time": 20,
        "difficulty": "보통",
        "meals": ["아침", "점심", "저녁"],
        "category": "국·찌개",
        "ingredients": ["김치", "콩나물", "대파", "육수"],
        "steps": ["김치를 먹기 좋은 크기로 썬다.", "육수에 김치를 넣고 끓인다.", "콩나물을 넣어 충분히 익히고 대파를 넣는다."],
        "description": "밥과 곁들이기 좋은 국물 메뉴",
    },
    {
        "name": "두부구이",
        "emoji": "🍽️",
        "time": 10,
        "difficulty": "쉬움",
        "meals": ["아침", "점심", "저녁"],
        "category": "한식",
        "ingredients": ["두부", "간장", "대파"],
        "steps": ["두부의 물기를 가볍게 제거한다.", "팬에 두부를 앞뒤로 굽는다.", "잘게 썬 대파와 간장을 곁들인다."],
        "description": "재료가 적고 조리 과정이 간단한 반찬",
    },
    {
        "name": "고구마와 우유",
        "emoji": "🍠",
        "time": 15,
        "difficulty": "쉬움",
        "meals": ["아침", "간식"],
        "category": "간편식",
        "ingredients": ["고구마", "우유"],
        "steps": ["고구마를 깨끗이 씻는다.", "전자레인지 또는 찜기로 속까지 익힌다.", "우유와 함께 먹는다."],
        "description": "간단하게 준비할 수 있는 식사 대용 메뉴",
    },
]

ALL_INGREDIENTS = sorted({
    ingredient
    for menu in MENUS
    for ingredient in menu["ingredients"]
})

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #F7F9F6;
    }
    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(120deg, #E5F1E5, #F1F6EB);
        padding: 30px;
        border-radius: 22px;
        margin-bottom: 22px;
    }
    .hero h1 {
        color: #294C37;
        font-size: 2.1rem;
        margin-bottom: 8px;
    }
    .hero p {
        color: #53695A;
        margin-bottom: 0;
    }
    .subtle {
        color: #68766B;
        font-size: 0.9rem;
    }
    div.stButton > button {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 세션 상태
# -----------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "recommendation_seed" not in st.session_state:
    st.session_state.recommendation_seed = 0

# -----------------------------
# 상단 소개
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🍽️ 오늘뭐먹지?</h1>
    <p>육아로 바쁜 하루, 오늘의 식사를 조금 더 간편하게.</p>
    <p>시간과 냉장고 속 재료에 맞춰 나에게 맞는 메뉴를 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

tab_recommend, tab_favorites = st.tabs(["🥗 메뉴 추천", "♡ 저장한 메뉴"])

# -----------------------------
# 메뉴 추천 화면
# -----------------------------
with tab_recommend:
    st.subheader("어떤 메뉴가 필요하세요?")
    st.caption("현재 상황에 맞는 조건을 선택하면 메뉴를 찾아드려요.")

    with st.form("menu_filter_form"):
        col1, col2 = st.columns(2)

        with col1:
            max_time = st.selectbox(
                "⏱️ 요리 가능 시간",
                options=[10, 20, 30],
                format_func=lambda x: f"{x}분 이내",
                index=1,
            )
            meal_type = st.selectbox(
                "🍚 식사 종류",
                ["전체", "아침", "점심", "저녁", "간식"],
            )
            difficulty = st.selectbox(
                "👩‍🍳 조리 난이도",
                ["전체", "쉬움", "보통"],
            )

        with col2:
            menu_type = st.selectbox(
                "🥘 메뉴 종류",
                ["전체", "한식", "양식", "일식", "간편식", "국·찌개"],
            )
            ingredients = st.multiselect(
                "🧺 보유 재료 선택",
                options=ALL_INGREDIENTS,
                placeholder="집에 있는 재료를 선택하세요",
                help="선택한 재료가 하나 이상 들어가는 메뉴를 우선 추천해요.",
            )
            strict_ingredients = st.checkbox(
                "선택한 재료만으로 만들 수 있는 메뉴 우선",
                value=False,
                help="선택한 재료 외에 필요한 재료가 적은 메뉴를 우선 보여줘요.",
            )

        submitted = st.form_submit_button(
            "✨ 내 조건으로 메뉴 찾기",
            type="primary",
            use_container_width=True,
        )

    if "filters" not in st.session_state:
        st.session_state.filters = {
            "max_time": 20,
            "meal_type": "전체",
            "difficulty": "전체",
            "menu_type": "전체",
            "ingredients": [],
            "strict_ingredients": False,
        }

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

    try:
        results = []

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
            matched = [item for item in selected if item in menu["ingredients"]]

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

        # 보유 재료가 많은 메뉴를 먼저 표시
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
            exact_results = [
                item for item in results
                if not item["missing"]
            ]
            if exact_results:
                results = exact_results

        if results:
            seed = st.session_state.recommendation_seed
            if seed:
                rng = random.Random(seed)
                rng.shuffle(results)

            st.markdown("---")
            st.subheader(f"오늘의 추천 메뉴  ·  {len(results)}개")
            st.caption("메뉴를 선택해 조리법을 확인하고, 마음에 들면 저장하세요.")

            for start in range(0, len(results), 2):
                columns = st.columns(2)

                for col, menu in zip(columns, results[start:start + 2]):
                    with col:
                        with st.container(border=True):
                            st.markdown(
                                f"### {menu['emoji']} {menu['name']}"
                            )
                            st.caption(menu["description"])

                            st.markdown(
                                f"⏱️ **{menu['time']}분**  ·  "
                                f"👩‍🍳 **{menu['difficulty']}**  ·  "
                                f"🥘 **{menu['category']}**"
                            )

                            if filters["meal_type"] == "전체":
                                st.caption(
                                    "추천 식사: " + ", ".join(menu["meals"])
                                )

                            if filters["ingredients"]:
                                if menu["missing"]:
                                    st.caption(
                                        "추가 필요: " + ", ".join(menu["missing"])
                                    )
                                else:
                                    st.caption("선택한 재료로 만들 수 있어요.")

                            with st.expander("재료와 조리법 보기"):
                                st.markdown("**필요한 재료**")
                                st.write(", ".join(menu["ingredients"]))
                                st.markdown("**만드는 방법**")
                                for i, step in enumerate(menu["steps"], 1):
                                    st.write(f"{i}. {step}")

                            if menu["name"] in st.session_state.favorites:
                                if st.button(
                                    "♥ 저장됨",
                                    key=f"remove_{menu['name']}",
                                    use_container_width=True,
                                ):
                                    st.session_state.favorites.remove(menu["name"])
                                    st.rerun()
                            else:
                                if st.button(
                                    "♡ 메뉴 저장",
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
                "선택한 조건에 맞는 메뉴가 없어요. "
                "요리 시간을 늘리거나 재료 조건을 줄여보세요."
            )

    except Exception:
        st.error(
            "메뉴를 불러오는 중 문제가 발생했어요. "
            "조건을 다시 선택한 뒤 시도해 주세요."
        )

# -----------------------------
# 저장한 메뉴 화면
# -----------------------------
with tab_favorites:
    st.subheader("♡ 내가 저장한 메뉴")
    st.caption("마음에 드는 메뉴를 모아두고 필요할 때 확인하세요.")

    favorites = [
        menu for menu in MENUS
        if menu["name"] in st.session_state.favorites
    ]

    if not favorites:
        st.info("아직 저장한 메뉴가 없어요. 메뉴 추천 화면에서 하트를 눌러보세요.")
    else:
        for menu in favorites:
            with st.container(border=True):
                left, right = st.columns([4, 1])

                with left:
                    st.markdown(f"### {menu['emoji']} {menu['name']}")
                    st.caption(
                        f"{menu['time']}분 · {menu['difficulty']} · "
                        f"{menu['category']}"
                    )
                    st.write("재료: " + ", ".join(menu["ingredients"]))

                    with st.expander("조리법 보기"):
                        for i, step in enumerate(menu["steps"], 1):
                            st.write(f"{i}. {step}")

                with right:
                    if st.button(
                        "저장 취소",
                        key=f"favorite_remove_{menu['name']}",
                    ):
                        st.session_state.favorites.remove(menu["name"])
                        st.rerun()

st.markdown("---")
st.caption(
    "※ 조리시간은 예상치이며 재료 준비와 조리 환경에 따라 달라질 수 있어요. "
    "알레르기 유발 식품은 개인의 상황에 맞게 확인해 주세요."
)

