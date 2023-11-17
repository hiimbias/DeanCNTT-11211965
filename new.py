import pandas as pd

# Đọc dữ liệu từ tệp CSV
file_path = "bread basket (1).csv"
df = pd.read_csv(file_path)

# Thêm từ "New" vào phía trước của mỗi mục trong cột 'Item'
df['Item'] = 'New ' + df['Item']

# Lưu dữ liệu đã được cập nhật vào một tệp mới
new_file_path = "new bread basket (1).csv"
df.to_csv(new_file_path, index=False)

# In ra dữ liệu đã được cập nhật
print(df.head(100))