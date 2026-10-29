import streamlit as st
from datetime import date
import random

st.set_page_config(page_title="꼬마식탁", page_icon="🥕", layout="wide")

RECIPES = [
    {
        "name": "닭고기 채소 덮밥", "category": "한 그릇", "minutes": 20, "age": 12,
        "allergens": [], "ingredients": ["밥 1공기", "닭고기 80g", "당근 20g", "애호박 20g", "양파 15g"],
        "steps": ["닭고기와 채소를 잘게 썹니다.", "닭고기를 팬에서 속까지 완전히 익힙니다.", "채소를 넣고 부드러워질 때까지 볶습니다.", "밥 위에 올리고 충분히 식혀 제공합니다."],
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80",
        "tip": "아이의 씹기 능력에 맞춰 작고 부드럽게 준비하세요."
    },
    {
        "name": "소고기 채소죽", "category": "죽", "minutes": 25, "age": 7,
        "allergens": [], "ingredients": ["밥 1/2공기", "다진 소고기 40g", "당근 15g", "애호박 15g", "물 250ml"],
        "steps": ["채소를 아주 잘게 다집니다.", "소고기를 냄비에서 완전히 익힙니다.", "밥, 채소, 물을 넣고 약불에서 저어 가며 끓입니다.", "재료가 부드러워지면 식혀서 제공합니다."],
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
        "tip": "월령과 씹기 능력에 맞춰 물의 양과 입자 크기를 조절하세요."
    },
    {
        "name": "연어 채소 파스타", "category": "면", "minutes": 25, "age": 12,
        "allergens": ["생선", "밀"], "ingredients": ["짧은 파스타 60g", "연어 60g", "브로콜리 25g", "양파 15g"],
        "steps": ["파스타를 충분히 익힙니다.", "연어의 가시를 확인하고 속까지 완전히 익힌 뒤 잘게 부숩니다.", "브로콜리와 양파를 부드럽게 익혀 잘게 다집니다.", "재료를 섞고 아이가 먹기 좋은 크기인지 확인합니다."],
        "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=80",
        "tip": "생선 가시를 꼼꼼히 확인하세요."
    },
    {
        "name": "채소 달걀전", "category": "반찬", "minutes": 15, "age": 12,
        "allergens": ["달걀"], "ingredients": ["달걀 1개", "당근 15g", "애호박 15g", "양파 10g"],
        "steps": ["채소를 잘게 다집니다.", "달걀을 풀고 채소를 섞습니다.", "기름을 조금 두른 팬에서 한입 크기로 부칩니다.", "속까지 완전히 익혀 식혀서 제공합니다."],
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=900&q=80",
        "tip": "달걀 알레르기가 있으면 이 메뉴를 선택하지 마세요."
    },
    {
        "name": "두부 버섯 덮밥", "category": "한 그릇", "minutes": 20, "age": 12,
        "allergens": ["대두"], "ingredients": ["밥 1공기", "두부 80g", "버섯 20g", "당근 15g"],
        "steps": ["두부의 물기를 빼고 작게 자릅니다.", "버섯과 당근을 잘게 썰어 충분히 익힙니다.", "두부를 넣고 부드럽게 볶습니다.", "밥 위에 올려 식혀서 제공합니다."],
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
        "tip": "두부는 대두 성분을 포함합니다."
    },
    {
        "name": "닭고기 감자 수프", "category": "국·수프", "minutes": 25, "age": 9,
        "allergens": [], "ingredients": ["닭고기 60g", "감자 1/2개", "양파 15g", "물 250ml"],
        "steps": ["닭고기와 감자, 양파를 작게 썹니다.", "냄비에 물과 재료를 넣고 충분히 익힙니다.", "감자를 으깨 농도를 조절합니다.", "뜨겁지 않게 식혀서 제공합니다."],
        "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=900&q=80",
        "tip": "닭고기는 속까지 완전히 익혀 주세요."
    },
    {
        "name": "바나나 오트밀", "category": "간식", "minutes": 10, "age": 8,
        "allergens": ["귀리"], "ingredients": ["오트밀 25g", "바나나 1/2개", "물 100ml"],
        "steps": ["바나나를 포크로 으깹니다.", "오트밀과 물을 냄비에 넣고 약불에서 끓입니다.", "부드러워지면 바나나를 섞습니다.", "충분히 식혀서 제공합니다."],
        "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=900&q=80",
        "tip": "귀리 제품의 포장 성분과 교차접촉 표시를 확인하세요."
    },
    {
        "name": "고구마 요거트 볼", "category": "간식", "minutes": 15, "age": 12,
        "allergens": ["우유"], "ingredients": ["고구마 1/2개", "플레인 요거트 2큰술"],
        "steps": ["고구마를 부드럽게 찌거나 삶습니다.", "껍질을 벗기고 덩어리가 없게 으깹니다.", "식힌 고구마에 요거트를 섞습니다.", "아이에게 맞는 질감인지 확인합니다."],
        "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=900&q=80",
        "tip": "요거트는 우유 성분을 포함합니다."
    },
    {
        "name": "돼지고기 채소 볶음밥", "category": "한 그릇", "minutes": 20, "age": 12,
        "allergens": [], "ingredients": ["밥 1공기", "다진 돼지고기 60g", "애호박 25g", "당근 15g", "양파 15g"],
        "steps": ["채소를 잘게 다집니다.", "돼지고기를 팬에서 속까지 완전히 익힙니다.", "채소를 넣고 부드럽게 볶습니다.", "밥을 넣어 골고루 섞고 식혀서 제공합니다."],
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80",
        "tip": "고기는 속까지 완전히 익혀 주세요."
    },
    {
        "name": "렌틸콩 채소 수프", "category": "국·수프", "minutes": 30, "age": 12,
        "allergens": [], "ingredients": ["렌틸콩 40g", "당근 20g", "감자 1/2개", "양파 15g", "물 300ml"],
        "steps": ["렌틸콩을 씻고 채소를 작게 썹니다.", "냄비에 재료와 물을 넣습니다.", "콩과 채소가 완전히 부드러워질 때까지 끓입니다.", "필요하면 으깨 아이에게 맞는 질감으로 조절합니다."],
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
        "tip": "콩류를 처음 먹는 경우 소량으로 시작하고 반응을 살펴보세요."
    }
]

