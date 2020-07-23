# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import urllib
import urllib.parse


class Request(object):
    cookie = {
        "first_time": "",  # incr
        "tgs_uuid": "523965d4-ae13-11ea-9754-525400eb29da",
        "tgs_session": "780",
        "n_session_id": "xgfkmskc4xm",
        "isGPS": "true",
        "initUrl": "https%3A%2F%2Fm.hostname.com%2Flogin%2Flogin.html",
        "global": "webapp",
        "goApp": "true",
        "cityId": "2554",
        "cityName": "%E5%A4%A7%E8%BF%9E%E5%B8%82",
        "token": "xxx",  # 这个要动态配置
        "memberId": "xxx",
        "cellPhone": "xxx",
        "username": "xxx",
        "isLogin": "true",
        "validate": "1",
        "tgVersion": "web%2F2020514",
        "webp": "true",
        "userImageUrl": "%2F%2Fimage1.hostname.com%2Ftgou2%2Fimg2%2Fmine%2FdefaultPhoto.png!s",
        "storeId": "181",  # 不知道为什么和入参不同 写死了
        "visitStores": "%7B%222554%22%3A%5B%221065%22%5D%7D",
        "pageInitTime": ""  # incr
    }

    def formatCookie(self):
        strCookie = ""
        for key, value in self.cookie.items():
            strCookie = strCookie + key + "=" + value + "; "
        return strCookie

    def doRequest(self, url, params=None, header=None):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Origin": "https://m.hostname.com",
                "Cookie": self.formatCookie()
            }
            # params = urllib.parse.urlencode(params)
            # print(params)
            # headers["Cookie"] = 'first_time=2020-06-14 15:47:39; tgs_uuid=523965d4-ae13-11ea-9754-525400eb29da; n_session_id=xgfkmskc4xm; isGPS=true; initUrl=https%3A%2F%2Fm.hostname.com%2Flogin%2Flogin.html; global=webapp; goApp=true; cityId=2554; cityName=%E5%A4%A7%E8%BF%9E%E5%B8%82; token=cab80f12a40bc75f77bfb143ba104073; memberId=16784880; cellPhone=13898120854; username=13898120854; isLogin=true; validate=1; tgVersion=web%2F2020514; webp=true; userImageUrl=%2F%2Fimage1.hostname.com%2Ftgou2%2Fimg2%2Fmine%2FdefaultPhoto.png!s; storeId=1065; visitStores=%7B%222554%22%3A%5B%221065%22%5D%7D; tgs_session=780; pageInitTime=1592131793355; first_time=2020-06-14 15:47:39; tgs_uuid=523965d4-ae13-11ea-9754-525400eb29da; n_session_id=xgfkmskc4xm; isGPS=true; initUrl=https%3A%2F%2Fm.hostname.com%2Flogin%2Flogin.html; global=webapp; goApp=true; cityId=2554; cityName=%E5%A4%A7%E8%BF%9E%E5%B8%82; token=cab80f12a40bc75f77bfb143ba104073; memberId=16784880; cellPhone=13898120854; username=13898120854; isLogin=true; validate=1; tgVersion=web%2F2020514; webp=true; userImageUrl=%2F%2Fimage1.hostname.com%2Ftgou2%2Fimg2%2Fmine%2FdefaultPhoto.png!s; storeId=1065; visitStores=%7B%222554%22%3A%5B%221065%22%5D%7D; tgs_session=780; pageInitTime=1592132468936'
            if header != None:
                for k, v in header.items():
                    headers[k] = v
            if params == None:
                response = requests.get(url, params, headers=headers)
            else:
                response = requests.post(url, params, headers=headers)
            return response.text
        except  Exception as e:
            return False


