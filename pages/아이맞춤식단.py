import streamlit as st
from collections import Counter
from datetime import date
from pathlib import Path
import csv
import io

st.set_page_config(page_title="아이맞춤 식단", page_icon="🥦", layout="wide")

# ---- 디자인 ----
st.markdown("""
<style>
.stApp { background: #fbfcf8; }
[data-testid="stSidebar"] { background: #eff7f0; }
.hero { background: linear-gradient(110deg,#e1f3e8,#fff3df); padding: 1.4rem;
        border-radius: 20px; border: 1px solid #dcebe0; margin-bottom: 1rem; }
.hero h1 { color:#20563c; margin:0; }
.hero p { color:#4b6c59; margin:.4rem 0 0; }
.info-card { background:white; border:1px solid #e4ece5; border-radius:16px; padding:1rem; }
.small { color:#66776b; font-size:.9rem; }
div[data-testid="stMetric"] { background:white; padding:12px; border-radius:14px; border:1px solid #e4ece5; }
</style>
""", unsafe_allow_html=True)

# Each recipe has ingredients, steps, allergens, food groups and a local image category.
RECIPES = [
    {"name":"닭가슴살 채소덮밥","meal":"점심","ages":["1~2세","3~5세","6세 이상"],
     "ingredients":[("닭가슴살","150g"),("밥","아이 1공기"),("당근","1/3개"),("브로콜리","작은 송이 3개"),("양파","1/4개")],
     "allergens":[],"groups":["곡류","단백질","채소"],"minutes":20,
     "steps":["닭가슴살과 채소를 깨끗이 씻습니다.","당근·브로콜리·양파를 아이가 먹기 쉬운 크기로 잘게 썹니다.","닭고기를 속까지 완전히 익히고 채소도 부드럽게 익힙니다.","밥 위에 올려 제공합니다. 어린아이에게는 재료를 더 잘게 잘라 주세요."],
     "tip":"소금과 간장은 최소한으로 사용하세요."},
    {"name":"소고기 채소죽","meal":"아침","ages":["6~11개월","1~2세","3~5세","6세 이상"],
     "ingredients":[("쌀","밥 기준 1/3공기"),("소고기","30~50g"),("당근","조금"),("애호박","조금"),("물","적당량")],
     "allergens":[],"groups":["곡류","단백질","채소"],"minutes":25,
     "steps":["쌀을 씻어 불립니다.","소고기와 채소를 잘게 다집니다.","냄비에 재료와 물을 넣고 충분히 끓입니다.","월령과 씹기 능력에 맞춰 입자와 농도를 조절합니다."],
     "tip":"이유식 진행 단계와 아이의 삼킴 능력에 맞게 질감을 조절하세요."},
    {"name":"두부 버섯덮밥","meal":"점심","ages":["1~2세","3~5세","6세 이상"],
     "ingredients":[("두부","1/4모"),("버섯","소량"),("밥","아이 1공기"),("양파","조금")],
     "allergens":["대두"],"groups":["곡류","단백질","채소"],"minutes":20,
     "steps":["두부와 버섯, 양파를 잘게 썹니다.","재료를 팬에 넣고 물을 조금 더해 충분히 익힙니다.","밥 위에 올려 따뜻하게 제공합니다."],
     "tip":"버섯은 질기지 않도록 잘게 썰어 충분히 익히세요."},
    {"name":"연어 채소밥","meal":"저녁","ages":["1~2세","3~5세","6세 이상"],
     "ingredients":[("연어","80~100g"),("밥","아이 1공기"),("브로콜리","조금"),("당근","조금")],
     "allergens":["생선"],"groups":["곡류","단백질","채소"],"minutes":25,
     "steps":["연어를 속까지 완전히 익힙니다.","가시가 남아 있지 않은지 여러 번 확인하고 잘게 부숩니다.","채소를 부드럽게 익혀 밥과 함께 제공합니다."],
     "tip":"생선 가시를 꼼꼼히 확인하고, 생선 알레르기가 있다면 선택하지 마세요."},
    {"name":"단호박 두부수프","meal":"저녁","ages":["6~11개월","1~2세","3~5세","6세 이상"],
     "ingredients":[("단호박","1/8개"),("두부","조금"),("물","적당량")],
     "allergens":["대두"],"groups":["채소","단백질"],"minutes":20,
     "steps":["단호박을 푹 쪄서 껍질과 씨를 제거합니다.","단호박과 두부, 물을 넣고 부드럽게 끓입니다.","아이에게 적합한 농도로 으깨거나 갈아 제공합니다."],
     "tip":"대두 알레르기가 있다면 두부를 넣지 마세요."},
    {"name":"바나나 오트밀","meal":"아침","ages":["6~11개월","1~2세","3~5세","6세 이상"],
     "ingredients":[("오트밀","20~30g"),("바나나","1/2개"),("물","적당량")],
     "allergens":[],"groups":["곡류","과일"],"minutes":10,
     "steps":["오트밀에 물을 넣고 부드럽게 끓입니다.","바나나를 포크로 으깹니다.","오트밀이 식으면 바나나를 섞어 제공합니다."],
     "tip":"우유를 넣지 않는 기본 레시피입니다. 질감은 아이의 발달 단계에 맞추세요."},
    {"name":"고구마와 배","meal":"간식","ages":["6~11개월","1~2세","3~5세","6세 이상"],
     "ingredients":[("고구마","작은 것 1개"),("배","조금")],
     "allergens":[],"groups":["채소","과일"],"minutes":15,
     "steps":["고구마를 속까지 푹 찝니다.","배를 깨끗이 씻고 씨와 단단한 부분을 제거합니다.","아이에게 안전한 부드러운 질감과 크기로 준비합니다."],
     "tip":"둥글고 단단한 조각은 질식 위험이 있으니 안전한 크기로 자르세요."},
    {"name":"플레인 요거트와 딸기","meal":"간식","ages":["1~2세","3~5세","6세 이상"],
     "ingredients":[("무가당 플레인 요거트","1개"),("딸기","1~2개")],
     "allergens":["우유"],"groups":["유제품","과일"],"minutes":5,
     "steps":["딸기를 깨끗이 씻고 꼭지를 제거합니다.","딸기를 아이가 먹기 쉬운 작은 크기로 자릅니다.","무가당 요거트와 섞어 제공합니다."],
     "tip":"우유 알레르기가 있으면 이 메뉴를 제외하세요."},
    {"name":"닭고기 감자조림","meal":"저녁","ages":["1~2세","3~5세","6세 이상"],
     "ingredients":[("닭고기","100g"),("감자","1/2개"),("당근","조금"),("밥","아이 1공기")],
     "allergens":[],"groups":["곡류","단백질","채소"],"minutes":25,
     "steps":["닭고기와 감자, 당근을 작게 썹니다.","냄비에 재료와 물을 넣고 푹 익힙니다.","닭고기가 속까지 익고 감자가 부드러워졌는지 확인합니다.","밥과 함께 제공하고 아이에 맞게 더 잘게 자릅니다."],
     "tip":"간장과 소금은 최소한으로 사용하세요."},
]

