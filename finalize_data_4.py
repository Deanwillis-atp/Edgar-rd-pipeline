import json


def open_data():
    with open ('price_data.json', 'r') as f:
        result = json.load(f)
    return result

data = open_data()


def sort_on_spike(all_dta):
    buckets = {
        '0-10': {},
        '10-20': {},
        '20-50': {},
        '50-100': {},
        '100+': {}
    }
    for name in all_dta:
        spike = all_dta[name][2]
        if spike <= 10:
            buckets['0-10'][name] = all_dta[name]
        elif spike <= 20:
            buckets['10-20'][name] = all_dta[name]
        elif spike <=50:
            buckets['20-50'][name] = all_dta[name]
        elif spike <= 100:
            buckets['50-100'][name] = all_dta[name]
        elif spike > 100:
            buckets['100+'][name] = all_dta[name]
    return buckets

spiked_sorted = sort_on_spike(data)



def sort_inc_dec(spk_dta):
    for bucket in spk_dta:
        increase = 0
        decrease = 0
        for name in spk_dta[bucket]:
            before = spk_dta[bucket][name][3][25:]
            after = spk_dta[bucket][name][4][25:]
            if after > before:
                increase += 1
            else:
                decrease += 1
        total = increase + decrease
        if total > 0:
            print(f'{bucket}: {total} companies, {decrease} decreases, {increase} increases, {round(decrease/total*100, 1)}% drop rate')
       

sorted_inc = sort_inc_dec(spiked_sorted)


