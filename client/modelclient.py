import pandas as pd
import requests
import time
import logging
import os
import argparse

if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(filename='logs/client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(description='Send requests to evaluate essays.')
parser.add_argument('--host', type=str, default='localhost', help='Host IP of the model server')
parser.add_argument('--port', type=int, default=8000, help='Port of the model server')
parser.add_argument('--file', type=str, default='Mixtral8x7b_4k_essays_for_DetectAIGeneratedTextCompetition.csv', help='Name of the dataset csv file')
parser.add_argument('--start', type=int, default=0, help='Start index for data range to process from the csv')
parser.add_argument('--end', type=int, default=10, help='End index for data range to process from the csv')
parser.add_argument('--interval', type=int, default=2, help='Seconds to sleep between server requests')
args = parser.parse_args()

BASE_URL = f"http://{args.host}:{args.port}"

df = pd.read_csv(args.file)
ranged_df = df.iloc[args.start:args.end]

def send_request(row):
    essay_data = {
        "prompt_id": row['prompt_id'],
        "essay_output": row["AI_Essay"], 
        "student_id": row["student_id"]
    }
    try:
        logging.info(f"Sending data for student ID: {row['student_id']}")
        response = requests.post(f"{BASE_URL}/evaluate", json=essay_data, timeout=3000)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Request failed with HTTPError: {response.status_code} - {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed with RequestException: {e}")
        return None

def process_dataset_loop(df, sleep_time):
    results = []
    for index, row in df.iterrows():
        logging.info(f"Processing row {index}")
        results.append(send_request(row))
        time.sleep(sleep_time) 
    return results

responses = process_dataset_loop(ranged_df, args.interval)

responses_df = pd.DataFrame(responses)
responses_df.to_csv('evaluation_responses.csv', index=False)

logging.info("Finished sending requests and receiving responses.")
