import asyncio
import logging
import constants
from aioconsole import ainput
from slixmpp import ClientXMPP
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class MessengerAccount(ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0077')  # In-Band Registration
        self.register_plugin('xep_0045')  # Multi-User Chat


        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("session_start", self.messaging_app)
        self.add_event_handler("failed_auth", self.failed_auth)



    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        xmpp.send_message('admin@alumchat.xyz', 'hello', mtype='chat')


    def failed_auth(self, event):
        quit()

    def message(self, event):
        xmpp.send_message('admin@alumchat.xyz', 'hello', mtype='chat')

    def message2(self):
        xmpp.send_message('admin@alumchat.xyz', 'hello', mtype='chat')

    def validate_input(self, option):
        try:
            option = int(option)
            if 8 >= option >= 1:
                return option
            return False
        except ValueError:
            return False

    async def messaging_app(self, event):

        running = True
        while running:
            option = int(input(constants.MAIN_MENU))
            print("captured option", option)
            if option == 1:
                print("logged out")
                await self.disconnect()
                running = False
            if option == 2:
                self.delete_account()
            if option == 3:
                self.show_users_contacts()
            if option == 4:
                self.add_user_to_contacts()
            if option == 5:
                username = await ainput("Username to send message to\n>> ")
                message_destinatary = f"{username}@alumchat.xyz"
                print(message_destinatary, "the message destinatary")
                message = await ainput("Message content\n>> ")
                self.send_message(message_destinatary, message, mtype='chat')
            if option == 6:
                self.start_group_chat()
            if option == 7:
                self.change_presence_message()

            else:
                print("Invalid option")

    def end_session(self):
        self.disconnect()

    def show_users_contacts(self):
        roster = yield from self.get_roster()
        print(roster, "the roster")

        pass
    def change_presence_message(self):
        #send_prescence
        self.make_presence(pstatus="Hi this is my new status")

    def add_user_to_contacts(self):
        # Subscribe
        username = input("Username to add as a contact\n>> ")
        self.send_presence_subscription(pto=f"{username}@alumchat.xyz", pfrom='echobot@alumchat.xyz')

    def start_conversation(self):
        username = input("Username to send message to\n>> ")
        message = input("Message content\n>> ")
        self.send_message(f"{username}@alumchat.xyz", message, mtype='chat')
        pass

    def start_group_chat(self):
        pass

    def delete_account(self):
        engine = self.Iq()
        engine['register']['remove'] = True
        pass


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = MessengerAccount('echobot@192.168.56.1', 'eco')
    xmpp['feature_mechanisms'].unencrypted_plain = True
    xmpp.register_plugin('xep_0199')
    xmpp.connect()
    print("Conectado!")
    xmpp.process()
    xmpp.disconnect()

