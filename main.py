import requests
import csv

from terminaltables import AsciiTable

address = ''


# 過濾地址及診所類別
def get_clinic_by_address_and_medicine(item):
    return address in item['地址'] and item['西醫診所'] == '西醫診所'

# 去除\ufeff
def replace_ufeff(item):
    return {k.replace('\ufeff', ''): v for k, v in item.items()}


def main():
    res = requests.get('http://opendataap2.e-land.gov.tw/resource/files/2016-12-16/bde7f966757788e0d2428ff9fbd12541.json')
    if not res.ok:
        print('Can not find request!')
        exit()

    address = input('Enter address：')
    data = res.json()
    data = list(map(replace_ufeff, data))
    data = list(filter(get_clinic_by_address_and_medicine, data))
    if len(data) <= 0:
        print('No matching data!')
        exit()

    result_table_head = data[0].keys()
    result = []
    for d in data:
        result.append(list(d.values()))

    table = AsciiTable([result_table_head, *result])
    print(table.table)

    #寫入資料產生csv檔
    with open('yilan_clinic_{}.csv'.format(address), 'w', encoding = 'utf-8', newline = '') as f:
            writer = csv.writer(f)
            writer.writerows(result)

    print('Export success!')

if __name__ == '__main__':
    main()