import logging
from slixmpp import ClientXMPP, exceptions
# Reference: https://groups.google.com/g/sleekxmpp-discussion/c/iAFJGcpH-Ps
class Registration(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.register)

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.disconnect()


    async def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print(f"{self.boundjid}'s account has been created!")
        except exceptions.IqError as e:
            if e.iq['error']['code'] == '409':
                print(f"There is already an account with the username: {resp['register']['username']}")
            else:
                print("Account could not be registered")
            await self.disconnect()
        except exceptions.IqTimeout as e:
            print("Timeout error, please try again")
            await self.disconnect()







