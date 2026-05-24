import json
import time
from playwright.sync_api import sync_playwright

urls = [
"https://qr.ae/psjVtk",
"https://qr.ae/pKlMwv",
"https://qr.ae/pKaXAS",
"https://qr.ae/pFvOVN",
"https://qr.ae/pFvOJN",
"https://qr.ae/pKtVTh",
"https://qr.ae/pKr9Q7",
"https://qr.ae/pKAH2F",
"https://qr.ae/pKrD8p",
"https://qr.ae/pFvOVY",
"https://qr.ae/pvqeS3",
"https://qr.ae/pvgjxe",
"https://qr.ae/pvuG04",
"https://qr.ae/pv2kXO",
"https://qr.ae/pGL6Ya",
"https://qr.ae/pFvOmy",
"https://qr.ae/pFvOJt",
"https://qr.ae/pG6gke",
"https://qr.ae/pG6Hwg",
"https://qr.ae/pFvOms",
"https://qr.ae/pFvOx4",
"https://qr.ae/pvuhEq",
"https://qr.ae/pFvOxy",
"https://qr.ae/pFvODH",
"https://qr.ae/pFvOmE",
"https://qr.ae/pFvOlb",
"https://qr.ae/pv2CM7",
"https://qr.ae/pFvOqq",
"https://qr.ae/pFvOqv",
"https://qr.ae/pFvOmq",
"https://qr.ae/pvKajh",
"https://qr.ae/pFvOmz",
"https://qr.ae/pFvMPf",
"https://qr.ae/pFvOzt",
"https://qr.ae/pFvOz8"
]
urls.reverse()

data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for i, url in enumerate(urls[:2]): # test with 2 first
        print(f"Scraping {i+1}: {url}")
        try:
            page.goto(url, timeout=60000)
            page.wait_for_selector(".q-text", timeout=15000)
            # scroll down to load lazy images
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            title = page.title()
            
            # Use JS to extract the main post content.
            # In Quora, the post body is usually the largest continuous block of text or has a specific structure.
            # We can find all text blocks and images within the main article content.
            
            content_json = page.evaluate("""() => {
                // Find all elements that look like post content
                // A good heuristic for Quora is the .spacing_log_answer_content or just the largest text container
                let main_content = document.querySelector('.q-box.qu-pt--medium.qu-pb--medium') || document.body;
                
                // Let's just extract all paragraphs and images in order from the main content.
                // We'll walk the DOM.
                let elements = [];
                let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT, {
                    acceptNode: function(node) {
                        if (node.tagName === 'IMG' || node.classList.contains('q-text')) {
                            return NodeFilter.FILTER_ACCEPT;
                        }
                        return NodeFilter.FILTER_SKIP;
                    }
                });
                
                let node;
                while(node = walker.nextNode()) {
                    if (node.tagName === 'IMG') {
                        if (node.src && !node.src.includes('data:image')) {
                            elements.push({type: 'image', src: node.src});
                        }
                    } else if (node.classList.contains('q-text')) {
                        // avoid duplicate text if nested
                        if (node.innerText && node.innerText.trim().length > 0) {
                            elements.push({type: 'text', content: node.innerText.trim()});
                        }
                    }
                }
                return elements;
            }""")
            
            data.append({"url": url, "title": title, "content": content_json})
        except Exception as e:
            print(f"Failed {url}: {e}")
            
    browser.close()

with open("quora_posts.json", "w") as f:
    json.dump(data, f, indent=2)

print("Done. Saved to quora_posts.json")
