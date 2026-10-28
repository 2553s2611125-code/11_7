        placeholder="예: 천안 불당동, 서울 마포구",
        help="시·구·동 또는 동네 이름을 입력해 주세요.",
    )
    c1, c2 = st.columns(2)
    with c1:
        food_type = st.selectbox(
            "먹고 싶은 음식",
            ["전체", "한식", "양식", "일식", "중식", "분식", "카페·브런치", "고기·구이"],
        )
        baby_age = st.selectbox(
            "아기 월령",
            ["선택 안 함", "0~5개월", "6~11개월", "12~23개월", "24개월 이상"],
            help="월령에 따라 필요한 식사 환경이 다를 수 있어요.",
        )
    with c2:
        occasion = st.selectbox(
            "오늘의 식사 상황",
            ["편안한 한 끼", "가족 외식", "빠른 식사", "브런치·카페"],
        )
        travel = st.selectbox(
            "이동 방식",
            ["상관없음", "유모차를 가져가요", "대중교통으로 이동해요", "주차가 필요해요"],
        )

    st.markdown("**있으면 좋은 편의시설**")
    f1, f2, f3 = st.columns(3)
    with f1:
        high_chair = st.checkbox("유아용 의자")
    with f2:
        baby_tableware = st.checkbox("아기 식기")
    with f3:
        stroller = st.checkbox("유모차 이용 편리")

    submitted = st.form_submit_button("우리 가족 식당 찾기", type="primary", use_container_width=True)

if submitted:
    if not location.strip():
        st.warning("먼저 지역을 입력해 주세요. 예: 천안 불당동")
    else:
        # 검색어를 명확하게 구성하고 URL 인코딩
        terms = [location.strip(), "아기 동반 가능 식당"]
        if food_type != "전체":
            terms.append(food_type)
        if high_chair:
            terms.append("유아용 의자")
        if baby_tableware:
            terms.append("아기 식기")
        if stroller:
            terms.append("유모차")
        if travel == "주차가 필요해요":
            terms.append("주차 가능")
        elif travel == "유모차를 가져가요":
            terms.append("유모차 접근 가능")
        elif travel == "대중교통으로 이동해요":
            terms.append("대중교통 접근")
        if occasion == "브런치·카페":
            terms.append("브런치 카페")
        elif occasion == "가족 외식":
            terms.append("가족 외식")
        elif occasion == "빠른 식사":
            terms.append("식사")
        search_query = " ".join(terms)
        encoded_query = quote_plus(search_query)
        map_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        naver_url = f"https://map.naver.com/p/search/{quote_plus(search_query)}"

        st.markdown("---")
        st.markdown('<div class="section-title">검색 결과로 이동하기</div>', unsafe_allow_html=True)
        st.write(f"**검색 조건:** {search_query}")
        st.info(
            "아래 링크에서 실제 식당과 최근 리뷰를 확인해 주세요. "
            "유아용 의자·아기 식기·유모차 이용 여부는 매장마다 다르므로 방문 전 전화로 확인하는 것이 좋아요."
        )
        b1, b2 = st.columns(2)
        with b1:
            st.link_button("🗺️ Google 지도에서 찾기", map_url, use_container_width=True)
        with b2:
            st.link_button("📍 네이버 지도에서 찾기", naver_url, use_container_width=True)

        st.markdown('<div class="section-title">방문 전 체크리스트</div>', unsafe_allow_html=True)
        checks = [
            "유아용 의자 또는 아기용 좌석이 있는지",
            "아기 식기와 물을 제공하는지",
            "유모차를 둘 공간과 출입구 턱이 있는지",
            "기저귀 교환 공간과 아기 동반 화장실이 있는지",
            "아기 식사 시간에 맞춰 대기 시간을 줄일 수 있는지",
        ]
        for item in checks:
            st.checkbox(item, key="check_" + item)

# 정적 도움말 영역
st.markdown("---")
st.markdown('<div class="section-title">우리끼니 사용 팁</div>', unsafe_allow_html=True)
cols = st.columns(3)
tips = [
    ("🪑", "자리부터 확인하기", "유아용 의자와 테이블 간격은 매장마다 다르니 예약 전 확인해요."),
    ("🥣", "아기 식사는 따로 확인하기", "월령에 맞는 음식과 알레르기 유발 식재료를 직원에게 문의해요."),
    ("🧸", "혼잡 시간 피하기", "가능하다면 식사 피크 시간대를 피해 여유롭게 방문해요."),
]
for col, (emoji, title, desc) in zip(cols, tips):
    with col:
        st.markdown(
            f'<div class="soft-card"><div style="font-size:1.6rem">{emoji}</div>'
            f'<div style="font-weight:800;color:#28382B;margin:8px 0">{title}</div>'
            f'<div style="color:#687064;font-size:.9rem;line-height:1.6">{desc}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <p class="note" style="text-align:center; margin-top:28px;">
    우리끼니는 식당 검색을 돕는 서비스예요. 편의시설·영업시간·아기 메뉴는 방문 전에 매장에 확인해 주세요.
    </p>
    """,
    unsafe_allow_html=True,
)
