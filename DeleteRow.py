import pandas as pd

filePath = './CSV/accommodation.csv'

# 음식점 데이터 로드
data = pd.read_csv(filePath, encoding="CP949")
# 제거 전
print(len(data))
deleteAfterRow = data[data['좌표정보(x)'] == ''].index
reslut = data.drop(deleteAfterRow)
reslut.to_csv('./CSV/updateData.csv', encoding="CP949")
# 제거 후
print(len(reslut))