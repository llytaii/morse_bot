from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bidict import bidict
import os

morse_dict = bidict({'A' : '.-',
                     'B' : '-...',
                     'C' : '-.-.',
                     'D' : '-..',
                     'E' : '.',
                     'F' : '..-.',
                     'G' : '--.',
                     'H' : '....',
                     'I' : '..',
                     'J' : '.---',
                     'K' : '-.-',
                     'L' : '.-..',
                     'M' : '--',
                     'N' : '-.',
                     'O' : '---',
                     'P' : '.--.',
                     'Q' : '--.-',
                     'R' : '.-.',
                     'S' : '...',
                     'T' : '-',
                     'U' : '..-',
                     'V' : '...-',
                     'W' : '.--',
                     'X' : '-..-',
                     'Y' : '-.--',
                     'Z' : '--..',
                     'Ö' : '---.',
                     'ß' : '...--..',
                     'Ü' : '..--',
                     'Ä' : '.-.-',
                     'CH': '----',
                     '.' : '.-.-.-',
                     ':' : '---...',
                     ',' : '--..--',
                     ';' : '-.-.-.',
                     '?' : '..--..',
                     '!' : '-.-.--',
                     '-' : '-....-',
                     '_' : '..--.-',
                     '(' : '-.--.',
                     ')' : '-.--.-',
                     '=' : '-...-',
                     '+' : '.-.-.',
                     '/' : '-..-.',
                     '@' : '.--.-.',
                     ' ' : ' /',
                     '1' : '.----',
                     '2' : '..---',
                     '3' : '...--',
                     '4' : '....-',
                     '5' : '.....',
                     '6' : '-....',
                     '7' : '--...',
                     '8' : '---..',
                     '9' : '----.',
                     '0' : '-----',
                     #'KA (Spruchanfang)' : '-.-.-',
                     #'BT (Pause)' : '-...-',
                     #'AR (Spruchende)' : '.-.-.',
                     #'VE (verstanden)' : '...-.',
                     #'SK (Verkehrsende)' : '...-.-',
                     'SOS' : '...---...',
                     #'HH (Fehler; Irrung; Wiederholung ab letztem vollständigen Wort' : '........'
                     })

#BotCommands
def start(update, context):
    update.message.reply_text('.... ..!\nText me for translation!')

def help(update, context):
    update.message.reply_text('I translate from and to morse!')

def toMorse(text):
    for x in text:
        if(x != '-' and x != '.' and x != ' ' and x != '/'):
            return True #is not morse
    return False #is morse

def decrypt(text):
    text = text.split()
    cypher = ""
    for x in text:
        if(x == '/'):
            cypher += ' '
        elif(x in morse_dict.inverse):
            cypher += morse_dict.inverse[x]
        else:
            cypher += 'UNKOWN' + '0'
    return cypher

def encrypt(text):
    cypher = ""
    for x in text:
        if(x in morse_dict):
            cypher += morse_dict[x] + ' '
        else:
            cypher += 'UNKNOWN' + ' '
    return cypher

def translate(update, context):
    text = update.message.text.upper()
    cypher = ""
    if(toMorse(text)):
        cypher = encrypt(text)
    else:
        cypher = decrypt(text)
    update.message.reply_text(cypher)

def main():
    with open('token.txt') as f:
        token = f.read().strip()

    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()