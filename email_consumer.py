from datetime import datetime, timedelta
from imbox import Imbox
import json
import os
import re

TESTING_CLASS = True

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
        
            try:
                for uid, message in messages:
                    # imbox.mark_seen(uid)
                    if message.attachments:
                        sender_email = message.sent_from[0]["email"]

                        # Extract domain from sender's email and check if domain name is ok for creating folder
                        domain = sender_email.split('@')[1].split('.')[0]
                        domain = self.filter_name(domain)

                        # Create subdirectory based on domain if it doesn't exist
                        domain_dir = os.path.join(self.attachments, domain)
                        if not os.path.exists(domain_dir):
                            os.mkdir(domain_dir)

                        for attachment in message.attachments:
                            # Save attachments to the designated domain subdirectory
                            file_data = attachment.get('content')
                            filename = self.filter_name(attachment.get('filename'))

                            if filename == '':
                                filename = dateprint + str(error_counter) + '.pdf'
                                error_counter += 1

                            filepath = os.path.join(domain_dir, filename)

                            try:
                                with open(filepath, "wb") as f:
                                    f.write(file_data.read())
                            except:
                                print("\t\t\tERRO:")
                                print(f"SENDER_EMAIL: {sender_email}")
                                print(f"DOMAIN: {domain}")
                                print(f"DOMAIN_DIR: {domain_dir}")
                                print(f"DOMAIN_DIR: {domain_dir}")
                                print(f"FILENAME: {filename}")
                                print(f"FILEPATH: {filepath}")
                                print(f"TITULO: {message.subject}")
                                quit()

                            if self.con_lvl >= 3:
                                print(f"Saved attachment {filename} for message {uid} from {sender_email}")
                                print(f'\t\tPATH: {filepath}')

                            session_counter += 1
            except:
                import pdb;pdb.set_trace()

    def filter_name(self, name):
        # Define a regular expression pattern to match disallowed characters
        disallowed_chars = r'[<>:"/\\|?*]'
        
        # Remove disallowed characters using the re.sub() function
        clean_name = re.sub(disallowed_chars, '', name)
    
        return clean_name


if __name__ == '__main__':
    if TESTING_CLASS:
        # Calculate the datetime 10 days before
        date_since = datetime.now() - timedelta(days=5)
    else:
        date_since = None
           
    Mailer = CopeMail('creds.json', consciousness_lvl = 3)
    Mailer.get_attachments(date_since)
    