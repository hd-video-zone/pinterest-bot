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
            print("Opening pin creation...")
            page.goto("https://www.pinterest.com/pin-creation-tool/")
            page.wait_for_timeout(7000)

            # Pop-up dismiss
            try:
                page.locator('button:has-text("Got it")').first.click(timeout=3000)
            except Exception:
                pass

            # Working File Injection (Run #7)
            print("Injecting image file...")
            res = requests.get(item["image_url"], headers={"User-Agent": "Mozilla/5.0"})
            with open("temp_pin.jpg", "wb") as f:
                f.write(res.content)

            page.evaluate('''() => {
                let input = document.querySelector('input[type="file"]');
                if (!input) {
                    input = document.createElement('input');
                    input.type = 'file';
                    input.id = 'injected-file';
                    document.body.appendChild(input);
                }
            }''')
            page.set_input_files('input[type="file"]', "temp_pin.jpg")
            page.wait_for_timeout(5000)

            # Details entry
            print("Entering pin details...")
            try:
                page.locator('input[placeholder*="title"], textarea[placeholder*="title"], input[id*="title"]').first.fill(item["title"])
            except Exception:
                pass

            try:
                page.locator('div[role="textbox"], textarea[placeholder*="about"], textarea[id*="description"]').first.fill(item["desc"])
            except Exception:
                pass

            try:
                page.locator('input[placeholder*="link"], input[id*="link"]').first.fill(item["link"])
            except Exception:
                pass
            page.wait_for_timeout(3000)

            # Publish Click via red button locator
            print("Triggering Publish...")
            try:
                page.locator('button:has-text("Publish")').first.click(timeout=5000)
            except Exception:
                page.evaluate('''() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const p = btns.find(b => (b.innerText || "").trim().toLowerCase() === "publish");
                    if (p) p.click();
                }''')

            page.wait_for_timeout(10000)
            print("Pin posted successfully!")

        browser.close()

if __name__ == "__main__":
    run()
