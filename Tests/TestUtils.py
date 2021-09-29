from pprint import pprint
import json

def evaluateTest(arg1, arg2):
    if arg1 == arg2:
        print("Test Passed")
    else:
        print("Test Failed")


def printResult(response):
    print("------------")

    if response.text != "":
        content = response.text
        jsoniced = json.loads(content)
        pprint(jsoniced)
    print("------------")
