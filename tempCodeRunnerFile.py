
a = (
    {'urls': 'https://www.youtube.com/watch?v=i3RMlrx4ol4&t=603s', 'status': 'benign'},
    {'urls': 'https://www.youtube.com/watch?v=i3RMlrx4ol4&t=603s', 'status': 'benign'},
    {'urls': 'https://spectrum.um.edu.my', 'status': 'benign'},
    {'urls': 'https://google.com', 'status': 'benign'},
    {'urls': 'https://google.com', 'status': 'benign'},
    {'urls': 'https://google.com', 'status': 'benign'},
    {'urls': 'https://google.com', 'status': 'benign'}
)

k = {}
t = []
e = 0
el = 0

for i in range (7):
    if i >= 5:
        t.pop(0)
        print(t)

    k['urls'] = e
    k['status'] = el
    t.append(k.copy())
    print(t)
    e += 1
    el += 1
print(tuple(t))
