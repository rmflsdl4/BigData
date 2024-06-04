import pandas as pd
import folium
import numpy as np
import pyproj

### 함수 정의 ###

def coordinateToFormat(x, y):
    p1_type = "epsg:5174"
    p2_type = "epsg:4326"
    transformer = pyproj.Transformer.from_crs(p1_type, p2_type, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat


bakery_file_path='./CSV/bakery.csv'
recess_file_path='./CSV/recess.csv'
normal_file_path='./CSV/normal.csv'

# 음식점 데이터 로드
bakery = pd.read_csv(bakery_file_path, encoding="CP949")
recess = pd.read_csv(recess_file_path, encoding="CP949")
normal = pd.read_csv(normal_file_path, encoding="CP949")

# 위 3개의 데이터를 합침
totalData = pd.concat([bakery, recess, normal])

# 좌표계를 정수값으로 변환
totalData['좌표정보(x)'] = pd.to_numeric(totalData['좌표정보(x)'], errors="coerce")
totalData['좌표정보(y)'] = pd.to_numeric(totalData['좌표정보(y)'], errors="coerce")

totalData['lon'], totalData['lat'] = coordinateToFormat(totalData['좌표정보(x)'].values, totalData['좌표정보(y)'].values)

# 필요한 열들을 리스트로 묶음
columns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', 'lon', 'lat']

# 위 colmun으로 totalData에 대한 데이터프레임 생성
totalDf = totalData.loc[totalData['영업상태명'] == '영업/정상', columns]

inuptAddress = input("주소 입력: ")


# 사용자가 입력한 데이터와 totlaDf 값과 동일한 값들 searchData에 저장
searchData = totalDf.loc[
                        totalDf['소재지전체주소'].str.contains(inuptAddress) |
                        totalDf['도로명전체주소'].str.contains(inuptAddress) |
                        totalDf['사업장명'].str.contains(inuptAddress)
                    ] 

storeLocation = searchData[['사업장명', 'lon', 'lat']]
print("검색된 가게 목록: ", len(storeLocation))
print(storeLocation)

idx = int(input("원하는 번호 입력: "))

print("선택한 가게 정보")
print(storeLocation.iloc[idx])

# 위도, 경도
lat, lon = storeLocation.iloc[idx]['lat'], storeLocation.iloc[idx]['lon']

# 줌 크기
zoom_size = 20

storeName = storeLocation.iloc[idx]['사업장명']

print(storeName)
map = folium.Map([lat, lon], zoom_start = zoom_size)
marker = folium.Marker([lat, lon],
                       popup = storeName,
                       icon = folium.Icon(color = 'blue'))

marker.add_to(map)

map.save('map.html')
print(f"지도 저장에 성공했음")
#print(len(normal.info))