
# Contrast Checker -----------------------------------------------------------------------

from wcag_contrast_ratio import rgb, passes_AA, passes_AAA

def parse_rgb(css_color): # Convert rgb(r,g,b) to (r, g, b) ints.
    nums = css_color[css_color.find("(")+1 : css_color.find(")")].split(",") # AI helped to look for the right position
    return tuple(int(value.strip().rstrip("%")) for value in nums[:3])  # it then turns it into a int 

def check_contrast(texts): # converts it to numbers, not a valid number it skips it
    results = []
    for item in texts:
        fg = parse_rgb(item["color"])
        bg = parse_rgb(item["bg"])
        if not fg or not bg:
            continue

        # Normalize 0–255 ints → 0.0–1.0 floats for the library (AI helped)
        fg_norm = tuple(rgb_int / 255 for rgb_int in fg)
        bg_norm = tuple(rgb_int / 255 for rgb_int in bg)

        # Compute contrast ratio
        ratio = rgb(fg_norm, bg_norm)

        # Check Pass/Fail
        aa_pass  = passes_AA(ratio)
        aaa_pass = passes_AAA(ratio)

        # A snippet is a short preview of the text (AI helped)
        snippet = item["text"][:30] + ("…" if len(item["text"]) > 30 else "")

        results.append({
            "tag":      item.get("tag", ""),
            "id":       item.get("id", ""),
            "classes":  (item.get("classes", "").split()[0] if item.get("classes") else ""),
            "snippet":  snippet,
            "ratio":    round(ratio, 2),
            "AA":       "Pass" if aa_pass else "Fail",
            "AAA":      "Pass" if aaa_pass else "Fail"
        })

    return results

# Typography Checker --------------------------------------
def parse_px(text_size):
    try:
        # strip spaces, lowercase, remove "px" - Similar to the top one we want to only get numbers no extra spacing or px
        num_str = text_size.strip().lower().rstrip("px") 
        # convert to a number and it rounds to the nearest
        return int(round(float(num_str)))
    except:
        return None

def check_typography(texts):
    results = []
    for item in texts:
        size_px = parse_px(item.get("size", "")) # we do empty string so it can return something
        if size_px is None or item.get("tag", "").lower() == "footer":
            continue  # skip anything we can’t read

        # WCAG recommends at least 16px body text for readability
        if size_px >= 16:
            status = "Pass"
        elif size_px >= 12: 
            status = "Warning"
        else: 
            status = "Fail"

        snippet = item["text"][:30] + ("…" if len(item["text"]) > 30 else "") #AI helped

        results.append({
            "tag": item.get("tag", ""),
            "id": item.get("id", ""),
            "classes": (item.get("classes","").split()[0] if item.get("classes") else ""),
            "snippet": snippet,
            "size_px": size_px,
            "WCAG": status
        })
    return results

# Alt Text Checker for Images -------------------------------------------------------
def check_alt_text(images):
    results = []
    for img in images:
        alt = img.get("alt", "").strip() # gets alt description and it removes any extra space
        if alt:
            status = "Pass"
        else:
            status = "Fail"
        results.append({"src": img.get("src", ""), "alt": alt, "status": status})
    return results 

# Heading Structure Checker -------------------------------------------------------
def check_heading_structure(headings):

    warnings = []

    # Check for exactly one H1
    h1_count = sum(1 for h in headings if h["tag"].upper() == "H1")
    if h1_count == 0:
        warnings.append("Missing H1 heading")
    elif h1_count > 1:
        warnings.append(f"Multiple H1 headings found ({h1_count})")

    # Check for skipped levels 
    previous_level = 0
    for h in headings:
        # Now safe to convert, since we know tag is "H1"–"H6"
        level = int(h["tag"][1])
        if previous_level and level > previous_level + 1:
            warnings.append(f"Skipped from H{previous_level} to {h['tag']}")
        previous_level = level

    return warnings

# Button Checker ---------------------------------
def check_link_buttons(elements):
    results = []
    for el in elements:
        text = el["text"].strip()
        aria = el["aria"].strip()

        label = el["tag"]
        if el.get("id"):
            label += f"#{el['id']}"
        elif el.get("classes"):
            label += f".{el['classes']}"

        snippet = text if text else '""'
        
        if not text and not aria:
            results.append({
            "label": label,
            "snippet": snippet,
            "reason": "No text or aria-label",
            "status": "Fail"
        })
    
        else:
            results.append({
            "label": label,
            "snippet": snippet,
            "reason": "-",
            "status": "Pass"
        })

    return results
