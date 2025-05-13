Changelog

All notable changes to the Chat Room project will be documented in this file.

[1.0.0] - 2025-05-13

Added





Initial implementation of a secure chat application with client-server architecture.



Authentication system with username/password using SQLite database.



Encryption for messages using the cryptography library with Fernet.



Admin panel for viewing users and clearing chat history.



GUI built with customtkinter for user interaction.



Logging for debugging server and client operations.

Fixed





Resolved encryption key mismatch by enforcing ENCRYPTION_KEY environment variable.



Fixed client disconnection issues ([WinError 10054]) after authentication.



Improved client-side authentication handling with retry logic and better error messages.



Corrected typo in gui.py (update_queue to message_queue).



Enhanced server-side logging to capture client disconnections.



Prevented client application crash by showing connection errors in GUI instead of exiting.



Added thread-safe client handling in handler.py using a Lock.

Changed





Updated main.py to initialize GUI before network connection for better error handling.



Modified crypto.py to log encryption key for debugging and raise ValueError if unset.



Improved network.py to handle decryption failures gracefully.



Added PING/PONG support in handler.py for reliable connection checking.