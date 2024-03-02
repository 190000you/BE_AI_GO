import pandas as pd

# CSV 파일을 읽어옵니다.
file_path = "C:\Langchain\poat\langchain\관광지_대구광역시0.csv"
df = pd.read_csv(file_path, encoding='cp949')

# 데이터의 첫 몇 개 행을 확인합니다.
print("첫 몇 개의 행:")
print(df.head())

# 'name' 열의 중복 행을 제거합니다.
df = df.drop_duplicates(subset=['name'])

# 중복이 제거된 데이터의 첫 몇 개 행을 확인합니다.
print("중복이 제거된 데이터의 첫 몇 개 행:")
print(df.head())

# 전처리된 데이터를 새로운 CSV 파일로 저장합니다.
output_file_path = "C:\Langchain\poat\langchain\대구광역시_관광지_완.csv"
df.to_csv(output_file_path, index=False, encoding='cp949')
print("전처리된 데이터를 {}에 저장했습니다.".format(output_file_path))
