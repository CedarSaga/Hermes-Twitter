import os
import time
import schedule
import tweepy
import tarotDeck
from credentials import *


# Creating api reference
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessSecret)
twit = tweepy.API(auth)


# Tarot Reading Objects
hermes = tarotDeck.Reader()
deck = tarotDeck.Deck()
deck.shuffle()


def dailycard():
    hermes.dailyDraw(deck)
    cardRank, cardSuit = hermes.read()
    cardRank = str(cardRank)

    # Navigating to card assets
    cardPath = r"C:\Users\"
    os.chdir(cardPath)

    print("Drawn: ", cardRank, " of ", cardSuit)

    cardSuitBook = cardSuit + ".txt"
    cardMarker = "!" + cardRank

    print("Searching for ", cardMarker, "in", cardSuitBook)

    #  Finds card entry text
    with open(cardSuitBook, "r") as book:
        for line in book:
            if cardMarker in line:
                cardLog = line.replace("!", '')

    # Removes spaces from Major Arcana card names for search
    if "Major" in cardSuit:
        cardRank = cardRank.replace(" ", '')
        cardRank += ".jpg"
        cardSuit = cardSuit.replace(" ", '')
    else:
        cardRank += ".jpg"

    # Searches for Card Picture
    if cardSuit in os.listdir():
        os.chdir(cardSuit)
        print(os.getcwd())

        # Tweets picture
        twit.update_with_media(cardRank, cardLog)
        print("Completed Reading Number:", len(tarotDeck.drawnCards))
        os.chdir(cardPath)
        book.close()

        hermes.clear()
    else:
        return


def verifycred():
    twit.verify_credentials()
    print("Authentication Successful")

def clearhistory():
    hermes.clearHistory()


print("Welcome. Schedule Set.")

schedule.every().day.at("09:00").do(dailycard)
schedule.every().day.at("15:00").do(dailycard)
schedule.every().day.at("21:00").do(dailycard)

schedule.every().day.at("00:01").do(clearhistory)

while True:
    schedule.run_pending()
    time.sleep(1)
