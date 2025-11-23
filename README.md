
# Python-Copy_trader  
Automated Trade Replication System for GWCIndia Accounts

https://github.com/user-attachments/assets/51431c2c-8aaf-4859-8fdf-2379a3f2bdc8



## Overview
- Real-time mirroring of trades from a parent account to multiple child accounts.  
- Uses GWCIndia API for fast and reliable order replication.  
- Supports per-account multipliers for flexible position sizing.  
- Secure token flow through a local HTTP authentication server.  
- Excel-driven configuration for managing accounts and multipliers.

## Features
- **Instant Sync:** Replicates parent trades to child accounts immediately.  
- **Multipliers:** Control lot sizes per child with simple config values.  
- **Secure Auth:** Local token exchange ensures safe, private login flow.  
- **Excel Config:** Manage accounts/settings without touching code.  
- **Resilient:** Error handling + logs keep replication stable.

## Repository Structure
```

/                         → Project root
├─ Goodwill_copy_trader.py  → Main trade replication engine
├─ load_keys.py             → Loads API tokens & credentials
├─ credentials.xlsx         → Excel config for child accounts & multipliers
├─ logs/                    → Runtime log output
└─ README.md                → Documentation

````

## Tech Stack
- **Language:** Python 3.8+  
- **API:** GWCIndia REST API  
- **Config:** Excel (openpyxl)  
- **Libraries:** requests, openpyxl, logging  

## Installation
```bash
git clone https://github.com/calvincandiec137/Python-Copy_trader
cd Python-Copy_trader

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
````

## Usage

1. Fill `credentials.xlsx` with:

   * Parent API key/secret
   * Child account credentials
   * Multipliers
2. Start the replication engine:

```bash
python Goodwill_copy_trader.py
```

### What Happens

* Parent trades are detected in real time.
* Child orders are placed using configured multipliers.
* Logs track execution, failures, and sync status.

## Security Notes

* Never commit tokens or sensitive data.
* Use 2FA where possible.
* Monitor log files for unusual activity.

## License
This project is licensed under the MIT `License`. See the LICENSE file for details.



