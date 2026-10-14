import random
from datetime import date
import streamlit as st

st.set_page_config(
    page_title="아이랑 한 끼",
    page_icon="🍚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 앱 내에서 사용하는 간단한 예시 데이터입니다. 외부 API나 별도 데이터 파일이 필요 없습니다.
MEALS = [
    {
        "name": "두부 달걀 덮밥",
        "time": 10,
        "ingredients": ["두부", "달걀", "밥"],
        "tags": ["부드러움", "한 그릇"],
        "adult": "부모님 그릇에는 간장이나 양념을 따로 더해도 좋아요.",
        "child": "아이의 발달 단계에 맞게 충분히 익히고, 부드럽고 안전한 크기로 준비하세요.",
        "steps": ["두부를 작게 으깨거나 잘게 썰어요.", "달걀을 완전히 익혀 두부와 함께 볶아요.", "밥 위에 올리고 아이 몫을 먼저 덜어 식혀요."],
    },
    {
        "name": "닭고기 채소 볶음밥",
        "time": 15,
        "ingredients": ["닭고기", "당근", "애호박", "밥"],
        "tags": ["한 그릇", "냉장고 재료"],
        "adult": "부모님 몫은 아이 몫을 덜어낸 뒤 간을 맞추세요.",
        "child": "닭고기는 속까지 완전히 익히고, 채소는 아이가 먹기 알맞게 익혀 주세요.",
        "steps": ["닭고기와 채소를 잘게 준비해요.", "팬에서 재료가 완전히 익을 때까지 볶아요.", "밥을 넣어 섞고 아이 몫은 적절히 식혀 제공해요."],
    },
    {
        "name": "감자·단호박 으깬 한 접시",
        "time": 15,
        "ingredients": ["감자", "단호박", "달걀"],
        "tags": ["부드러움", "간단"],
        "adult": "부모님은 구운 빵이나 샐러드 등 곁들임을 더해도 좋아요.",
        "child": "푹 익혀 부드럽게 으깨고, 질식 위험이 있는 덩어리가 남지 않았는지 확인하세요.",
        "steps": ["감자와 단호박을 푹 익혀요.", "포크로 부드럽게 으깨요.", "달걀을 완전히 익혀 곁들이고 먹기 좋은 온도로 식혀요."],
    },
    {
        "name": "순한 소고기 채소 국밥",
        "time": 20,
        "ingredients": ["소고기", "당근", "애호박", "밥"],
        "tags": ["따뜻한 식사", "한 그릇"],
        "adult": "아이 몫을 덜어낸 다음 부모님 취향에 맞게 간을 추가하세요.",
        "child": "고기는 질기지 않게 충분히 익히고 잘게 다져 주세요. 국물 온도를 꼭 확인하세요.",
        "steps": ["소고기와 채소를 잘게 썰어요.", "냄비에서 고기를 충분히 익힌 뒤 채소와 물을 넣어요.", "채소가 부드러워지면 밥과 함께 내고 충분히 식혀요."],
    },
    {
        "name": "바나나 오트밀",
        "time": 5,
        "ingredients": ["바나나", "오트밀", "우유"],
        "tags": ["아침", "빠른 식사"],
        "adult": "부모님은 견과류 등 추가 재료를 별도로 곁들일 수 있어요. 아이에게는 연령과 알레르기 여부를 고려하세요.",
        "child": "사용하는 우유와 오트밀의 적합 연령을 확인하고, 부드러운 질감과 온도로 준비하세요.",
        "steps": ["오트밀을 제품 안내에 따라 부드럽게 익혀요.", "바나나를 잘 으깨 섞어요.", "아이 몫의 온도를 확인한 뒤 제공해요."],
    },
    {
        "name": "채소 달걀찜과 밥",
        "time": 15,
        "ingredients": ["달걀", "당근", "애호박", "밥"],
        "tags": ["부드러움", "한 그릇"],
        "adult": "부모님은 김이나 다른 반찬을 곁들여도 좋아요.",
        "child": "달걀은 속까지 완전히 익히고, 채소는 아주 잘게 다져 부드럽게 조리하세요.",
        "steps": ["채소를 잘게 다져요.", "달걀과 물을 섞고 채소를 넣어요.", "속까지 완전히 익혀 밥과 함께 내고 식혀요."],
    },
    {
        "name": "콩·두부 채소 비빔밥",
        "time": 15,
        "ingredients": ["두부", "당근", "애호박", "밥"],
        "tags": ["채소", "한 그릇"],
        "adult": "부모님은 고추장이나 양념을 아이 몫과 분리해 넣으세요.",
        "child": "콩류는 아이가 먹을 수 있는 형태로 충분히 부드럽게 준비하고, 통알 형태는 피하세요.",
        "steps": ["두부와 채소를 부드럽게 익혀요.", "밥 위에 재료를 나누어 올려요.", "아이 몫은 잘게 섞고 온도를 확인해요."],
    },
    {
        "name": "빠른 치즈 채소 토스트",
        "time": 10,
        "ingredients": ["식빵", "치즈", "당근", "달걀"],
        "tags": ["빠른 식사", "간단"],
        "adult": "부모님은 샐러드나 과일을 곁들여 식사를 완성하세요.",
        "child": "빵의 질감과 치즈의 염분을 고려하고, 아이가 안전하게 씹고 삼킬 수 있는 형태로 제공하세요.",
        "steps": ["당근을 부드럽게 익혀 잘게 준비해요.", "달걀을 완전히 익혀 빵과 함께 준비해요.", "아이 몫은 알맞은 크기로 나누고 식혀요."],
    },
]

INGREDIENTS = ["밥", "달걀", "두부", "닭고기", "소고기", "당근", "애호박", "감자", "단호박", "바나나", "오트밀", "우유", "식빵", "치즈"]
TIME_OPTIONS = {"5분 정도": 5, "10분 정도": 10, "15분 정도": 15, "20분 정도": 20}

def safe_meal_text(meal):
    """데이터 누락 시 화면이 중단되지 않도록 안전하게 문자열을 반환합니다."""
    return str(meal.get("name", "간편 메뉴"))

def find_meals(available, max_time, preference):
    matches = []
    for meal in MEALS:
        if meal.get("time", 999) > max_time:
            continue
        if available and not set(meal.get("ingredients", [])).intersection(set(available)):
            continue
        if preference != "상관없음" and preference not in meal.get("tags", []):
            continue
        matches.append(meal)
    return matches

if "checked_tasks" not in st.session_state:
    st.session_state.checked_tasks = {}

st.markdown(
    """
    <div style="padding:1.2rem 1.4rem;border-radius:18px;background:linear-gradient(120deg,#fff4e6,#eef8ee);">
      <div style="font-size:0.95rem;color:#536455;">육아하는 하루, 식사는 조금 더 가볍게</div>
      <h1 style="margin:0.25rem 0;color:#284b3a;">🍚 아이랑 한 끼</h1>
      <p style="margin:0;color:#46564b;">아이도 편하고, 부모도 덜 바쁜 식사 준비 도우미</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

with st.sidebar:
    st.header("오늘의 상황")
    child_stage = st.selectbox(
        "아이의 식사 단계",
        ["이유식 시작 전", "이유식 초기·중기", "이유식 후기", "유아식", "가족 식사 함께 먹기"],
        index=3,
        help="추천은 참고용입니다. 실제 제공 음식은 아이의 발달 상태와 의료진의 안내를 우선하세요.",
    )
    max_time_label = st.radio("조리할 수 있는 시간", list(TIME_OPTIONS.keys()), index=1)
    max_time = TIME_OPTIONS[max_time_label]
    available = st.multiselect("집에 있는 재료", INGREDIENTS, default=["밥", "달걀", "두부"])
    preference = st.selectbox("원하는 식사 느낌", ["상관없음", "부드러움", "한 그릇", "빠른 식사", "간단", "채소"])
    st.caption("재료를 선택하지 않으면 시간에 맞는 메뉴 전체에서 추천해요.")

tab1, tab2, tab3 = st.tabs(["🥣 오늘 메뉴 찾기", "⏱️ 식사 생존 플랜", "✅ 준비 체크리스트"])

with tab1:
    st.subheader("냉장고 재료로 한 끼 찾기")
    st.write("선택한 시간과 재료를 기준으로 만들기 쉬운 메뉴를 골라봐요.")
    if st.button("✨ 오늘 메뉴 추천받기", type="primary", use_container_width=True):
        st.session_state["recommendation_seed"] = random.randint(1, 1_000_000)
    matches = find_meals(available, max_time, preference)
    if not matches:
        st.info("조건에 맞는 메뉴가 없어요. 조리 시간을 늘리거나 재료를 더 선택해 보세요.")
        matches = find_meals([], max_time, preference)
        if not matches:
            matches = [m for m in MEALS if m["time"] <= max_time] or MEALS[:]
    seed = st.session_state.get("recommendation_seed", 42)
    rng = random.Random(seed)
    chosen = rng.choice(matches)
    st.markdown(f"### 🍽️ 추천 메뉴: {safe_meal_text(chosen)}")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("예상 조리 시간", f"{chosen.get('time', '—')}분")
    col_b.metric("주요 재료 수", f"{len(chosen.get('ingredients', []))}개")
    col_c.metric("식사 방식", chosen.get("tags", ["간단"])[0])
    st.write("**필요한 재료**")
    st.write(" · ".join(chosen.get("ingredients", [])))
    st.write("**만드는 순서**")
    for i, step in enumerate(chosen.get("steps", []), start=1):
        st.write(f"{i}. {step}")
    st.divider()
    left, right = st.columns(2)
    with left:
        st.markdown("#### 👶 아이 몫")
        st.write(chosen.get("child", "아이의 발달 단계에 맞춰 안전하게 준비하세요."))
    with right:
        st.markdown("#### 🧑‍🍳 부모 몫")
        st.write(chosen.get("adult", "아이 몫을 먼저 덜어낸 뒤 부모님 취향에 맞게 조절하세요."))
    if child_stage == "이유식 시작 전":
        st.warning("이유식을 시작하기 전이라면 아래 메뉴를 아이에게 제공하지 마세요. 아이의 수유와 이유식 시작 시기는 소아청소년과 의료진의 안내를 따르세요.")
    elif child_stage in ["이유식 초기·중기", "이유식 후기"]:
        st.warning("이 메뉴는 일반적인 아이디어예요. 이유식 단계, 알레르기, 질감·크기 적합성을 확인하고 필요하면 별도 조리하세요.")
    else:
        st.caption("아이에게 제공하기 전, 충분히 익었는지·먹기 좋은 크기인지·온도가 적당한지 확인하세요.")
    with st.expander("다른 메뉴도 보고 싶어요"):
        for meal in matches:
            st.markdown(f"**{meal['name']}** · {meal['time']}분")
            st.caption("재료: " + ", ".join(meal.get("ingredients", [])))

with tab2:
    st.subheader("정신없는 날을 위한 식사 생존 플랜")
    st.write("완벽한 식사보다, 안전하고 현실적으로 먹을 수 있는 한 끼를 목표로 해요.")
    situation = st.radio(
        "오늘은 어떤 날인가요?",
        ["아이가 보채서 손이 부족해요", "요리할 기운이 거의 없어요", "설거지를 줄이고 싶어요", "가족이 함께 먹고 싶어요"],
        horizontal=False,
    )
    plans = {
        "아이가 보채서 손이 부족해요": [
            ("1단계 · 안전한 자리 만들기", "아이를 연령에 맞는 안전한 공간에 두고, 조리 중에는 뜨거운 조리기구와 손이 닿지 않게 해요. 아이를 안은 채 뜨거운 음식을 조리하지 마세요."),
            ("2단계 · 조리 한 번으로 끝내기", "밥 + 완전히 익힌 달걀 또는 두부처럼 조리 단계가 적은 메뉴를 골라요."),
            ("3단계 · 먼저 덜고 식히기", "아이 몫을 먼저 덜어 안전한 온도로 식히고, 부모님 음식은 나중에 간을 맞춰요."),
        ],
        "요리할 기운이 거의 없어요": [
            ("1단계 · 조리 부담 줄이기", "이미 준비된 밥과 바로 쓸 수 있는 재료를 활용하고, 조리 과정은 한 가지로 줄여요."),
            ("2단계 · 간단한 조합", "밥 + 부드러운 단백질 식품 + 익힌 채소처럼 단순한 구성을 생각해요."),
            ("3단계 · 도움 요청하기", "가능하다면 가족이나 주변 사람에게 한 끼 준비 또는 설거지 한 가지를 부탁해도 괜찮아요."),
        ],
        "설거지를 줄이고 싶어요": [
            ("1단계 · 조리 도구 하나", "가능하면 냄비 하나나 팬 하나로 조리할 메뉴를 골라요."),
            ("2단계 · 한 그릇으로 구성", "밥과 익힌 재료를 한 그릇에 담되, 아이 몫은 안전한 크기와 질감으로 따로 준비해요."),
            ("3단계 · 남은 음식 관리", "먹던 음식과 보관할 음식은 미리 분리하고, 남은 음식은 안전한 보관 기준을 지켜요."),
        ],
        "가족이 함께 먹고 싶어요": [
            ("1단계 · 기본 메뉴 공유", "밥, 충분히 익힌 단백질, 부드러운 채소를 기본으로 준비해요."),
            ("2단계 · 간은 나중에", "아이 몫을 먼저 덜어낸 다음 성인 음식에 양념을 더해요."),
            ("3단계 · 각자 먹기 편하게", "아이에게는 발달 단계에 맞는 질감과 크기로, 성인에게는 원하는 곁들임을 더해요."),
        ],
    }
    for title, description in plans[situation]:
        st.markdown(f"**{title}**")
        st.write(description)
    st.info("가능하면 아이가 안전한 상태인지 먼저 확인하고, 뜨거운 음식이나 날카로운 도구를 다루는 동안에는 조리와 돌봄을 동시에 하지 않도록 해요.")

with tab3:
    st.subheader("식사 준비 체크리스트")
    st.write("필요한 항목만 체크해요. 체크 상태는 현재 세션에서 유지됩니다.")
    tasks = [
        "집에 있는 재료 확인하기",
        "아이에게 맞는 질감과 크기로 준비하기",
        "고기·달걀 등 충분히 익히기",
        "아이 몫을 먼저 덜어 식히기",
        "아이 음식의 온도 확인하기",
        "부모님 음식은 따로 간 맞추기",
        "먹던 음식과 보관할 음식 분리하기",
    ]
    for task in tasks:
        key = "task_" + task
        checked = st.checkbox(task, value=st.session_state.checked_tasks.get(key, False), key=key)
        st.session_state.checked_tasks[key] = checked
    done = sum(st.session_state.checked_tasks.get("task_" + task, False) for task in tasks)
    st.progress(done / len(tasks))
    st.caption(f"{done}/{len(tasks)}개 완료")
    if st.button("체크리스트 초기화"):
        for task in tasks:
            st.session_state.checked_tasks["task_" + task] = False
        st.rerun()

st.divider()
st.markdown("### 💛 기억해요")
st.write("부모님이 매 끼니 모든 것을 직접 만들 필요는 없어요. 가능한 만큼 간단하게 준비하고, 도움을 받을 수 있다면 도움을 요청해도 괜찮아요.")
with st.expander("아이 식사 안전 안내"):
    st.write(
        "이 앱은 일반적인 식사 아이디어를 제공하며 의료·영양 상담을 대신하지 않습니다. "
        "아이의 연령, 발달, 알레르기, 삼킴 능력에 따라 먹을 수 있는 음식과 형태가 다릅니다. "
        "질식 위험이 있는 단단하거나 둥근 음식은 피하고, 아이가 먹는 동안에는 가까이에서 지켜봐 주세요. "
        "생후 12개월 미만 영아에게 꿀을 주지 마세요. 특정 식품 도입이나 알레르기가 걱정된다면 소아청소년과 의료진과 상의하세요."
    )
st.caption("아이랑 한 끼 · 가족의 식사 준비 부담을 덜기 위한 간단한 도구")
