# import requests

# s = requests.Session()

# list_url = ["https://google.com","https://spectrum.um.edu.my","https://yahoo.com","https://um.edu.my"]
# print(list_url[0])

# l = len(list_url)
# for j in  range(l):
#     x = s.get(list_url[j])
#     print(x)

# import concurrent.futures
# import requests
# import time

# out = []
# CONNECTIONS = 100
# TIMEOUT = 5

# tlds = open('testing.txt').read().splitlines()
# urls = ['https://{}'.format(x) for x in tlds[1:]]
# print(urls)

# def load_url(url, timeout):
#     ans = requests.head(url, timeout=timeout)
#     print(requests.get(url))
#     return ans.status_code

# with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
#     future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
#     # time1 = time.time()
#     for future in concurrent.futures.as_completed(future_to_url):
#         try:
#             data = future.result()
#             print(data)
#         except Exception as exc:
#             data = str(type(exc))
#         finally:
#             out.append(data)

#             print(str(len(out)),end="\r")

    # time2 = time.time()

# print(f'Took {time2-time1:.2f} s')



# Testing code ML prediction
# import pickle
# import numpy as np
# import time

# model = pickle.load(open('url_predict.pkl', 'rb'))
# arr = np.array([[16, 0, 0, 6, 0, 0, 0, 0, 0, 0, 1, 12, 0]])
# time1 = time.time()
# prediction = model.predict(arr)
# time2 = time.time()

# print(prediction)
# print(f'Took {time2-time1:.2f} s')


from datetime import datetime, timedelta, date
start_date = date.today()
number_of_days = 5

date_list = [(start_date + timedelta(5)) for day in range(number_of_days)]

print(date_list)
