import streamlit as st
from datetime import date, timedelta
from collections import Counter

st.set_page_config(
    page_title="아이맞춤 식단",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 아이맞춤 식단: 외부 API 없이 실행되는 Streamlit 앱
# -----------------------------
st.markdown("""
<style>
    .stApp { background: #fbfcf8; }
    [data-testid="stSidebar"] { background: #f0f7f1; }
    .hero {
        padding: 1.35rem 1.5rem; border-radius: 22px;
        background: linear-gradient(115deg, #e2f3e8, #fff4df);
        border: 1px solid #e5eee5; margin-bottom: 1rem;
    }
    .hero h1 { color: #214c3b; margin: 0; font-size: 2.1rem; }
    .hero p { color: #496657; margin: .4rem 0 0 0; }
    .small-muted { color: #6b7c72; font-size: .9rem; }
    .meal-card {
        background: white; border: 1px solid #e8eee8; border-radius: 14px;
        padding: .8rem; min-height: 112px;
    }
    .meal-title { color: #214c3b; font-weight: 700; margin-bottom: .35rem; }
    .tag {
        display: inline-block; background: #edf6ee; color: #35684e;
        padding: 2px 8px; border-radius: 20px; font-size: .78rem; margin: 2px 2px 2px 0;
    }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e8eee8;
        padding: 12px; border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)

MEALS = [
    {"name":"소고기 채소죽", "type":"아침", "ages":["6~11개월","1~2세","3~5세","6세 이상"], "ingredients":["쌀","소고기","당근","애호박"], "allergens":[], "groups":["곡류","단백질","채소"], "time":25, "recipe":"쌀을 씻어 불린 뒤 잘게 다진 소고기와 채소를 넣고 충분히 끓입니다. 월령에 맞춰 물의 양과 입자 크기를 조절하세요."},
    {"name":"두부 달걀찜", "type":"아침", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["두부","달걀","당근"], "allergens":["달걀","대두"], "groups":["단백질","채소"], "time":15, "recipe":"두부를 으깨고 달걀과 잘게 다진 당근을 섞습니다. 물을 약간 넣고 약불 또는 찜기로 속까지 완전히 익힙니다."},
    {"name":"바나나 오트밀", "type":"아침", "ages":["6~11개월","1~2세","3~5세","6세 이상"], "ingredients":["오트밀","바나나","우유"], "allergens":["우유"], "groups":["곡류","과일"], "time":10, "recipe":"오트밀을 물이나 아이에게 적합한 음료에 부드럽게 끓이고 으깬 바나나를 섞습니다. 우유 알레르기가 있으면 물로 조리하세요."},
    {"name":"닭고기 채소밥", "type":"점심", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["쌀","닭고기","당근","브로콜리"], "allergens":[], "groups":["곡류","단백질","채소"], "time":25, "recipe":"닭고기를 완전히 익혀 잘게 찢고, 부드럽게 익힌 채소와 밥을 섞습니다. 아이의 씹기 능력에 맞게 잘게 다집니다."},
    {"name":"두부 버섯덮밥", "type":"점심", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["두부","버섯","쌀","양파"], "allergens":["대두"], "groups":["곡류","단백질","채소"], "time":20, "recipe":"두부와 버섯, 양파를 잘게 썰어 충분히 익힌 뒤 밥 위에 올립니다. 버섯은 질기지 않게 잘게 다집니다."},
    {"name":"연어 채소밥", "type":"점심", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["연어","쌀","브로콜리","당근"], "allergens":["생선"], "groups":["곡류","단백질","채소"], "time":25, "recipe":"연어를 완전히 익힌 뒤 가시가 없는지 꼼꼼히 확인하고 잘게 부숩니다. 밥과 부드럽게 익힌 채소를 곁들입니다."},
    {"name":"소고기 무국과 밥", "type":"저녁", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["소고기","무","쌀"], "allergens":[], "groups":["곡류","단백질","채소"], "time":30, "recipe":"소고기와 무를 작게 썰어 푹 끓입니다. 어린아이에게는 국물의 간을 최소화하고 건더기를 먹기 좋은 크기로 제공합니다."},
    {"name":"닭고기 감자조림과 밥", "type":"저녁", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["닭고기","감자","당근","쌀"], "allergens":[], "groups":["곡류","단백질","채소"], "time":25, "recipe":"닭고기와 감자, 당근을 작은 크기로 썰어 물을 넣고 푹 익힙니다. 간장이나 소금은 최소화하고 밥과 함께 냅니다."},
    {"name":"고구마와 배", "type":"간식", "ages":["6~11개월","1~2세","3~5세","6세 이상"], "ingredients":["고구마","배"], "allergens":[], "groups":["채소","과일"], "time":15, "recipe":"고구마를 속까지 푹 찌고 배는 깨끗이 씻어 씨와 단단한 부분을 제거합니다. 연령에 맞는 부드러운 질감과 크기로 준비합니다."},
    {"name":"플레인 요거트와 딸기", "type":"간식", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["요거트","딸기"], "allergens":["우유"], "groups":["유제품","과일"], "time":5, "recipe":"무가당 플레인 요거트에 깨끗이 씻은 딸기를 잘게 잘라 섞습니다. 딸기는 질식 위험이 없도록 아이에게 맞는 크기로 자릅니다."},
    {"name":"채소 주먹밥", "type":"점심", "ages":["1~2세","3~5세","6세 이상"], "ingredients":["쌀","당근","애호박","참기름"], "allergens":["참깨"], "groups":["곡류","채소"], "time":20, "recipe":"당근과 애호박을 잘게 다져 익힌 뒤 밥과 소량의 참기름을 섞습니다. 아이가 먹기 쉬운 작은 크기로 뭉칩니다."},
    {"name":"단호박 두부수프", "type":"저녁", "ages":["6~11개월","1~2세","3~5세","6세 이상"], "ingredients":["단호박","두부","물"], "allergens":["대두"], "groups":["채소","단백질"], "time":20, "recipe":"단호박을 푹 쪄서 으깨고 두부와 물을 넣어 부드럽게 끓입니다. 월령과 삼킴 능력에 맞춰 농도를 조절합니다."},
]

# Correct a data entry typo defensively, keeping the app simple and stable.
for meal in MEALS:
    meal.setdefault("allergens", [])
    meal.setdefault("ingredients", [])
    meal.setdefault("groups", [])

ALLERGEN_OPTIONS = ["달걀", "우유", "땅콩", "견과류", "대두", "밀", "생선", "새우·갑각류", "참깨"]
AGE_OPTIONS = ["6~11개월", "1~2세", "3~5세", "6세 이상"]
DAY_NAMES = ["월", "화", "수", "목", "금", "토", "일"]

def suitable(meal, age, allergies, dislikes):
    if age not in meal["ages"]:
        return False
    if set(meal["allergens"]) & set(allergies):
        return False
    text = " ".join(meal["ingredients"] + [meal["name"]])
    if any(item.strip() and item.strip() in text for item in dislikes):
        return False
    return True

def build_plan(age, allergies, dislikes, include_snacks):
    types = ["아침", "점심", "저녁"] + (["간식"] if include_snacks else [])
    plan = []
    used = Counter()
    for day_idx in range(7):
        day = {"day": DAY_NAMES[day_idx], "meals": []}
        for meal_type in types:
            candidates = [m for m in MEALS if m["type"] == meal_type and suitable(m, age, allergies, dislikes)]
            # For infants, keep to softer, age-tagged options and avoid the standard meal types with no candidates.
            if not candidates:
                day["meals"].append({"type": meal_type, "name":"조건에 맞는 메뉴가 부족해요", "ingredients":[], "groups":[], "time":0, "recipe":"알레르기와 기피 식재료 조건을 확인하거나 기피 식재료를 줄여 주세요.", "allergens":[]})
                continue
            candidates.sort(key=lambda m: (used[m["name"]], (MEALS.index(m) + day_idx) % len(MEALS)))
            chosen = candidates[0]
            used[chosen["name"]] += 1
            day["meals"].append(chosen)
        plan.append(day)
    return plan

st.sidebar.markdown("## 🥦 아이맞춤 식단")
page = st.sidebar.radio("메뉴", ["홈 대시보드", "주간 식단표", "레시피 모음", "장보기 목록", "아이 정보 설정"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption("아이의 성장 단계와 식재료 선호를 고려한 식단 도우미")

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name":"우리 아이", "age":"3~5세", "allergies":[], "dislikes":"",
        "snacks":True
    }
profile = st.session_state.profile

st.markdown('<div class="hero"><h1>🥦 아이맞춤 식단</h1><p>우리 아이에게 맞는 한 끼부터, 균형 잡힌 일주일 식단까지.</p></div>', unsafe_allow_html=True)

with st.sidebar.expander("현재 설정 요약", expanded=True):
    st.write(f"**아이:** {profile['name']}")
    st.write(f"**연령:** {profile['age']}")
    st.write("**알레르기:** " + (", ".join(profile["allergies"]) if profile["allergies"] else "미등록"))
    st.write("**간식 포함:** " + ("예" if profile["snacks"] else "아니요"))

allergies = profile["allergies"]
dislikes = [x.strip() for x in profile["dislikes"].split(",") if x.strip()]
plan = build_plan(profile["age"], allergies, dislikes, profile["snacks"])

if page == "아이 정보 설정":
    st.subheader("👶 우리 아이 정보")
    st.caption("입력한 정보는 현재 앱 세션에서만 사용됩니다. 별도 데이터베이스에 저장하지 않습니다.")
    with st.form("profile_form"):
        name = st.text_input("아이 별명", value=profile["name"], max_chars=30)
        age = st.selectbox("연령대", AGE_OPTIONS, index=AGE_OPTIONS.index(profile["age"]) if profile["age"] in AGE_OPTIONS else 2)
        selected_allergies = st.multiselect("알레르기 식재료", ALLERGEN_OPTIONS, default=[a for a in profile["allergies"] if a in ALLERGEN_OPTIONS])
        dislikes_text = st.text_input("기피 식재료 (쉼표로 구분)", value=profile["dislikes"], placeholder="예: 버섯, 양파")
        snacks = st.checkbox("주간 식단에 간식 포함", value=profile["snacks"])
        submitted = st.form_submit_button("정보 저장", type="primary", use_container_width=True)
    if submitted:
        st.session_state.profile = {"name":name.strip() or "우리 아이", "age":age, "allergies":selected_allergies, "dislikes":dislikes_text, "snacks":snacks}
        st.success("아이 정보가 이 세션에 반영되었습니다.")
        st.rerun()

elif page == "홈 대시보드":
    st.subheader(f"안녕하세요, {profile['name']} 보호자님! 🌱")
    st.write("아이 정보를 바탕으로 이번 주 식단을 구성했어요.")
    c1, c2, c3 = st.columns(3)
    c1.metric("식단 기간", "7일")
    c2.metric("알레르기 제외", f"{len(allergies)}개")
    c3.metric("식사 구성", "3끼 + 간식" if profile["snacks"] else "하루 3끼")
    st.markdown("### 오늘의 추천 메뉴")
    today_idx = date.today().weekday()
    today = plan[today_idx]
    cols = st.columns(min(4, len(today["meals"])))
    for i, meal in enumerate(today["meals"]):
        with cols[i % len(cols)]:
            st.markdown('<div class="meal-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="meal-title">{meal["type"]}</div>', unsafe_allow_html=True)
            st.write(meal["name"])
            if meal["time"]:
                st.caption(f"⏱️ 약 {meal['time']}분")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### 서비스 한눈에 보기")
    a,b,c = st.columns(3)
    a.info("🥕 **맞춤 추천**\n\n연령과 선호 식재료에 맞춰 메뉴를 구성합니다.")
    b.info("🛡️ **알레르기 관리**\n\n등록한 알레르기 식재료가 포함된 메뉴를 제외합니다.")
    c.info("📖 **간편 레시피**\n\n재료와 조리 순서를 확인하고 장보기 목록을 만듭니다.")
    st.caption("식단은 참고용 예시입니다. 아이의 건강 상태와 의료진의 지침을 우선해 주세요.")

elif page == "주간 식단표":
    st.subheader("📅 주간 맞춤 식단표")
    st.caption("메뉴를 선택하면 레시피 페이지에서 조리법을 확인할 수 있어요.")
    for day in plan:
        with st.container(border=True):
            st.markdown(f"### {day['day']}요일")
            cols = st.columns(len(day["meals"]))
            for i, meal in enumerate(day["meals"]):
                with cols[i]:
                    st.markdown(f"**{meal['type']}**")
                    st.write(meal["name"])
                    if meal["ingredients"]:
                        st.caption(" · ".join(meal["ingredients"]))
                    if meal["allergens"]:
                        st.caption("알레르기 정보: " + ", ".join(meal["allergens"]))
    st.download_button("주간 식단표 다운로드 (CSV)", data="요일,식사,메뉴,재료\n" + "\n".join(
        f"{d['day']}요일,{m['type']},{m['name']},{' / '.join(m['ingredients'])}" for d in plan for m in d["meals"]
    ), file_name="아이맞춤_주간식단표.csv", mime="text/csv", use_container_width=True)

elif page == "레시피 모음":
    st.subheader("📖 레시피 모음")
    all_meals = []
    seen = set()
    for day in plan:
        for meal in day["meals"]:
            if meal["name"] != "조건에 맞는 메뉴가 부족해요" and meal["name"] not in seen:
                all_meals.append(meal)
                seen.add(meal["name"])
    if not all_meals:
        st.warning("현재 조건에 맞는 메뉴가 없습니다. 아이 정보 설정에서 기피 식재료를 조정해 주세요.")
    else:
        names = [m["name"] for m in all_meals]
        selected_name = st.selectbox("메뉴 선택", names)
        recipe = next(m for m in all_meals if m["name"] == selected_name)
        st.markdown(f"### 🍲 {recipe['name']}")
        c1,c2 = st.columns(2)
        c1.metric("예상 조리 시간", f"{recipe['time']}분")
        c2.metric("식품군", ", ".join(recipe["groups"]))
        st.markdown("**주요 재료**")
        st.write(" · ".join(recipe["ingredients"]))
        st.markdown("**조리 방법**")
        st.write(recipe["recipe"])
        if recipe["allergens"]:
            st.warning("포함 가능 알레르기 식재료: " + ", ".join(recipe["allergens"]))
        st.caption("분량은 아이의 연령과 식사량에 맞춰 조절하고, 재료는 충분히 익혀 주세요.")

elif page == "장보기 목록":
    st.subheader("🛒 이번 주 장보기 목록")
    counts = Counter()
    for day in plan:
        for meal in day["meals"]:
            counts.update(meal["ingredients"])
    if not counts:
        st.info("장보기 목록을 만들 재료가 없습니다. 아이 정보를 확인해 주세요.")
    else:
        st.write("이번 주 메뉴에 필요한 재료입니다. 구매한 항목을 체크하세요.")
        checked = []
        for ingredient in sorted(counts):
            if st.checkbox(f"{ingredient}  ·  {counts[ingredient]}회 메뉴에 사용", key=f"shop_{ingredient}"):
                checked.append(ingredient)
        st.caption(f"{len(checked)} / {len(counts)}개 재료 준비 완료")
        shopping_text = "아이맞춤 식단 - 장보기 목록\n" + "\n".join(f"- {item}" for item in sorted(counts))
        st.download_button("장보기 목록 다운로드", data=shopping_text, file_name="아이맞춤_장보기목록.txt", mime="text/plain", use_container_width=True)

st.markdown("---")
st.caption("💚 아이맞춤 식단 | 식단 아이디어를 제공하는 참고용 도구입니다. 알레르기 중증도, 성장 상태, 질환 및 이유식 진행은 소아청소년과 의료진과 상담하세요.")
