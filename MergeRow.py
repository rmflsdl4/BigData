import pandas as pd



data = []
for i in range(1, 33):
    file_path=f'./CSV/data{i}.csv'
    storeName = pd.read_csv(file_path, encoding="CP949", usecols=['상호명'])
    data.append(storeName)


uniqueData = pd.concat(data, ignore_index=True)['상호명'].drop_duplicates()

# 음식점 상호명 로드
print(uniqueData)

uniqueData.to_csv('./CSV/bestStoreName.csv')