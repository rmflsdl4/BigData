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
    lat, lon = stores[0]['lat'], stores[0]['lon']

    map = folium.Map([lat, lon], zoom_start = 18)
    maxIdx = len(stores)

    # 마커 아이콘
    for i in range(maxIdx):
        
        storeName = stores[i]['사업장명']
        location = stores[i]['도로명전체주소']
        query = f"{stores[i]['소재지전체주소']} {storeName}"
        popup = f"<div style='width:300px; text-align: center;'><span style='font-size: 17px'>{storeName}</span><br>{location}<br><a href='https://www.google.com/search?q={query}'>세부 정보</div>"
        
        # 업태구분명 아이콘 설정
        if stores[i]['업태구분명'] == '기타' or stores[i]['업태구분명'] == '커피숍':
            iconColor = 'red'
            iconType = 'time'
        elif i == 0:
            iconColor = 'lightblue'
            iconType = 'home'
        else:
            iconColor = 'orange'
            iconType = 'cutlery'

        marker = folium.Marker([stores[i]['lat'], stores[i]['lon']],
                                popup = popup,
                                icon = folium.Icon(color=iconColor, icon=iconType)
                            )
        marker.add_to(map)

    # 선으로 마커들 연결
    points = [[stores[i]['lat'], stores[i]['lon']] for i in range(maxIdx)]
    folium.PolyLine(points, color="#5faaf5", weight=8, opacity=1).add_to(map)

    map.save('map.html')
    print(f"지도 저장에 성공했습니다.")

def openMap():
    # 현재 작업 디렉토리 가져오기
    currentDir = os.getcwd()

    # 실행할 HTML 파일 경로
    mapPath = os.path.join(currentDir, 'map.html')

    # 웹 브라우저를 사용하여 HTML 파일 열기
    webbrowser.open(mapPath)

def createRoutine(stores, accommodation, bestStoreName):
    routine = []
    

    # 랜덤 숙소 선정
    routine.append(accommodation.iloc[random.randint(0, len(accommodation)-1)])

    filteredBreakfast = stores[(stores['업태구분명'] != '기타') & (stores['업태구분명'] != '호프/통닭') & (stores['업태구분명'] != '커피숍')]
    filteredLunch = stores[(stores['업태구분명'] != '기타') & (stores['업태구분명'] != '호프/통닭') & (stores['업태구분명'] != '커피숍')]
    filteredEtc = stores[(stores['업태구분명'] == '기타') | (stores['업태구분명'] == '커피숍')]
    filteredDinner = stores[stores['업태구분명'] != '기타']

    # 맛집이 존재할 경우에는 맛집 중 랜덤 추가, 없으면 전체 음식점 중 랜덤 추가

    ## 아침 식사
    breakfastBest = filteredBreakfast[filteredBreakfast['사업장명'].isin(bestStoreName['상호명'])]     
    
    if breakfastBest.empty:
        routine.append(filteredBreakfast.iloc[random.randint(0, len(filteredBreakfast)-1)])
    else:
        routine.append(breakfastBest.iloc[random.randint(0, len(breakfastBest)-1)])    

    ## 점심 식사
    lunchBest = filteredLunch[filteredLunch['사업장명'].isin(bestStoreName['상호명'])]     
    
    if lunchBest.empty:
        routine.append(filteredLunch.iloc[random.randint(0, len(filteredLunch)-1)])
    else:
        routine.append(lunchBest.iloc[random.randint(0, len(lunchBest)-1)])  

    ## 식후
    etcBest = filteredEtc[filteredEtc['사업장명'].isin(bestStoreName['상호명'])]     
    
    if etcBest.empty:
        routine.append(filteredEtc.iloc[random.randint(0, len(filteredEtc)-1)])
    else:
        routine.append(etcBest.iloc[random.randint(0, len(etcBest)-1)])  
        
    ## 저녁 식사
    dinnerBest = filteredDinner[filteredDinner['사업장명'].isin(bestStoreName['상호명'])]     
    
    if dinnerBest.empty:
        routine.append(filteredDinner.iloc[random.randint(0, len(filteredDinner)-1)])
    else:
        routine.append(dinnerBest.iloc[random.randint(0, len(dinnerBest)-1)])  


    print(f"숙소: {routine[1]['사업장명']}")
    print(f"아침: {routine[1]['사업장명']} , {routine[1]['업태구분명']}")
    print(f"점심: {routine[2]['사업장명']} , {routine[2]['업태구분명']}")
    print(f"식후: {routine[3]['사업장명']} , {routine[3]['업태구분명']}")
    print(f"저녁: {routine[4]['사업장명']} , {routine[4]['업태구분명']}")
    
    return routine

    

bakeryFilePath='./CSV/bakery.csv'
recessFilePath='./CSV/recess.csv'
normalFilePath='./CSV/normal.csv'
accommodationFilePath='./CSV/accommodation.csv'
bestStoreNamePath='./CSV/bestStoreName.csv'

# 필요한 열들을 리스트로 묶음
initColumns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', '업태구분명', '좌표정보(x)', '좌표정보(y)']
accommodationColumns = ['소재지전체주소', '도로명전체주소', '사업장명', '좌표정보(x)', '좌표정보(y)']
columns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', 'lon', 'lat']

# 음식점 데이터 로드
bakery = pd.read_csv(bakeryFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
recess = pd.read_csv(recessFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
normal = pd.read_csv(normalFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
accommodation = pd.read_csv(accommodationFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
bestStoreName = pd.read_csv(bestStoreNamePath, usecols=['상호명'])


# 위 3개의 데이터를 합침
totalData = pd.concat([bakery, recess, normal])
print(totalData)

# x, y 좌표를 위도, 경도로 수정
totalData['lon'], totalData['lat'] = coordinateToFormat(totalData['좌표정보(x)'].values, totalData['좌표정보(y)'].values)
accommodation['lon'], accommodation['lat'] = coordinateToFormat(accommodation['좌표정보(x)'].values, accommodation['좌표정보(y)'].values)



inuptAddress = input("주소 입력: ")

# 사용자가 입력한 데이터와 totlaDf 값과 동일한 값들 searchData에 저장
searchData = totalData.loc[
                        totalData['소재지전체주소'].str.contains(inuptAddress) |
                        totalData['도로명전체주소'].str.contains(inuptAddress) |
                        totalData['사업장명'].str.contains(inuptAddress)
                    ] 
filterAccommodation = accommodation.loc[
                        accommodation['소재지전체주소'].str.contains(inuptAddress) |
                        accommodation['도로명전체주소'].str.contains(inuptAddress) 
                    ] 
stores = searchData[['도로명전체주소','사업장명', 'lon', 'lat', '업태구분명', '소재지전체주소']]

# 요청 보내기
print("검색된 가게 목록: ", len(stores))

# 아침 - 점심 - 식후 - 저녁 - 랜덤하게 영화관 등의 장소
routine = createRoutine(stores, filterAccommodation, bestStoreName)
# 지도 생성
createMap(routine)


# 만들어진 지도를 실행
openMap()
