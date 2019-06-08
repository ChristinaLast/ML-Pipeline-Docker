import numpy as np
import pandas as pd

l=0.02
m=0.04
n=0.06

p=np.arange(0, 100, 1)

h=1 - l
j=1 - m
k=1 - n

q=1-(h**p)
r=1-(j**p)
s=1-(k**p)

print(q)
print(r)
print(s)
