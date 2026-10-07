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

        print("Logging into Pinterest...")
        page.goto("https://www.pinterest.com/login/")
        page.wait_for_selector('input[id="email"]', timeout=30000)
        page.fill('input[id="email"]', EMAIL)
        page.fill('input[id="password"]', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(8000)

        for item in PRODUCTS:
            print("Navigating to creation tool...")
            page.goto("https://www.pinterest.com/pin-creation-tool/")
            page.wait_for_timeout(6000)

            # Close popup if visible
            try:
                got_it = page.locator('button:has-text("Got it")').first
                if got_it.is_visible():
                    got_it.click()
                    page.wait_for_timeout(1000)
            except Exception:
                pass

            # Download Image
            print("Downloading product image...")
            res = requests.get(item["image_url"], headers={"User-Agent": "Mozilla/5.0"})
            with open("temp_pin.jpg", "wb") as f:
                f.write(res.content)

            # Upload Image
            print("Uploading image...")
            file_input = page.locator('input[type="file"]')
            if file_input.count() > 0:
                file_input.first.set_input_files("temp_pin.jpg")
            else:
                page.set_input_files('input[type="file"]', "temp_pin.jpg")
            page.wait_for_timeout(5000)

            # Title
            print("Entering title...")
            title_field = page.locator('input[placeholder*="title"], textarea[placeholder*="title"], input[id*="title"]').first
            title_field.click()
            title_field.fill(item["title"])
            page.wait_for_timeout(1000)

            # Description
            print("Entering description...")
            desc_field = page.locator('div[role="textbox"], textarea[placeholder*="about"], textarea[id*="description"]').first
            desc_field.click()
            desc_field.fill(item["desc"])
            page.wait_for_timeout(1000)

            # Destination Link
            print("Entering link...")
            link_field = page.locator('input[placeholder*="link"], input[id*="link"]').first
            link_field.click()
            link_field.fill(item["link"])
            page.wait_for_timeout(2000)

            # Real UI Click on Publish button
            print("Clicking red Publish button...")
            publish_btn = page.locator('button:has-text("Publish")').first
            publish_btn.wait_for(state="visible", timeout=10000)
            publish_btn.click(force=True)

            print("Waiting for pin creation...")
            page.wait_for_timeout(10000)
            page.screenshot(path="after_publish.png")

        browser.close()
        print("Bot execution finished.")

if __name__ == "__main__":
    run()
