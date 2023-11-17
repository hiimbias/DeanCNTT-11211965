import pandas as pd
from mlxtend.frequent_patterns import association_rules, apriori
from sklearn.neighbors import NearestNeighbors
import tkinter as tk
from tkinter import filedialog

class SystemData:
    def __init__(self):
        self.my_basket = None
        self.frequent_items = None
        self.rules = None
        self.recommendation_model = None

def load_and_preprocess_data(file_path):
    try:
        df = pd.read_csv(file_path, usecols=['Transaction', 'Item'])
        if 'Transaction' not in df.columns or 'Item' not in df.columns:
            raise ValueError("Missing required columns in the file.")

        df['Item'] = df['Item'].str.strip().str.lower()
        transactions_str = df.groupby(['Transaction', 'Item'])['Item'].count().reset_index(name='Count')
        my_basket = transactions_str.pivot_table(index='Transaction', columns='Item', values='Count', aggfunc='sum').fillna(0)
        return my_basket
    except Exception as e:
        print(f"Error loading and preprocessing data: {e}")
        return None

def encode(x):
    return 1 if x >= 1 else 0

def update_system_data(system_data, input_data):
    system_data.my_basket = pd.concat([system_data.my_basket, input_data]).groupby(level=0).sum()
    system_data.frequent_items = apriori(system_data.my_basket.applymap(encode), min_support=0.001, use_colnames=True)
    system_data.rules = association_rules(system_data.frequent_items, metric="lift", min_threshold=1)
    system_data.rules.sort_values('confidence', ascending=False, inplace=True)
    system_data.recommendation_model = train_recommendation_model(system_data.my_basket)
    return system_data

def train_recommendation_model(my_basket):
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5)
    model.fit(my_basket.T)
    return model

def find_frequent_itemsets(input_text, system_data):
    if system_data.rules is None:
        print("System data rules have not been initialized.")
        return []

    input_items = [item.strip() for item in input_text.split(',')]
    frequent_itemsets = []
    for index, row in system_data.rules.iterrows():
        antecedents = set(row['antecedents'])
        consequents = set(row['consequents'])
        if all(item in antecedents for item in input_items):
            frequent_itemsets.append((consequents, row['support'], row['confidence'], row['lift']))
    return frequent_itemsets

def find_similar_items(input_text, system_data):
    input_item = input_text.strip().lower()

    if input_item in system_data.my_basket.columns:
        distances, indices = system_data.recommendation_model.kneighbors(system_data.my_basket[input_item].values.reshape(1, -1))
        similar_items = system_data.my_basket.columns[indices.flatten()][1:]  # Exclude the input item itself
        return similar_items
    else:
        return []

def show_frequent_itemsets():
    global system_data
    input_text = input_entry.get().strip().lower()
    frequent_itemsets = find_frequent_itemsets(input_text, system_data)
    if frequent_itemsets:
        result_label.config(text="Frequent itemsets frequently appearing with {}:".format(input_text))
        frequent_itemsets_text.config(state=tk.NORMAL)
        frequent_itemsets_text.delete(1.0, tk.END)
        for itemsets in frequent_itemsets:
            frequent_itemsets_text.insert(tk.END, f"Items: {', '.join(itemsets[0])}\n")
        frequent_itemsets_text.config(state=tk.DISABLED)
    else:
        result_label.config(text="No frequent itemsets found for {}".format(input_text))

def show_similar_items():
    global system_data
    input_text = input_entry.get().strip().lower()
    similar_items = find_similar_items(input_text, system_data)
    if len(similar_items) > 0:
        result_label.config(text="Sản phẩm {} nên được kết hợp với những sản phẩm sau đây:".format(input_text))
        frequent_itemsets_text.config(state=tk.NORMAL)
        frequent_itemsets_text.delete(1.0, tk.END)
        frequent_itemsets_text.insert(tk.END, ", ".join(similar_items))
        frequent_itemsets_text.config(state=tk.DISABLED)
    else:
        result_label.config(text="Không tìm thấy sản phẩm tương tự cho {}".format(input_text))

def load_new_data(system_data):
    try:
        file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
        if file_path:
            new_data = load_and_preprocess_data(file_path)
            if new_data is not None:
                if system_data.my_basket is None:
                    system_data = SystemData()
                system_data = update_system_data(system_data, new_data)
                result_label.config(text="New dataset loaded successfully.")
                return system_data
            else:
                result_label.config(text="Error loading the new dataset.")
    except Exception as e:
        print(f"Error loading new data: {e}")

# Create SystemData instance
system_data = SystemData()

# Load and preprocess initial data
initial_data_path = "bread basket (1).csv"
initial_data = load_and_preprocess_data(initial_data_path)

if initial_data is not None:
    update_system_data(system_data, initial_data)
else:
    print("Error loading initial data.")

# Create the GUI window
root = tk.Tk()
root.title("Integrated System")

input_label = tk.Label(root, text="Enter a product or itemset (comma-separated):")
input_label.pack(pady=10)

input_entry = tk.Entry(root)
input_entry.pack()

find_button = tk.Button(root, text="Find Frequent Itemsets", command=show_frequent_itemsets)
find_button.pack(pady=10)

recommend_button = tk.Button(root, text="Recommend Similar Items", command=show_similar_items)
recommend_button.pack(pady=10)

load_data_button = tk.Button(root, text="Load New Dataset", command=lambda: load_new_data(system_data))
load_data_button.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=300)
result_label.pack()

frequent_itemsets_text = tk.Text(root, height=30, width=60, state=tk.DISABLED)
frequent_itemsets_text.pack()

root.mainloop()
