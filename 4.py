import pandas as pd
import hashlib
import time
import json

# Block class with SHA-256 hashing
class Block:
    def __init__(self, index, previous_hash, timestamp, sensor_data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sensor_data = sensor_data  # Dictionary: heart rate and glucose
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate SHA-256 hash of the block for security and integrity"""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.sensor_data)}".encode()
        return hashlib.sha256(block_string).hexdigest()

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Create the Genesis block with initial dummy data"""
        genesis_data = {"heart_rate": 0, "glucose": 0}
        timestamp = time.time()
        return Block(0, "0", timestamp, genesis_data)

    def add_block(self, sensor_data):
        """Add a new block with SHA-256 hashed data"""
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = time.time()
        new_block = Block(index, previous_block.current_hash, timestamp, sensor_data)
        self.chain.append(new_block)
        return new_block

    def print_chain(self):
        """Display the blockchain with hashed data"""
        for block in self.chain:
            print(json.dumps({
                "Index": block.index,
                "Previous Hash": block.previous_hash,
                "Timestamp": block.timestamp,
                "Sensor Data": block.sensor_data,
                "Current Hash": block.current_hash
            }, indent=4))

    def is_chain_valid(self):
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            # Recalculate hash to check integrity
            if current_block.current_hash != current_block.calculate_hash():
                print(f"Integrity check failed at Block {i}: Hash mismatch")
                return False
            if current_block.previous_hash != previous_block.current_hash:
                print(f"Integrity check failed at Block {i}: Previous hash mismatch")
                return False
        return True

# Load and process ECG data for heart rate (no averaging, individual rows)
def load_ecg_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        ecg_signals = data.iloc[:, :-1].head(5)  # First 5 rows, excluding label
        # Convert each row's ECG signals to an approximate heart rate
        heart_rates = ecg_signals.mean(axis=1).apply(lambda x: int(60 + (x * 10)))
        return heart_rates.tolist()  # Return as a list of 5 values
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return [0] * 5  # Return 5 zeros if error
    except Exception as e:
        print(f"Error loading ECG data: {e}")
        return [0] * 5

# Load and process Diabetes data for glucose (no averaging, individual rows)
def load_glucose_sensor_data(file_path):
    try:
        data = pd.read_csv(file_path)
        glucose_data = data['blood_glucose_level'].head(5)  # First 5 rows
        return glucose_data.tolist()  # Return as a list of 5 values
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return [0] * 5  # Return 5 zeros if error
    except Exception as e:
        print(f"Error loading Diabetes data: {e}")
        return [0] * 5

# Main function
def main():
    # File paths
    ecg_path = r"D:\سارا\ترم 3 دانشگاه قم\mitbih_test.csv"
    diabetes_path = r"D:\سارا\ترم 3 دانشگاه قم\diabetes_prediction_dataset.csv"

    # Load sensor data
    heart_rates = load_ecg_sensor_data(ecg_path)
    glucose_levels = load_glucose_sensor_data(diabetes_path)

    # Initialize blockchain
    blockchain = Blockchain()

    # Add 5 blocks using actual data from each row
    for i in range(5):
        sensor_data = {
            "heart_rate": heart_rates[i],    # Individual heart rate from ECG
            "glucose": glucose_levels[i]     # Individual glucose level
        }
        block = blockchain.add_block(sensor_data)
        print(f"Added Block {block.index} with SHA-256 Hash: {block.current_hash[:8]}...")

    # Display the blockchain
    print("\nBlockchain Structure with SHA-256 Hashing:")
    blockchain.print_chain()

    # Verify blockchain integrity
    print("\nBlockchain Integrity Check:")
    is_valid = blockchain.is_chain_valid()
    print(f"Is the blockchain valid? {is_valid}")

if __name__ == "__main__":
    main()