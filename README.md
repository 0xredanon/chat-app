Secure Chat Room
A secure client-server chat application built with Python, featuring encrypted communication, user authentication, and an admin panel for managing chat history. The client uses a GUI built with customtkinter, and the server stores messages in a SQLite database.
Features

User authentication with username and password.
Encrypted messages using the cryptography library.
Admin panel to view registered users and clear chat history.
Real-time chat with timestamped messages.
Thread-safe client handling on the server.
Logging for debugging client and server operations.

Prerequisites

Python 3.12 or higher
SQLite (included with Python)
pip for installing dependencies

Setup
1. Clone the Repository
git clone <repository-url>
cd chat_room

2. Install Dependencies
Install required Python packages:
pip install -r requirements.txt

3. Set Environment Variables
Set the encryption key for secure communication (use the same key for client and server):
export ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

On Windows:
set ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

4. Initialize the Database
Run the setup script to create the SQLite database and schema:
bash setup.sh

5. Run the Server
Start the server in one terminal:
cd server
python server.py

6. Run the Client
Start the client in another terminal:
cd client
python main.py

Usage

Login or Register:

Enter a username (3-32 characters) and password (6+ characters) in the login window.
Click "Register" to create a new account or "Login" to access an existing one.


Chat:

Type messages in the text box and press Enter or click "Send".
Messages are displayed with timestamps and session IDs.


Admin Features (for admin user):

Click "Admin Panel" to access admin tools.
Use "View Users" to see all registered usernames.
Use "Clear Chat History" to delete all messages.


Exit:

Close the GUI window and confirm the quit prompt.



Project Structure
chat_room/
├── client/
│   ├── gui.py
│   ├── main.py
│   ├── network.py
│   └── utils.py
├── server/
│   ├── config.py
│   ├── crypto.py
│   ├── db.py
│   ├── handler.py
│   └── server.py
├── database/
│   ├── schema.sql
│   └── seed.py
├── .gitignore
├── CHANGELOG.md
├── README.md
├── requirements.txt
└── setup.sh

Troubleshooting

Decryption Error: Ensure the ENCRYPTION_KEY is set identically for both client and server.
Connection Error: Verify the server is running on localhost:12345 and no firewall is blocking the port.
Database Error: Check that database/schema.sql exists and is readable.
Logs: Check chat.log (if enabled) or console output for detailed error messages.

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a pull request.

License
MIT License (see LICENSE file for details).
