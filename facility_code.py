import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 데이터 경로
file_paths = {
    "헬스장": 'https://raw.githubusercontent.com/cdshadow/facility/main/health.shp',
    "필라테스/요가": 'https://raw.githubusercontent.com/cdshadow/facility/main/philites_yoga.shp',
    "수영장": 'https://raw.githubusercontent.com/cdshadow/facility/main/swim.shp',
    "댄스학원": 'https://raw.githubusercontent.com/cdshadow/facility/main/dance_academy.shp',
    "1인 시설": 'https://raw.githubusercontent.com/cdshadow/facility/main/one_person.shp',
    "대전 경계선": 'https://raw.githubusercontent.com/cdshadow/facility/main/daejeon_line.shp',
}

# 마커 색상 설정
marker_colors = {
    "헬스장": "red",
    "필라테스/요가": "green",
    "수영장": "blue",
    "댄스학원": "purple",
    "1인 시설": "orange",
}

# Streamlit 설정
st.set_page_config(layout="wide")

# Folium 지도 생성 함수
def create_map():
    # Folium 지도 설정 (대전광역시 중심)
    map_obj = folium.Map(
        location=[36.3504, 127.3845],
        zoom_start=12,  # 줌 레벨 조정
    )

    # 파일 추가
    for name, path in file_paths.items():
        try:
            if path.endswith('.shp'):
                # 쉐이프파일 처리
                gdf = gpd.read_file(path)
                gdf = gdf.to_crs(epsg=4326)  # 좌표계 변환

                # 포인트 데이터 처리
                if gdf.geom_type.iloc[0] == 'Point':
                    feature_group = folium.FeatureGroup(name=name)

                    for _, row in gdf.iterrows():
                        folium.CircleMarker(
                            location=[row.geometry.y, row.geometry.x],
                            radius=6,  # 마커 크기 설정
                            color=marker_colors.get(name, "gray"),  # 테두리 색상
                            fill=True,  # 내부 채우기 활성화
                            fill_color=marker_colors.get(name, "gray"),  # 내부 색상
                            fill_opacity=0.7,  # 투명도 설정
                            popup=row.get("상호명", "정보 없음"),  # 상호명 표시
                        ).add_to(feature_group)

                    feature_group.add_to(map_obj)

                # 라인 데이터 처리
                elif gdf.geom_type.iloc[0] == 'LineString' or gdf.geom_type.iloc[0] == 'MultiLineString':
                    folium.GeoJson(
                        gdf,
                        name=name,
                        style_function=lambda x: {
                            "color": "black",  # 라인 색상
                            "weight": 2,  # 라인 두께
                            "opacity": 0.8,  # 투명도
                        },
                    ).add_to(map_obj)
            else:
                st.error(f"지원되지 않는 파일 형식입니다: {path}")
        except Exception as e:
            st.error(f"{name} 데이터를 불러오는 중 오류가 발생했습니다: {e}")

    # 레이어 컨트롤 추가
    folium.LayerControl(position='topleft').add_to(map_obj)

    return map_obj

# Streamlit 레이아웃 설정
st.title('대전광역시 소규모체육시설 지도')

# 지도 생성 및 출력
map_display = create_map()
st_folium(map_display, width=1200, height=700)
