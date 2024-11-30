# Emailer - Automated Email Solution 📧

**Made with ❤️ by [Jaweria](https://jaweria-batool.vercel.app/)**

## Overview
Emailer is a tool designed to automate personalized email sending for freelance writers. It:
- Scrapes company websites for insights.
- Generates unique email templates to reduce spam risk.
- Sends tailored emails to multiple companies.

## Features
- 📥 Upload a list of companies in an Excel file.
- 🌐 Automatically analyze company websites.
- 📝 Generate unique, personalized email content.
- ✉️ Send emails directly via Gmail.

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/emailer.git
   cd emailer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Gmail credentials:
   - Enable **2-Step Verification** and create an **App Password**:
     1. Go to [Google Account Security](https://myaccount.google.com/security).
     2. Enable **2-Step Verification**.
     3. Generate an **App Password** under "App Passwords."
   - Add your email and password to a `.env` file:
     ```plaintext
     EMAIL_ADDRESS=your_email@gmail.com
     EMAIL_PASSWORD=your_generated_app_password
     ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Excel File Format
Your Excel file should have these columns:
- `Company Name`
- `Website URL`
- `Email ID`

## Future Versions
- Enhanced AI-based text generation for better personalization.
- Advanced analytics for email performance.

---

![Made with Love](https://media.giphy.com/media/3o6MbbZ3dqAHmOjQ8o/giphy.gif)

---
