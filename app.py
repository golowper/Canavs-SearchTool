from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)


# 获取 web-cache 文件夹中的 HTML 文件列表及其内容
def get_html_files(folder_path, keyword=None):
    if not os.path.exists(folder_path):
        print(f"Error: The directory '{folder_path}' does not exist.")  # 控制台报错
        raise FileNotFoundError(f"The directory '{folder_path}' does not exist.")

    results = []

    # 遍历目录中的文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # 如果有关键词则进行高亮处理
                if keyword:
                    # 对文件名和内容中的关键词进行高亮
                    highlighted_title = re.sub(f"({re.escape(keyword)})", r'<span class="highlight">\1</span>',
                                               file_name, flags=re.IGNORECASE)
                    highlighted_content = re.sub(f"({re.escape(keyword)})", r'<span class="highlight">\1</span>',
                                                 content, flags=re.IGNORECASE)
                else:
                    highlighted_title = file_name
                    highlighted_content = content

                # 将结果添加到列表
                results.append({
                    "title": highlighted_title,
                    "content": highlighted_content
                })

    return results


# 主页路由，展示搜索框和搜索结果
@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = request.form.get('keyword', '').strip()
    results = []
    try:
        results = get_html_files('web-cache', keyword) if keyword else []
    except FileNotFoundError as e:
        print(e)  # 控制台打印错误信息

    return render_template('index.html', results=results, keyword=keyword)


# API 路由：获取 web-cache 文件夹中的 HTML 文件列表
@app.route('/file-list', methods=['GET'])
def get_file_list():
    folder_path = 'web-cache'

    if not os.path.exists(folder_path):
        error_message = f"Error: The directory '{folder_path}' does not exist."
        print(error_message)  # 控制台报错
        return jsonify({"error": error_message}), 500

    try:
        # 获取文件夹中的所有 HTML 文件
        files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
        return jsonify(files)  # 返回 JSON 格式的文件列表
    except Exception as e:
        print(f"Unexpected error: {e}")  # 控制台打印错误信息
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
