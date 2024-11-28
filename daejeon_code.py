import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# GitHub에서 shapefile 경로 설정
SHAPEFILE_URL = "https://raw.githubusercontent.com/cdshadow/daejeon/main/daejeon.shp"

# Streamlit 페이지 설정
st.set_page_config(page_title="Daejeon Map", layout="wide")

st.title("Daejeon Administrative Boundary")

@st.cache_data
def load_shapefile(url):
    # Shapefile 데이터 로드
    gdf = gpd.read_file(url)
    return gdf

# Shapefile 데이터 읽기
try:
    gdf = load_shapefile(SHAPEFILE_URL)
    st.write("Shapefile loaded successfully!")
except Exception as e:
    st.error(f"Failed to load shapefile: {e}")

# 지도 생성
if 'gdf' in locals():
    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=12)

    # GeoDataFrame을 folium으로 추가
    folium.GeoJson(
        gdf,
        name="Daejeon Boundary",
        style_function=lambda x: {
            "fillColor": "blue",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.4,
        },
    ).add_to(m)

    # Streamlit에 지도 표시
    st_folium(m, width=700, height=500)
