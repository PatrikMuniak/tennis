#!/bin/bash
sudo apt install python3.12-venv sqlite3 -y
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt