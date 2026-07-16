import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

st.title("🌌 FITS/FZ 파일 분석기")
st.write("FITS 또는 FZ 파일을 업로드하여 이미지와 헤더 정보를 확인하세요.")

# 파일 선택창 (fz, fits.fz 추가)
uploaded_file = st.file_uploader("FITS 파일 선택", type=["fits", "fit", "fz", "fits.fz"])

if uploaded_file is not None:
    try:
        with fits.open(uploaded_file) as hdul:
            # 1. 데이터가 있는 HDU를 자동으로 찾기
            data = None
            header = None
            
            for hdu in hdul:
                if hdu.data is not None:
                    data = hdu.data
                    header = hdu.header
                    break # 찾았으면 종료
            
            if data is None:
                st.error("이 파일에서 이미지 데이터를 찾을 수 없습니다.")
            else:
                st.subheader("📊 이미지 정보")
                st.write(f"- 이미지 크기: {data.shape}")
                st.write(f"- 노출 시간(EXPTIME): {header.get('EXPTIME', '정보 없음')} s")
                st.write(f"- 평균 밝기: {np.nanmean(data):.2f}")

                st.subheader("🖼️ 이미지 시각화")
                fig, ax = plt.subplots()
                # 밝기 정규화 (값이 튀는 것을 방지)
                norm_data = np.log1p(data - np.nanmin(data))
                ax.imshow(norm_data, cmap='gray', origin='lower')
                st.pyplot(fig)

                with st.expander("📄 전체 헤더 정보 보기"):
                    st.json(dict(header))

    except Exception as e:
        # 오류가 발생하면 친절하게 화면에 보여줍니다.
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
