import pandas as pd
import hashlib
import time
import json

# کلاس بلوک
class Block:
    def __init__(self, index, previous_hash, timestamp, sensor_data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sensor_data = sensor_data  # دیکشنری شامل ضربان قلب و گلوکز
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """محاسبه هش SHA-256 برای بلوک جهت امنیت و یکپارچگی"""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.sensor_data)}".encode()
        return hashlib.sha256(block_string).hexdigest()

# کلاس زنجیره بلاکچین
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """ایجاد بلوک اولیه (جنسیس) با داده‌های صفر"""
        genesis_data = {"heart_rate": 0, "glucose": 0}
        timestamp = time.time()
        return Block(0, "0", timestamp, genesis_data)

    def add_block(self, sensor_data):
        """اضافه کردن بلوک جدید به زنجیره"""
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = time.time()
        new_block = Block(index, previous_block.current_hash, timestamp, sensor_data)
        self.chain.append(new_block)
        return new_block

    def verify_chain(self):
        """تأیید درستی زنجیره بلاکچین"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # بررسی صحت هش فعلی
            if current_block.current_hash != current_block.calculate_hash():
                print(f"خطا در تأیید بلوک {i}: عدم تطابق هش")
                return False
            
            # بررسی ارتباط هش قبلی
            if current_block.previous_hash != previous_block.current_hash:
                print(f"خطا در تأیید بلوک {i}: عدم تطابق هش قبلی")
                return False
        
        return True

    def print_chain(self):
        """نمایش ساختار زنجیره بلاکچین"""
        for block in self.chain:
            print(json.dumps({
                "Index": block.index,
                "Previous Hash": block.previous_hash,
                "Timestamp": block.timestamp,
                "Sensor Data": block.sensor_data,
                "Current Hash": block.current_hash
            }, indent=4))

# تابع بارگذاری داده‌های حسگر ضربان قلب از ECG
def load_ecg_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        ecg_signals = data.iloc[:, :-1].head(5)  # ۵ ردیف اول، بدون ستون برچسب
        # محاسبه تقریبی ضربان قلب برای هر ردیف
        heart_rates = ecg_signals.mean(axis=1).apply(lambda x: int(60 + (x * 10)))
        return heart_rates.tolist()
    except FileNotFoundError:
        print(f"خطا: فایل {file_path} یافت نشد.")
        return [0] * 5
    except Exception as e:
        print(f"خطا در بارگذاری داده‌های ECG: {e}")
        return [0] * 5

# تابع بارگذاری داده‌های حسگر گلوکز از دیتاست دیابت
def load_glucose_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        glucose_data = data['blood_glucose_level'].head(5)  # ۵ ردیف اول
        return glucose_data.tolist()
    except FileNotFoundError:
        print(f"خطا: فایل {file_path} یافت نشد.")
        return [0] * 5
    except Exception as e:
        print(f"خطا در بارگذاری داده‌های دیابت: {e}")
        return [0] * 5

# تابع اصلی
def main():
    # مسیر فایل‌ها
    ecg_path = r"D:\سارا\ترم 3 دانشگاه قم\mitbih_test.csv"
    diabetes_path = r"D:\سارا\ترم 3 دانشگاه قم\diabetes_prediction_dataset.csv"

    # بارگذاری داده‌های حسگر
    heart_rates = load_ecg_sensor_data(ecg_path)
    glucose_levels = load_glucose_sensor_data(diabetes_path)

    # ایجاد زنجیره بلاکچین
    blockchain = Blockchain()

    # اضافه کردن بلوک‌ها با داده‌های واقعی
    for i in range(5):
        sensor_data = {
            "heart_rate": heart_rates[i],
            "glucose": glucose_levels[i]
        }
        block = blockchain.add_block(sensor_data)
        print(f"بلوک {block.index} با هش: {block.current_hash[:8]}... اضافه شد")

    # نمایش زنجیره بلاکچین
    print("\nساختار زنجیره بلاکچین:")
    blockchain.print_chain()

    # تأیید زنجیره بلاکچین
    print("\nبررسی صحت زنجیره بلاکچین:")
    is_valid = blockchain.verify_chain()
    print(f"آیا زنجیره بلاکچین معتبر است؟ {is_valid}")

if __name__ == "__main__":
    main()