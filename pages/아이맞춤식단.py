import streamlit as st
from datetime import date
from collections import Counter
from pathlib import Path
import csv
import io
import random
import hashlib

st.set_page_config(page_title="오늘의 꼬마식탁", page_icon="🥑", layout="wide")

# ---------- 스타일 ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');
html, body, [class*="css"] { font-family: 'Gowun Dodum', sans-serif; }
.stApp { background: #fffdf8; color: #26352b; }
[data-testid="stSidebar"] { background: #f1f6ed; border-right: 1px solid #e5eadf; }
.hero {
  padding: 1.6rem 1.7rem; border-radius: 24px;
  background: linear-gradient(120deg, #e5f3df 0%, #fff0d9 100%);
  border: 1px solid #e2ebdc; margin-bottom: 1.15rem;
}
.hero h1 { font-family: 'Jua', sans-serif; color: #315b3d; font-size: 2.45rem; margin: 0; }
.hero p { color: #58715b; margin: .5rem 0 0; font-size: 1.03rem; }
.eyebrow { color:#6d8c67; font-size:.82rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.recipe-name { font-family:'Jua',sans-serif; color:#315b3d; font-size:1.25rem; }
div[data-testid="stMetric"] { background:#fff; border:1px solid #e8ecdf; padding:12px 14px; border-radius:16px; }
div.stButton > button { border-radius: 12px; font-weight:700; }
div[data-testid="stForm"] { background:#fff; padding:1rem; border:1px solid #e8ecdf; border-radius:18px; }
.tipbox { background:#f3f7ed; border-radius:14px; padding:12px 14px; border:1px solid #e2ead9; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# Food-specific images: the displayed image changes with the selected recipe.
# These are remote Unsplash CDN images; if a URL is unavailable, the app shows an emoji fallback.
RECIPES = [
    {"name":"소고기 채소죽","meal":"아침","ages":["6~11개월","1~2세","3~5세","6세 이상"],"ingredients":[("쌀","밥 기준 1/3공기"),("소고기","30~50g"),("당근","조금"),("애호박","조금")],"allergens":[],"groups":["곡류","단백질","채소"],"minutes":25,"emoji":"🥣","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=85","steps":["쌀을 씻어 불립니다.","소고기와 채소를 잘게 다집니다.","냄비에 재료와 물을 넣고 재료가 충분히 부드러워질 때까지 끓입니다.","아이의 발달 단계에 맞춰 입자와 농도를 조절합니다."],"tip":"이유식 진행 단계와 삼킴 능력에 맞춰 질감을 조절하세요."},
    {"name":"바나나 오트밀","meal":"아침","ages":["6~11개월","1~2세","3~5세","6세 이상"],"ingredients":[("오트밀","20~30g"),("바나나","1/2개"),("물","적당량")],"allergens":[],"groups":["곡류","과일"],"minutes":10,"emoji":"🍌","image":"https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=1000&q=85","steps":["오트밀에 물을 넣고 부드럽게 끓입니다.","바나나를 포크로 으깹니다.","오트밀이 적당히 식으면 바나나를 섞어 제공합니다."],"tip":"우유를 넣지 않는 기본 레시피입니다."},
    {"name":"두부 달걀찜","meal":"아침","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("두부","1/4모"),("달걀","1개"),("당근","조금")],"allergens":["대두","달걀"],"groups":["단백질","채소"],"minutes":15,"emoji":"🍳","image":"https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1000&q=85","steps":["두부를 으깨고 당근을 잘게 다집니다.","달걀과 재료를 골고루 섞습니다.","찜기나 약불에서 속까지 완전히 익힙니다."],"tip":"달걀 또는 대두 알레르기가 등록되어 있다면 추천 목록에서 제외됩니다."},
    {"name":"닭고기 채소덮밥","meal":"점심","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("닭고기","100~150g"),("밥","아이 1공기"),("당근","1/3개"),("브로콜리","작은 송이 3개")],"allergens":[],"groups":["곡류","단백질","채소"],"minutes":20,"emoji":"🍚","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=85","steps":["닭고기와 채소를 깨끗이 씻습니다.","당근과 브로콜리를 잘게 썹니다.","닭고기를 속까지 완전히 익히고 채소도 부드럽게 익힙니다.","밥 위에 올리고 아이에게 알맞은 크기로 잘라 제공합니다."],"tip":"소금과 간장은 최소한으로 사용하세요."},
    {"name":"두부 버섯덮밥","meal":"점심","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("두부","1/4모"),("버섯","소량"),("밥","아이 1공기"),("양파","조금")],"allergens":["대두"],"groups":["곡류","단백질","채소"],"minutes":20,"emoji":"🍄","image":"https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1000&q=85","steps":["두부와 버섯, 양파를 잘게 썹니다.","재료에 물을 조금 넣고 충분히 익힙니다.","밥 위에 올려 따뜻하게 제공합니다."],"tip":"버섯은 질기지 않도록 잘게 썰어 충분히 익히세요."},
    {"name":"연어 채소밥","meal":"점심","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("연어","80~100g"),("밥","아이 1공기"),("브로콜리","조금"),("당근","조금")],"allergens":["생선"],"groups":["곡류","단백질","채소"],"minutes":25,"emoji":"🐟","image":"https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=1000&q=85","steps":["연어를 속까지 완전히 익힙니다.","가시가 남아 있지 않은지 꼼꼼히 확인하고 잘게 부숩니다.","부드럽게 익힌 채소와 밥을 함께 제공합니다."],"tip":"생선 가시를 꼼꼼히 확인하세요."},
    {"name":"소고기 무국과 밥","meal":"저녁","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("소고기","80g"),("무","조금"),("밥","아이 1공기")],"allergens":[],"groups":["곡류","단백질","채소"],"minutes":30,"emoji":"🍲","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=85","steps":["소고기와 무를 작게 썹니다.","재료를 물에 넣고 충분히 푹 끓입니다.","간을 최소화하고 건더기를 먹기 좋은 크기로 제공합니다."],"tip":"어린아이에게는 국물의 간을 최소화하세요."},
    {"name":"닭고기 감자조림","meal":"저녁","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("닭고기","100g"),("감자","1/2개"),("당근","조금"),("밥","아이 1공기")],"allergens":[],"groups":["곡류","단백질","채소"],"minutes":25,"emoji":"🥔","image":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=85","steps":["닭고기와 감자, 당근을 작게 썹니다.","냄비에 재료와 물을 넣고 푹 익힙니다.","닭고기가 속까지 익고 감자가 부드러워졌는지 확인합니다.","밥과 함께 제공하고 필요하면 더 잘게 자릅니다."],"tip":"간장과 소금은 최소한으로 사용하세요."},
    {"name":"고구마와 배","meal":"간식","ages":["6~11개월","1~2세","3~5세","6세 이상"],"ingredients":[("고구마","작은 것 1개"),("배","조금")],"allergens":[],"groups":["채소","과일"],"minutes":15,"emoji":"🍠","image":"https://images.unsplash.com/photo-1596097635121-14b63b7a0c19?auto=format&fit=crop&w=1000&q=85","steps":["고구마를 속까지 푹 찝니다.","배를 씻고 씨와 단단한 부분을 제거합니다.","부드럽고 안전한 크기로 준비합니다."],"tip":"둥글고 단단한 조각은 질식 위험이 있으니 크기와 질감을 조절하세요."},
    {"name":"플레인 요거트와 딸기","meal":"간식","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("무가당 플레인 요거트","1개"),("딸기","1~2개")],"allergens":["우유"],"groups":["유제품","과일"],"minutes":5,"emoji":"🍓","image":"https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=1000&q=85","steps":["딸기를 깨끗이 씻고 꼭지를 제거합니다.","아이에게 알맞은 작은 크기로 자릅니다.","무가당 플레인 요거트와 섞어 제공합니다."],"tip":"우유 알레르기가 있으면 이 메뉴를 제외하세요."},
    {"name":"채소 주먹밥","meal":"점심","ages":["1~2세","3~5세","6세 이상"],"ingredients":[("밥","아이 1공기"),("당근","조금"),("애호박","조금"),("참기름","몇 방울")],"allergens":["참깨"],"groups":["곡류","채소"],"minutes":20,"emoji":"🍙","image":"https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=1000&q=85","steps":["당근과 애호박을 잘게 다져 충분히 익힙니다.","밥과 채소를 섞고 참기름을 소량 넣습니다.","아이가 먹기 쉬운 작은 크기로 만듭니다."],"tip":"참깨 알레르기가 등록되어 있다면 추천 목록에서 제외됩니다."},
    {"name":"단호박 두부수프","meal":"저녁","ages":["6~11개월","1~2세","3~5세","6세 이상"],"ingredients":[("단호박","1/8개"),("두부","조금"),("물","적당량")],"allergens":["대두"],"groups":["채소","단백질"],"minutes":20,"emoji":"🎃","image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=85","steps":["단호박을 푹 쪄서 껍질과 씨를 제거합니다.","단호박과 두부, 물을 넣고 부드럽게 끓입니다.","아이에게 알맞은 농도로 으깨거나 갈아 제공합니다."],"tip":"대두 알레르기가 있다면 두부를 넣지 마세요."},
]

AGE_OPTIONS = ["6~11개월", "1~2세", "3~5세", "6세 이상"]
ALLERGENS = ["달걀", "우유", "땅콩", "견과류", "대두", "밀", "생선", "새우·갑각류", "참깨"]
DAYS = ["월", "화", "수", "목", "금", "토", "일"]

def allowed(recipe, age, allergies, dislikes):
    if age not in recipe["ages"]:
        return False
    if set(recipe["allergens"]) & set(allergies):
        return False
    searchable = recipe["name"] + " " + " ".join(n for n, _ in recipe["ingredients"])
    return not any(word and word in searchable for word in dislikes)

def make_plan(age, allergies, dislikes, snacks, seed):
    meal_types = ["아침", "점심", "저녁"] + (["간식"] if snacks else [])
    rng = random.Random(seed)
    plan = []
    usage = Counter()
    for day_index, day in enumerate(DAYS):
        day_items = []
        for meal_type in meal_types:
            choices = [r for r in RECIPES if r["meal"] == meal_type and allowed(r, age, allergies, dislikes)]
            if not choices:
                choices = [r for r in RECIPES if allowed(r, age, allergies, dislikes)]
            if choices:
                rng.shuffle(choices)
                choices.sort(key=lambda r: usage[r["name"]])
                recipe = choices[0]
                usage[recipe["name"]] += 1
                day_items.append({"meal": meal_type, "recipe": recipe})
            else:
                day_items.append({"meal": meal_type, "recipe": None})
        plan.append({"day": day, "items": day_items})
    return plan

def plan_csv(plan):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["요일", "식사", "메뉴", "재료"])
    for day in plan:
        for item in day["items"]:
            recipe = item["recipe"]
            writer.writerow([day["day"] + "요일", item["meal"], recipe["name"] if recipe else "조건에 맞는 메뉴 없음",
                             ", ".join(n for n, _ in recipe["ingredients"]) if recipe else ""])
    return ("\ufeff" + output.getvalue()).encode("utf-8")

def show_food_image(recipe, caption=None):
    if recipe:
        try:
            st.image(recipe["image"], caption=caption or recipe["name"], use_container_width=True)
        except Exception:
            st.markdown(f"<div style='font-size:5rem;text-align:center;padding:2rem;background:#f4f6eb;border-radius:16px'>{recipe['emoji']}</div>", unsafe_allow_html=True)

if "profile" not in st.session_state:
    st.session_state.profile = {"name": "우리 아이", "age": "3~5세", "allergies": [], "dislikes": "", "snacks": True}
if "menu_seed" not in st.session_state:
    st.session_state.menu_seed = date.today().isoformat()

profile = st.session_state.profile
with st.sidebar:
    st.markdown("## 🥑 꼬마식탁")
    page = st.radio("페이지", ["오늘의 식단", "주간 식단표", "레시피와 재료", "장보기 목록", "아이 정보 입력"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 아이 프로필")
    st.write(f"👧 **{profile['name']}**")
    st.write(f"🌱 {profile['age']}")
    st.write("🚫 " + (", ".join(profile["allergies"]) if profile["allergies"] else "알레르기 미등록"))
    st.caption("입력 내용은 이 세션에서만 사용됩니다.")

st.markdown("""
<div class="hero">
  <div class="eyebrow">LITTLE TABLE · DAILY MENU</div>
  <h1>오늘의 꼬마식탁 🥦</h1>
  <p>우리 아이에게 꼭 맞는 메뉴를 고르고, 재료부터 만드는 방법까지 한 번에 확인해요.</p>
</div>
""", unsafe_allow_html=True)

allergies = profile["allergies"]
dislikes = [x.strip() for x in profile["dislikes"].split(",") if x.strip()]
# Seed changes by date automatically. The button also lets the user get another set immediately.
today_seed = date.today().isoformat() + "|" + st.session_state.menu_seed
seed = int(hashlib.sha256(today_seed.encode("utf-8")).hexdigest()[:8], 16)
week = make_plan(profile["age"], allergies, dislikes, profile["snacks"], seed)

if page == "아이 정보 입력":
    st.subheader("🧸 우리 아이 정보")
    st.write("아이의 연령과 먹을 수 없는 재료를 입력하면 메뉴 추천에 반영됩니다.")
    with st.form("profile_form"):
        name = st.text_input("아이 별명", value=profile["name"], max_chars=30, placeholder="예: 튼튼이")
        age = st.selectbox("연령대", AGE_OPTIONS, index=AGE_OPTIONS.index(profile["age"]) if profile["age"] in AGE_OPTIONS else 2)
        allergies_input = st.multiselect("알레르기 식재료", ALLERGENS, default=[a for a in profile["allergies"] if a in ALLERGENS])
        dislikes_input = st.text_input("기피 식재료 (쉼표로 구분)", value=profile["dislikes"], placeholder="예: 버섯, 양파")
        snacks_input = st.checkbox("간식도 식단에 포함하기", value=profile["snacks"])
        saved = st.form_submit_button("🌿 내 아이 식단에 적용", type="primary", use_container_width=True)
    if saved:
        st.session_state.profile = {
            "name": name.strip() or "우리 아이", "age": age,
            "allergies": allergies_input, "dislikes": dislikes_input, "snacks": snacks_input
        }
        st.success("입력한 정보를 식단에 적용했어요!")
        st.rerun()

elif page == "오늘의 식단":
    st.subheader(f"반가워요, {profile['name']} 보호자님! 🌼")
    m1, m2, m3 = st.columns(3)
    m1.metric("오늘 날짜", date.today().strftime("%Y.%m.%d"))
    m2.metric("제외한 알레르기", f"{len(allergies)}개")
    m3.metric("식단 구성", "3끼 + 간식" if profile["snacks"] else "하루 3끼")
    st.markdown("### 🍽️ 오늘 추천 메뉴")
    today_items = week[date.today().weekday()]["items"]
    cols = st.columns(len(today_items))
    for idx, item in enumerate(today_items):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(f"**{item['meal']}**")
                if item["recipe"]:
                    show_food_image(item["recipe"])
                    st.markdown(f"<div class='recipe-name'>{item['recipe']['name']}</div>", unsafe_allow_html=True)
                    st.caption(f"⏱️ {item['recipe']['minutes']}분 · " + " · ".join(item["recipe"]["groups"]))
                else:
                    st.info("현재 조건에 맞는 메뉴가 부족해요.")
    if st.button("🔄 다른 메뉴로 다시 추천받기", type="primary", use_container_width=True):
        st.session_state.menu_seed = str(random.random())
        st.rerun()
    st.markdown("### ✨ 추천 메뉴는 이렇게 정해져요")
    a, b, c = st.columns(3)
    with a:
        st.markdown("<div class='tipbox'><b>1. 아이 정보</b><br>연령과 알레르기, 기피 재료를 확인해요.</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='tipbox'><b>2. 메뉴 필터링</b><br>조건에 맞지 않는 레시피를 추천 후보에서 제외해요.</div>", unsafe_allow_html=True)
    with c:
        st.markdown("<div class='tipbox'><b>3. 매일 새롭게</b><br>날짜에 따라 메뉴 구성이 바뀌고, 버튼으로 다시 추천할 수 있어요.</div>", unsafe_allow_html=True)

elif page == "주간 식단표":
    st.subheader("📅 일주일 식단")
    st.caption("날짜에 따라 메뉴 구성이 바뀝니다. 다른 메뉴가 필요하면 오늘의 식단에서 다시 추천받을 수 있어요.")
    for day in week:
        with st.container(border=True):
            st.markdown(f"### {day['day']}요일")
            cols = st.columns(len(day["items"]))
            for idx, item in enumerate(day["items"]):
                with cols[idx]:
                    st.markdown(f"**{item['meal']}**")
                    if item["recipe"]:
                        show_food_image(item["recipe"])
                        st.write(item["recipe"]["name"])
                        st.caption(f"{item['recipe']['minutes']}분")
                    else:
                        st.write("조건에 맞는 메뉴 없음")
    st.download_button("⬇️ 주간 식단표 CSV 다운로드", data=plan_csv(week), file_name="꼬마식탁_주간식단표.csv", mime="text/csv", use_container_width=True)

elif page == "레시피와 재료":
    st.subheader("👩‍🍳 메뉴별 재료와 만드는 방법")
    choices = [r for r in RECIPES if allowed(r, profile["age"], allergies, dislikes)]
    if not choices:
        st.warning("조건에 맞는 메뉴가 없습니다. 아이 정보 입력에서 기피 재료를 확인해 주세요.")
    else:
        selected_name = st.selectbox("궁금한 메뉴를 선택하세요", [r["name"] for r in choices])
        recipe = next(r for r in choices if r["name"] == selected_name)
        left, right = st.columns([1, 1.15])
        with left:
            show_food_image(recipe)
            st.metric("예상 조리 시간", f"{recipe['minutes']}분")
            st.write("**식품군:** " + " · ".join(recipe["groups"]))
            if recipe["allergens"]:
                st.warning("알레르기 확인 재료: " + ", ".join(recipe["allergens"]))
        with right:
            st.markdown("### 🧺 준비할 재료")
            for ingredient, amount in recipe["ingredients"]:
                st.write(f"- **{ingredient}** — {amount}")
            st.markdown("### 🥄 만드는 순서")
            for idx, step in enumerate(recipe["steps"], start=1):
                st.write(f"{idx}. {step}")
            st.info("보호자 팁: " + recipe["tip"])

elif page == "장보기 목록":
    st.subheader("🛒 이번 주 장보기")
    totals = Counter()
    for day in week:
        for item in day["items"]:
            if item["recipe"]:
                totals.update(name for name, _ in item["recipe"]["ingredients"])
    if not totals:
        st.warning("현재 조건에 맞는 메뉴가 없어 장보기 목록을 만들 수 없습니다.")
    else:
        st.caption("체크하면서 장을 보세요. 재료 수량은 메뉴에 등장하는 횟수 기준입니다.")
        checked = 0
        for ingredient, count in sorted(totals.items()):
            if st.checkbox(f"{ingredient} · {count}회 사용", key="shop_" + ingredient):
                checked += 1
        st.progress(checked / len(totals))
        st.write(f"준비 완료: {checked}/{len(totals)}개")
        shopping_text = "꼬마식탁 장보기 목록\n" + "\n".join(f"- {name} ({count}회 사용)" for name, count in sorted(totals.items()))
        st.download_button("⬇️ 장보기 목록 다운로드", data=shopping_text, file_name="꼬마식탁_장보기.txt", mime="text/plain", use_container_width=True)

st.markdown("---")
st.caption("💚 참고용 식단 아이디어입니다. 알레르기는 제품 성분표와 교차오염 정보를 확인하세요. 영유아는 질식 위험을 고려해 안전한 크기와 질감으로 조리하고, 의료진의 지침을 우선하세요.")
