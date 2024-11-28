import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import numpy as np

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

# 'sum' 변수 확인 및 단계 생성
if 'gdf_grid' in locals():
    if 'sum' in gdf_grid.columns:
        # 5단계로 나누기
        gdf_grid['category'] = np.digitize(gdf_grid['sum'], bins=np.linspace(gdf_grid['sum'].min(), gdf_grid['sum'].max(), 6))
    else:
        st.error("The 'sum' column is missing in the grid shapefile.")

# 지도 생성
if 'gdf_daejeon' in locals() and 'gdf_grid' in locals():
    center = [gdf_daejeon.geometry.centroid.y.mean(), gdf_daejeon.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=10)

    # Daejeon Boundary 레이어 추가
    daejeon_layer = folium.FeatureGroup(name="Daejeon Boundary", show=True)
    folium.GeoJson(
        gdf_daejeon,
        style_function=lambda x: {
            "fillColor": "transparent",  # 내부 비우기
            "color": "blue",             # 경계선 파란색
            "weight": 4,                 # 경계선 두께
            "fillOpacity": 0,            # 내부 투명도
        },
    ).add_to(daejeon_layer)
    daejeon_layer.add_to(m)

    # 그라데이션 컬러맵 생성 (빨간색 계열)
    colormap = {
        1: "#ffcccc",  # Light red
        2: "#ff9999",  # Medium light red
        3: "#ff6666",  # Medium red
        4: "#ff3333",  # Medium dark red
        5: "#ff0000",  # Dark red
    }

    # One Person Grid 레이어 추가
    grid_layer = folium.FeatureGroup(name="One Person Grid", show=True)  # 기본 활성화
    folium.GeoJson(
        gdf_grid,
        style_function=lambda x: {
            "fillColor": colormap.get(x['properties']['category'], "transparent"),  # 단계에 따른 색상
            "color": "black",  # 경계선 검정색
            "weight": 1,       # 경계선 두께
            "fillOpacity": 0.7,  # 내부 투명도
        },
        tooltip=folium.GeoJsonTooltip(fields=['sum'], aliases=['Sum Value']),  # 툴팁에 'sum' 값 표시
    ).add_to(grid_layer)
    grid_layer.add_to(m)

    # 레이어 컨트롤 추가
    folium.LayerControl().add_to(m)

    # Streamlit에 지도 표시 (화면에 꽉 차게)
    st_folium(m, width=1200, height=800)  # 지도 크기를 크게 설정
