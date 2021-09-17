#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import time
from fastapi import WebSocket, FastAPI
from product import productEntityAdd
from product import productEntityDelete


DATABASE_URL = "mongodb+srv://admin:admin@market.sdvm0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db = pymongo.MongoClient(DATABASE_URL)
categories = db.test
categories = db.get_database('Categories')

# Query all collections
bread = categories.Bread
cannedFood = categories.Canned_Food
cosmetics = categories.Cosmetics
freshFruit = categories.Fresh_Fruit
freshMilk = categories.Fresh_Milk
instantNoodle = categories.Instant_Noodle
sauce = categories.Sauce
snack = categories.Snack
toothpaste = categories.Toothpaste
washingPowder = categories.Washing_Powder

# Initiating FastAPI Server
app = FastAPI()

# # Managing CORS for the React Frontend connections

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://shopping-cart-srtknk-cxnam-ews.education.wise-paas.com",
    "https://shopping-cart-srtknk-cxnam-ews.education.wise-paas.com"
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

cart = []

# this is url, default is 0 (webcam)
url = 0
# url = 'http://192.168.1.16:4747/video'
cap = cv2.VideoCapture(url)
detector = cv2.QRCodeDetector()
value = None


def getProductDetail(argument, value) -> dict:
    if(argument == "bread"):
        return bread.find_one({"code": value})
    if(argument == "cannedFood"):
        return cannedFood.find_one({"code": value})
    if(argument == "cosmetics"):
        return cosmetics.find_one({"code": value})
    if(argument == "freshFruit"):
        return freshFruit.find_one({"code": value})
    if(argument == "freshMilk"):
        return freshMilk.find_one({"code": value})
    if(argument == "instantNoodle"):
        return instantNoodle.find_one({"code": value})
    if(argument == "sauce"):
        return sauce.find_one({"code": value})
    if(argument == "snack"):
        return snack.find_one({"code": value})
    if(argument == "toothpaste"):
        return toothpaste.find_one({"code": value})
    if(argument == "washingPowder"):
        return washingPowder.find_one({"code": value})


def scanProduct() -> dict:
    global cart
    message = None
    while True:
        _, img = cap.read()
        qrcode, one, _ = detector.detectAndDecode(img)
        if qrcode:
            result = qrcode.split(",")
            pointer = getProductDetail(result[0], result[1])
            # if qrcode in cart:
            #     cart.remove(qrcode)
            #     message = productEntityDelete(pointer)
            # else:
            #     message = productEntityAdd(pointer)
            #     cart.append(qrcode)
            message = productEntityAdd(pointer)
            return message
        # cv2.imshow('qrcode', img)
        # if cv2.waitKey(1)==ord('q'):
        #     break


@app.websocket("/item")
async def websocket_add_item(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = websocket.receive_text()
        # if (data == "Logout"):
        #     break
        message = scanProduct()
        if (message):
            print(message)
            await websocket.send_json(message)
            time.sleep(3)
