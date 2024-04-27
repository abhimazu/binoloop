python3 -m venv client_env
source client_env/bin/activate
pip install -r requirements.txt
python3 modelclient.py --host localhost --file Dataset.csv --port 8000 --start 0 --end 1 --interval 3