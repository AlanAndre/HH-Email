from bs4 import BeautifulSoup
import config
from datetime import datetime, timedelta
from imap_tools import MailBox


def get_mail_since_yesterday():
    with MailBox(config.mail_imap).login(config.mail_user, config.mail_passwd, initial_folder='INBOX') as mailbox:
        yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%d-%b-%Y")
        return [msg for msg in mailbox.fetch(f"SINCE {yesterday}")]


def hh_mail_code():
    messages = [msg for msg in get_mail_since_yesterday() if
                (msg.subject == 'Код подтверждения' and msg.from_ == 'noreply@hh.ru')]
    if messages:
        webpage = messages[len(messages) - 1].html
        soup = BeautifulSoup(webpage, "html.parser")
        code = soup.select_one(".paragraph > b").text
        return code
    return 'No recent HH mails since yesterday'


if __name__ == '__main__':
    print(hh_mail_code())
