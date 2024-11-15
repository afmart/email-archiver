Set Up Your Environment

Ensure Python 3.x is installed on your system.
Create a virtual environment and activate it:

python3 -m venv imap_env
source imap_env/bin/activate  # On Windows: imap_env\Scripts\activate

*Install Requirements*


pip install -r requirements.txt


Prepare the Configuration File (Optional):

    If you prefer using a configuration file, create a file (e.g., config.ini) with the following structure:

[IMAP]
server = mail.example.com
username = your_email@example.com
folder = Archive


*USAGE*

To run the script with command-line arguments:

    python imap_archive_script.py --server eden.dei.uc.pt --username afmart --folder Archives

To use a configuration file:

    python imap_archive_script.py --config config.ini

