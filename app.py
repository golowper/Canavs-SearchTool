from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

# 主页面
@app.route('/')
def index():
    return render_template('index.html')

# 获取 web-cache 文件夹中的 HTML 文件列表
@app.route('/file-list', methods=['GET'])
def get_file_list():
    folder_path = 'web-cache'  # web-cache 文件夹路径
    try:
        files = os.listdir(folder_path)
        html_files = [f for f in files if f.endswith('.html')]
        return jsonify(html_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
