import os
import smtplib

from dotenv import load_dotenv

load_dotenv()
ADMINEMAIL = os.getenv("ADMINEMAIL")
PASSWORD = os.getenv("PASSWORD")
COMPANY_NAME = os.getenv("COMPANY_NAME")


def send_email(to_addr, subject, html_content):
    sender = f"{COMPANY_NAME} <{ADMINEMAIL}>"
    msg = f"From: {sender}\r\nTo: {to_addr}\r\nSubject: {subject}\r\nContent-Type: text/html\r\n\r\n{html_content}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(ADMINEMAIL, PASSWORD)
    server.sendmail(sender, to_addr, msg)
    server.quit()


# Determine color based on the price
def get_price_color(price):
    if price < 50:
        return "#27ae60"
    elif price < 100 and price >= 50:
        return "#f39c12"
    elif price < 200 and price >= 100:
        return "#6f32a8"
    elif price < 300 and price >= 200:
        return "#3498db"
    else:
        return "#07bbe3"


def package_email_html(package_name, package_price, contents_list):
    price_color = get_price_color(package_price)
    return f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        max-width: 600px;
                        margin: auto;
                    }}
                    h2 {{
                        color: #2c3e50;
                        font-size: 1.8em;
                        margin-bottom: 10px;
                    }}
                    p {{
                        color: #7f8c8d;
                        line-height: 1.6;
                        margin: 10px 0;
                    }}
                    ul {{
                        padding-left: 20px;
                    }}
                    li {{
                        margin-bottom: 10px;
                        color: #34495e;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 0.85em;
                        color: #bdc3c7;
                        border-top: 1px solid #ecf0f1;
                        padding-top: 10px;
                    }}
                    .highlight {{
                        font-weight: bold;
                    }}
                    .price {{
                        font-size: 1.2em;
                        color: {price_color};
                    }}
                    .dependency {{
                        font-size: 0.8em;
                        color: #7f8c8d;
                        margin-left: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="container payment-confirmation">
                    <h2>Thank you for your payment!</h2>
                    <p>You have successfully purchased the <span class="highlight price">{package_name}</span> package for <span class="price">${package_price} </span>.</p>
                    <p><strong>Here are the contents of the package:</strong></p>
                    <ul>
                        {''.join(f'<li>{content}</li>' for content in contents_list)}
                    </ul>
                    <p>We hope you enjoy your purchase! Feel free to explore our <a href="/special-offers" class="special-offers-link">special offers</a> for more exclusive deals.</p>
                    <div class="footer">
                        <p>If you have any questions or need assistance, please contact our friendly support team at <a href="flori.bica@fti.edu.al" class="support-email">flori.bica@fti.edu.al</a>.</p>
                    </div>
                </div>
            </body>
            </html>
            """


def account_email_html(full_name, username, password):
    return f"""
    <html>
    <head>
            <style>
                    body {{
                            font-family: Arial, sans-serif;
                            color: #333;
                            line-height: 1.6;
                    }}
                    .container {{
                            padding: 20px;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            background-color: #f5f5f5;
                            width: 80%;
                            margin: auto;
                    }}
                    .header {{
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            border-radius: 8px 8px 0 0;
                    }}
                    .content {{
                            padding: 20px;
                    }}
                    table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                    }}
                    td {{
                            padding: 10px;
                            border: 1px solid #ddd;
                    }}
                    .highlight {{
                            background-color: #f9f9f9;
                    }}
                    .warning {{
                            color: #d9534f;
                    }}
                    .footer {{
                            margin-top: 20px;
                            font-size: 0.9em;
                            color: #777;
                    }}
            </style>
    </head>
    <body>
            <div class="container">
                    <div class="header">
                            <h1>Welcome to WellCare Hospital</h1>
                    </div>
                    <div class="content">
                            <p>Hello <strong>{full_name}</strong>,</p>
                            <p>Please use the following information to log in to your account:</p>
                            <table>
                                    <tr class="highlight">
                                            <td><strong>Username:</strong></td>
                                            <td>{username}</td>
                                    </tr>
                                    <tr>
                                            <td><strong>Password:</strong></td>
                                            <td>{password}</td>
                                    </tr>
                            </table>
                            <p class="warning">Please change your password after you log in.</p>
                            <p>Best regards,</p>
                            <p><em>WellCare Hospital</em></p>
                    </div>
                    <div class="footer">
                    <p>This email was sent automatically. Please do not reply.</p>
                    </div>
            </div>
    </body>
    </html>
    """


def confirm_code_html(confirm_code):
    return f"""
    <html>
    <head>
            <style>
                    body {{
                            font-family: Arial, sans-serif;
                            color: #333;
                            line-height: 1.6;
                    }}
                    .container {{
                            padding: 20px;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            background-color: #f5f5f5;
                            width: 80%;
                            margin: auto;
                    }}
                    .header {{
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            border-radius: 8px 8px 0 0;
                    }}
                    .content {{
                            padding: 20px;
                    }}
                    table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                    }}
                    td {{
                            padding: 10px;
                            border: 1px solid #ddd;
                    }}
                    .highlight {{
                            background-color: #f9f9f9;
                    }}
                    .warning {{
                            color: #d9534f;
                    }}
                    .footer {{
                            margin-top: 20px;
                            font-size: 0.9em;
                            color: #777;
                    }}
            </style>
    </head>
    <body>
            <div class="container">
                    <div class="header">
                            <h1>Welcome to WellCare Hospital</h1>
                    </div>
                    <div class="content">
                            <p>Hello,</p>
                            <p>Your confirmation code for password reset is:</p>
                            <table>
                                    <tr class="highlight">
                                            <td><strong>Confirmation Code:</strong></td>
                                            <td>{confirm_code}</td>
                                    </tr>
                            </table>
                            <p class="warning">Please do not share this code with anyone.</p>
                            <p>Best regards,</p>
                            <p><em>WellCare Hospital</em></p>
                    </div>
                    <div class="footer">
                    <p>This email was sent automatically. Please do not reply.</p>
                    </div>
            </div>
    </body>
    </html>
    """


def reset_password_html(username, password):
    return f"""
    <html>
    <head>
            <style>
                    body {{
                            font-family: Arial, sans-serif;
                            color: #333;
                            line-height: 1.6;
                    }}
                    .container {{
                            padding: 20px;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            background-color: #f5f5f5;
                            width: 80%;
                            margin: auto;
                    }}
                    .header {{
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            border-radius: 8px 8px 0 0;
                    }}
                    .content {{
                            padding: 20px;
                    }}
                    table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                    }}
                    td {{
                            padding: 10px;
                            border: 1px solid #ddd;
                    }}
                    .highlight {{
                            background-color: #f9f9f9;
                    }}
                    .warning {{
                            color: #d9534f;
                    }}
                    .footer {{
                            margin-top: 20px;
                            font-size: 0.9em;
                            color: #777;
                    }}
            </style>
    </head>
    <body>
            <div class="container">
                    <div class="header">
                            <h1>Welcome to WellCare Hospital</h1>
                    </div>
                    <div class="content">
                            <p>Hello,</p>
                            <p>Your new password is:</p>
                            <table>
                                            <tr>
                                                    <td><strong>Username:</strong></td>
                                                    <td>{username}</td>
                                            </tr>
                                            <tr class="highlight">
                                                    <td><strong>Password:</strong></td>
                                                    <td>{password}</td>
                                            </tr>
                                            
                            </table>
                            <p class="warning">Please change your password after you log in.</p>
                            <p>Best regards,</p>
                            <p><em>WellCare Hospital</em></p>
                    </div>
                    <div class="footer">
                    <p>This email was sent automatically. Please do not reply.</p>
                    </div>
            </div>
    </body>
    </html>
    """
