import streamlit as st
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 페이지 및 레이아웃 설정
st.set_page_config(page_title="천문 데이터 분석기", layout="wide")
st.title("🌌 천문 데이터 분석기 (FITS/FZ)")
st.write("FITS 또는 FZ 파일을 업로드하여 관측 데이터를 분석하고 이미지를 시각화합니다.")

# 2. 파일 업로더 (fz 포함)
uploaded_file = st.file_uploader("FITS 또는 FZ 파일을 선택하세요", type=["fits", "fit", "fz", "fits.fz"])

if uploaded_file is not None:
    try:
        # 파일 열기 (try-except로 오류 방지)
        with fits.open(uploaded_file) as hdul:
            # 이미지 데이터가 있는 HDU 자동 탐색
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
                # 화면 레이아웃 (왼쪽: 이미지, 오른쪽: 데이터시트)
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("🖼️ 이미지 시각화")
                    # 이미지 밝기 정규화 (로그 스케일 변환)
                    # 데이터가 0보다 작을 수 있는 경우를 대비해 처리
                    safe_data = data - np.nanmin(data)
                    norm_data = np.log1p(safe_data)
                    
                    fig, ax = plt.subplots(figsize=(8, 8))
                    im = ax.imshow(norm_data, cmap='magma', origin='lower')
                    plt.colorbar(im, ax=ax)
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("📋 관측 데이터 시트")
                    # 단위가 포함된 핵심 헤더 정보 정의
                    info_keys = {
                        "OBJECT": "관측 대상",
                        "DATE-OBS": "관측 일시 (UTC)",
                        "EXPTIME": "노출 시간 (초)",
                        "FILTER": "관측 필터",
                        "TELESCOP": "망원경",
                        "INSTRUME": "관측 기기",
                        "OBSERVER": "관측자",
                        "RA": "적경 (degree)",
                        "DEC": "적위 (degree)"
                    }
                    
                    data_list = []
                    for key, desc in info_keys.items():
                        val = header.get(key, "정보 없음")
                        data_list.append({"항목": desc, "값": val})
                    
                    # 표로 출력 (Pandas DataFrame 사용)
                    df = pd.DataFrame(data_list)
                    st.table(df)

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("분석할 FITS 파일을 업로드해 주세요.")
