import asyncio
import logging

from slixmpp import ClientXMPP
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class MessengerAccount(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("got_online", self.messaging_app)



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

    def messaging_app(self, event):
        menu = """
        Select an option to proceed:
        1 -> Log out
        2 -> Delete account
        3 -> Show all users & contacts
        4 -> Add a user to contacts
        5 -> Start a conversation
        6 -> Start a group chat
        7 -> Define presence message
        8 -> Exit
        >> """
        running = True
        while running:
            option = self.validate_input(input(menu))
            if option:
                if option == 1:
                    self.end_session()
                    running = False
                if option == 2:
                    self.delete_account()
                if option == 3:
                    self.show_users_contacts()
                if option == 4:
                    self.add_user_to_contacts()
                if option == 5:
                    self.start_conversation()
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
        self.send_presence_subscription(pto='admin@alumchat.xyz', pfrom='echobot@alumchat.xyz')

    def start_conversation(self):
        pass

    def start_group_chat(self):
        pass

    def delete_account(self):
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

