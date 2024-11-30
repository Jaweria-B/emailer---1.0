import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText

def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df


def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from the website
        all_text = " ".join([p.get_text() for p in soup.find_all('p')])
        
        # Analyze text (basic example: find keywords)
        keywords = ["content", "writing", "blog", "freelance", "editorial"]
        matches = [word for word in keywords if word in all_text.lower()]
        
        return {
            "keywords_found": matches,
            "content_snippet": all_text[:300]  # First 300 characters
        }
    except Exception as e:
        return {"error": str(e)}


email_template = """
Hello {{ company_name }},

I noticed your focus on {{ keywords }} while exploring {{ website }}. It seems like {{ improvement_area }} could benefit from well-crafted content.

As a freelance writer, I specialize in {{ specialization }} and have experience in {{ relevant_experience }}. Here's a link to some of my work: {{ profile_link }}

Looking forward to collaborating and helping {{ company_name }} grow.

Best regards,  
Jaweria
"""

def generate_email(data):
    template = Template(email_template)
    return template.render(data)


def send_email(to_address, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_address = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body, 'plain')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_address, password)
        server.send_message(msg)


def process_companies(file_path):
    companies = read_excel(file_path)
    for _, company in companies.iterrows():
        website_data = scrape_website(company['Website URL'])
        
        if "error" in website_data:
            print(f"Error scraping {company['Website URL']}: {website_data['error']}")
            continue
        
        email_body = generate_email({
            "company_name": company['Company Name'],
            "keywords": ", ".join(website_data['keywords_found']),
            "website": company['Website URL'],
            "improvement_area": "expanding blog outreach",  # Example improvement
            "specialization": "freelance writing and content creation",
            "relevant_experience": "creating impactful blogs for tech and startups",
            "profile_link": "https://www.linkedin.com/in/jaweria-batool/"  # Replace with dynamic logic
        })

        send_email(company['Email ID'], "Freelance Writing Opportunity", email_body)

process_companies("./companies.xlsx")
