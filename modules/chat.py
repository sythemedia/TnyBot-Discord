import asyncio

from exceptions.expections import SameUserException
from .abstract_module import AbstractMethod
from chatterbot import ChatBot
from chatterbot.training.trainers import ChatterBotCorpusTrainer, ListTrainer


class Chat(AbstractMethod):
    _sentence = []
    _chatbot = None

    def __init__(self, bot):
        super().__init__(bot)

    @asyncio.coroutine
    def on_ready(self):
        print("listening in another class " + __name__)

        self._chatbot = ChatBot("Tny",
            storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
            database="chatterbot-database"
        )

        self._chatbot.set_trainer(ListTrainer)
        self._chatbot.train([
            "What music do you like?",
            "kpop",
            "favorite group?",
            "I.O.I",
            "who is your bias?",
            "Chungha",
        ])

        self._chatbot.set_trainer(ChatterBotCorpusTrainer)

        # Train based on the english corpus
        self._chatbot.train("chatterbot.corpus.english")

        # Get a response to an input statement

    @asyncio.coroutine
    def on_message(self, message):
        try:
            super().on_message(message)
        except SameUserException:
            return

        self._sentence = message.content.split(" ")

        response = self._chatbot.get_response(message.content)
        yield from self.bot.send_message(message.channel, response)
