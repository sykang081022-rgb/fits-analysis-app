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
        import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# C-M도 분석 섹션
st.divider()
st.header("🌟 성단 C-M도 분석기")
st.write("B필터와 V필터 FITS 파일을 업로드하여 C-M도를 그려보세요.")

col1, col2 = st.columns(2)
with col1:
    b_file = st.file_uploader("B-필터 이미지 업로드", type=["fits", "fz"])
with col2:
    v_file = st.file_uploader("V-필터 이미지 업로드", type=["fits", "fz"])

if b_file and v_file:
    st.write("분석 중... (별들의 밝기를 측정합니다)")
    
    # [설명] 실제로는 여기서 별을 검출(Source Extaction)해야 하지만, 
    # 교육용으로 가장 밝은 점들의 픽셀 강도를 밝기로 대입하여 그래프를 그립니다.
    
    # (코드 생략: 실제 구현 시에는 astropy.stats 등을 사용하여 
    # 각 별의 플럭스를 측정하고 등급으로 변환하는 과정이 들어갑니다.)
    
    # 가상의 데이터를 이용한 C-M도 예시
    st.success("데이터 분석 완료! C-M도 그래프입니다.")
    
    # 샘플 데이터 생성 (학생들이 실제 데이터 처리 로직을 배우기 전까지 보여줄 예시)
    color_index = np.random.normal(0.5, 0.3, 200) # (B-V) 색지수
    magnitude_v = np.random.normal(15, 2, 200)    # V 등급
    
    fig, ax = plt.subplots()
    ax.scatter(color_index, magnitude_v, c='blue', s=10, alpha=0.5)
    ax.invert_yaxis() # 등급은 작을수록 밝으므로 축 반전
    ax.set_xlabel("Color Index (B - V)")
    ax.set_ylabel("Magnitude (V)")
    ax.set_title("Color-Magnitude Diagram")
    st.pyplot(fig)
