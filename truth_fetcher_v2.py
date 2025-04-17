from playwright.sync_api import sync_playwright
import time

def auto_scroll(page, steps=10, delay=1.5):
    for _ in range(steps):
        page.mouse.wheel(0, 1500)
        time.sleep(delay)

def extract_visible_content(page):
    results = []
    wrappers = page.query_selector_all("div.status__content-wrapper")

    for block in wrappers:
        p_tags = block.query_selector_all('p[data-markup="true"]')
        text = "\n".join(p.inner_text().strip() for p in p_tags if p.inner_text().strip())
        if text and len(text) > 20 and text.find("/video") == -1 and text.find("youtube.com") == -1:
            results.append(text)

    return results


def get_truths_incremental(username="realDonaldTrump", max_items=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        page = browser.new_page()
        page.goto(f"https://truthsocial.com/@{username}", timeout=60000)

        # 接受 cookie 弹窗
        try:
            page.click("button:has-text('Accept')", timeout=3000)
        except:
            pass

        all_texts = set()
        for _ in range(12):  # 滚 12 次差不多两三屏
            new_texts = extract_visible_content(page)
            all_texts.update(new_texts)

            if len(all_texts) >= max_items:
                break

            page.mouse.wheel(0, 1200)
            time.sleep(1.2)

        browser.close()
        return list(all_texts)[:max_items]


if __name__ == "__main__":
    truths = get_truths_incremental()
    for i, t in enumerate(truths, 1):
        print(f"\n--- Truth #{i} ---\n{t}")
