# Accesibility Checker (User's Guide)
Accessibility Checker is a web-based tool for testing one page at a time accessibility against WCAG standards for contrast, typography, alt text, headings, and buttons.

## Before Running the App 
1. Create a virtual environment (highly recommended to avoid package conflicts).
2. Install required dependencies pip install -r requirements.txt
   
## Let's Start the App 
Here is a step by step!
1. Open your terminal make sure you are in your virtual enviroment and run: streamlit run GUI.py
2. Enter the full URL of the webpage you want to audit (must start with http:// or https://).
3. Click the “Run Accessibility Audit” button.
4. Review the results are shown in table format with tabs:
    - Contrast: Check if text and background colors meet WCAG AA/AAA standards.
    - Typography: Highlights fonts smaller than 16px.
    - Alt Text: Flags images missing alt text.
    - Headings: Identifies missing or multiple H1 tags and heading level skips.
    - Buttons/Links: Shows buttons and links that lack labels or aria-label attributes.
5. Optionally you can download the results as a CSV file.
6. If you want to do another page just simple insert a new URL and run it again. 

ADD PICTURES OF SCREENSHO Also addd the importals useful notes for when error occurs.  
### App Homescreen 
<p align="left">
  <img src="https://github.com/user-attachments/assets/2466f961-76c8-4135-b685-6977e7872805" width="500" alt="App launch screen">
</p>

### After Page has Succesfully loaded you should get an output similar to this one. 
<p align="center">
  <img src="https://github.com/user-attachments/assets/287501b2-665c-4d91-9228-3c9abf297f6b" width="500" alt="Audit results tab">
</p>

