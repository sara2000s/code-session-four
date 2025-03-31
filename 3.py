import pandas as pd
import hashlib
import time
import json

# Block class for blockchain structure
class Block:
    def __init__(self, index, previous_hash, timestamp, sensor_data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sensor_data = sensor_data  # Dictionary: avg heart rate and glucose
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the current block's hash"""
        value = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.sensor_data)}".encode()
        return hashlib.sha256(value).hexdigest()

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Create the Genesis block"""
        genesis_data = {"avg_heart_rate": 0, "glucose": 0}
        timestamp = time.time()
        return Block(0, "0", timestamp, genesis_data)

    def add_block(self, sensor_data):
        """Add a new block to the chain"""
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = time.time()
        new_block = Block(index, previous_block.current_hash, timestamp, sensor_data)
        self.chain.append(new_block)
        return new_block

    def print_chain(self):
        """Display the blockchain"""
        for block in self.chain:
            print(json.dumps({
                "Index": block.index,
                "Previous Hash": block.previous_hash,
                "Timestamp": block.timestamp,
                "Sensor Data": block.sensor_data,
                "Current Hash": block.current_hash
            }, indent=4))

# Load and process ECG data for average heart rate
def load_ecg_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        ecg_signals = data.iloc[:, :-1]  # Columns 0-186 (ECG signals)
        
        # Simulate a 5-minute interval with first 5 rows
        interval_data = ecg_signals.head(5)
        avg_heart_rate = interval_data.mean().mean() * 10 + 60  # Simple approximation
        return avg_heart_rate
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0
    except Exception as e:
        print(f"Error loading ECG data: {e}")
        return 0

# Load and process Diabetes data for glucose
def load_glucose_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        glucose_data = data['blood_glucose_level'].head(5)  # First 5 rows
        avg_glucose = glucose_data.mean()  # Average over interval
        return avg_glucose
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return 0
    except Exception as e:
        print(f"Error loading Diabetes data: {e}")
        return 0

# Main function
def main():
    # File paths
    ecg_path = r"D:\سارا\ترم 3 دانشگاه قم\mitbih_test.csv"
    diabetes_path = r"D:\سارا\ترم 3 دانشگاه قم\diabetes_prediction_dataset.csv"

    # Load sensor data
    avg_heart_rate = load_ecg_sensor_data(ecg_path)
    avg_glucose = load_glucose_sensor_data(diabetes_path)

    # Initialize blockchain
    blockchain = Blockchain()

    # Add 5 blocks to simulate 5 intervals
    for i in range(5):
        sensor_data = {
            "avg_heart_rate": avg_heart_rate + random.uniform(-5, 5),  # Add variation
            "glucose": avg_glucose + random.uniform(-10, 10)           # Add variation
        }
        block = blockchain.add_block(sensor_data)
        print(f"Added Block {block.index} with Hash: {block.current_hash[:8]}...")

    # Display the blockchain
    print("\nBlockchain Structure:")
    blockchain.print_chain()

if __name__ == "__main__":
    import random  # For simulating variations
    main()