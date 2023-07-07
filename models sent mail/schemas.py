import email

from config import HOST, USERNAME, PASSWORD, PORT, MailBody
from ssl import create_default_context
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from jinja2 import Template
# create render template to mail
def render_template(template_path: str, **kwargs) -> str:
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    template = Template(template_content)
    return template.render(**kwargs)
#function send mail with content and sender for flow account
def send_mail(data: dict | None = None):
    msg = MailBody(**data)

    # Render the email body from the template
    template_data = {
        "subject": msg.subject,
    }
    msg.body = render_template("./templates/MessageType.html", **template_data)
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = USERNAME
    message["To"] = ",".join(msg.to)
    message["Subject"] = msg.subject
    ctx = create_default_context()
    # Attach the body to the message as HTML
    message.attach(MIMEText(msg.body, "html"))
# create the step check information for https
    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}
    finally:
        server.close()
