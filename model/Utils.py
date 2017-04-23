import requests
import urllib2


class Utils:


    urlHash = "http://localhost:8080/wordnet/Hash"
    headers = {'content-type': 'application/json'}
    data = dict()
    def __init__(self):
        pass

    #
    # @staticmethod
    # def hash(value):
    #     h = 0
    #     for i in range(0, len(value)):
    #         h = 31 * h + ord(value[i])
    #     return h
    @staticmethod
    def hash(value):
        urlCalc = "http://localhost:8080/wordnet/Hash?value="+value
        response = requests.get(urlCalc, headers=Utils.headers)
        return int(response.text)

    @staticmethod
    def calc(a, b, c):
        urlCalc = "http://localhost:8080/wordnet/Calculation?a=" + str(a) + "&b=" + str(b) + "&c=" + str(c)
        response = requests.get(urlCalc, headers=Utils.headers)
        return int(response.text)
