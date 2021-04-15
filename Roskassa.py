import requests
import urllib.parse
import os
import re
import copy
import time
import hmac
import hashlib

from roskassa_lib import *
from urllib.request import urlopen


class Roskassa:


    __private_apiUrl = 'https://api.roskassa.net/'
    __privat_authData = {}

    def __construct(self, shopId, apiKey):
        self.__privat_authData = {
            'shopId': os.getenv('shopId'),
            'apiKey': os.getenv('apiKey'),
        }

    def createOrder(self, shop_id, nonce, currency, amount, order_id, payment_system, fields):
        self.data = {
            'currency': currency,
            'amount': amount,
            'order_id': order_id,
            'payment_system': payment_system,
            'fields': fields,
        }
        self.res = self.makeRequest('createOrder', self.data)
        return self.res

    def shops(self, shop_id, nonce):
        self.res = self.makeRequest('shops', [])
        return self.res
    
    def balance(self):
        self.res = self.makeRequest('balance', [])
        return self.res

    def orderByPaymentId(self, paymentId):
        self.data = {
            'payment_id': paymentId,
        }
        self.res = self.makeRequest('order', self.data)
        return self.res

    def orderByOrderId(self, orderId):
        self.data = {
            'order_id': orderId,
        }
        self.res = self.makeRequest('order', self.data)
        return self.res
    
    def orders(self, status=False, page=0):
        self.data = {
            'status': status,
            'page': page,
        }
        self.res = self.makeRequest('orders', self.data)
        return self.res

    def createWithdrawal(self,currency, amount, account, paymentSystem, paymentId):
        self.data = {
            'currency': currency,
            'amount': amount,
            'account': account,
            'payment_system': paymentSystem,
            'payment_id': paymentId,
            
        }
        self.res = self.makeRequest('createWithdrawals', self.data)
        return self.res

    def withdrawals(self, page, status=False):
        self.data = {
            'page': page
        }
        if status:
            self.data['status'] = status
        self.res = self.makeRequest('withdrawals', self.data)
        return self.res

    def withdrawalByOrderId(self, orderId):
        self.data = {
            'order_id': orderId
        }
        self.res = self.makeRequest('withdrawal', self.data)
        return self.res

    def withdrawalByPaymentId(self, paymentId):
        self.data = {
            'payment_id': paymentId
        }
        self.res = self.makeRequest('withdrawal', self.data)
        return self.res

    @private
    def makeRequest(self, method, data=[]):
        data['shop_id'] = self.authData['shopId']
        data['nonce'] = time()
        self.url = self.__privete_apiUrl + method + '/'
        self.sign = hmac.new(data, self.authData['apiKey'], hashlib.sha256).hexdigest()
        self.headers = {
            'Authorization': 'Bearer {self.sign}',
            'Content-type': 'application/json',
        }
        response = requests.post(self.url, headers=self.headers, data=data)
        return response
