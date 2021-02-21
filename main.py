from bs4 import BeautifulSoup
import config
from datetime import datetime, timedelta
from imap_tools import MailBox

YESTERDAY = (datetime.now().date() - timedelta(days=1)).strftime("%d-%b-%Y")

with MailBox(config.mail_imap).login(config.mail_user, config.mail_passwd, initial_folder='INBOX') as mailbox:
    messages = [msg for msg in mailbox.fetch(f"SINCE 20-Feb-2021") if msg.subject == "Код подтверждения"]
    webpage = messages[len(messages) - 1].html
    soup = BeautifulSoup(webpage, "html.parser")
    code = soup.select_one(".paragraph > b").text
    print(code)