AGE_OPTIONS = ["6~11개월","1~2세","3~5세","6세 이상"]
ALLERGENS = ["달걀","우유","땅콩","견과류","대두","밀","생선","새우·갑각류","참깨"]
DAYS = ["월","화","수","목","금","토","일"]

def is_allowed(recipe, age, allergies, dislikes):
    if age not in recipe["ages"]:
        return False
    if set(recipe["allergens"]) & set(allergies):
        return False
    text = recipe["name"] + " " + " ".join(name for name, _ in recipe["ingredients"])
    return not any(x.strip() and x.strip() in text for x in dislikes)

def create_week(age, allergies, dislikes, snacks):
    types = ["아침","점심","저녁"] + (["간식"] if snacks else [])
    plan = []
    usage = Counter()
    for di, day in enumerate(DAYS):
        items = []
        for mt in types:
            choices = [r for r in RECIPES if r["meal"] == mt and is_allowed(r, age, allergies, dislikes)]
            if not choices:
                # fallback to any safe recipe for that meal slot, never bypass allergy filters
                choices = [r for r in RECIPES if is_allowed(r, age, allergies, dislikes)]
            if choices:
                choices.sort(key=lambda r: (usage[r["name"]], (RECIPES.index(r) + di) % len(RECIPES)))
                recipe = choices[0]
                usage[recipe["name"]] += 1
                items.append({"meal":mt, "recipe":recipe})
            else:
                items.append({"meal":mt, "recipe":None})
        plan.append({"day":day,"items":items})
    return plan

