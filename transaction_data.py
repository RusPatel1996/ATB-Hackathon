from __future__ import print_function
from props.default import *
import lib.obp as obp
import sys
import requests
import json
import os.path
import datetime
from functools import reduce

obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

def getAccounts(bank):
    # Save Accounts file for faster Access
    if os.path.isfile('accounts.txt'):
        print("Reading...")
        with open("accounts.txt", 'r') as fileToRead:
            accounts = json.load(fileToRead)
    else:
        print("Writing...")
        accounts = obp.getAccountsAtBankIdOnly(bank)
        with open("accounts.txt", 'w') as fileToWrite:
            json.dump(accounts, fileToWrite)
    return accounts
        

def getTransactions(bank, accounts):
    # Save Transactions file for faster Access
    if os.path.isfile('transactions.txt'):
        print("Reading...")
        with open("transactions.txt", 'r') as fileToRead:
            transactions = json.load(fileToRead)
    else:
        print("Writing...")
        for account in accounts:
            transactions = obp.getTransactions(bank, account['id'])
        with open("transactions.txt", 'w') as fileToWrite:
            json.dump(transactions, fileToWrite)
    return transactions


def getTransactionsWithinTimeFrame(transactions, startTimeFrame, endTimeFrame):
    startTimeFrame = datetime.datetime.strptime(startTimeFrame,  "%Y-%m-%dT%H:%M:%S%z") 
    endTimeFrame = datetime.datetime.strptime(endTimeFrame,  "%Y-%m-%dT%H:%M:%S%z")
    return list(filter(lambda x:
            startTimeFrame <= datetime.datetime.strptime(x['details']['posted'],  "%Y-%m-%dT%H:%M:%S%z") and
            endTimeFrame >= datetime.datetime.strptime(x['details']['posted'],  "%Y-%m-%dT%H:%M:%S%z"), transactions))

def payWithinTimeFrame(transactions, startTimeFrame, endTimeFrame):
    # Look for recurring amounts, not all deposits made. <-- Going to take all deposits
    transactions = getTransactionsWithinTimeFrame(transactions, startTimeFrame, endTimeFrame)
    totalPay = 0
    for transaction in transactions:
        transactionValue = float(transaction['details']['value']['amount'])
        if  transactionValue > 0:
            totalPay += transactionValue
    return totalPay

# def averageMonthlyBalanceWithinTimeFrame(accounts, startTimeFrame, endTimeFrame):
#     startTimeFrame = datetime.datetime.strptime(startTimeFrame,  "%Y-%m-%dT%H:%M:%S%z") 
#     endTimeFrame = datetime.datetime.strptime(endTimeFrame,  "%Y-%m-%dT%H:%M:%S%z")
#     return 

def getAccountOpenDate(bank, account_id):
    # Not sure if accessing the right data :\
    x = []
    users = obp.getAccountByIdCore(bank, account_id)['account_attributes']
    for user in users:
        x.append(user['value'])
    return x

def getBankId(bank, account_id):
    return obp.getAccountByIdCore(bank, account_id)['bank_id']

def getUserIds(bank, account_id):
    listOfUserIds = []
    users = obp.getAccountByIdCore(bank, account_id)['owners']
    for user in users:
        listOfUserIds.append(user['id'])
    return listOfUserIds

def getAccountNumber(bank, account_id):
    return obp.getAccountByIdCore(bank, account_id)['number']


def main():
    bank = OUR_BANK
    accounts = getAccounts(bank)
    transactions = getTransactions(bank, accounts)

    print(obp.getTransactions(bank, accounts[0]['id']))

    # for i in accounts:
    #     print(getAccountOpenDate(bank, i['id']))
    #print(obp.getBalances(bank))
    #print(payWithinTimeFrame(transactions, "2020-02-01T00:00:00Z", "2020-02-09T00:00:00Z"))
    #print(len(getTransactionsWithinTimeFrame(transactions, "2020-02-01T00:00:00Z", "2020-02-09T00:00:00Z")))
    #print(json.dumps(transactions[0], indent=2, sort_keys=True)) #prettyfi the JSON data
    # for i in transactions:
    #     print(i['details']['description'])
    

# ----------------------
main()
print("\n---- End ----")