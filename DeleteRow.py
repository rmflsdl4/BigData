import pandas as pd

accommodationFilePath = './CSV/accommodation2.csv'

# 음식점 데이터 로드
data = pd.read_csv(accommodationFilePath, encoding="CP949", dtype={'좌표정보(x)': float, '좌표정보(y)': float})
print(len(data))
deleteAfterRow = data[data['좌표정보(x)'] == ''].index
reslut = data.drop(deleteAfterRow)
reslut.to_csv('./CSV/updateData.csv', encoding="CP949")
print(len(reslut))