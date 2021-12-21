import telebot

API_KEY = "your api key"

bot = telebot.TeleBot(token=API_KEY)

pinnedMessagesId= [] 
pinnedMessages = []
@bot.message_handler(commands=['pin'])
def pinMyMessage(message): #this gets the user input and passes it to  the pinnedMessage function
    mId = message.chat.id
    message_sent = bot.send_message(mId, "Write down the message you want to pin --->")
    pinnedMessagesId.append(mId)
    bot.register_next_step_handler(message_sent, pinnedMessage)

def pinnedMessage(message): #Just pins the message
    pinnedMessages.append(message.text)
    cId = message.chat.id
    mId = message.message_id
    bot.pin_chat_message(cId, mId)

@bot.message_handler(commands=['unpin']) #it looks  at the pinnedMessages list and sends it to the user. Then it stores the user input and sends it to unpinMessage2
def unpinMessage1(message):
    try:
        cId = message.chat.id
        message_sent = bot.send_message(cId, "Select the message you want to unpin --->")
        pinned = ""
        for n in range(len(pinnedMessages)):
            pinned = pinned+(f"| {pinnedMessages[n]}  - {n+1} |\n")
        bot.send_message(cId, pinned)
        bot.register_next_step_handler(message_sent, unpinMessage2)
    except:
        bot.send_message(cId, "There are no pinned messages to unpin")

def unpinMessage2(message): #takes the corresponding messsage id from the pinnedMessagesId list and unpins it with the 'unpin_chat_message' method
    try:
        cId = message.chat.id
        mId = pinnedMessagesId[int(message.text)-1]
        pinnedMessagesId.pop(int(message.text)-1)
        pinnedMessages.pop(int(message.text)-1)
        bot.unpin_chat_message(cId, mId)
        bot.send_message(cId, "Message succesfully unpinned!")
    except:
        bot.send_message(cId, "We could not find the pinned message you were looking for.")
        
bot.polling()
