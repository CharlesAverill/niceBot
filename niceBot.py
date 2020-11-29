import discord
import math
import flair
flair_sentiment = flair.models.TextClassifier.load('en-sentiment')


class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.count = 0
        # If these words are in a message they are probably sad
        self.keywords = ["sad", "failed", "die", "dead", "mad", "cry", "...", "worried", "scared", "frightened", "fuck",
                         "shit", "sucks", "damn", "die", "die", "cry", "so sad", "really sad", "really worrying",
                         "wrong", "went wrong", "really bad", "worthless", "meaningless", "depressed", "hate", "death"]

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == client.user:
            return

        # Sadness = emotion_reading(0, 1.0) + message_len(0, 1.0) + (2 * log(num of sad keywords in message))

        s = flair.data.Sentence(message.content)
        flair_sentiment.predict(s)
        total_sentiment = s.labels[0].to_dict()

        emotion_reading = (1 if total_sentiment['value'] == 'NEGATIVE' else .1) * float(total_sentiment['confidence'])
        print(message.content, total_sentiment['value'], total_sentiment['confidence'])

        # theory is "longer messages are sadder usually"
        # 2000 is discord character limit
        message_len = len(message.content) / 2000.0
        sad_keywords = 0

        for word in self.keywords:
            if word in message.content:
                sad_keywords += 1

        sadness_value = emotion_reading + (sad_keywords / len(self.keywords))

        await message.channel.send(sadness_value)
        self.count += 1


with open("token", "r") as file:
    token = "".join(file.readlines())

client = MyClient()
client.run(token)