class Init(Request):
    params = {}

    def doInit(self, itemId, skuId, count, storeId, price):
        self.cookie["first_time"] = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.cookie["pageInitTime"] = str(int(time.time()) * 1000)
        self.params["itemId"] = itemId
        self.params["skuId"] = skuId
        self.params["count"] = count
        self.params["storeId"] = storeId
        self.params["price"] = price
        print("Robot Init Success...[" + json.dumps(self.params) + "]")
        return self

    def createSecVal(self, secKey=None, preTime=None):
        # [8 * (653880 + 8), 653880 + 1592148305653 % 1000000, 2000 + 653880, 653880 + 821029, +653880[6 - 1],653880 % 10 * +653880[66 - 1] - 653880, 1592148305653 + 653880, 777, 987648, 3 + 653880][653880 % 10]
        if secKey != None:
            self.params["secKey"] = secKey
        if preTime != None:
            self.params["preTime"] = preTime
        secKeyLen = len(str(self.params["secKey"]))
        tmp = [
            8 * (self.params["secKey"] + 8),
            self.params["secKey"] + self.params["preTime"] % 1000000,
            2000 + self.params["secKey"],
            self.params["secKey"] + 821029,
            int(str(self.params["secKey"])[secKeyLen - 1]),
            self.params["secKey"] % 10 * +int(str(self.params["secKey"])[secKeyLen - 1]) - self.params["secKey"],
            self.params["preTime"] + self.params["secKey"],
            777,
            987648,
            3 + self.params["secKey"]
        ]
        print(tmp)
        tmpIndex = self.params["secKey"] % 10
        return tmp[tmpIndex]


class Sku(Init):
    def queryActivityRuleInfo(self):
        url = "https://coupon.hostname.com/publics/activity/queryActivityRuleInfo"
        params = {
            "itemId": self.params["itemId"],
            "skuId": self.params["skuId"],
            "count": self.params["count"],
            "storeId": self.params["storeId"],
            "price": self.params["price"]
        }
        header = {
            "Referer": "https://m.hostname.com/product/listing.html?id=" + str(self.params["itemId"]),
            "Host": "coupon.hostname.com",
        }
        ret = self.doRequest(url, params, header)
        if False == ret:
            raise Exception("Sku.queryActivityRuleInfo Request False")

        retDict = json.loads(ret)
        if retDict["code"] != 0:
            raise Exception("Sku.queryActivityRuleInfo Fail", retDict["message"])
        else:
            print("Sku QueryActivityRuleInfo Success...")
            return self


class PreOrder(Init):
    def validate(self):
        url = "https://orderserver.hostname.com/publics/tgouOrder/validate"
        params = {
            "from": 1,
            "products": '[{"activityProductId":' + str(self.params["itemId"]) + ',"quantity":' + str(
                self.params["count"]) + ',"skuId":' + str(self.params["skuId"]) + ',"storeId":' + str(
                self.params["storeId"]) + '}]'
        }
        header = {
            "Referer": "https://m.hostname.com/product/listing.html?id=" + str(self.params["itemId"]),
        }
        ret = self.doRequest(url, params, header)
        retDict = json.loads(ret)
        if retDict["code"] != 0:
            raise Exception("PreOrder.validate Fail", ret)
        else:
            self.params["secKey"] = retDict["secKey"]
            self.params["preTime"] = retDict["timestamp"]
            print("PreOrder Validate Success...[secKey:" + str(retDict["secKey"]) + "]")
            return self

    def doPreOrder(self):
        url = "https://orderserver.hostname.com/publics/tgouOrder/preOrder"
        params = {
            "from": 1,
            "fxStoreId": 20,
            "subOrderType": 0,
            "products": '[{"activityProductId":"' + str(self.params["itemId"]) + '","skuId":"' + str(
                self.params["skuId"]) + '","quantity":"' + str(self.params["count"]) + '"}]'
        }
        header = {
            "Referer": "https://m.hostname.com/purchase/preorder.html?activityProductId=" + str(
                self.params["itemId"]) + "&quantity=" + str(self.params["count"]) + "&skuId=" + str(
                self.params["skuId"]) + "&storeId=" + str(self.params["storeId"]) + "&source=1&time=" + str(
                self.params["preTime"]) + "&from=1",
        }
        ret = self.doRequest(url, params, header)
        retDict = json.loads(ret)
        if retDict["code"] != 0:
            raise Exception("PreOrder.doPreOrder Fail", ret)
        else:
            self.params["secKey"] = retDict["secKey"]
            self.params["preTime"] = retDict["timestamp"]
            self.params["perOrderInfo"] = retDict["data"]["preOrders"][0]
            print("PreOrder DoPreOrder Success...[secKey:" + str(retDict["secKey"]) + "]  [timestamp:" + str(
                retDict["timestamp"]) + "]")
            return self

    def doPromotions(self):
        url = "https://orderserver.hostname.com/publics/tgouOrder/promotions"
        barcode = self.params["perOrderInfo"]["products"][0]["barcode"]
        merchantProductCode = self.params["perOrderInfo"]["products"][0]["merchantProductCode"]
        activityId = self.params["perOrderInfo"]["products"][0]["activityId"]
        counterId = self.params["perOrderInfo"]["products"][0]["counterId"]
        params = {
            "receiveType": 10,
            "receiveCityId": 2478,  # 估计是黑河
            "needPromotion": "true",
            "subOrderType": 0,
            "products": '[{"storeId":' + str(self.params[
                                                 "storeId"]) + ',"source":1,"barcode":"' + barcode + '","merchantProductCode":"' + merchantProductCode + '","skuId":"' + str(
                self.params["skuId"]) + '","activityId":' + str(activityId) + ',"price":' + str(
                self.params["price"]) + ',"id":' + str(self.params["itemId"]) + ',"counterId":' + str(
                counterId) + ',"quantity":' + str(self.params["count"]) + '}]'
        }
        header = {
            "Referer": "https://m.hostname.com/purchase/preorder.html?activityProductId=" + str(
                self.params["itemId"]) + "&quantity=" + str(self.params["count"]) + "&skuId=" + str(
                self.params["skuId"]) + "&storeId=" + str(self.params["storeId"]) + "&source=1&time=" + str(
                self.params["preTime"]) + "&from=1",
        }
        ret = self.doRequest(url, params, header)
        # print(ret)
        retDict = json.loads(ret)
        if retDict["code"] != 0:
            raise Exception("PreOrder.doPromotions Fail", ret)
        else:
            self.params["secKey"] = retDict["secKey"]
            self.params["preTime"] = retDict["timestamp"]
            print("PreOrder DoPromotions Success...[secKey:" + str(retDict["secKey"]) + "] [timestamp:" + str(
                retDict["timestamp"]) + "]")
            return self


