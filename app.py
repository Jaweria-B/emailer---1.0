from dotenv import load_dotenv
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
import random
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Email Template with Randomization
def generate_dynamic_email(data):
    greetings = [
        "Hello {{ company_name }},",
        "Hi {{ company_name }},",
        "Greetings {{ company_name }},"  
    ]
    
    openings = [
        "I noticed your focus on {{ keywords }} while exploring {{ website }}.",
        "While browsing {{ website }}, I came across your work on {{ keywords }}.",
        "Your expertise in {{ keywords }} caught my attention on {{ website }}."
    ]
    
    improvements = [
        "It seems like {{ improvement_area }} could benefit from well-crafted content.",
        "I believe I could assist in enhancing {{ improvement_area }} with impactful writing.",
        "There's potential to elevate {{ improvement_area }} with targeted content strategies."
    ]
    
    closings = [
        "Looking forward to collaborating and helping {{ company_name }} grow.",
        "Let’s discuss how I can contribute to {{ company_name }}'s success.",
        "Eager to explore collaboration opportunities with {{ company_name }}."
    ]
    
    closing_statements = [
        "Best regards,", 
        "Sincerely,", 
        "Warm regards,"
    ]
    
    # Combine all components into a Jinja2 template
    template_string = f"""{random.choice(greetings)}
    
    {random.choice(openings)} {random.choice(improvements)}
    
    {"As a freelance writer, I specialize in {{ specialization }} and have experience in {{ relevant_experience }}. Here's a link to some of my work: {{ profile_link }}"}
    {random.choice(closings)}
    
    {random.choice(closing_statements)}
    Jaweria
    """
    
    # Render the template with Jinja2
    jinja_template = Template(template_string)
    rendered_email = jinja_template.render(data)  # Make sure the data is passed properly
    
    return rendered_email

# Function to Scrape Website
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_text = " ".join([p.get_text() for p in soup.find_all('p')])
        
        # Check for keywords
        keywords = ["content", "writing", "blog", "freelance", "editorial"]
        matches = [word for word in keywords if word in all_text.lower()]
        
        # Default message if no keywords are found
        if not matches:
            matches = ["general writing services"]
        
        return {
            "keywords_found": matches,
            "content_snippet": all_text[:300]
        }
    except Exception as e:
        return {"error": str(e)}

# Email Sending Function
def send_email(to_address, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_address = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    print(f"Email Address: {os.getenv('EMAIL_ADDRESS')}")
    print(f"Password: {os.getenv('EMAIL_PASSWORD')}")


    msg = MIMEText(body, 'plain')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_address, password)
        server.send_message(msg)

# Main App
st.set_page_config(
    page_title="Emailer: Automate Personalized Emails",
    page_icon="📧",
    layout="centered",
)

st.title("📧 Emailer: Automate Personalized Emails")
st.markdown(
    """
    **Emailer** is a tool that helps automate personalized email generation and sending, specifically tailored for freelance writers.  
    *Made with ❤️ by [Jaweria](https://jaweria-batool.vercel.app/).*
    """
)

uploaded_file = st.file_uploader("📄 Upload Excel File (Companies List)", type=["xlsx"])

if uploaded_file:
    st.success("File uploaded successfully! Processing...")
    
    # Read Excel
    companies = pd.read_excel(uploaded_file)
    st.write("Here are the companies from your file:", companies.head())

    # Store the generated emails in a list for display and sending
    emails_to_send = []
    
    for _, company in companies.iterrows():
        website_data = scrape_website(company['Website URL'])
        
        if "error" in website_data:
            st.error(f"Error scraping {company['Website URL']}: {website_data['error']}")
            continue
        
        # Prepare email data with fallbacks
        # Prepare email data with fallbacks
        email_data = {
            "company_name": company['Company Name'],
            "keywords": ", ".join(website_data.get('keywords_found', [])) or "your expertise",
            "website": company['Website URL'],
            "improvement_area": "expanding blog outreach",
            "specialization": "freelance writing and content creation",
            "relevant_experience": "creating impactful blogs for tech and startups",
            "profile_link": "https://www.linkedin.com/in/jaweria-batool/"
        }

        email_body = generate_dynamic_email(email_data)
        emails_to_send.append({
            "to_address": company['Email ID'],
            "subject": f"Collaboration Opportunity with {company['Company Name']}",
            "body": email_body
        })

        st.text_area(f"Email for {company['Company Name']} ({company['Email ID']})", email_body, height=200)

    st.markdown("Once you're ready, run the script to send emails to all listed companies.")

    # Add a button to send the emails
    if st.button("Send Emails"):
        for email in emails_to_send:
            try:
                send_email(email['to_address'], email['subject'], email['body'])
                st.success(f"Email sent to {email['to_address']} successfully!")
            except Exception as e:
                st.error(f"Failed to send email to {email['to_address']}: {str(e)}")

    

st.markdown(
    """
    ### Notes:
    - Follow [these steps](https://support.google.com/accounts/answer/185833?hl=en) to enable Gmail App Passwords.
    - Ensure your credentials are stored securely in environment variables.
    """
)
