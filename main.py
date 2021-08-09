import slixmpp
from MessengerAccount import MessengerAccount
from client import Client
import logging

def main():


    start_message = """
    Welcome to the secret internet of the robots.
    
    Select an option:
    1 -> Register a new account
    2 -> Log in
    """
    menu = """
    Select an option to proceed:
    1 -> Log out
    2 -> Delete account
    3 -> Show all users & contacts
    4 -> Add a user to contacts
    5 -> Start a conversation
    6 -> Start a group chat
    7 -> Define presence message
    >> 
    """
    while True:
        print(start_message)
        input(">> ")




    print("Hello world!")


if __name__ == '__main__':
    main()
