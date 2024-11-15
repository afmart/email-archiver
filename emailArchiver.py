import imaplib
import email
from email.header import decode_header
import datetime
import argparse
import configparser
import getpass

# Function to read configuration from a file
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['IMAP']


def connect_to_mailbox(server, username, password):
    # Connect to the server
    mail = imaplib.IMAP4_SSL(server)
    # Login to your account
    mail.login(username, password)
    return mail

def create_archive_folder(mail, folder_name):
    # Create the archive folder if it doesn't exist
    status, folders = mail.list()
    if folder_name not in str(folders):
        mail.create(folder_name)

def list_mail_folders(mail):
    # List all email folders
    #status, folders = mail.list(directory="INBOX")
    #if status == 'OK':
    #    print("Available mail folders:")
    #    for folder in folders:
    #        print(folder.decode())      
    status, folders = mail.lsub()
    if status == 'OK':
        print("Available mail folders:")
        print("/INBOX")
        for folder in folders:
            print(folder.decode())
    else:
        print("Failed to list mail folders.")

def archive_emails(mail, archive_folder):
    mail.select('INBOX')
    result, data = mail.search(None, 'ALL')
    if result != 'OK':
        print("Failed to search emails.")
        return

    email_ids = data[0].split()
    year_count = {}
    current_year = datetime.datetime.now().year

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        if result != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            email_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            email_year = email_date.year
            if email_year < current_year:
                year_count[email_year] = year_count.get(email_year, 0) + 1

    for year, count in year_count.items():
        print(f"{count} emails will be archived to {archive_folder}/{year}.")

    confirm = input("Proceed with archiving? (y/n): ").lower()
    if confirm != 'y':
        print("Archiving cancelled.")
        return

    move_count = 0
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        if result != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            email_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            email_year = email_date.year
            if email_year < current_year:
                archive_path = f'"{archive_folder}/{email_year}"'
                mail.copy(email_id, archive_path)
                mail.store(email_id, '+FLAGS', '\\Deleted')
                move_count += 1

                # Show progress for every 10 emails moved
                if move_count % 10 == 0:
                    print(f"{move_count} emails archived so far...")

    mail.expunge()
    print("Archiving completed.")


def main():
    parser = argparse.ArgumentParser(description="IMAP Email Management Script.")
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    parser.add_argument('--server', type=str, help='IMAP server address')
    parser.add_argument('--username', type=str, help='Email username')
    parser.add_argument('--folder', type=str, help='Archive folder path')
    args = parser.parse_args()

    # Check if parameters are provided via arguments or config file
    if args.server and args.username and args.folder:
        IMAP_SERVER = args.server
        USERNAME = args.username
        ARCHIVE_FOLDER = args.folder
        PASSWORD = getpass.getpass(prompt='Enter your email password: ')
    elif args.config:
        config = read_config(args.config)
        IMAP_SERVER = config.get('server')
        USERNAME = config.get('username')
        ARCHIVE_FOLDER = config.get('folder')
        PASSWORD = config.get('password', getpass.getpass(prompt='Enter your email password: '))
    else:
        print("Error: Either --server, --username, and --folder or --config must be provided.")
        return

    # Connect and login to the mail server
    mail = connect_to_mailbox(IMAP_SERVER, USERNAME, PASSWORD)

    try:
        while True:
            print("\nSelect an option:")
            print("1. List IMAP folders")
            print("2. Archive emails")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                list_mail_folders(mail)
            elif choice == '2':
                archive_emails(mail, ARCHIVE_FOLDER)
            elif choice == '3':
                print("Exiting.")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        # Logout from the server
        mail.logout()


if __name__ == "__main__":
    main()
