import streamlit as st
import geopandas as gpd
import pydeck as pdk

# Streamlit 페이지 제목
st.title("대전시 행정경계선 시각화")

# 데이터 로드
shapefile_path = "daejeon.shp"  # 경로를 수정하세요
gdf = gpd.read_file(shapefile_path)

# 좌표계 변환 (EPSG:4326)
gdf = gdf.to_crs(epsg=4326)

# GeoJSON 형식으로 변환
geojson = gdf.to_json()

# Pydeck Layer 설정
layer = pdk.Layer(
    "GeoJsonLayer",
    geojson,
    pickable=True,
    stroked=True,
    filled=True,
    get_fill_color="[255, 0, 0, 100]",  # 빨간색 투명 채우기
    get_line_color="[0, 0, 0, 200]",    # 검정색 테두리
    line_width_min_pixels=1,
)

# Pydeck View 설정
view_state = pdk.ViewState(
    latitude=gdf.geometry.centroid.y.mean(),
    longitude=gdf.geometry.centroid.x.mean(),
    zoom=10,
    pitch=0,
)

# Streamlit에 지도 렌더링
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
