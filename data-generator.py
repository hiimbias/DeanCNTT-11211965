import random
from datetime import datetime, timedelta

def format_item_name(item_name):
    # Viết hoa chữ cái đầu và bỏ dấu cách giữa các từ
    return ' '.join(word.capitalize() for word in item_name.split())

def generate_sample(transaction_id):
    # items = [
    #     'bread', 'scandinavian', 'hot chocolate', 'jam', 'cookies', 'muffin', 'coffee',
    #     'pastry', 'medialuna', 'tea', 'tartine', 'basket', 'mineral water', 'farm house',
    #     'fudge', 'juice', "ella's kitchen pouches", 'victorian sponge', 'frittata',
    #     'hearty & seasonal', 'soup', 'pick and mix bowls', 'smoothies', 'cake',
    #     'mighty protein', 'chicken sand', 'coke', 'my-5 fruit shoot', 'focaccia', 'sandwich',
    #     'alfajores', 'eggs', 'brownie', 'dulce de leche', 'honey', 'the bart', 'granola',
    #     'fairy doors', 'empanadas', 'keeping it local', 'art tray', 'bowl nic pitt',
    #     'bread pudding', 'adjustment', 'truffles', 'chimichurri oil', 'bacon', 'spread',
    #     'kids biscuit', 'siblings', 'caramel bites', 'jammie dodgers', 'tiffin',
    #     'olum & polenta', 'polenta', 'the nomad', 'hack the stack', 'bakewell',
    #     'lemon and coconut', 'toast', 'scone', 'crepes', 'vegan mincepie', 'bare popcorn',
    #     'muesli', 'crisps', 'pintxos', 'gingerbread syrup', 'panatone', 'brioche and salami',
    #     'afternoon with the baker', 'salad', 'chicken stew', 'spanish brunch',
    #     'raspberry shortbread sandwich', 'extra salami or feta', 'duck egg', 'baguette',
    #     "valentine's card", 'tshirt', 'vegan feast', 'postcard', 'nomad bag', 'chocolates',
    #     'coffee granules', 'drinking chocolate spoons', 'christmas common', 'argentina night',
    #     'half slice monster', 'gift voucher', 'cherry me dried fruit', 'mortimer', 'raw bars',
    #     'tacos/fajita', 'latte', 'croissant', 'cappuccino', 'danish', 'americano', 'espresso',
    #     'bagel', 'macchiato', 'flatwhite', 'eclair', 'cortado', 'oatmeal', 'affogato', 'mocha',
    #     'quiche', 'ristretto', 'lungo', 'irish coffee', 'fruittart', 'biscotti', 'cheesecake'
    # ]
    items = [
    'new bread', 'new scandinavian', 'new hot chocolate', 'new jam', 'new cookies', 'new muffin', 'new coffee',
    'new pastry', 'new medialuna', 'new tea', 'new tartine', 'new basket', 'new mineral water', 'new farm house',
    'new fudge', 'new juice', "new ella's kitchen pouches", 'new victorian sponge', 'new frittata',
    'new hearty & seasonal', 'new soup', 'new pick and mix bowls', 'new smoothies', 'new cake',
    'new mighty protein', 'new chicken sand', 'new coke', 'new my-5 fruit shoot', 'new focaccia', 'new sandwich',
    'new alfajores', 'new eggs', 'new brownie', 'new dulce de leche', 'new honey', 'new the bart', 'new granola',
    'new fairy doors', 'new empanadas', 'new keeping it local', 'new art tray', 'new bowl nic pitt',
    'new bread pudding', 'new adjustment', 'new truffles', 'new chimichurri oil', 'new bacon', 'new spread',
    'new kids biscuit', 'new siblings', 'new caramel bites', 'new jammie dodgers', 'new tiffin',
    'new olum & polenta', 'new polenta', 'new the nomad', 'new hack the stack', 'new bakewell',
    'new lemon and coconut', 'new toast', 'new scone', 'new crepes', 'new vegan mincepie', 'new bare popcorn',
    'new muesli', 'new crisps', 'new pintxos', 'new gingerbread syrup', 'new panatone', 'new brioche and salami',
    'new afternoon with the baker', 'new salad', 'new chicken stew', 'new spanish brunch',
    'new raspberry shortbread sandwich', 'new extra salami or feta', 'new duck egg', 'new baguette',
    "new valentine's card", 'new tshirt', 'new vegan feast', 'new postcard', 'new nomad bag', 'new chocolates',
    'new coffee granules', 'new drinking chocolate spoons', 'new christmas common', 'new argentina night',
    'new half slice monster', 'new gift voucher', 'new cherry me dried fruit', 'new mortimer', 'new raw bars',
    'new tacos/fajita', 'new latte', 'new croissant', 'new cappuccino', 'new danish', 'new americano', 'new espresso',
    'new bagel', 'new macchiato', 'new flatwhite', 'new eclair', 'new cortado', 'new oatmeal', 'new affogato', 'new mocha',
    'new quiche', 'new ristretto', 'new lungo', 'new irish coffee', 'new fruittart', 'new biscotti', 'new cheesecake']


    period_of_day_mapping = {
        'morning': (6, 11),
        'afternoon': (12, 16),
        'evening': (17, 19),
        'night': (20, 23)
    }

    period_of_day = random.choice(['morning', 'afternoon', 'evening', 'night'])
    weekday = random.choice(['weekday', 'weekend'])
    start_hour, end_hour = period_of_day_mapping[period_of_day]
    time_format = "%d-%m-%Y %H:%M"
    base_date = datetime(2017, 1, 1)
    date_time = base_date + timedelta(
        days=random.randint(0, 500),
        hours=random.randint(start_hour, end_hour),
        minutes=random.randint(0, 59)
    )

    num_items = random.randint(1, 15)
    selected_items = random.sample(items, num_items)
    formatted_items = [format_item_name(item) for item in selected_items]

    samples = []
    for item in formatted_items:
        sample = f"{transaction_id},{item},{date_time.strftime(time_format)},{period_of_day},{weekday}"
        samples.append(sample)

    return samples

def generate_samples(start_transaction_id, num_samples):
    all_samples = []
    for i in range(start_transaction_id, start_transaction_id + num_samples):
        samples = generate_sample(i)
        all_samples.extend(samples)
    return all_samples

# Example: Generate 10 samples starting from transaction ID 9912
samples = generate_samples(1, 100)
for sample in samples:
    print(sample)
