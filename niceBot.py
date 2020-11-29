import discord
import emoji
from emosent import get_emoji_sentiment_rank
import flair
flair_sentiment = flair.models.TextClassifier.load('en-sentiment')


def extract_emojis(words):
    return ''.join(c for c in words if c in emoji.UNICODE_EMOJI)


class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.count = 0
        # If these words are in a message they are probably sad
        self.keywords = ["sad", "failed", "die", "dead", "mad", "cry", "...", "worried", "scared", "frightened", "fuck",
                         "shit", "sucks", "damn", "die", "die", "cry", "so sad", "really sad", "really worrying",
                         "wrong", "went wrong", "really bad", "worthless", "meaningless", "depressed", "hate", "death"]
        self.negative_keywords = ["lmao", "lol", "ha"]

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == client.user:
            return

        message_len = len(message.content) / 2000.0

        # Sadness = emotion_reading(0, 1.0) + message_len(0, 1.0) + (2 * log(num of sad keywords in message))

        s = flair.data.Sentence(message.content)
        flair_sentiment.predict(s)
        total_sentiment = s.labels[0].to_dict()

        emotion_reading = (1 if total_sentiment['value'] == 'NEGATIVE' else .1) * float(total_sentiment['confidence'])
        print(message.content, total_sentiment['value'], total_sentiment['confidence'])

        sad_keywords = 0
        happy_keywords = 0

        for word in self.keywords:
            if word in message.content.lower():
                sad_keywords += 1

        for word in self.negative_keywords:
            if word in message.content.lower():
                happy_keywords += 1

        emojis = extract_emojis(message.content.split(" "))

        emoji_score = 1
        for e in emojis:
            score = get_emoji_sentiment_rank(e)
            emoji_score += score["sentiment_score"]

        sadness_value = emotion_reading + (1 / emoji_score) + (message_len * 1.25 * (sad_keywords - happy_keywords) / len(self.keywords + self.negative_keywords))

        if sadness_value > 1.95:
            out_message = "Your message \"" + message.content + "\" had a sadness value of " + \
                          str(round(sadness_value, 2)) + ". Is everything alright?"
        else:
            out_message = "Wow, you must be pretty happy!"

        await message.channel.send(out_message)
        self.count += 1


with open("token", "r") as file:
    token = "".join(file.readlines())

client = MyClient()
client.run(token)
