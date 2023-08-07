from imbox import Imbox
import json
import os

class CopeMail:
    def __init__(self, credentials_path: str):
        with open(credentials_path, 'r') as f:
            credentials = json.dumps(f)

        self.host = 'imap.gmail.com'
        self.email = credentials['email']
        self.password = credentials['password']
        self.attachments = 'attachments'

def email_logger(self, credentials_path):
    pass

def email_consumer(self, ):
    if not os.path.exists(self.attachments):
        os.mkdir(self.attachments)

    with Imbox(self.host, username=self.email, password=self.password) as imbox:
        messages = imbox.messages(folder="inbox", query="HAS attachment")
    
    for uid, message in messages:
        sender_email = message.sent_from[0]["email"]

        # Extract domain from sender's email
        domain = sender_email.split('@')[1]

        # Create subdirectory based on domain if it doesn't exist
        domain_dir = os.path.join(self.attachments, domain)
        if not os.path.exists(domain_dir):
            os.mkdir(domain_dir)

        for idx, attachment in enumerate(message.attachments):
            # Save attachments to the designated domain subdirectory
            file_data = attachment.get('content')
            filename = attachment.get('filename')
            filepath = os.path.join(domain_dir, filename)

            with open(filepath, "wb") as f:
                f.write(file_data)

            print(f"Saved attachment {filename} for message {uid} from {sender_email}")

def email_filter(self, ):
    pass



if __name__ == '__main__':
    pass   
    # = 'imap.gmail.com'
    # mail = Imbox(host, username=email, password=senha)