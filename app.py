import os
import csv
from flask import Flask, render_template, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import pandas as pd
app = Flask(__name__)

# 定义绝对路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))    # 当前目录
WEB_CACHE_FOLDER = os.path.join(CURRENT_DIR, 'web-cache')   # web-cache 文件夹
CSV_FILE = os.path.join(WEB_CACHE_FOLDER, 'web-cache.csv')  # CSV 文件


# 初始化一个列表，用于存储从 CSV 文件中读取的信息
search_data = []

# 读取 web-cache.csv 文件
try:
    df = pd.read_csv(CSV_FILE, sep='\t', encoding='utf-8')
except FileNotFoundError:
    print(f"CSV 文件 '{CSV_FILE}' 不存在。请检查路径是否正确。")
    exit(1)

# 遍历 DataFrame 的每一行
for index, row in df.iterrows():
    filename = row['filename'] + '.html'
    url = row['url']

    file_path = os.path.join(WEB_CACHE_FOLDER, filename)    # 定义 HTML 文件的绝对路径
    # 检查文件是否存在
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用 BeautifulSoup 解析 HTML 内容
            soup = BeautifulSoup(content, 'html.parser')
            # 提取标题或使用文件名
            title = soup.title.string.strip() if soup.title and soup.title.string else filename
            # 将信息添加到 search_data 列表中
            search_data.append({
                'title': title,
                'filename': filename,
                'url': url,
                'content': content  # 保存内容以便后续高亮显示
            })
    else:
        print(f"文件 {filename} 不存在，已跳过。")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    suggestions = []
    for item in search_data:
        if query.lower() in item['title'].lower() or query.lower() in item['content'].lower():
            # 返回标题和匹配的内容片段
            # 这里可以截取包含搜索词的部分内容
            start_index = item['content'].lower().find(query.lower())
            snippet = ''
            if start_index != -1:
                snippet = item['content'][max(0, start_index - 50):start_index + 50]
            suggestions.append({
                'title': item['title'],
                'filename': item['filename'],
                'url': item['url'],
                'snippet': snippet
            })
    return jsonify(suggestions)

# 提供静态文件服务
@app.route('/view/<path:filename>')
def display_html(filename):
    return send_from_directory(WEB_CACHE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)