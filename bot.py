import os
import time
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
            page.wait_for_timeout(7000)

            # Check if direct file input exists or Save from URL
            save_from_url_btn = page.locator('button:has-text("Save from URL"), div[role="button"]:has-text("Save from URL")')
            
            if save_from_url_btn.count() > 0 and save_from_url_btn.first.is_visible():
                print("Using Save from URL option...")
                save_from_url_btn.first.click()
                page.wait_for_timeout(2000)
                url_input = page.locator('input[placeholder*="http"], input[type="text"]').first
                url_input.fill(item["image_url"])
                page.keyboard.press("Enter")
                page.wait_for_timeout(5000)
                # Select first image thumbnail
                thumb = page.locator('div[role="button"] img, img').first
                if thumb.is_visible():
                    thumb.click()
                    add_pin_btn = page.locator('button:has-text("Add Pin"), button:has-text("Add pin")').first
                    if add_pin_btn.is_visible():
                        add_pin_btn.click()
            else:
                print("Setting image via input element directly...")
                import requests
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

            page.wait_for_timeout(5000)

            # Details
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

            # Publish Click
            print("Clicking Publish...")
            publish_btn = page.locator('button[data-test-id*="board-dropdown-save-button"], button:has-text("Publish"), button:has-text("Save")').first
            publish_btn.click()
            page.wait_for_timeout(7000)
            print("Pin posted!")

        browser.close()

if __name__ == "__main__":
    run()