def csv_bytes(plan):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["요일","식사","메뉴","재료"])
    for d in plan:
        for item in d["items"]:
            r = item["recipe"]
            writer.writerow([d["day"]+"요일", item["meal"], r["name"] if r else "조건에 맞는 메뉴 없음",
                             ", ".join(n for n,_ in r["ingredients"]) if r else ""])
    return ("\ufeff" + output.getvalue()).encode("utf-8")

if "profile" not in st.session_state:
    st.session_state.profile = {"name":"우리 아이","age":"3~5세","allergies":[],"dislikes":"","snacks":True}
profile = st.session_state.profile

with st.sidebar:
    st.markdown("## 🥦 아이맞춤 식단")
    page = st.radio("메뉴", ["홈","주간 식단표","레시피 자세히 보기","장보기 목록","아이 정보 설정"])
    st.markdown("---")
    st.caption("아이의 연령과 식재료 정보를 반영해 메뉴를 구성해요.")
    st.markdown("**현재 프로필**")
    st.write(f"👶 {profile['name']} · {profile['age']}")
    st.write("🚫 " + (", ".join(profile["allergies"]) if profile["allergies"] else "알레르기 미등록"))

st.markdown('<div class="hero"><h1>🥦 아이맞춤 식단</h1><p>우리 아이의 건강한 한 끼를 쉽고 즐겁게 준비해요.</p></div>', unsafe_allow_html=True)

# Local image is bundled with the app, so the app doesn't depend on external image hosting.
image_file = Path(__file__).parent / "meal_dashboard.png"
if image_file.exists() and page == "홈":
    st.image(str(image_file), caption="아이맞춤 식단 화면 예시", use_container_width=True)

allergies = profile["allergies"]
dislikes = [x.strip() for x in profile["dislikes"].split(",") if x.strip()]
week = create_week(profile["age"], allergies, dislikes, profile["snacks"])

if page == "아이 정보 설정":
    st.subheader("👶 우리 아이 정보 설정")
    st.info("입력한 정보는 현재 브라우저 세션에서만 사용되며, 앱에서 별도로 저장하지 않습니다.")
    with st.form("profile_form"):
        name = st.text_input("아이 별명", value=profile["name"], max_chars=30)
        age = st.selectbox("연령대", AGE_OPTIONS, index=AGE_OPTIONS.index(profile["age"]) if profile["age"] in AGE_OPTIONS else 2)
        selected_allergies = st.multiselect("알레르기 식재료", ALLERGENS, default=[x for x in profile["allergies"] if x in ALLERGENS])
        dislikes_text = st.text_input("기피 식재료 (쉼표로 구분)", value=profile["dislikes"], placeholder="예: 버섯, 양파")
        snacks = st.checkbox("주간 식단에 간식 포함", value=profile["snacks"])
        save = st.form_submit_button("설정 적용", type="primary", use_container_width=True)
    if save:
        st.session_state.profile = {"name":name.strip() or "우리 아이","age":age,"allergies":selected_allergies,"dislikes":dislikes_text,"snacks":snacks}
        st.success("설정을 적용했어요.")
        st.rerun()

elif page == "홈":
    st.subheader(f"반가워요, {profile['name']} 보호자님! 🌱")
    c1,c2,c3 = st.columns(3)
    c1.metric("식단 기간","7일")
    c2.metric("등록한 알레르기",f"{len(allergies)}개")
    c3.metric("식사 구성","3끼 + 간식" if profile["snacks"] else "하루 3끼")
    st.markdown("### 🍽️ 오늘의 추천 메뉴")
    today = week[date.today().weekday()]
    cols = st.columns(len(today["items"]))
    for idx, item in enumerate(today["items"]):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(f"**{item['meal']}**")
                if item["recipe"]:
                    st.markdown(f"### {item['recipe']['name']}")
                    st.caption(f"⏱️ 약 {item['recipe']['minutes']}분")
                    st.write("주요 재료: " + ", ".join(n for n,_ in item["recipe"]["ingredients"][:3]))
                else:
                    st.warning("조건에 맞는 메뉴가 부족합니다.")
    st.markdown("### 💡 추천 메뉴는 이렇게 만들어요")
    s1,s2,s3 = st.columns(3)
    s1.info("**1. 아이 정보 확인**\n\n연령, 알레르기, 기피 식재료를 입력해요.")
    s2.info("**2. 안전한 메뉴 필터링**\n\n연령에 맞지 않거나 등록한 알레르기 식재료가 있는 메뉴를 제외해요.")
    s3.info("**3. 식품군을 다양하게**\n\n곡류·단백질·채소·과일 등을 조합하고 레시피를 안내해요.")
    st.caption("이 앱은 미리 준비된 레시피를 조건에 맞게 조합합니다. 의료적 진단이나 영양 처방을 대신하지 않습니다.")

