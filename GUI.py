import streamlit as st
from url_validator import valid_url, is_reachable
from page_loader import load_page_data
from accesibility_analyzer import check_contrast, check_typography, check_alt_text, check_heading_structure, check_link_buttons
from result_formatter import (build_contrast_df, build_typography_df, build_alt_text_df, build_heading_df, build_button_df)
import time


st.set_page_config(page_title="Accessibility Analyzer", layout="centered")


st.title("Accessibility Analyzer")

st.write("Test your website's accessibility against WCAG standards for contrast, typography, headings, and interactive elements.")

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
            full_col.success("✅ Site is reachable!") 

            with st.spinner("Loading page data..."):
                data = load_page_data(url_input)
                html = data["html"]
                texts = data["texts"]
                headings = data["headings"]
                images = data["images"]
                buttons = data["buttons"]

            full_col.success("✅ Page data loaded successfully!")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Contrast", "Typography", "Alt Text", "Headings", "Buttons/Links"])

            with tab1:
                st.subheader("Contrast Check")
                st.caption("Evaluating text and background color combinations for WCAG contrast compliance.")
                contrast_results = check_contrast(texts)
                df_contrast = build_contrast_df(contrast_results)
                if df_contrast.empty:
                    st.info("No contrast issues!")
                else:
                    df_contrast = df_contrast.reset_index(drop=True)
                    st.dataframe(df_contrast)

            with tab2:
                st.subheader("Typography Check")
                st.caption("Verifying font sizes to ensure readability and WCAG compliance (minimum 16px).")
                typography_results = check_typography(texts)
                df_typo = build_typography_df(typography_results)
                if df_typo.empty:
                    st.info("No typography issues!")
                else:
                    df_typo  = df_typo.reset_index(drop=True)
                    st.dataframe(df_typo)
            
            with tab3:
                st.subheader("Alt Text Check")
                st.caption("Ensuring images have descriptive alternative text.")
                alt_results = check_alt_text(images)
                df_alt = build_alt_text_df(alt_results)
                if df_alt.empty:
                    st.info("No alt-text issues!")
                else:
                    df_alt  = df_alt.reset_index(drop=True)
                    st.dataframe(df_alt)
            
            with tab4:
                st.subheader("Heading Structure Check")
                st.caption("Checking heading hierarchy for structure and accessibility.")
                heading_warnings = check_heading_structure(headings)

                if not heading_warnings:
                    st.info("All headings are in good order!")
                else:
                    st.markdown("**Heading structure warnings:**")
                    for warning in heading_warnings:
                        st.markdown(f"- {warning}")
            with tab5:
                st.subheader("Buttons and Links Check")
                st.caption("Validating that all buttons and links have accessible labels or aria-labels.")
                btn_results = check_link_buttons(buttons)
                df_buttons = build_button_df(btn_results)
                if df_buttons.empty:
                    st.info("All buttons have text or aria-labels.")
                else:
                    df_buttons = df_buttons.reset_index(drop=True)
                    st.dataframe(df_buttons)
