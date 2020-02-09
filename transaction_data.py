from __future__ import print_function
from props.default import *
import lib.obp as obp
import sys
import requests
import json
import os.path
import datetime

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



def main():
    bank = OUR_BANK
    accounts = getAccounts(bank)
    transactions = getTransactions(bank, accounts)
    #print(len(getTransactionsWithinTimeFrame(transactions, "2020-02-01T00:00:00Z", "2020-02-09T00:00:00Z")))
    #print(json.dumps(transactions[0], indent=2, sort_keys=True)) #prettyfi the JSON data
    print(accounts[0]['id'])
    print(obp.getTransactionRequest(bank, accounts[0]['id']))

# ----------------------
main()
print("\n---- End ----")