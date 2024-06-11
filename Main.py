from flask import Flask, request, render_template
import pandas as pd
import folium
import pyproj
import random
import os
from geopy.distance import geodesic

app = Flask(__name__, template_folder='templates')

def coordinateToFormat(x, y):
    p1_type = "epsg:5174"
    p2_type = "epsg:4326"
    transformer = pyproj.Transformer.from_crs(p1_type, p2_type, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat

def createMap(stores):
    lat, lon = stores[0]['lat'], stores[0]['lon']
    map = folium.Map([lat, lon], zoom_start=14)
    maxIdx = len(stores)
    for i in range(maxIdx):
        storeName = stores[i]['사업장명']
        location = stores[i]['도로명전체주소']
        query = f"{stores[i]['도로명전체주소']} {storeName}"
        kind = stores[i]['업태구분명']
        popup = f"""<div style='width:300px; text-align: center;'>
                        <span style='font-size: 17px'>{storeName}</span> ({kind})
                        <br>
                        {location}
                        <br>
                        <a href='https://www.google.com/search?q={query}'>세부 정보
                    </div>"""
        if stores[i]['업태구분명'] == '기타' or stores[i]['업태구분명'] == '커피숍':
            iconColor = 'orange'
            iconType = 'time'
        elif i == 0:
            iconColor = 'lightblue'
            iconType = 'home'
        else:
            iconColor = 'lightgreen'
            iconType = 'cutlery'
        marker = folium.Marker([stores[i]['lat'], stores[i]['lon']], popup=popup, icon=folium.Icon(color=iconColor, icon=iconType))
        marker.add_to(map)
    points = [[stores[i]['lat'], stores[i]['lon']] for i in range(maxIdx)]
    folium.PolyLine(points, color="#888888", weight=8, opacity=1).add_to(map)
    map.save('static/map.html')

def createRoutine(stores, accommodation, bestStoreName):
    def storeWithin5km(store):
        location = (store['lat'], store['lon']) 
        return geodesic(accommodationLocation, location).km <= 5
    
    routine = []

    routine.append(accommodation.iloc[random.randint(0, len(accommodation)-1)])

    accommodationLocation = (routine[0]['lat'], routine[0]['lon'])
    accommodation = accommodation.dropna(subset = ['lat', 'lon'])
    stores = stores.dropna(subset = ['lat', 'lon'])
    storesWithin5km = stores.dropna(subset=['lat', 'lon'])[stores.apply(storeWithin5km, axis=1)]

    filteredBreakfast = storesWithin5km[(storesWithin5km['업태구분명'] != '기타') & (storesWithin5km['업태구분명'] != '호프/통닭') & (storesWithin5km['업태구분명'] != '커피숍')]
    filteredLunch = storesWithin5km[(storesWithin5km['업태구분명'] != '기타') & (storesWithin5km['업태구분명'] != '호프/통닭') & (storesWithin5km['업태구분명'] != '커피숍')]
    filteredEtc = storesWithin5km[(storesWithin5km['업태구분명'] == '기타') | (storesWithin5km['업태구분명'] == '커피숍')]
    filteredDinner = storesWithin5km[storesWithin5km['업태구분명'] != '기타']
    breakfastBest = filteredBreakfast[filteredBreakfast['사업장명'].isin(bestStoreName['상호명'])] 

    if breakfastBest.empty:
        routine.append(filteredBreakfast.iloc[random.randint(0, len(filteredBreakfast)-1)])
    else:
        routine.append(breakfastBest.iloc[random.randint(0, len(breakfastBest)-1)])  

    lunchBest = filteredLunch[filteredLunch['사업장명'].isin(bestStoreName['상호명'])]   

    if lunchBest.empty:
        routine.append(filteredLunch.iloc[random.randint(0, len(filteredLunch)-1)])
    else:
        routine.append(lunchBest.iloc[random.randint(0, len(lunchBest)-1)])  

    etcBest = filteredEtc[filteredEtc['사업장명'].isin(bestStoreName['상호명'])]     

    if etcBest.empty:
        routine.append(filteredEtc.iloc[random.randint(0, len(filteredEtc)-1)])
    else:
        routine.append(etcBest.iloc[random.randint(0, len(etcBest)-1)])  

    dinnerBest = filteredDinner[filteredDinner['사업장명'].isin(bestStoreName['상호명'])]    

    if dinnerBest.empty:
        routine.append(filteredDinner.iloc[random.randint(0, len(filteredDinner)-1)])
    else:
        routine.append(dinnerBest.iloc[random.randint(0, len(dinnerBest)-1)])  

    return routine

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        inuptAddress = request.form['address']

        bakeryFilePath = './CSV/bakery.csv'
        recessFilePath = './CSV/recess.csv'
        normalFilePath = './CSV/normal.csv'
        accommodationFilePath = './CSV/accommodation.csv'
        bestStoreNamePath = './CSV/bestStoreName.csv'

        initColumns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', '업태구분명', '좌표정보(x)', '좌표정보(y)']
        columns = ['소재지전체주소', '도로명전체주소', '도로명우편번호', '사업장명', 'lon', 'lat']

        bakery = pd.read_csv(bakeryFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
        recess = pd.read_csv(recessFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
        normal = pd.read_csv(normalFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
        accommodation = pd.read_csv(accommodationFilePath, encoding="CP949", usecols=initColumns, dtype={'좌표정보(x)': float, '좌표정보(y)': float})
        bestStoreName = pd.read_csv(bestStoreNamePath, usecols=['상호명'])

        totalData = pd.concat([bakery, recess, normal])

        totalData['lon'], totalData['lat'] = coordinateToFormat(totalData['좌표정보(x)'].values, totalData['좌표정보(y)'].values)
        accommodation['lon'], accommodation['lat'] = coordinateToFormat(accommodation['좌표정보(x)'].values, accommodation['좌표정보(y)'].values)

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

        routine = createRoutine(stores, filterAccommodation, bestStoreName)

        createMap(routine)
        
        result = routine
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
