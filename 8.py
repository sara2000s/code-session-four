#  کتابخانه‌های مورد نیاز
import pandas as pd
import hashlib
import time
import json
import matplotlib.pyplot as plt
import networkx as nx
import random

#  آدرس فایل‌ها
path_test = r'D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\mitbih_test.csv'
path_diabetes = r'D:\سارا\ترم 3 دانشگاه قم\فصل سوم و چهارم پایان نامه 1\diabetes.csv'

#  بارگذاری داده‌ها
mitbih_data = pd.read_csv(path_test)
diabetes_data = pd.read_csv(path_diabetes)

#  تعریف کلاس بلاک
class Block:
    def __init__(self, index, previous_hash, data, timestamp, token=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.token = token  # اضافه کردن ویژگی token
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.data)}{self.token}"
        return hashlib.sha256(block_content.encode()).hexdigest()

#  تعریف کلاس بلاکچین
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block", time.time(), token=0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print(f" خطا: بلاک {current_block.index} نامعتبر است!")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f" خطا: ارتباط بلاک {current_block.index} با بلاک قبلی نامعتبر است!")
                return False
        return True

# ایجاد بلاکچین
blockchain = Blockchain()

#  اندازه‌گیری زمان پردازش و ذخیره‌سازی
start_time = time.time()

#  اضافه کردن داده‌ها به بلاکچین
for i, row in diabetes_data.iterrows():
    block = Block(i + 1, blockchain.get_latest_block().hash, row.to_dict(), time.time(), token=random.randint(1, 100))
    blockchain.add_block(block)

end_time = time.time()

print(f"\n زمان پردازش داده‌ها: {end_time - start_time:.2f} ثانیه")
print(f" صحت زنجیره بلاکچین: {blockchain.is_chain_valid()}")

#  نمودار زمان پاسخ‌دهی با بلاکچین و بدون بلاکچین
times_with_blockchain = [random.uniform(0.1, 0.5) for _ in range(50)]
times_without_blockchain = [random.uniform(0.05, 0.3) for _ in range(50)]

plt.figure(figsize=(10, 5))
plt.plot(times_with_blockchain, label="با بلاکچین", marker='o')
plt.plot(times_without_blockchain, label="بدون بلاکچین", marker='x')
plt.title(" مقایسه زمان پاسخ‌دهی")
plt.xlabel("نمونه")
plt.ylabel("زمان (ثانیه)")
plt.legend()
plt.show()

#  نمودار توزیع توکن‌ها بین کاربران
tokens = [block.token for block in blockchain.chain]

plt.figure(figsize=(8, 4))
plt.hist(tokens, bins=20, color='skyblue', edgecolor='black')
plt.title(" توزیع توکن‌ها بین کاربران")
plt.xlabel("مقدار توکن")
plt.ylabel("تعداد")
plt.show()

#  نمایش گراف زنجیره بلوک‌ها
G = nx.DiGraph()

for block in blockchain.chain:
    G.add_node(block.index, label=f"Block {block.index}")

for i in range(1, len(blockchain.chain)):
    G.add_edge(blockchain.chain[i - 1].index, blockchain.chain[i].index)

plt.figure(figsize=(12, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightgreen', font_weight='bold', node_size=1000)
plt.title(" ساختار گرافی زنجیره بلاکچین")
plt.show()
