# Input handler URL validator: Checks if URL format is correct and if the site is reachable.

import re
import requests

def valid_url(url):
    return bool(re.match(r"^(http|https)://", url))

def is_reachable(url):
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        return resp.status_code < 400
    except requests.RequestException:
        return False
    

# Page Loader: Loads page content and extracts relevant elements for analysis.
from playwright.sync_api import sync_playwright

def load_page_data(url, viewport=None):

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page()
        if viewport:
            page.set_viewport_size(viewport)
        page.goto(url, timeout=10000)

        html = page.content()

        texts = []
        for element in page.query_selector_all("*"):
            if not element.is_visible():               
                continue
            try:
                txt = element.inner_text().strip()
            except:
                continue
            if not txt:                                
                continue

            color  = element.evaluate("el => getComputedStyle(el).color")
            bg     = element.evaluate("el => getComputedStyle(el).backgroundColor")
            size   = element.evaluate("el => getComputedStyle(el).fontSize")
            weight = element.evaluate("el => getComputedStyle(el).fontWeight")

            texts.append({
                "tag":      element.evaluate("el => el.tagName"),
                "id":       element.get_attribute("id") or "",
                "classes":  element.get_attribute("class") or "",
                "text":     txt,
                "color":    color,
                "bg":       bg,
                "size":     size,
                "weight":   weight
            })
     # Headings (H1–H6)
        heading_elems = page.query_selector_all("h1, h2, h3, h4, h5, h6")
        headings = []
        for h in heading_elems:
            try:
                tag = h.evaluate("el => el.tagName")
                text = h.inner_text().strip()
                headings.append({"tag": tag, "text": text})
            except:
                continue

        # Images (collecting src)
        image_elems = page.query_selector_all("img")
        images = []
        for img in image_elems:
            images.append({ "src": img.get_attribute("src") or "", "alt": img.get_attribute("alt") or ""})

        link_btn_elems = page.query_selector_all("a, button")
        buttons = []
        for el in link_btn_elems:
            tag = el.evaluate("e => e.tagName")

    # Try to grab visible text
            try:
                text = el.inner_text().strip()
            except:
                text = ""

    # Try to grab aria-label (or empty string if none) AI helped me 
            try:
                aria = el.get_attribute("aria-label") or ""
            except:
                aria = ""

    # Store all three in a dict
            buttons.append({
                "tag": tag,
                "text": text,
             "aria": aria
            })

        browser.close()

    return {"html": html, "texts": texts, "headings":headings, "images":images, "buttons":buttons}