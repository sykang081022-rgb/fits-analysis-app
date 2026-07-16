import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 앱 설정
st.set_page_config(page_title="천문 데이터 분석기", layout="wide")
st.title("🌌 천문 데이터 분석기 (FITS/FZ)")
st.write("FITS 파일을 업로드하여 관측 데이터를 분석하고 이미지를 시각화합니다.")

# 2. 파일 업로더
uploaded_file = st.file_uploader("FITS 또는 FZ 파일을 선택하세요", type=["fits", "fit", "fz", "fits.fz"])

if uploaded_file is not None:
    try:
        # 파일 열기
        with fits.open(uploaded_file) as hdul:
            # 이미지 데이터가 있는 HDU 찾기
            data = None
            header = None
            for hdu in hdul:
                if hdu.data is not None:
                    data = hdu.data
                    header = hdu.header
                    break
            
            if data is None:
                st.error("이미지 데이터를 찾을 수 없습니다. 파일 형식을 확인해주세요.")
            else:
                # 화면을 둘로 나누기 (왼쪽: 시각화, 오른쪽: 데이터 시트)
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("🖼️ 이미지 시각화")
                    # 이미지 밝기 조절을 위한 로그 변환 (데이터가 튀는 현상 방지)
                    norm_data = np.log1p(data - np.nanmin(data))
                    
                    fig, ax = plt.subplots(figsize=(8, 8))
                    im = ax.imshow(norm_data, cmap='magma', origin='lower')
                    plt.colorbar(im, ax=ax)
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("📋 관측 데이터 시트")
                    # 핵심 헤더 정보 추출
                    info_keys = {
                        "OBJECT": "관측 대상",
                        "DATE-OBS": "관측 일시",
                        "EXPTIME": "노출 시간 (s)",
                        "FILTER": "관측 필터",
                        "TELESCOP": "망원경",
                        "INSTRUME": "관측 기기",
                        "OBSERVER": "관측자",
                        "RA": "적경 (RA)",
                        "DEC": "적위 (Dec)"
                    }
                    
                    data_list = []
                    for key, desc in info_keys.items():
                        val = header.get(key, "정보 없음")
                        data_list.append({"항목": desc, "값": val})
                    
                    df = pd.DataFrame(data_list)
                    st.table(df)

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("분석할 FITS 파일을 업로드해 주세요.")
