import chardet

def fix_encoding(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(file_path, 'w', encoding='cp949') as f:
        f.write(content)

# 파일 경로
csv_file_path = "C:\Langchain\poat\langchain\대구광역시_관광지_완.csv"

# 인코딩 수정
fix_encoding(csv_file_path)
