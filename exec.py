import streamlit as st

# 앱 제목 설정
st.title("✨ 나의 자기소개 앱")
st.write("이름, 직업, 취미를 입력하고 멋진 자기소개 카드를 만들어보세요!")

# 구분선
st.markdown("---")

# 사용자 입력 받기
name = st.text_input("이름을 입력해주세요", placeholder="예: 홍길동")
job = st.text_input("직업을 입력해주세요", placeholder="예: 데이터 분석가")
hobby = st.text_input("취미를 입력해주세요", placeholder="예: 등산, 영화 감상")

# 여백 생성
st.write("")

# '소개 보기' 버튼 생성
if st.button("소개 보기", type="primary"):
    # 입력값이 모두 채워져 있는지 확인
    if name and job and hobby:
        st.success("자기소개가 완성되었습니다! 🎉")
        
        # 깔끔하게 출력
        introduction = f"저는 {job}으로 일하는 {name}입니다. 취미는 {hobby}예요."
        
        # 시각적으로 돋보이게 박스 형태(markdown)로 출력
        st.markdown(
            f"""
            > ### 📝 자기소개 카드
            > **{introduction}**
            """,
            unsafe_allow_html=True
        )
    else:
        # 입력되지 않은 항목이 있을 경우 경고 메시지 출력
        st.warning("이름, 직업, 취미를 모두 입력해주세요!")
        