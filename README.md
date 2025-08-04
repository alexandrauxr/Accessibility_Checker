# Accesibility Checker (User's Guide)
Accessibility Checker is a web-based tool for testing one page at a time accessibility against WCAG standards for contrast, typography, alt text, headings, and buttons.

## Before Running the App 
1. Create a virtual environment (highly recommended to avoid package conflicts).
2. Install required dependencies pip install -r requirements.txt
   
## Let's Start the App 
Here is a step by step!
1. Open your terminal make sure you are in your virtual enviroment and run: streamlit run main.py
2. Enter the full URL of the webpage you want to audit (must start with http:// or https://).
3. Click the **“Run Accessibility Checker”** button.
4. Review the results shown in table format with tabs:
    - Contrast: Check if text and background colors meet WCAG AA/AAA standards.
    - Typography: Highlights fonts smaller than 16px.
    - Alt Text: Flags images missing alt text.
    - Headings: Identifies missing or multiple H1 tags and heading level skips.
    - Buttons/Links: Shows buttons and links that lack labels or aria-label attributes.
5. Optionally you can download the results as a CSV file.
6. If you want to do check another webpage just insert a new URL and run it again.

> [!TIP]
> If data fetching times out, simply click the **Run Accessibility Audit** button again. An error message will usually appear prompting you to retry, if it doesn't just click the button again. 


## App Screenshots 
<table> <tr> <td align="center"> <img src="https://github.com/user-attachments/assets/312496bb-f48d-46f4-87d7-550ced4a89a1" width="300" alt="Home screen with URL input"/> <br/> <sub><b>Home Screen</b></sub> </td> <td align="center"> <img src="https://github.com/user-attachments/assets/054691a1-7f39-44af-89be-39aa4d3f34b3" width="300" alt="Fetching data screen"/> <br/> <sub><b>Fetching Data</b></sub> </td> <td align="center"> <img src="https://github.com/user-attachments/assets/513fbd48-6884-4248-9244-4931dfcb20ee" width="300" alt="Results displayed in tabs"/> <br/> <sub><b>Results Displayed</b></sub> </td> </tr> </table>

