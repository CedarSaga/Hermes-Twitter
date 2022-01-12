import os
import time
import schedule
import tweepy
import logging
import tarotDeck
from credentials import *

# Creating api reference
client = tweepy.Client(bearerToken)
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessSecret)
twit = tweepy.API(auth)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Tarot Reading Objects
hermes = tarotDeck.Reader()
deck = tarotDeck.Deck()
deck.shuffle()


def dailycard():
    hermes.dailyDraw(deck)
    cardRank, cardSuit = hermes.read()
    cardRank = str(cardRank)

    # Navigating to card assets
    cardPath = r"C:\Users\Hermes\Documents\Code Projects\Python\HermesTwitter\BookOfShadows"
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
        ##print(os.getcwd())

        # Tweets picture
        twit.update_status_with_media(cardLog, cardRank)
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


def checkmentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(twit.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
                continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            hermes.oneCardDraw(deck)
            cardRank, cardSuit = hermes.read()
            cardRank = str(cardRank)

            # Navigating to card assets
            cardPath = r"C:\Users\Hermes\Documents\Code Projects\Python\HermesTwitter\BookOfShadows"
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
            replyStatus = ('@' + tweet.user.screen_name + " " + cardLog)
            tweetIdString = tweet.id
            twit.update_status_with_media(status=(replyStatus), filename=cardRank, in_reply_to_status_id=tweet.id_str)
            hermes.clear()
    return new_since_id

print("Welcome. Schedule Set.")

since_id = 1


schedule.every().day.at("09:00").do(dailycard)
schedule.every().day.at("15:00").do(dailycard)
schedule.every().day.at("21:00").do(dailycard)

schedule.every().day.at("06:00").do(clearhistory)

while True:
    schedule.run_pending()
    since_id = checkmentions(twit, ["reading"], since_id)
    logger.info("Waiting...")
    time.sleep(60)
