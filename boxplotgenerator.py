import matplotlib.pyplot as plt
import numpy as np

S = lambda i: i.split('------------------------------------------------------------------')[0]
TS_1 = B1 = lambda i: int(S(i).split('/')[-1].split()[0])
B2 = lambda i: int(S(i).split('/')[-2].split()[0])
TS_2 = lambda i: TS_1(i) + B2(i)
def find(i, c):
    s = S(i).split("\n")[:-1]
    for j in reversed(s):
        if c(j):
            return j
FIRST = lambda i: int(find(i, lambda j: int(j.split()[0]) % 2 == 1).split('/')[1].split()[0])
SECOND = lambda i: int(find(i, lambda j: int(j.split()[0]) % 2 == 0).split('/')[1].split()[0])

def generate_data(directory, typ=TS_1):
    data = []
    for i in range(100):
        try:
            with open(f'/Users/chervjay/Documents/GitHub/Pyrotor/{directory}/run{i}.txt') as f:
                data.append(typ(f.read()))
        except FileNotFoundError:
            print(f"{directory}: File {i} not found, exiting.")
            data.pop(-1)
            break
    return data

# dirs = ['cpu-testing-israel 0.3696 1.5757', 'cpu-testing-israel 1.7064 0.6206', 'cpu-testing-israel 3.5539 0.3116']
dirs = ['cpu-testing-two-players 1.1408 2.8333', 'cpu-testing-two-players 3.0417 0.2135', 'cpu-testing-two-players 2.5157 3.0136']
# dirs = sorted(dirs, key=lambda i: float(i.split('/')[1].split()[0])/float(i.split('/')[1].split()[1]))
data = [generate_data(dirs[0], typ=TS_2), generate_data(dirs[1], typ=TS_2), generate_data(dirs[2], typ=TS_2)]# , generate_data(dirs[0], typ=FIRST), generate_data(dirs[0], typ=SECOND)]
titles = ['1.1408 2.8333', '3.0417 0.2135', '2.5157 3.0136']
plt.boxplot(data)
plt.xticks(np.arange(len(titles))+1, titles, rotation=0)
plt.show()
