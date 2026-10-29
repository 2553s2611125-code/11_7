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
