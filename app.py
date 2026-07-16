import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

st.title("🌌 FITS 파일 분석기") 
st.write("FITS 파일을 업로드하여 이미지와 헤더 정보를 확인하세요.")

uploaded_file = st.file_uploader("FITS 파일 선택", type=["fits", "fit", "fz", "fits.fz"])

if uploaded_file is not None:
    try:
        with fits.open(uploaded_file) as hdul:
            header = hdul[0].header
            # 기존의 hdul[0].data 부분을 아래 코드로 교체하세요
with fits.open(uploaded_file) as hdul:
    # 1. 데이터가 있는 HDU를 자동으로 찾기
    data = None
    header = None
    
    for hdu in hdul:
        if hdu.data is not None:
            data = hdu.data
            header = hdu.header
            break # 데이터가 있는 곳을 찾으면 멈춤

    if data is None:
        st.error("이 파일에서 이미지 데이터를 찾을 수 없습니다.")
    else:
        # 이제 아래에 시각화 로직을 그대로 사용하면 됩니다
        st.subheader("📊 이미지 정보")
        st.write(f"- 이미지 크기: {data.shape}")
        # ... (나머지 코드 생략)

            st.subheader("📊 이미지 정보")
            st.write(f"- 이미지 크기: {data.shape}")
            st.write(f"- 노출 시간(EXPTIME): {header.get('EXPTIME', '정보 없음')} s")
            st.write(f"- 평균 밝기: {np.nanmean(data):.2f}")

            st.subheader("🖼️ 이미지 시각화")
            fig, ax = plt.subplots()
            norm_data = np.log1p(data - np.nanmin(data))
            ax.imshow(norm_data, cmap='gray', origin='lower')
            st.pyplot(fig)

            with st.expander("📄 전체 헤더 정보 보기"):
                st.json(dict(header))
    except Exception as e:
        st.error(f"오류 발생: {e}")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌟 성단 C-M도 분석기")

# 1. 파일 두 개 받기
b_file = st.file_uploader("B-필터 FITS 업로드", type=["fits"])
v_file = st.file_uploader("V-필터 FITS 업로드", type=["fits"])

if b_file and v_file:
    # 2. 데이터 처리 (예시: 실제로는 여기서 별 밝기를 계산해야 함)
    # 단순화를 위해 무작위 데이터를 생성합니다.
    st.write("분석 중...")
    color_index = np.random.normal(0.5, 0.3, 100) # (B-V) 값
    magnitude = np.random.normal(15, 2, 100)       # V 등급
    
    # 3. 그래프 그리기
    fig, ax = plt.subplots()
    ax.scatter(color_index, magnitude, alpha=0.6)
    ax.invert_yaxis() # 등급은 숫자가 작을수록 밝으므로 반전
    ax.set_xlabel("Color Index (B-V)")
    ax.set_ylabel("Magnitude (V)")
    ax.set_title("Color-Magnitude Diagram")
    
    st.pyplot(fig)
