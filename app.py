import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

st.title("🌌 FITS 파일 분석기")
st.write("FITS 파일을 업로드하여 이미지와 헤더 정보를 확인하세요.")

uploaded_file = st.file_uploader("FITS 파일 선택", type=["fits", "fit"])

if uploaded_file is not None:
    try:
        with fits.open(uploaded_file) as hdul:
            header = hdul[0].header
            data = hdul[0].data

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
