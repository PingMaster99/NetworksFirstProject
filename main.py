import slixmpp
from MessengerAccount import MessengerAccount
from client import Client
import logging
import constants
from registration import Registration

def main():
    running = True
    while running:
        option = input(constants.APP_MENU)

        try:
            option = int(option)
        except ValueError:
            print("Incorrect option")
            continue

        if option == 1:
            jid = input("Username: ")
            password = input("Password: ")
            jid = f"{jid}@192.168.56.1"     #TODO: change this to alumchat

            xmpp = Registration(jid, password)
            xmpp.register_plugin('xep_0030')  # Service Discovery
            xmpp.register_plugin('xep_0004')  # Data forms
            xmpp.register_plugin('xep_0066')  # Out-of-band Data
            xmpp.register_plugin('xep_0077')  # In-band Registration
            xmpp['xep_0077'].force_registration = True
            xmpp.connect()
            xmpp.process(forever=False)

        elif option == 2:
            jid = input("Username: ")
            password = input("Password: ")
            xmpp = MessengerAccount(jid, password)
            xmpp.connect()
            xmpp.process()

        elif option == 3:
            print("Thank you for using the XMPP secret chat")
            exit()


if __name__ == '__main__':
    main()
