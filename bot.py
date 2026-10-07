import os
import time
import requests
from playwright.sync_api import sync_playwright

EMAIL = os.environ.get("PINTEREST_EMAIL")
PASSWORD = os.environ.get("PINTEREST_PASSWORD")

PRODUCTS = [
    {
        "title": "Aesthetic Oversized Cable Knit Sweater",
        "desc": "Upgrade your autumn wardrobe with this cozy oversized chunky knit sweater. Trendy casual fall fashion. #amazonfinds #fashion #ad",
        "link": "https://www.amazon.com/dp/B08XYZ1234?tag=iamkieravox-20",
        "image_url": "https://m.media-amazon.com/images/I/71wK7YQZqNL._AC_UY1000_.jpg",
        "board": "Everyday Chic Fashion"
    }
]

def run():
    print("Starting Headless Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900}
        )
        page = context.new_page()

        # Login
        print("Logging into Pinterest...")
        page.goto("https://www.pinterest.com/login/")
        page.wait_for_selector('input[id="email"]', timeout=30000)
        page.fill('input[id="email"]', EMAIL)
        page.fill('input[id="password"]', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(8000)

        for item in PRODUCTS:
            print(f"Creating Pin: {item['title']}")
            page.goto("https://www.pinterest.com/pin-creation-tool/")
            page.wait_for_timeout(6000)

            # Upload Image
            print("Setting image...")
            res = requests.get(item["image_url"], headers={"User-Agent": "Mozilla/5.0"})
            with open("temp_pin.jpg", "wb") as f:
                f.write(res.content)
                
            page.evaluate("""() => {
                let input = document.querySelector('input[type="file"]');
                if (!input) {
                    input = document.createElement('input');
                    input.type = 'file';
                    input.id = 'injected-file';
                    document.body.appendChild(input);
                }
            }""")
            page.set_input_files('input[type="file"]', "temp_pin.jpg")
            page.wait_for_timeout(4000)

            # Fill Details
            print("Entering title, description and link...")
            try:
                page.locator('input[id*="title"], textarea[id*="title"]').first.fill(item["title"])
            except Exception:
                pass

            try:
                page.locator('div[role="textbox"], textarea[id*="description"]').first.fill(item["desc"])
            except Exception:
                pass

            try:
                page.locator('input[id*="link"], input[placeholder*="link"]').first.fill(item["link"])
            except Exception:
                pass
            page.wait_for_timeout(2000)

            # Select Board & Publish
            print("Selecting board and publishing...")
            try:
                # Board dropdown open karein agar exist karta hai
                board_btn = page.locator('button[data-test-id*="board-dropdown-select-button"], div[data-test-id*="board-dropdown"]').first
                if board_btn.is_visible():
                    board_btn.click()
                    page.wait_for_timeout(1500)
                    # Board name select
                    target_board = page.locator(f'div[title*="{item[\"board\"]}"]').first
                    if target_board.is_visible():
                        target_board.click()
                        page.wait_for_timeout(1000)
            except Exception as e:
                print("Board select bypass:", e)

            # Final Save/Publish click
            save_btn = page.locator('button[data-test-id*="board-dropdown-save-button"], button:has-text("Publish"), button:has-text("Save")').first
            save_btn.dispatch_event('click')
            print("Publish clicked!")
            page.wait_for_timeout(8000)

        browser.close()

if __name__ == "__main__":
    run()
