import json
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 设置浏览器选项
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 不显示浏览器窗口
options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')



# 使用 ChromeDriverManager 安装 ChromeDriver，并用 Service 包装路径
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


class Crawler:
    def __init__(self, start_url, depth_limit):
        self.start_url = start_url
        self.depth_limit = depth_limit
        self.visited = set()

    def deep_crawl(self, url, depth):
        if depth == 0 or url in self.visited:
            return

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("Page is fully loaded!")

            print(f"Depth {depth}: {driver.title} - {url}")

            self.visited.add(url)

            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href and href.startswith('http') and href not in self.visited:
                    self.deep_crawl(href, depth - 1)

        except Exception as e:
            print(f"Error occurred: {e}")

    def login(self):
        try:
            driver.get("https://canvas.sydney.edu.au/")
            # 读取 cookies
            if os.path.exists("cookies.json"):
                with open("cookies.json", "r") as file:
                    cookies = json.load(file)
                    for cookie in cookies:
                        cookie['domain'] = '.sydney.edu.au'
                        driver.add_cookie(cookie)
            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("Page is fully loaded!")
        except Exception as e:
            print(f"Error occurred: {e}")

        # 检测是否有可以登陆 如果访问start_url没有跳转就是已经登录 跳转了就是未登录
        driver.get(self.start_url)
        driver.get(self.start_url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        if driver.current_url == self.start_url:
            print("Already logged in!")
            return

        # 否则登录
        driver.get("https://canvas.sydney.edu.au/")
        input("Login First, Press Enter to continue...")
        # 保存登录后的 cookies
        with open("cookies.json", "w") as f:
            cookies = driver.get_cookies()
            json.dump(cookies, f)

    def start(self):
        # 登录
        self.login()
        input()
        self.deep_crawl(self.start_url, self.depth_limit)


def main():
    # 启动爬虫
    start_url = "https://canvas.sydney.edu.au/courses/61585"
    depth_limit = 20  # 设置最大深度
    crawler = Crawler(start_url, depth_limit)
    crawler.start()

    # 关闭浏览器
    driver.quit()

if __name__ == '__main__':
    main()