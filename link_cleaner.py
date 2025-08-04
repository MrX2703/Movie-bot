from playwright.async_api import async_playwright

async def clean_links(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(3000)  # Wait for redirects/ads
            
            # Here you tweak based on how your target website loads the video
            frame = page.main_frame
            videos = await frame.query_selector_all("video")

            video_src = ""
            for v in videos:
                src = await v.get_attribute("src")
                if src and "http" in src:
                    video_src = src
                    break

            await browser.close()

            # Fallback: stream = video, download = video (same link)
            return (video_src, video_src)
    except Exception as e:
        print("Error:", e)
        return (None, None)
