import hashlib
import time
import json
from typing import List
from cryptography.fernet import Fernet
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import random

# تابع خواندن داده‌های حسگر قند خون
def load_glucose_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        glucose_data = data[['Glucose']].head(5)  # ۵ ردیف اول، ستون Glucose
        glucose_data.columns = ['Glucose']  # نام ستون ثابت می‌مونه
        glucose_data['patient_id'] = [f"P{str(i+1).zfill(3)}" for i in range(len(glucose_data))]
        return glucose_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading glucose data: {e}")
        return pd.DataFrame()

# تابع خواندن داده‌های حسگر ضربان قلب
def load_heart_rate_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        ecg_data = data.iloc[:, :-1].head(5)  # ۵ ردیف اول بدون برچسب
        # تبدیل ساده سیگنال ECG به ضربان قلب تقریبی (میانگین سیگنال)
        heart_rate_data = pd.DataFrame({
            'Heart_Rate': ecg_data.mean(axis=1).apply(lambda x: int(60 + (x * 10)))
        })
        heart_rate_data['patient_id'] = [f"P{str(i+1).zfill(3)}" for i in range(len(heart_rate_data))]
        return heart_rate_data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading ECG data: {e}")
        return pd.DataFrame()

# تابع ترکیب داده‌ها
def combine_sensor_data(glucose_data, heart_rate_data):
    if glucose_data.empty or heart_rate_data.empty:
        return pd.DataFrame()
    combined_data = pd.merge(
        glucose_data[['patient_id', 'Glucose']],
        heart_rate_data[['patient_id', 'Heart_Rate']],
        on='patient_id'
    )
    return combined_data

# مسیر فایل‌ها
glucose_path = r"D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\diabetes.csv"
heart_rate_path = r"D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\mitbih_test.csv"

# خواندن داده‌ها
glucose_sensor_data = load_glucose_sensor_data(glucose_path)
heart_rate_sensor_data = load_heart_rate_sensor_data(heart_rate_path)

# ترکیب داده‌ها
sensor_data = combine_sensor_data(glucose_sensor_data, heart_rate_sensor_data)

# نمایش داده‌ها
if not sensor_data.empty:
    print("Sensor Data (Glucose and Heart Rate):")
    print(sensor_data.to_string(index=False))
else:
    print("No sensor data loaded.")
