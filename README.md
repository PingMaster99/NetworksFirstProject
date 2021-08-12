# NetworksFirstProject
CLI client that supports the XMPP protocol. Includes account administration and communication.

Connects to the server: ```alumchat.xyz```

#### NOTE: You can also test the program locally by changing ```SERVER = <Your Ipv4>``` in the constants.py file.  

## Requirements
- asyncio
- aiconsole
- slixmpp
- logging
- Python 3.7+

## Installation
1. Clone this repository: ```git clone https://github.com/PingMaster99/NetworksFirstProject```
2. Run the command: ```python main.py``` in a command window on the folder location
3. Follow on screen instructions
4. To edit the logging configuration, set LOGGING to True in constants.py

## Functionalities
### Account administration
- Register a new account
- Log in
- Log off
- Delete an account

### Communication
- Show all users
- Add a user to contacts
- Show contact details of users
- Send a message to a user/contact
- Participate in group chats
- Define presence message
- Notifications
- Files

print("Thank you for reading this :)")
