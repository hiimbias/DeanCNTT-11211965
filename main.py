import pandas as pd
from mlxtend.frequent_patterns import association_rules, apriori
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

def find_frequent_itemsets(input_text, my_basket, rules):
    input_items = [item.strip() for item in input_text.split(',')]
    frequent_itemsets = set()
    for index, row in rules.iterrows():
        itemset = set(row['antecedents'])
        consequent_item = list(row['consequents'])[0]
        if all(item in itemset for item in input_items):
            frequent_itemsets.add(consequent_item)
    return frequent_itemsets

def show_frequent_itemsets():
    input_text = input_entry.get().strip().lower()
    frequent_itemsets = find_frequent_itemsets(input_text, my_basket, rules)
    if frequent_itemsets:
        result_label.config(text="The frequent itemsets that frequently appear with {} are:".format(input_text))
        frequent_itemsets_text.config(state=tk.NORMAL)
        frequent_itemsets_text.delete(1.0, tk.END)
        for item in frequent_itemsets:
            frequent_itemsets_text.insert(tk.END, item + "\n")
        frequent_itemsets_text.config(state=tk.DISABLED)
    else:
        result_label.config(text="No frequent itemsets found for {}".format(input_text))
        


# Load and preprocess data
my_basket = load_and_preprocess_data("new_dataset.csv")

# Use the 'apriori algorithm' with min_support=0.01
frequent_items = apriori(my_basket.applymap(encode), min_support=0.001, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_items, metric="lift", min_threshold=1)
rules.sort_values('confidence', ascending=False, inplace=True)

# Create the GUI window
root = tk.Tk()
root.title("Frequent Itemsets Finder")

input_label = tk.Label(root, text="Enter a product or itemset (comma-separated):")
input_label.pack(pady=10)

input_entry = tk.Entry(root)
input_entry.pack()

find_button = tk.Button(root, text="Find Frequent Itemsets", command=show_frequent_itemsets)
find_button.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=300)
result_label.pack()

frequent_itemsets_text = tk.Text(root, height=30, width=40, state=tk.DISABLED)  # Increase the height
frequent_itemsets_text.pack()



root.mainloop()
