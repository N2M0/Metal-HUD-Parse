import random
import csv

def GeneratorData(count):
    data = []
    for _ in range(count):
        row = ["metal-HUD: " + str(random.randint(100000, 300000)), 0, round(random.uniform(1000, 3000), 2)]
        for _ in range(162):
            row.append(round(random.uniform(40, 140), 2))
        data.append(row)
    
    with open('output2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    # print(data)

GeneratorData(10000)
print("완료!")
