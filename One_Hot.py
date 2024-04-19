import random
import pandas as pd

def one_hot_convert(data):
    keys = set(data)
    df = pd.DataFrame()      
    for k in keys:
        df[k] = [1 if el==k else 0 for el in data]
    return df

lst = ['robot'] * 5
lst += ['human'] * 5
lst += ['alien'] * 5
lst += ['animal'] * 5
random.shuffle(lst)
data = pd.DataFrame({'whoAmI':lst})
one_hot = one_hot_convert(data['whoAmI'])
print(data.join(one_hot))
 