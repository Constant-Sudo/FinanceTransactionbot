from datetime import datetime
import re
from telegram import Update
import googleSheets
import currency


def handle_response(message) -> str:
    if str(message.content)[:5] == '/sent' or str(message.content)[:9] == '/received':
        # here = ''
        export = extractData(message.content, message)
        googleSheets.write(export)
        # for a in export:
        #     here = here + str(a) + "\n"
        response_str = f"""
Transaction recorded\n
Date:                      {export[0]}
Time:                      {export[1]}
Sent/Received:    {export[2]}
Amount:               {export[4]} {export[6]}
Sent on:                {export[7]}
Note:                      {export[8]}
Who wrote:          {export[9]}
Value:                     {export[5]}
"""
        return response_str

    if message.content == '/help':
        return "Help Message: Use /sent & /received\nExample: /sent €1.363 on Skrill Note: here goes the note"


def handle_response_tele(message) -> bool:
    try:
        export = extractDataTele(message.text, message)
        googleSheets.write(export)
        return export
    except Exception as e:
        raise Exception("handle - tele - " + str(e))


def extractDataTele(data: str, message) -> list:
    """
    /sent $1,425.25 on Skrill
    /received €530.00 in BTC Note: other address than usualy
    /sent 210 USDT on TRC20
    """
    while "  " in data:
        data = data.replace("  ", " ")
    list_str = data.split(" ")
    Date = str(datetime.today().strftime('%Y-%m-%d'))
    Time = str(datetime.now().strftime('%H:%M:%S'))
    if str(data)[:5] == '/sent':
        SendReceived = 'sent'
    elif str(data)[:9] == '/received':
        SendReceived = 'received'
    if message.chat.title:
        PartnerChat = str(message.chat.title) 
    else:
        PartnerChat = "Private Chat"
    Amount = str(convertToEur(list_str[1]))
    if 'EUR' in data or '€' in data:
        Currency = 'EUR'
        if 'Value:' in data:
            Value = str(convertToEur(data.split("Value:", 1)[1]))
            data = str(data.split("Value:", 1)[0])
        else:
            Value = currency.EURtoUSD(Amount)
    else:
        Currency = 'USD'
        Value = ''
    for a in range(len(list_str)):
        if list_str[a] == 'on' or list_str[a] == 'in':
            SentOn = list_str[a+1]
    if 'Note:' in data:
        Note = str(data.split("Note:", 1)[1])[1:]
    else:
        Note = ''
    WhoWrote = str(message.from_user.username)

    return [Date, Time, SendReceived, PartnerChat, Amount, Value, Currency, SentOn, Note, WhoWrote, "Telegram"]


def extractData(data: str, message) -> list:
    """
    /sent $1,425.25 on Skrill
    /received €530.00 in BTC Note: other address than usualy
    /sent 210 USDT on TRC20
    """
    while "  " in data:
        data = data.replace("  ", " ")
    list_str = data.split(" ")
    Date = str(datetime.today().strftime('%Y-%m-%d'))
    Time = str(datetime.now().strftime('%H:%M:%S'))
    if str(message.content)[:5] == '/sent':
        SendReceived = 'sent'
    elif str(message.content)[:9] == '/received':
        SendReceived = 'received'
    PartnerChat = str(message.channel)
    Amount = str(convertToEur(list_str[1]))
    if 'EUR' in data or '€' in data:
        Currency = 'EUR'
        if 'Value:' in data:
            Value = str(convertToEur(data.split("Value:", 1)[1]))
            data = str(data.split("Value:", 1)[0])
        else:
            Value = currency.EURtoUSD(Amount)
    else:
        Currency = 'USD'
        Value = ''
    for a in range(len(list_str)):
        if list_str[a] == 'on' or list_str[a] == 'in':
            SentOn = list_str[a+1]
    if 'Note:' in data:
        Note = str(data.split("Note:", 1)[1])[1:]
    else:
        Note = ''
    WhoWrote = str(message.author)

    return [Date, Time, SendReceived, PartnerChat, Amount, Value, Currency, SentOn, Note, WhoWrote, "Discord"]


def notworking(x):
    while " " in number:
        number = number.replace(" ", "")
    number = number.replace("$", "").replace("€", "").replace("EUR", "").replace("USD", "")
    if '.' not in x and ',' not in x:
        return x
    le = None
    r = re.search(r'(\d+)[.,](\d+)[.,]?(\d*)', x)
    if r:
        if r.group(3):
            le = '{0}{1},{2}'.format(*r.groups())
        elif r.group(2):
            le = '{0},{1}'.format(*r.groups())
        else:
            le = '{}'.format(*r.groups())
    return le


def convertToEur(number: str) -> str:
    while " " in number:
        number = number.replace(" ", "")
    number = number.replace("$", "").replace("€", "").replace("EUR", "").replace("USD", "")
    if "." not in number and "," not in number:
        return number
    elif "." in number and "," not in number:
        if number[-3] == "." or number[-2] == ".":
            return number.replace(".", ",")
        else:
            return number.replace(".", "")
    elif "." not in number and "," in number:
        if "," == number[-4]:
            return number.replace(",", "")
        else:
            return number
    elif "." in number and "," in number:
        if number[-3] == ".":
            number = number.replace(".", ",")
            return number.replace(",", "", 1)
        elif number[-3] == ",":
            return number.replace(".", "")
            return number
    raise ValueError("Not a real number")


def convertEurToUsd(input: str) -> str:
    pass