ALLERGENS = ["우유", "달걀", "대두", "밀", "생선", "땅콩", "견과류", "새우·갑각류", "메밀", "참깨", "귀리"]

def get_safe_recipes(allergies, age_months, dislikes):
    safe = []
    for recipe in RECIPES:
        if recipe["age"] > age_months:
            continue
        if set(recipe["allergens"]).intersection(set(allergies)):
            continue
        all_text = recipe["name"] + " " + " ".join(recipe["ingredients"])
        if any(item.strip() and item.strip().lower() in all_text.lower() for item in dislikes):
            continue
        safe.append(recipe)
    return safe

def show_recipe(recipe):
    st.subheader(recipe["name"])
    left, right = st.columns([1, 1.2])
    with left:
        st.image(recipe["image"], use_container_width=True)
        st.caption("조리 시간: {}분 · 종류: {}".format(recipe["minutes"], recipe["category"]))
        st.write("**알레르기 표시:** " + (", ".join(recipe["allergens"]) if recipe["allergens"] else "등록된 주요 성분 없음"))
    with right:
        st.markdown("**재료**")
        for ingredient in recipe["ingredients"]:
            st.write("- " + ingredient)
        st.markdown("**조리 순서**")
        for number, step in enumerate(recipe["steps"], start=1):
            st.write("{}. {}".format(number, step))
        st.info("조리 팁: " + recipe["tip"])

st.markdown("""
<style>
.stApp {background-color: #fffaf0;}
.block-container {max-width: 1150px; padding-top: 1.5rem;}
</style>
""", unsafe_allow_html=True)
st.title("🥕 오늘의 꼬마식탁")
st.write("아이의 나이와 알레르기 정보를 반영해 메뉴를 추천하고 조리법을 보여줘요.")

