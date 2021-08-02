#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
from fastapi import WebSocket
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
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://frontend-srtknk-cxnam-ews.education.wise-paas.com",
    "https://frontend-srtknk-cxnam-ews.education.wise-paas.com"
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

import cv2
# this is url, default is 0 (webcam)
url = 0
cap = cv2.VideoCapture(url)
detector = cv2.QRCodeDetector()
value = None

def getProductDetail(argument, value) -> dict:
    if(argument == "bread"):
        return bread.find_one({"code" : value})
    if(argument == "cannedFood"):
        return cannedFood.find_one({"code" : value})
    if(argument == "cosmetics"):
        return cosmetics.find_one({"code" : value})
    if(argument == "freshFruit"):
        return freshFruit.find_one({"code" : value})
    if(argument == "freshMilk"):
        return freshMilk.find_one({"code" : value})
    if(argument == "instantNoodle"):
        return instantNoodle.find_one({"code" : value})
    if(argument == "sauce"):
        return sauce.find_one({"code" : value})
    if(argument == "snack"):
        return snack.find_one({"code" : value})
    if(argument == "toothpaste"):
        return toothpaste.find_one({"code" : value})
    if(argument == "washingPowder"):
        return washingPowder.find_one({"code" : value})

def scanProduct() -> dict:
    global value
    message = None
    while True:
        _,img=cap.read()
        qrcode,one,_=detector.detectAndDecode(img)
        if qrcode:
            if value != qrcode:
                value = qrcode
                print(qrcode)
                result = qrcode.split(",")
                pointer = getProductDetail(result[0], result[1])
                message = productEntityAdd(pointer)
                # print(message)
            return message
        # cv2.imshow('qrcode', img)
        # if cv2.waitKey(1)==ord('q'):
        #     break

@app.websocket("/add-item")
async def websocket_add_item(websocket : WebSocket):
    await websocket.accept()       
    while True:
        # data = websocket.receive_text()
        # if (data == "Logout"):
        #     break
        message = scanProduct()
        print(message)
        if (message):
            await websocket.send_json(message)