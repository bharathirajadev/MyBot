from chatterbot import ChatBot #import the chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

bot = ChatBot("Bot", preprocessors=["chatterbot.preprocessors.clean_whitespace"]) #"mypreprocessors.fix_typos_in_statement"
trainer = ChatterBotCorpusTrainer(bot)

corpus_path='F:/BackUpMyData/MySVNRepo/MyData/Tech_TargetLearns/Machine_Learning/Workspaces/MyBot/data/english/'

while True:
	message = input('You:')
	if message.strip() == 'Bye':
		print('ChatBot: Bye')
		break
	else:
		reply = bot.get_response(message)
		print('ChatBot:', reply)