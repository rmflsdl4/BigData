import pandas as pd
import folium
import pyproj
import random
import webbrowser
import os

# apiKey = "AIzaSyBBpOKSEwnCFu2M9fSdLSGEthLUwqrEkXo"
# map = googlemaps.Client(key = apiKey)
### 함수 정의 ###

def coordinateToFormat(x, y):
    p1_type = "epsg:5174"
    p2_type = "epsg:4326"
    transformer = pyproj.Transformer.from_crs(p1_type, p2_type, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat

def createMap(stores):
    # 위도, 경도
    lat, lon = stores.iloc[2]['lat'], stores.iloc[2]['lon']

    map = folium.Map([lat, lon], zoom_start = 16)
    randIdx = set()

    maxIdx = 4
    # 랜덤 인덱스
    while len(randIdx) < maxIdx:
        randIdx.add(random.randint(0, len(stores)-1))

    randIdx = list(randIdx)
    # 마커 아이콘
    for i in range(maxIdx):
        idx = randIdx[i]
        
        storeName = stores.iloc[idx]['사업장명']
        location = stores.iloc[idx]['도로명전체주소']
        popup = f"<div style='width: 200px'><span style='font-size: 17px'>{storeName}</span><br>{location}</div>"
        marker = folium.Marker([stores.iloc[idx]['lat'], stores.iloc[i]['lon']],
                                popup = popup,
                                icon = folium.Icon(color = 'blue')
                            )
        marker.add_to(map)
    map.save('map.html')
    print(f"지도 저장에 성공했습니다.")

def openMap():
    # 현재 작업 디렉토리 가져오기
    currentDir = os.getcwd()

    # 실행할 HTML 파일 경로
    mapPath = os.path.join(currentDir, 'map.html')

    # 웹 브라우저를 사용하여 HTML 파일 열기
    webbrowser.open(mapPath)


bakeryFilePath='./CSV/bakery.csv'
recessFilePath='./CSV/recess.csv'
normalFilePath='./CSV/normal.csv'

# 필요한 열들을 리스트로 묶음
initColumns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', '좌표정보(x)', '좌표정보(y)']
columns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', 'lon', 'lat']

# 음식점 데이터 로드
bakery = pd.read_csv(bakeryFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
recess = pd.read_csv(recessFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
normal = pd.read_csv(normalFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})


# 위 3개의 데이터를 합침
totalData = pd.concat([bakery, recess, normal])
print(totalData)
# 좌표계를 정수값으로 변환
totalData['좌표정보(x)'] = pd.to_numeric(totalData['좌표정보(x)'], errors="coerce")
totalData['좌표정보(y)'] = pd.to_numeric(totalData['좌표정보(y)'], errors="coerce")

totalData['lon'], totalData['lat'] = coordinateToFormat(totalData['좌표정보(x)'].values, totalData['좌표정보(y)'].values)



inuptAddress = input("주소 입력: ")

# 사용자가 입력한 데이터와 totlaDf 값과 동일한 값들 searchData에 저장
searchData = totalData.loc[
                        totalData['소재지전체주소'].str.contains(inuptAddress) |
                        totalData['도로명전체주소'].str.contains(inuptAddress) |
                        totalData['사업장명'].str.contains(inuptAddress)
                    ] 
stores = searchData[['도로명전체주소','사업장명', 'lon', 'lat']]


# 요청 보내기
print("검색된 가게 목록: ", len(stores))

# 지도 생성
createMap(stores)


# 만들어진 지도를 실행
openMap()
