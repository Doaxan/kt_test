import os
import threading

from fastapi import FastAPI

from btc_api import get_btc_api
from db import read_data_table, insert_api_to_table
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.get("/last")
async def get_last():
    timer.cancel()
    api = update_api_timer()
    return api


@app.get("/history")
async def get_history():
    return read_data_table()


def update_api_timer():
    global timer
    timer = threading.Timer(float(os.getenv('UPDATE_MIN', 5.0)) * 60.0, update_api_timer)
    api = get_btc_api()
    insert_api_to_table(api)
    timer.start()
    return api


update_api_timer()
