import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# GitHub에서 shapefile 경로 설정
SHAPEFILE_URL_DAEJEON = "https://raw.githubusercontent.com/cdshadow/daejeon/main/daejeon.shp"
SHAPEFILE_URL_GRID = "https://raw.githubusercontent.com/cdshadow/daejeon/main/one_person_grid.shp"

# Streamlit 페이지 설정
st.set_page_config(page_title="Daejeon Map", layout="wide")

st.title("Daejeon Administrative Boundary and Grid (WGS84)")

@st.cache_data
def load_and_transform_shapefile(url):
    # Shapefile 데이터 로드
    gdf = gpd.read_file(url)
    st.write("Original CRS:", gdf.crs)
    
    # 좌표계를 EPSG:4326으로 변환
    gdf = gdf.to_crs(epsg=4326)
    st.write("Transformed CRS:", gdf.crs)
    
    return gdf

# Shapefile 데이터 읽기 및 변환
try:
    gdf_daejeon = load_and_transform_shapefile(SHAPEFILE_URL_DAEJEON)
    gdf_grid = load_and_transform_shapefile(SHAPEFILE_URL_GRID)
    st.write("Shapefiles loaded and transformed successfully!")
except Exception as e:
    st.error(f"Failed to load or transform shapefiles: {e}")

# 지도 생성
if 'gdf_daejeon' in locals() and 'gdf_grid' in locals():
    center = [gdf_daejeon.geometry.centroid.y.mean(), gdf_daejeon.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=10)

    # Daejeon Boundary GeoDataFrame을 지도에 추가
    folium.GeoJson(
        gdf_daejeon,
        name="Daejeon Boundary",
        style_function=lambda x: {
            "fillColor": "transparent",  # 내부 비우기
            "color": "blue",             # 경계선 파란색
            "weight": 4,                 # 경계선 두께
            "fillOpacity": 0,            # 내부 투명도
        },
    ).add_to(m)

    # One Person Grid GeoDataFrame을 지도에 추가
    folium.GeoJson(
        gdf_grid,
        name="One Person Grid",
        style_function=lambda x: {
            "fillColor": "yellow",       # 내부 노란색
            "color": "red",              # 경계선 빨간색
            "weight": 2,                 # 경계선 두께
            "fillOpacity": 0.3,          # 내부 투명도
        },
    ).add_to(m)

    # Streamlit에 지도 표시
    st_folium(m, width=700, height=500)
