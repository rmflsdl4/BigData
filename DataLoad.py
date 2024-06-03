import pandas as pd
import folium

bakery_file_path='./CSV/bakery.csv'
recess_file_path='./CSV/recess.csv'
normal_file_path='./CSV/normal.csv'

bakery = pd.read_csv(bakery_file_path, encoding="CP949")
recess = pd.read_csv(recess_file_path, encoding="CP949")
#normal = pd.read_csv(normal_file_path, encoding="CP949")
totalData = pd.concat([bakery, recess])
print(totalData[['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', '좌표정보(x)', '좌표정보(y)', ]])

inuptAddress = input("주소 입력: ")

searchData = totalData[
    totalData['소재지전체주소'].isin(inuptAddress) |
    totalData['도로명전체주소'].isin(inuptAddress) |
    totalData['사업장명'].isin(inuptAddress)
]

print(searchData)



# 검색하 

# 위도, 경도
lat, lon = 37.504811111562, 127.025492036104
# 줌 크기
zoom_size = 20


map = folium.Map(location = [lat, lon], zoom_start=zoom_size)

map.save('map.html')
print(f"지도 저장에 성공했음")
#print(len(normal.info))