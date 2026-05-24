import json
import time
from playwright.sync_api import sync_playwright

urls = [
"https://qr.ae/psjVtk", "https://qr.ae/pKlMwv", "https://qr.ae/pKaXAS", "https://qr.ae/pFvOVN",
"https://qr.ae/pFvOJN", "https://qr.ae/pKtVTh", "https://qr.ae/pKr9Q7", "https://qr.ae/pKAH2F",
"https://qr.ae/pKrD8p", "https://qr.ae/pFvOVY", "https://qr.ae/pvqeS3", "https://qr.ae/pvgjxe",
"https://qr.ae/pvuG04", "https://qr.ae/pv2kXO", "https://qr.ae/pGL6Ya", "https://qr.ae/pFvOmy",
"https://qr.ae/pFvOJt", "https://qr.ae/pG6gke", "https://qr.ae/pG6Hwg", "https://qr.ae/pFvOms",
"https://qr.ae/pFvOx4", "https://qr.ae/pvuhEq", "https://qr.ae/pFvOxy", "https://qr.ae/pFvODH",
"https://qr.ae/pFvOmE", "https://qr.ae/pFvOlb", "https://qr.ae/pv2CM7", "https://qr.ae/pFvOqq",
"https://qr.ae/pFvOqv", "https://qr.ae/pFvOmq", "https://qr.ae/pvKajh", "https://qr.ae/pFvOmz",
"https://qr.ae/pFvMPf", "https://qr.ae/pFvOzt", "https://qr.ae/pFvOz8"
]
urls.reverse()

data = []

with sync_playwright() as p:
    # Use a persistent context so cookies are shared natively, or just a normal browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    print("Launching visible browser...")
    page.goto(urls[0])
    print("WAITING 15 SECONDS. Please solve any CAPTCHAs if they appear on screen!")
    time.sleep(15)
    
    for i, url in enumerate(urls):
        print(f"Scraping {i+1}/{len(urls)}: {url}")
        try:
            page.goto(url, timeout=30000, wait_until="load")
            time.sleep(2)
            for scroll_step in range(4):
                page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
                time.sleep(0.5)
            
            title = page.title()
            html_content = page.evaluate("""() => {
                let m = document.getElementById('mainContent');
                return m ? m.outerHTML : document.body.innerHTML;
            }""")
            
            data.append({"url": url, "title": title, "html": html_content})
        except Exception as e:
            print(f"Failed {url}: {e}")
            
    browser.close()

with open("raw_quora_content.json", "w") as f:
    json.dump(data, f)
print("Finished scraping all URLs!")
