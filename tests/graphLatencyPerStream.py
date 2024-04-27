import json
import matplotlib.pyplot as plt
import numpy as np


#read all file lines
with open('data.txt') as f:
    timestampLSL = 0
    timestampSystem = 0 
    latency = []
    lines = f.readlines()
    for index, line in enumerate(lines):
        if(index>251):
            break
        if(line.strip()==""):
            continue
        sample=line[32:]
        #print(sample)
        sampleAsJson = json.loads(sample)
        #print(sampleAsJson)
        kafkaTimestamp = line[11:25]
        #print(kafkaTimestamp)
        if index==0:
            timestampLSL = sampleAsJson["timestampLSL"]
            timestampSystem = sampleAsJson["timestampSystem"]
        else:
            lslAbsolute = timestampSystem + sampleAsJson["timestamp"] + sampleAsJson["time_correction"]-timestampLSL
            #print(float(kafkaTimestamp))
            #print(lslAbsolute)
            sampleLatency = float(kafkaTimestamp)-lslAbsolute*1000
            print(sampleLatency)
            latency.append(sampleLatency)
            #print(sampleLatency)

    x = np.array(range(1,len(latency)+1))
    plt.title("Plotting latency per sample")
    plt.xlabel("sample index")
    plt.ylabel("latency")
    plt.plot(x, latency, color="red", marker="o", label="Latency")
    plt.legend()
    plt.show()