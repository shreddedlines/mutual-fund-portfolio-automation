from playwright.sync_api import sync_playwright, TimeoutError
import os
import time

DOWNLOAD_DIR = os.path.abspath("downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=300,
        args=[
            "--disable-features=DownloadBubble",
            f"--download-default-directory={DOWNLOAD_DIR.replace(os.sep, '/')}"
        ]
    )

    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    page.goto("https://www.axismf.com/statutory-disclosures", timeout=60000)
    page.get_by_text("Monthly Scheme Portfolios", exact=False).click()
    page.wait_for_timeout(3000)

    page.get_by_text("2026", exact=True).click()
    page.locator("label", has_text="2025").click()
    page.keyboard.press("Escape")
    page.wait_for_timeout(1500)

    page.get_by_text("January", exact=True).click()
    page.locator("label", has_text="December").click()
    page.keyboard.press("Escape")
    page.wait_for_timeout(1500)

    page.get_by_text("Consolidated", exact=True).click()
    page.keyboard.press("Escape")
    page.wait_for_timeout(3000)

    links = page.locator("a:has-text('Portfolio')")
    count = links.count()
    print(f"Found {count} files")

    for i in range(count):
        link = links.nth(i)
        name = link.inner_text().strip()
        print(f"Clicking {i+1}/{count}: {name}")

        try:
            with page.expect_download(timeout=5000) as d:
                link.click(force=True)
            download = d.value
            download.save_as(os.path.join(DOWNLOAD_DIR, download.suggested_filename))
            print(f"Downloaded via Playwright: {download.suggested_filename}")

        except TimeoutError:
            print("Browser auto-download (forced to same folder)")
            link.click(force=True)
            time.sleep(2)

    browser.close()

print("DONE.... Check /downloads")
