# 📦 کتابخانه‌های مورد نیاز
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 📂 بارگذاری داده‌ها
file_path = 'path/to/dataset.csv'  # مسیر فایل خود را جایگزین کنید
data = pd.read_csv(file_path)

# 📝 1. شناسایی داده‌های گمشده
print("🔎 بررسی مقادیر گمشده:")
print(data.isnull().sum())

# 🚮 2. حذف داده‌های گمشده
data = data.dropna()
print("\n✅ پس از حذف داده‌های گمشده:")
print(data.info())

# 🚫 3. شناسایی مقادیر نامعتبر (مثل اعداد منفی در ویژگی‌های غیرمنطقی)
invalid_rows = data[(data < 0).any(axis=1)]
print("\n🚨 مقادیر نامعتبر:")
print(invalid_rows)

# 🗑️ 4. حذف داده‌های نامعتبر
data = data[(data >= 0).all(axis=1)]
print("\n✅ پس از حذف داده‌های نامعتبر:")
print(data.info())

# 📊 5. نرمال‌سازی داده‌ها با استفاده از Min-Max Scaler
scaler = MinMaxScaler()

# فقط ستون‌های عددی را نرمال‌سازی می‌کنیم
numeric_cols = data.select_dtypes(include=[np.number]).columns
data[numeric_cols] = scaler.fit_transform(data[numeric_cols])

print("\n📏 پس از نرمال‌سازی داده‌ها:")
print(data.head())

# 💾 ذخیره داده‌های پاکسازی و نرمال‌سازی شده
cleaned_file_path = 'cleaned_normalized_dataset.csv'
data.to_csv(cleaned_file_path, index=False)
print(f"\n✅ داده‌های پاکسازی و نرمال‌سازی شده در فایل '{cleaned_file_path}' ذخیره شدند.")
