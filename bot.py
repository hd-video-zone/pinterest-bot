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

def download_image(url, save_path="temp_pin.jpg"):
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    with open(save_path, "wb") as f:
        f.write(res.content)
    return save_path

def run():
    print("Starting Headless Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
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
            print(f"Opening Pin Creation: {item['title']}")
            img_path = download_image(item["image_url"])

            # Direct Pin Creation Tool
            page.goto("https://www.pinterest.com/pin-creation-tool/")
            page.wait_for_timeout(6000)

            # Agar redirect hokar pin-builder par chala jaye
            if "pin-creation-tool" not in page.url:
                page.goto("https://www.pinterest.com/pin-builder/")
                page.wait_for_timeout(6000)

            print("Uploading image file...")
            # Try multiple file input handles
            file_input = page.locator('input[type="file"]')
            try:
                file_input.wait_for(state="attached", timeout=15000)
                file_input.set_input_files(img_path)
            except Exception:
                # Fallback for hidden drag-drop targets
                page.set_input_files('input[type="file"]', img_path)
            
            page.wait_for_timeout(4000)

            print("Filling details...")
            # Title
            title_input = page.locator('input[placeholder*="title"], textarea[placeholder*="title"], input[id*="title"]').first
            if title_input.is_visible():
                title_input.fill(item["title"])

            # Description
            desc_input = page.locator('div[role="textbox"], textarea[placeholder*="description"], textarea[id*="description"]').first
            if desc_input.is_visible():
                desc_input.fill(item["desc"])

            # Destination Link
            link_input = page.locator('input[placeholder*="link"], input[id*="link"]').first
            if link_input.is_visible():
                link_input.fill(item["link"])

            page.wait_for_timeout(2000)

            # Publish
            print("Publishing Pin...")
            publish_btn = page.locator('button:has-text("Publish"), button:has-text("Save")').first
            publish_btn.click()
            page.wait_for_timeout(8000)
            print("Pin successfully published!")

        browser.close()

if __name__ == "__main__":
    run()
