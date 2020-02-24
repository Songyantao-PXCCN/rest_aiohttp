import json
import logging.config
import uuid

from com.Phoenixcontact.REST.RESTException import *
from com.Phoenixcontact.REST.RESTHttpClient import *


class Authentication(object):
    def __init__(self, Client):
        self.Client = Client
        self.authToken = None

    def __getAuthToken(self, ):
        logging.debug('getAuthToken ...')
        self.Client.authToken = None
        self.Client.accessToken = None
        _uuid = str(uuid.uuid1())
        _payload = {'state': _uuid,
                    'scope': RestConstant.TEMPORARY_TOCKEN_BODY_SCOPE_VALUES}

        for i in range(3):
            _status_code, _hearders, _text = self.Client.loop.run_until_complete(
                self.Client._Http.asyncHttpAPI(httpMethod=RestConstant.POST,
                                               function_uri=RestConstant.TEMPORARY_TOCKEN_URI,
                                               payload=json.dumps(_payload)))
            if _status_code == 200:
                _response = json.loads(_text)
                if _response['state'] == _uuid:
                    self.authToken = _response['code']
                    return
            elif _status_code == 410:
                self.Client._Session._createSessionID()

    def _Login(self):
        logging.debug('logging ...')
        for i in range(3):
            Authentication.__getAuthToken(self)
            _payload = {
                'code': self.authToken,
                'grant_type': 'authorization_code',
                'username': self.Client.PLCnUserName,
                'password': self.Client.PLCnPasswd
            }
            _status_code, _hearders, _text = self.Client.loop.run_until_complete(
                self.Client._Http.asyncHttpAPI(httpMethod=RestConstant.POST,
                                              function_uri=RestConstant.ACCESS_TOCKEN_URI,
                                              payload=json.dumps(_payload)))
            if _status_code == 200:
                _response = json.loads(_text)
                if _response['state'] == self.authToken:
                    self.Client.accessToken = _response['access_token']
                    return
            elif _status_code == 401:
                _response = json.loads(_text)
                _reason = _response['error']['details'][0]['reason']
                if _reason == 'wrongPassword':
                    logging.error('Wrong password')
                    raise RESTException('Wrong password')
            elif _status_code == 410:
                self.Client._Session._createSessionID()
