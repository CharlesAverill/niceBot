import discord


class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.count = 0

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == client.user:
            return

        await message.channel.send(message.content + " " + str(self.count))
        self.count += 1


with open("token", "r") as file:
    token = "".join(file.readlines())

client = MyClient()
client.run(token)
