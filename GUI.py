import streamlit as st
from url_validator import valid_url, is_reachable
from playwright._impl._errors import TimeoutError
from page_loader import load_page_data
from accesibility_analyzer import check_contrast, check_typography, check_alt_text, check_heading_structure, check_link_buttons
from result_formatter import (build_contrast_all_df, build_contrast_pass_df,build_contrast_fail_df, build_typography_all_df,build_typography_warning_df, build_typography_pass_df,build_typography_fail_df, build_alt_text_all_df,build_alt_text_fail_df,build_alt_text_pass_df, build_button_all_df ,build_button_fail_df,build_button_pass_df)
import time


st.set_page_config(page_title="Accessibility Analyzer", layout="centered")


st.title("Accessibility Audit")

st.write("Test your website's accessibility against WCAG standards for contrast, typography, alt text, headings, and buttons.")

st.subheader("How it works:")
st.write("""
1. Enter the website URL you want to audit.  
2. Click the Run Accessibility Audit button to start the analysis.  
3. Review results by category.
""")

st.markdown("---")

st.subheader("Enter Website URL:")
url_input = st.text_input("", placeholder="https://example.com")

col1, col2, col3 = st.columns(3)
with col2:
    run_audit = st.button("Run Accessibility Audit")

reach_placeholder = st.empty()
load_placeholder  = st.empty()
if run_audit:
    if not url_input:
        st.warning("Please enter a website URL.")
    elif not valid_url(url_input):
        st.error("Invalid URL! Must start with http:// or https://")
    else:
        with st.spinner("Checking site reachability..."):
            time.sleep(1)
            reachable = is_reachable(url_input)

        full_col = st.columns(1)[0]
        
        if not reachable:
            full_col.error("Site not reachable. Please check the address or your internet connection.")
        else:
            reach_placeholder.success("✅ Site is reachable!")
            try:
                with st.spinner("Loading page data..."):
                    data = load_page_data(url_input)

                html = data["html"]
                texts = data["texts"]
                headings = data["headings"]
                images = data["images"]
                buttons = data["buttons"]
                # store everything you need for later in session_state
                st.session_state.texts               = data["texts"]
                st.session_state.contrast_results    = check_contrast(data["texts"])
                st.session_state.typography_results  = check_typography(data["texts"])
                st.session_state.alt_results         = check_alt_text(data["images"])
                st.session_state.heading_warnings    = check_heading_structure(data["headings"])
                st.session_state.button_results      = check_link_buttons(data["buttons"])
                load_placeholder.success("✅ Page data loaded successfully!")
            except Exception:
                st.error(f"Failed to load page data: Please click 'Run Accessibility Audit' again to retry.")
                st.stop()
                
reach_placeholder.empty()
#load_placeholder.empty()---- Has a comment for now may delete later

if "contrast_results" in st.session_state:
            
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Contrast", "Typography", "Alt Text", "Headings", "Buttons/Links"])

    with tab1:
        st.subheader("Contrast Check")
        st.markdown("Measures the brightness between your text and its background and flags any combinations that fall below WCAG's minimum accessibility thresholds.")
        view = st.radio("Show:",["All", "Pass Only","Fail Only"], index = 0, horizontal = True , key="contrast_view")
        
        results = st.session_state.contrast_results

        if view == "All":
            df = build_contrast_all_df(results)
        elif view == "Pass Only":
            df = build_contrast_pass_df(results)
        else:  
            df = build_contrast_fail_df(results)

        if df.empty:
            st.info({ "All": "No contrast issues!", "Pass Only": "No passing rows (all failed)!", "Fail Only": "No failing rows (all passed)!"}[view])
        
        else:
            st.dataframe(df.reset_index(drop=True))

    with tab2:
        st.subheader("Typography Check")
        st.markdown("Verifies that all text is at least 16 px—the commonly accepted baseline for readability—"
        "since WCAG doesn't mandate an exact pixel size; any smaller font is flagged as a warning.")

        
        view = st.radio(
        "Show:",
        ["All", "Pass Only", "Warning Only","Fail Only"],
        index=0,
        horizontal=True,
        key="typo_view")
        results = st.session_state.typography_results

        if view == "All":
            df = build_typography_all_df(results)
        elif view == "Pass Only":
            df = build_typography_pass_df(results)
        elif view == "Warning Only":
            df = build_typography_warning_df(results)
        else:  
            df = build_typography_fail_df(results)
        
        if df.empty:
            empty_msgs = {"All": "No typography issues!", "Pass Only":  "No passing rows!", "Warning Only":  "No warnings, they all passed!","Fail Only":"No failed rows",}
            st.info(empty_msgs[view])
        else:
            st.dataframe(df.reset_index(drop=True))
        
    with tab3:
        st.subheader("Alt Text Check")
        st.markdown("Ensuring images have descriptive alternative text.")

        view = st.radio("Show:",["All", "Pass Only", "Fail Only"], index=0, horizontal=True, key="alt_view")


        results = st.session_state.alt_results
        if view == "All":
            df = build_alt_text_all_df(results)
        elif view == "Pass Only":
            df = build_alt_text_pass_df(results)
        else: 
            df = build_alt_text_fail_df(results)

        if df.empty:
            empty_msgs = {"All": "No alt-text results!", "Pass Only":  "No passing rows!", "Fail Only":  "No failing rows!",}
            st.info(empty_msgs[view])
        else:
            st.dataframe(df.reset_index(drop=True))
        
    
    with tab4:
        st.subheader("Heading Structure Check")
        st.markdown("Checking heading hierarchy for structure and accessibility.")

        heading_warnings = st.session_state.heading_warnings

        if not heading_warnings:
            st.info("All headings are in good order!")
        else:
            st.markdown("**Heading structure warnings:**")
        for warning in heading_warnings:
            st.markdown(f"- {warning}")
    with tab5:
        st.subheader("Buttons and Links Check")
        st.markdown("Validating that all buttons and links have accessible labels or aria-labels.")

        view = st.radio("Show:", ["All", "Pass Only", "Fail Only"], index=0, horizontal=True, key="button_view")

        results = st.session_state.button_results

        if view == "All":
            df = build_button_all_df(results)
        elif view == "Pass Only":
            df = build_button_pass_df(results)
        else:  
            df = build_button_fail_df(results)
        

        if df.empty:
            empty_msgs = {"All": "No buttons/links to show.", "Pass Only": "No passing buttons/links!", "Fail Only": "No failing buttons/links!"}
            st.info(empty_msgs[view])
        else:
            st.dataframe(df.reset_index(drop=True))