from datetime import datetime, timedelta
from imbox import Imbox
import json
import os
import re

class CopeMail:
    def __init__(self, 
                 credentials_path: str,
                 host: str = 'imap.gmail.com',
                 consciousness_lvl: int = 1):
        
        with open(credentials_path, 'r') as f:
            credentials_data = json.load(f)

        self.host = host
        self.email = credentials_data['email']
        self.password = credentials_data['google_password']

        self.attachments = 'attachments'
        self.con_lvl = consciousness_lvl

    # IMPLEMENTAR mark_seen(uid)
    def get_attachments(self, date_since: str = None):
        # Variables for saving error
        dateprint = datetime.now().strftime("%Y_%m_%d_%H:%M_")
        error_counter = 0
        session_counter = 0

        if not os.path.exists(self.attachments):
            os.mkdir(self.attachments)

        with Imbox(self.host, username=self.email, password=self.password) as imbox:
            messages = imbox.messages(folder="inbox", date__gt=date_since,  raw='has:attachment')
        
            for uid, message in messages:
                # imbox.mark_seen(uid)
                if message.attachments:
                    sender_email = message.sent_from[0]["email"]

                    # Extract domain from sender's email and check if domain name is ok for creating folder
                    domain = sender_email.split('@')[1].split('.')[0]
                    domain = self.__filter_name(domain)

                    # Create subdirectory based on domain if it doesn't exist
                    domain_dir = os.path.join(self.attachments, domain)
                    if not os.path.exists(domain_dir):
                        os.mkdir(domain_dir)

                    for attachment in message.attachments:
                        # Save attachments to the designated domain subdirectory
                        file_data = attachment.get('content')
                        filename = self.__filter_name(attachment.get('filename'))

                        if filename == '':
                            filename = dateprint + str(error_counter) + '.pdf'
                            error_counter += 1

                        filepath = os.path.join(domain_dir, filename)

                        with open(filepath.replace('\r', '').replace('\n', '').replace('\t', ''), "wb") as f:
                            f.write(file_data.read())

                        match self.con_lvl:
                            case 1:
                                pass
                            case 2:
                                pass
                            case 3:
                                print(f"Saved attachment {filename} for message {uid} from {sender_email}")
                                print(f'\tPATH: {filepath}\n')

                        session_counter += 1

    def __filter_name(self, name):
        # Define a regular expression pattern to match disallowed characters
        disallowed_chars = r'[<>:"/\\|?*]'
        
        # Remove disallowed characters using the re.sub() function
        clean_name = re.sub(disallowed_chars, '', name)
    
        return clean_name


if __name__ == '__main__':
    # Caso queira testar a classe, não é necessário fazer o Fetch de todos os emails.
    # Então executamos só nos ultimos 7 dias, que é o tempo suposto do script ser rodado
    TESTING_CLASS = True

    if TESTING_CLASS:
        # Calculate the datetime 7 days before
        date_since = datetime.now() - timedelta(days=7)
    else:
        date_since = None
           
    # Pega as credenciais e aplica a unica função da classe
    Mailer = CopeMail('creds.json', consciousness_lvl=3)
    Mailer.get_attachments(date_since)
    