class Order(Init):
    def doAdd(self):
        url = "https://orderserver.hostname.com/publics/tgouOrder/add"
        activityId = self.params["perOrderInfo"]["products"][0]["activityId"]
        counterId = self.params["perOrderInfo"]["products"][0]["counterId"]
        orderOption = {
            "needPay": True,
            "receiveType": "00",
            # "addressId": 1528032,
            "message": json.dumps([{"storeId": counterId, "counterId": counterId, "message": ""}]),
            "needCheckGift": False
        }
        params = {
            "from": 1,
            "fxStoreId": 20,
            "products": '[{"counterId": ' + str(counterId) + ', "skuId": "' + str(
                self.params["skuId"]) + '", "activityId": ' + str(activityId) + ', "activityProductId": ' + str(
                self.params["itemId"]) + ', "quantity": ' + str(self.params["count"]) + '}]',
            # "orderOption": '{"needPay": true, "receiveType": "10", "addressId": 1528032,"message": "[{\"storeId\":' + str(
            #     self.params["storeId"]) + ',\"counterId\":' + str(
            #     counterId) + ',\"message\":\"\"}]", "needCheckGift": false}',
            "orderOption": json.dumps(orderOption),
            "productType": 0,
            "subOrderType": 0,
            "storeId": self.params["storeId"],
            "secKey": self.params["secKey"],
            "timestamp": self.params["preTime"],
            "secValue": self.createSecVal()
        }
        header = {
            "Referer": "https://m.hostname.com/purchase/preorder.html?activityProductId=" + str(
                self.params["itemId"]) + "&quantity=" + str(self.params["count"]) + "&skuId=" + str(
                self.params["skuId"]) + "&storeId=" + str(self.params["storeId"]) + "&source=1&time=" + str(
                self.params["preTime"]) + "&from=1",
        }
        # print(params)
        ret = self.doRequest(url, params, header)
        # print(ret)
        retDict = json.loads(ret)
        if retDict["code"] != 0:
            raise Exception("Order.doAdd Fail", ret)
        else:
            print("Order doAdd Success...[orderId:" + str(retDict["data"]["orderId"]) + "]")
            return self


if __name__ == '__main__':
    while (1):
        now = time.strftime("%H%M", time.localtime())
        if int(now) >= 958 and int(now) <= 1002:
            try:
                # 初始化 robot
                Init().doInit(14969880, 8979, 2, 181, 1499)
                Sku().queryActivityRuleInfo()
                PreOrder().validate().doPreOrder().doPromotions()
                Order().doAdd()
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)
        else:
            print("Current Time Continue")
            continue
