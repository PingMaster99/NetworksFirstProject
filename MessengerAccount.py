"""

Reference: https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/roster_browser.py
"""

import asyncio
import logging
import constants
from aioconsole import ainput
from slixmpp import ClientXMPP, exceptions
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class MessengerAccount(ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0059')  # Result set management
        self.register_plugin('xep_0060')  # Publish-subscribe
        self.register_plugin('xep_0077')  # In-Band Registration
        self.register_plugin('xep_0045')  # Multi-User Chat
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("session_start", self.messaging_app)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("message", self.get_notification)
        self.add_event_handler("changed_status", self.wait_for_presences)
        self.add_event_handler("roster_subscription_request", self.get_notification)
        self.add_event_handler("groupchat_invite", self.group_chat_invite)
        self.received = set()
        self.presences_received = asyncio.Event()

    @staticmethod
    def get_notification(event):
        print(event['type'])
        if event['type'] in ('chat', 'normal'):
            print(f"New message from {event['from'].username}: {event['body']}")
        elif event['type'] in ('groupchat'):
            print(f"New message from group {event['from']}: {event['body']}")
        elif event['type'] in ('headline'):
            print(f"Headline received: {event['body']}")
        elif event['type'] in ('error'):
            print(f"An error has occurred: {event['body']}")
        elif event['type'] in ('subscribe'):
            print(f"New subscription received from: {event['from'].username}")

    @staticmethod
    def group_chat_invite(event):
        print(f"New groupchat invite. Room: {event['from']}")

    async def session_start(self, event):
        try:
            await self.get_roster()
        except exceptions.IqTimeout:
            print("Request timed out")

        self.send_presence()

    @staticmethod
    def failed_auth(event):
        print("La cuenta introducida no existe")

    @staticmethod
    def validate_input(option):
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
            try:
                option = int(await ainput(constants.MAIN_MENU))
            except ValueError:
                print("Invalid option")
                continue

            print("captured option", option)
            if option == 1:     # Log out
                print("logged out")
                await self.disconnect()
                break

            elif option == 2:   # Delete account
                await self.delete_account()
                break

            if option == 3:     # Show contacts
                await self.show_users_and_contacts()

            if option == 4:     # Add contact
                await self.add_user_to_contacts()
                continue

            if option == 5:     # Send a message
                try:
                    username = await ainput("Username to send message to\n>> ")
                    message_destinatary = f"{username}@alumchat.xyz"
                    print(message_destinatary, "the message destinatary")
                    message = await ainput("Message content\n>> ")
                    print(message, "the message content")
                    await self.message(message_destinatary, message, mtype='chat')
                except AttributeError:
                    print("El usuario no es correcto")
                continue
            if option == 6:     # Group message
                room_name = str(await ainput("Introduce the room name:\n>> "))
                room_name = f"{room_name}@conference.alumchat.xyz"
                self.plugin['xep_0045'].join_muc(room_name, self.username)

                message = str(await ainput("Message to send:\n>> "))
                self.send_message(room_name, message, mtype='groupchat')
                continue

            if option == 7:     # Change status message
                await self.change_presence_message()

            elif option == 8:   # TODO: ADD FILE SENDING
                pass

            elif option == 9:   # Exit
                self.end_session()
            else:
                print("Invalid option")

    async def message(self, message_destinatary, message, mtype='chat'):
        print("Messaging admin")
        self.send_message(message_destinatary, message, mtype=mtype)
        return True

    def end_session(self):
        self.disconnect()

    async def show_users_and_contacts(self):
        print('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])

    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        Reference: https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/roster_browser.py
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    async def change_presence_message(self):
        status = str(await ainput("Insert your new status (hint: away/dnd/chat/xa)\n>> "))
        status_message = str(await ainput("Type your new status message\n>> "))
        nickname = str(await ainput("Type in your new nickname\n>> "))

        self.send_presence(pshow=status, pstatus=status_message, pnick=nickname)

    async def add_user_to_contacts(self):
        # Subscribe
        username = str(await ainput("Username to add as a contact\n>> "))
        self.send_presence_subscription(pto=f"{username}@alumchat.xyz")

    def start_conversation(self):
        username = input("Username to send message to\n>> ")
        message = input("Message content\n>> ")
        self.send_message(f"{username}@alumchat.xyz", message, mtype='chat')
        pass

    async def delete_account(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['remove'] = True

        try:
            await resp.send()
            print(f"{self.boundjid}'s account has been removed")
        except exceptions.IqError as e:
            if e.iq['error']['code'] == '409':
                print(f"Could not delete account: {resp['register']['username']}")
            else:
                print("Account could not be deleted")
            await self.disconnect()
        except exceptions.IqTimeout as e:
            print("Timeout error, please try again")
            await self.disconnect()


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

