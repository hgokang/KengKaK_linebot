from Config import username,password
import imaplib
import email

class GmailClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")

    def login(self):
        self.imap.login(self.username, self.password)

    def select_inbox(self):
        self.imap.select("INBOX")

    def search_emails(self, criteria):
        status, message_ids = self.imap.search(None, criteria)
        print(status)
        return message_ids[0].split()

    def fetch_email(self, message_id):
        status, message_data = self.imap.fetch(message_id, "(RFC822)")
        raw_email = message_data[0][1]
        print(status)
        return email.message_from_bytes(raw_email)

    def save_email_content(self, msg):
        content = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                content += part.get_payload(decode=True).decode("utf-8", errors="ignore")
        
        with open("netflix.txt", "w", encoding="utf-8") as file:
            file.write(content + "\n\n")

    def extract_access_code(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if "https://www.netflix.com/account/travel/verify?nftoken=" in line:
                    link = line.strip()
                    with open("netflix_link.txt", "w", encoding="utf-8") as output_file:
                        output_file.write(link)
                    break
            else:
                print("ไม่พบลิงก์ที่ต้องการ")
                return("ไม่พบลิงก์ที่ต้องการ")

    def close(self):
        self.imap.close()

    def logout(self):
        self.imap.logout()

client = GmailClient(username, password)
client.login()
client.select_inbox()

criteria = '(SUBJECT "Netflix")'

criteria_bytes = criteria.encode('utf-8')

message_ids = client.search_emails(criteria_bytes)
print(len(message_ids))
msg = client.fetch_email(message_ids[len(message_ids)-1])
client.save_email_content(msg)

file_path = "netflix.txt"
client.extract_access_code(file_path)

client.close()
client.logout()