elif page == "주간 식단표":
    st.subheader("📅 우리 아이 주간 식단표")
    st.write("알레르기 및 기피 식재료 설정을 반영한 메뉴입니다.")
    for day in week:
        with st.container(border=True):
            st.markdown(f"### {day['day']}요일")
            cols = st.columns(len(day["items"]))
            for idx,item in enumerate(day["items"]):
                with cols[idx]:
                    st.markdown(f"**{item['meal']}**")
                    if item["recipe"]:
                        st.write(item["recipe"]["name"])
                        st.caption(f"{item['recipe']['minutes']}분 · " + ", ".join(n for n,_ in item["recipe"]["ingredients"][:2]))
                    else:
                        st.write("조건에 맞는 메뉴 없음")
    st.download_button("주간 식단표 CSV 다운로드", data=csv_bytes(week), file_name="아이맞춤_주간식단표.csv", mime="text/csv", use_container_width=True)

elif page == "레시피 자세히 보기":
    st.subheader("📖 추천 메뉴와 레시피")
    allowed = [r for r in RECIPES if is_allowed(r, profile["age"], allergies, dislikes)]
    if not allowed:
        st.warning("현재 조건에 맞는 레시피가 없습니다. 아이 정보 설정에서 기피 식재료를 조정해 주세요.")
    else:
        selected = st.selectbox("메뉴 선택", [r["name"] for r in allowed])
        recipe = next(r for r in allowed if r["name"] == selected)
        left,right = st.columns([1,1.4])
        with left:
            if image_file.exists():
                st.image(str(image_file), caption=recipe["name"], use_container_width=True)
            st.metric("예상 조리 시간", f"{recipe['minutes']}분")
            st.write("**식품군:** " + ", ".join(recipe["groups"]))
            if recipe["allergens"]:
                st.warning("알레르기 확인 항목: " + ", ".join(recipe["allergens"]))
        with right:
            st.markdown("### 🧺 필요한 재료")
            for ingredient, amount in recipe["ingredients"]:
                st.write(f"- {ingredient}: {amount}")
            st.markdown("### 👩‍🍳 만드는 방법")
            for i, step in enumerate(recipe["steps"], start=1):
                st.write(f"{i}. {step}")
            st.info("보호자 팁: " + recipe["tip"])
        st.caption("재료의 정확한 양은 예시이며, 아이의 식사량과 발달 단계에 맞게 조절하세요.")

elif page == "장보기 목록":
    st.subheader("🛒 이번 주 장보기 목록")
    needed = Counter()
    for day in week:
        for item in day["items"]:
            if item["recipe"]:
                needed.update(n for n,_ in item["recipe"]["ingredients"])
    if not needed:
        st.warning("장보기 목록을 만들 수 있는 메뉴가 없습니다.")
    else:
        st.caption("이번 주 식단에 등장하는 재료를 모았습니다. 수량은 메뉴에 사용되는 횟수 기준입니다.")
        done = 0
        for ingredient, count in sorted(needed.items()):
            if st.checkbox(f"{ingredient} · {count}회 사용", key="shop_"+ingredient):
                done += 1
        st.progress(done / len(needed))
        st.write(f"준비 완료: {done}/{len(needed)}개")
        shopping = "아이맞춤 식단 - 장보기 목록\n" + "\n".join(f"- {name} ({count}회 메뉴에 사용)" for name,count in sorted(needed.items()))
        st.download_button("장보기 목록 TXT 다운로드", data=shopping, file_name="아이맞춤_장보기목록.txt", mime="text/plain", use_container_width=True)

st.markdown("---")
st.caption("💚 아이맞춤 식단 | 알레르기 정보는 제품 성분표와 교차오염 안내를 반드시 확인하세요. 영유아의 질식 위험을 고려해 안전한 크기와 질감으로 조리하세요.")
