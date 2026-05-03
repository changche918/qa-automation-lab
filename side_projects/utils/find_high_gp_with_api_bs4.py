# Created: 2026-05-03
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


class FindHighGP:
    """純 API + BeautifulSoup 版本，不需要瀏覽器驅動。

    對應原本 utils/find_high_gp_with_api.py 的字串切片版，
    改用 bs4 的 CSS 選擇器讓解析邏輯更清楚、易維護。
    """

    def __init__(self):
        """API 版不需建立瀏覽器，建構子不接任何參數。"""
        pass

    def _get_soup(self, url):
        """抓取網頁 HTML 並轉成 BeautifulSoup 物件。

        Args:
            url: 目標網頁網址。
        Returns:
            BeautifulSoup 物件，可直接用 select / find 解析。
        """
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def _gp_to_value(self, gp_text):
        """把巴哈的 GP 文字轉成可比較大小的數值。

        Args:
            gp_text: GP 標籤裡的文字，例如 "爆"、"35"、"-3"。
        Returns:
            float("inf") 代表爆文，其餘回傳 int。沒有數字則回傳 0。
        """
        if "爆" in gp_text:
            return float("inf")
        digits = "".join(c for c in gp_text if c.isdigit())
        return int(digits) if digits else 0

    def scan_high_gp_post_api(self, url):
        """掃文章列表頁，取出 GP > 15 的文章與本頁 GP 最高文章的網址。

        Args:
            url: 文章列表頁網址。
        Returns:
            tuple(list[str], str|None)
                list[str]: 高 GP 標題清單，例 ["[爆] 標題A", "[35] 標題B"]
                str|None : 本頁 GP 最高文章的完整網址，若沒有文章則為 None。
        """
        soup = self._get_soup(url)

        high_gp_post_titles = []
        page_best_gp = -1
        page_best_title = None
        page_best_href = None

        # 文章列：class 包含 b-list__row 與 b-list-item，且不要置頂文
        rows = soup.select(".b-list__row.b-list-item")
        for row in rows:
            if "b-list__row--sticky" in row.get("class", []):
                continue

            title_tag = row.select_one("p.b-list__main__title")
            # GP 的 class 有三種變體：--good / --bad / --zero，用 ^= 前綴比對
            gp_tag = row.select_one('[class^="b-list__summary__gp"]')
            link_tag = row.select_one("a[href]")
            if not (title_tag and gp_tag and link_tag):
                continue

            title = title_tag.get_text(strip=True)
            gp_text = gp_tag.get_text(strip=True)
            gp_value = self._gp_to_value(gp_text)

            if gp_value > 15:
                display = gp_text if gp_value == float("inf") else gp_value
                high_gp_post_titles.append(f"[{display}] {title}")

            if gp_value > page_best_gp:
                page_best_gp = gp_value
                page_best_title = title
                page_best_href = link_tag["href"]

        if page_best_title is not None:
            display = "爆" if page_best_gp == float("inf") else page_best_gp
            high_gp_post_titles.append(f"[{display}] {page_best_title}")

        # 把相對路徑補上網域，變成完整網址
        best_art_url = None
        if page_best_href:
            if page_best_href.startswith("http"):
                best_art_url = page_best_href
            else:
                best_art_url = f"https://forum.gamer.com.tw/{page_best_href}"

        return high_gp_post_titles, best_art_url

    def scan_high_gp_content_api(self, url, choice):
        """掃文章內回覆，取出爆文回覆與本頁 GP 最高的一般回覆。

        Args:
            url: 文章頁網址（可含 page= 分頁）。
            choice: "1" 只抓第一筆爆文；"2" 抓所有爆文。
        Returns:
            tuple(list[str], bool)：回覆清單，以及是否還有下一頁。
        """
        soup = self._get_soup(url)

        # 是否還有下一頁：a.next 存在且不是 a.next.no
        has_next = soup.select_one("a.next:not(.no)") is not None

        high_gp_content = []
        page_best_gp = -1
        page_best_content = None

        # 每樓回覆是 <section id="post_xxx">
        posts = soup.select("section[id^='post_']")
        for post in posts:
            gp_tag = post.select_one(".postgp")
            content_tag = post.select_one(".c-article__content")
            if gp_tag is None or content_tag is None:
                continue

            gp_text = gp_tag.get_text(strip=True)
            # bs4 的 get_text 會自動處理巢狀 div，並用 separator 把段落用空白接起來
            content = " ".join(content_tag.get_text(separator=" ", strip=True).split())

            if "爆" in gp_text:
                high_gp_content.append(f"[{gp_text}] {content}")
                if choice == "1":
                    break
                continue

            gp_value = self._gp_to_value(gp_text)
            if gp_value > page_best_gp:
                page_best_gp = gp_value
                page_best_content = content

        if page_best_content is not None:
            high_gp_content.append(f"[{page_best_gp}] {page_best_content}")

        return high_gp_content, has_next
