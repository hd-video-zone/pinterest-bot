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

        # Step 1: Login
        print("Logging into Pinterest...")
        page.goto("https://www.pinterest.com/login/")
        page.wait_for_selector('input[id="email"]', timeout=30000)
        page.fill('input[id="email"]', EMAIL)
        page.fill('input[id="password"]', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(8000)

        for item in PRODUCTS:
            print("Navigating to creation screen...")
            # Direct Pin Creation Tool in Business Layout
            page.goto("https://www.pinterest.com/pin-creation-tool/")
            page.wait_for_timeout(6000)

            # Agar Business Hub par redirect ho jaye to Create Pin card dabayein
            if "business" in page.url.lower():
                print("Detected Business Hub, clicking Create Pin...")
                create_card = page.locator('div:has-text("Create Pin"), button:has-text("Create Pin")').first
                if create_card.is_visible():
                    create_card.click()
                    page.wait_for_timeout(5000)

            # Tooltip Dismiss
            try:
                page.locator('button:has-text("Got it")').first.click(timeout=3000)
                print("Dismissed tooltip.")
            except Exception:
                pass

            # Image download
            print("Downloading image...")
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
            page.wait_for_timeout(6000)

            # Fill Title
            print("Entering title...")
            title_box = page.locator('input[placeholder*="title"], textarea[placeholder*="title"], input[id*="title"]').first
            title_box.click()
            title_box.fill(item["title"])
            page.wait_for_timeout(1000)

            # Fill Description
            print("Entering description...")
            desc_box = page.locator('div[role="textbox"], textarea[placeholder*="about"], textarea[id*="description"]').first
            desc_box.click()
            desc_box.fill(item["desc"])
            page.wait_for_timeout(1000)

            # Fill Destination Link
            print("Entering link...")
            link_box = page.locator('input[placeholder*="link"], input[id*="link"]').first
            link_box.click()
            link_box.fill(item["link"])
            page.wait_for_timeout(2000)

            # Click Red Publish Button
            print("Clicking Publish...")
            pub_btn = page.locator('button:has-text("Publish")').first
            pub_btn.scroll_into_view_if_needed()
            pub_btn.click(force=True)
            
            print("Publish clicked, waiting for save confirmation...")
            page.wait_for_timeout(12000)

        browser.close()
        print("Bot execution finished.")

if __name__ == "__main__":
    run()
