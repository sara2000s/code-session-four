import pandas as pd
import hashlib
import time
import json
import numpy as np

# Class for individual blocks
class Block:
    def __init__(self, index, previous_hash, timestamp, sensor_stats):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sensor_stats = sensor_stats  # Dictionary with mean and std of heart rate and glucose
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate SHA-256 hash of the block for security and integrity"""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.sensor_stats)}".encode()
        return hashlib.sha256(block_string).hexdigest()

# Class for the blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Create the Genesis block with initial dummy stats"""
        genesis_stats = {
            "heart_rate_mean": 0,
            "heart_rate_std": 0,
            "glucose_mean": 0,
            "glucose_std": 0
        }
        timestamp = time.time()
        return Block(0, "0", timestamp, genesis_stats)

    def add_block(self, sensor_stats):
        """Add a new block to the blockchain"""
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = time.time()
        new_block = Block(index, previous_block.current_hash, timestamp, sensor_stats)
        self.chain.append(new_block)
        return new_block

    def verify_chain(self):
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.current_hash != current_block.calculate_hash():
                print(f"خطا در تأیید بلوک {i}: عدم تطابق هش")
                return False
            if current_block.previous_hash != previous_block.current_hash:
                print(f"خطا در تأیید بلوک {i}: عدم تطابق هش قبلی")
                return False
        return True

    def print_chain(self):
        """Display the blockchain structure"""
        for block in self.chain:
            print(json.dumps({
                "Index": block.index,
                "Previous Hash": block.previous_hash,
                "Timestamp": block.timestamp,
                "Sensor Stats": block.sensor_stats,
                "Current Hash": block.current_hash
            }, indent=4))

# Load ECG sensor data and calculate mean and std for heart rate
def load_ecg_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        ecg_signals = data.iloc[:, :-1].head(5)  # First 5 rows, excluding label
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

# Load Diabetes sensor data and calculate mean and std for glucose
def load_glucose_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        glucose_data = data['Glucose'].head(5)  # First 5 rows
        glucose_mean = np.mean(glucose_data)
        glucose_std = np.std(glucose_data)
        return glucose_mean, glucose_std, glucose_data.tolist()
    except FileNotFoundError:
        print(f"خطا: فایل {file_path} یافت نشد.")
        return 0, 0, [0] * 5
    except Exception as e:
        print(f"خطا در بارگذاری داده‌های دیابت: {e}")
        return 0, 0, [0] * 5

# Main function
def main():
    # File paths
    ecg_path = r"D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\mitbih_test.csv"
    diabetes_path = r"D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\diabetes.csv"

    # Load and calculate statistics
    heart_rate_mean, heart_rate_std, heart_rates = load_ecg_sensor_data(ecg_path)
    glucose_mean, glucose_std, glucose_levels = load_glucose_sensor_data(diabetes_path)

    # Display raw data and statistics
    print("داده‌های ضربان قلب (Heart Rate):")
    print(f"مقادیر: {heart_rates}")
    print(f"میانگین ضربان قلب: {heart_rate_mean:.2f}")
    print(f"انحراف معیار ضربان قلب: {heart_rate_std:.2f}\n")

    print("داده‌های گلوکز (Glucose):")
    print(f"مقادیر: {glucose_levels}")
    print(f"میانگین گلوکز: {glucose_mean:.2f}")
    print(f"انحراف معیار گلوکز: {glucose_std:.2f}\n")

    # Initialize blockchain
    blockchain = Blockchain()

    # Add block with sensor statistics
    sensor_stats = {
        "heart_rate_mean": heart_rate_mean,
        "heart_rate_std": heart_rate_std,
        "glucose_mean": glucose_mean,
        "glucose_std": glucose_std
    }
    block = blockchain.add_block(sensor_stats)
    print(f"بلوک {block.index} با هش: {block.current_hash[:8]}... اضافه شد")

    # Display the blockchain
    print("\nساختار زنجیره بلاکچین:")
    blockchain.print_chain()

    # Verify the blockchain
    print("\nبررسی صحت زنجیره بلاکچین:")
    is_valid = blockchain.verify_chain()
    print(f"آیا زنجیره بلاکچین معتبر است؟ {is_valid}")

if __name__ == "__main__":
    main()