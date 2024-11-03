import os
import json


def get_html_files(folder_path='web-cache'):
    # 确保文件夹路径存在
    if not os.path.exists(folder_path):
        print(f"Directory '{folder_path}' does not exist.")
        return []

    try:
        # 获取文件夹中的所有文件，并筛选出 HTML 文件
        html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
        return html_files

    except PermissionError as e:
        # 捕获权限错误并输出
        print(f"Permission Error: {e}")
        return []

    except Exception as e:
        # 捕获其他异常并输出
        print(f"An error occurred: {e}")
        return []


# 检查是否作为独立脚本运行
if __name__ == "__main__":
    # 使用绝对路径指定 web-cache 文件夹路径，或保持默认路径
    folder_path = r"H:\xjianWebProject24_files\github_TXJ4204\Canavs-SearchTool\web-cache"

    # 调用函数获取 HTML 文件列表
    html_files = get_html_files(folder_path)

    # 输出结果，以 JSON 格式显示
    print("HTML files:", json.dumps(html_files, indent=2))
