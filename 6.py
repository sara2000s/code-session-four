import pandas as pd
import numpy as np

# تابع بارگذاری و پردازش داده‌های ECG برای ضربان قلب
def load_ecg_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        ecg_signals = data.iloc[:, :-1].head(5)  # ۵ ردیف اول، بدون ستون برچسب
        # محاسبه تقریبی ضربان قلب برای هر ردیف
        heart_rates = ecg_signals.mean(axis=1).apply(lambda x: int(60 + (x * 10)))
        heart_rate_mean = np.mean(heart_rates)
        heart_rate_std = np.std(heart_rates)
        return heart_rate_mean, heart_rate_std, heart_rates.tolist()
    except FileNotFoundError:
        print(f"خطا: فایل {file_path} یافت نشد.")
        return 0, 0, [0] * 5
    except Exception as e:
        print(f"خطا در بارگذاری داده‌های ECG: {e}")
        return 0, 0, [0] * 5

# تابع بارگذاری و پردازش داده‌های گلوکز
def load_glucose_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        glucose_data = data['Glucose'].head(5)  # ۵ ردیف اول، ستون Glucose
        glucose_mean = np.mean(glucose_data)
        glucose_std = np.std(glucose_data)
        return glucose_mean, glucose_std, glucose_data.tolist()
    except FileNotFoundError:
        print(f"خطا: فایل {file_path} یافت نشد.")
        return 0, 0, [0] * 5
    except Exception as e:
        print(f"خطا در بارگذاری داده‌های دیابت: {e}")
        return 0, 0, [0] * 5

# تابع اصلی
def main():
    # مسیر فایل‌ها
    ecg_path = r"D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\mitbih_test.csv"
    diabetes_path = r"D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\diabetes.csv"

    # بارگذاری و محاسبه آمار ضربان قلب
    heart_rate_mean, heart_rate_std, heart_rates = load_ecg_sensor_data(ecg_path)
    print("داده‌های ضربان قلب (Heart Rate):")
    print(f"مقادیر: {heart_rates}")
    print(f"میانگین ضربان قلب: {heart_rate_mean:.2f}")
    print(f"انحراف معیار ضربان قلب: {heart_rate_std:.2f}\n")

    # بارگذاری و محاسبه آمار گلوکز
    glucose_mean, glucose_std, glucose_levels = load_glucose_sensor_data(diabetes_path)
    print("داده‌های گلوکز (Glucose):")
    print(f"مقادیر: {glucose_levels}")
    print(f"میانگین گلوکز: {glucose_mean:.2f}")
    print(f"انحراف معیار گلوکز: {glucose_std:.2f}")

if __name__ == "__main__":
    main()