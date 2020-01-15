## Get Started

```
pip install -r requirements.txt
```

## Setup
Put in the values for the following fields in `python/props/default.py`:

```
# leap.bank_id
OUR_BANK = ''

# leap.username
USERNAME     = ''

# leap.password
PASSWORD     = ''

#leap.consumer_key
CONSUMER_KEY = ''

# API server URL
BASE_URL  = ''

# counterparty id
OUR_COUNTERPARTY = ''

# counterparty bank id
COUNTERPARTY_BANK = ''
```

## Run
```
# hello obp
python hello_obp.py

# hello payments
python hello_payments.py
```
