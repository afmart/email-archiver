Email Archiver script for email INBOX with too much emails, in Pyhton
=====================================================================

## 1. Set Up Your Environment

Ensure Python 3.x is installed on your system.
Create a virtual environment and activate it:
´´´Console
python3 -m venv imap_env
source imap_env/bin/activate  
# On Windows: imap_env\Scripts\activate
´´´

## 2. Install Requirements

´´´Console
pip install -r requirements.txt
´´´

## 3. Prepare the Configuration File (Optional):
If you prefer using a configuration file, create a file (e.g., config.ini) with the following structure:
´´´Console
[IMAP]
server = mail.example.com
username = your_email@example.com
folder = Archive
´´´

## 4. USAGE
To run the script with command-line arguments:
´´´Console
python imap_archive_script.py --server mail.example.com --username username --folder Archives
´´´

To use a configuration file:
´´´Console
python imap_archive_script.py --config config.ini
´´´
