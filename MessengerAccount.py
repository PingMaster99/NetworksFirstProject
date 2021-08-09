import asyncio
import logging

from slixmpp import ClientXMPP
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class MessengerAccount(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("got_online", self.message)




    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        print(self.get_roster())
        xmpp.send_message('admin@alumchat.xyz', 'hello', mtype='chat')


    def failed_auth(self, event):
        quit()

    def message(self, event):
        xmpp.send_message('admin@alumchat.xyz', 'hello', mtype='chat')

    def message2(self):
        xmpp.send_message('admin@alumchat.xyz', 'hello', mtype='chat')




if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = MessengerAccount('echobot@192', 'eco')
    xmpp['feature_mechanisms'].unencrypted_plain = True
    xmpp.register_plugin('xep_0199')
    xmpp.connect()
    print("Conectado!")
    xmpp.process()

