import telebot
import json
import requests
import os

bot = telebot.TeleBot('6248408590:AAEknJrEt7eLxN0RS6otWNF7BqEuYdn5oDQ')

@bot.message_handler(content_types=['document'])
def handle(message):
    try:
        doc = message.document
        finfo = bot.get_file(doc.file_id)
        df = bot.download_file(finfo.file_path)
        dfs = df.decode('utf-8').split('\n')
        cards = []
        for card in dfs:
            if len(card)>16:
                card = card[:16]
            cards.append(card)
        cards = [x for x in cards if x != ""]        
        response = requests.post(
            'https://api.antipublic.cc/cards',
            json=cards
        ).json()
        lenpub = len(response["public"])
        lenpv = len(response["private"])
        lenpp = response['private_percentage']
        with open('@hanniscrappublic.txt', 'w') as file:
            for pub in response["public"]:
                file.write(str(pub) + '\n')
        with open('@hanniscrapprivate.txt', 'w') as file:
            for pv in response["private"]:
                file.write(str(pv) + '\n')
        with open("@hanniscrappublic.txt", "rb") as file:
            if lenpub == 0:
                pass
            else:
                bot.send_document(message.chat.id, file,reply_to_message_id=message.message_id)
        with open("@hanniscrapprivate.txt", "rb") as file:
            if lenpv == 0:
                pass
            else:
                bot.send_document(message.chat.id, file,reply_to_message_id=message.message_id)
        caption = '𝗣𝘂𝗯𝗹𝗶𝗰: '+str(lenpub)+'\n𝗣𝗿𝗶𝘃𝗮𝘁𝗲: '+str(lenpv)+'\n𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗣𝗲𝗿𝗰𝗲𝗻𝘁𝗮𝗴𝗲: '+str(lenpp)+'\n\n© Hanni'
        bot.reply_to(message,caption)
        os.remove('@hanniscrappublic.txt')
        os.remove('@hanniscrapprivate.txt')
    except Exception as e:
        res = response['detail']
        if not res:
            res = str(e)
        bot.reply_to(message, res)
bot.polling()
