# Eth_Tracker_Project
The Ethereum Deposit Tracker is a real-time blockchain monitoring tool designed to track deposits made to the Ethereum 2.0 Beacon Deposit Contract. Built using Python, Web3.py, and Django, it provides a robust solution for monitoring deposits, storing data in a relational database.
# Ethereum Deposit Tracker

The **Ethereum Deposit Tracker** is a real-time blockchain monitoring tool designed to track and record deposits made to the Ethereum 2.0 Beacon Deposit Contract. This project utilizes **Python**, **Web3.py**, and **Django** to interact with the Ethereum blockchain, manage deposit records, and optionally send **Telegram notifications** for real-time alerts. A **Grafana dashboard** integration is also available for visualizing deposit data and system metrics.

## Features

- **Real-time Deposit Tracking**: Continuously monitors Ethereum transactions directed to the Beacon Deposit Contract.
- **Database Storage**: Stores deposit details (transaction hash, sender, amount, etc.) in a **PostgreSQL/MySQL** database using **Django ORM**.
- **Error Handling and Logging**: Comprehensive error logging for improved reliability and troubleshooting.

## Prerequisites

- Python 3.7 or higher
- Web3.py
- Django
- PostgreSQL/MySQL (for deposit storage)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ethereum-deposit-tracker.git
   cd ethereum-deposit-tracker