with st.sidebar:
    st.header("우리 아이 설정")
    nickname = st.text_input("아이 별명", value="꼬마")
    age_label = st.selectbox("아이 나이", ["7~11개월", "12~23개월", "2~3세", "4세 이상"], index=2)
    age_map = {"7~11개월": 11, "12~23개월": 23, "2~3세": 47, "4세 이상": 100}
    age_months = age_map[age_label]
    allergies = st.multiselect("피해야 할 알레르기 성분", ALLERGENS)
    dislikes_text = st.text_input("싫어하는 식재료 (쉼표로 구분)", placeholder="예: 버섯, 브로콜리")
    dislikes = [x.strip() for x in dislikes_text.split(",") if x.strip()]
    include_snacks = st.checkbox("간식 포함", value=True)

safe = get_safe_recipes(allergies, age_months, dislikes)
if not safe:
    st.error("설정에 맞는 레시피가 없어요. 선택한 알레르기와 기피 재료를 확인해 주세요.")
    st.stop()

st.success("{}를 위한 추천 가능 메뉴 {}개".format(nickname, len(safe)))
today_key = date.today().isoformat()
if "refresh_count" not in st.session_state:
    st.session_state["refresh_count"] = 0
if st.button("🔄 다른 메뉴로 추천받기"):
    st.session_state["refresh_count"] += 1

seed = sum(ord(char) for char in today_key + nickname) + st.session_state["refresh_count"]
rng = random.Random(seed)
pool = list(safe)
rng.shuffle(pool)
meals = ["아침", "점심", "저녁"]
if include_snacks:
    meals.append("간식")
daily = []
for i, meal in enumerate(meals):
    daily.append((meal, pool[i % len(pool)]))

tab_today, tab_week, tab_recipes = st.tabs(["오늘의 식단", "7일 식단표", "레시피 모음"])

with tab_today:
    columns = st.columns(2)
    for index, item in enumerate(daily):
        meal, recipe = item
        with columns[index % len(columns)]:
            with st.container(border=True):
                st.markdown("#### " + meal)
                st.markdown("### " + recipe["name"])
                st.image(recipe["image"], use_container_width=True)
                st.caption("{}분 · {}".format(recipe["minutes"], recipe["category"]))
                if st.button("조리법 보기", key="recipe_" + meal):
                    st.session_state["chosen_recipe"] = recipe["name"]
    chosen = st.session_state.get("chosen_recipe")
    chosen_recipe = next((r for r in safe if r["name"] == chosen), None)
    if chosen_recipe:
        st.divider()
        show_recipe(chosen_recipe)

with tab_week:
    st.subheader("7일 식단표")
    week_rng = random.Random(seed + 77)
    for offset in range(7):
        current_day = date.today().fromordinal(date.today().toordinal() + offset)
        week_rng.shuffle(pool)
        with st.expander("{}월 {}일".format(current_day.month, current_day.day)):
            for i, meal in enumerate(meals):
                recipe = pool[(i + offset) % len(pool)]
                st.write("{}: {} ({}분)".format(meal, recipe["name"], recipe["minutes"]))
    shopping = []
    for recipe in safe:
        shopping.extend(recipe["ingredients"])
    shopping = list(dict.fromkeys(shopping))
    st.subheader("장보기 목록")
    for ingredient in shopping:
        st.checkbox(ingredient, key="shop_" + ingredient)
    text_list = "장보기 목록\n" + "\n".join("- " + ingredient for ingredient in shopping)
    st.download_button("장보기 목록 다운로드", text_list, file_name="장보기목록.txt", mime="text/plain")

with tab_recipes:
    st.subheader("레시피 모음")
    category = st.selectbox("종류 필터", ["전체"] + sorted(set(r["category"] for r in safe)))
    query = st.text_input("레시피 검색", placeholder="메뉴명 또는 재료")
    filtered = []
    for recipe in safe:
        if category != "전체" and recipe["category"] != category:
            continue
        searchable = recipe["name"] + " " + " ".join(recipe["ingredients"])
        if query.lower() not in searchable.lower():
            continue
        filtered.append(recipe)
    for recipe in filtered:
        with st.expander(recipe["name"]):
            show_recipe(recipe)

st.divider()
st.caption("주의: 이 앱은 식단 아이디어를 제공하며 알레르기 안전을 보장하지 않습니다. 식품 포장지의 원재료·알레르기 표시와 교차접촉 안내를 반드시 확인하고 의료진의 지침을 우선하세요.")
