import pandas as pd
from mlxtend.frequent_patterns import association_rules, apriori
from sklearn.neighbors import NearestNeighbors
import joblib
import tkinter as tk

# Load and preprocess the data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['Item'] = df['Item'].str.strip().str.lower()
    transactions_str = df.groupby(['Transaction', 'Item'])['Item'].count().reset_index(name='Count')
    my_basket = transactions_str.pivot_table(index='Transaction', columns='Item', values='Count', aggfunc='sum').fillna(0)
    return my_basket

def encode(x):
    return 1 if x >= 1 else 0

def train_recommendation_model(my_basket):
    # Train a recommendation model using Nearest Neighbors
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5)
    model.fit(my_basket.T)  # Transpose the basket data for item-based recommendations
    return model

def find_similar_items(input_text, my_basket, model):
    # input_item = input_text.strip().lower()
    input_item = [item.strip() for item in input_text.split(',')]
    
    # Check if the input item is in the basket data
    if input_item in my_basket.columns:
        # Find similar items using the recommendation model
        distances, indices = model.kneighbors(my_basket[input_item].values.reshape(1, -1))
        similar_items = my_basket.columns[indices.flatten()]
        return similar_items[1:]  # Exclude the input item itself
    else:
        return []

def show_similar_items():
    input_text = input_entry.get().strip().lower()
    
    # Find similar items using the recommendation model
    similar_items = find_similar_items(input_text, my_basket, recommendation_model)
    
    if len(similar_items) > 0:
        result_label.config(text="Sản phẩm {} nên được kết hợp với những sản phẩm sau đây:".format(input_text))
        frequent_itemsets_text.config(state=tk.NORMAL)
        frequent_itemsets_text.delete(1.0, tk.END)
        frequent_itemsets_text.insert(tk.END, ", ".join(similar_items))
        frequent_itemsets_text.config(state=tk.DISABLED)
    else:
        result_label.config(text="No similar items found for {}".format(input_text))


# Load and preprocess data
my_basket = load_and_preprocess_data("new.csv")

# Train recommendation model
recommendation_model = train_recommendation_model(my_basket)

# Create the GUI window
root = tk.Tk()
root.title("Hệ thống gợi ý kết hợp sản phẩm")

input_label = tk.Label(root, text="Nhập vào tên sản phẩm:")
input_label.pack(pady=10)

input_entry = tk.Entry(root)
input_entry.pack()

find_button = tk.Button(root, text="Gợi ý sản phẩm kết hợp", command=show_similar_items)
find_button.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=300)
result_label.pack()

frequent_itemsets_text = tk.Text(root, height=30, width=60, state=tk.DISABLED)
frequent_itemsets_text.pack()

root.mainloop()
