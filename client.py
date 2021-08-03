import asyncio
import logging
from slixmpp import ClientXMPP


class Client(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, message):
        if message['type'] in ('chat', 'normal'):
            message.reply(f"Hello world {message}").send()




