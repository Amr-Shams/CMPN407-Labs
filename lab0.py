import matplotlib.pyplot as plt
from scipy import integrate
import numpy as np
from scipy.stats import norm
def integrand(x):
     return (15*x**3 + 21*x**2 + 41*x + 3)**(1/4) * np.exp(-0.5*x)

a,b = 1,4
true_integral = integrate.quad(integrand,a,b)[0]

num_trials = 100
step_size = 100

# req: 1.1
max_samples = step_size * num_trials
sample_size = np.arange(num_trials,max_samples+1,step_size)
estimates = np.zeros(num_trials)

for i,N in enumerate(sample_size):
    x = np.random.uniform(a,b,size=N)
    estimates[i] = (b-a)/N * np.sum(integrand(x))

plt.figure(figsize=(10,5))
plt.plot(sample_size,estimates,'g-',label = 'Estimated Values')
plt.plot(sample_size,np.full(num_trials,true_integral),'-b',label = 'Actual Value')
plt.xlabel('Sample Size')
plt.ylabel('Integral Value')
plt.legend()
plt.hlines(true_integral, 0, max_samples, colors='r', linestyles='dashed')
plt.title('Integral Estimates vs. Sample Size')

# req: 1.2

num_trials = 500
N = 1000
auc = np.zeros(num_trials)

for i in range(num_trials):
    x = np.random.uniform(a,b,size=N)
    auc[i] = (b-a)/N * np.sum(integrand(x))

plt.figure(figsize=(10,5))
plt.hist(auc, bins=50, density=True)
plt.xlabel('Integral Value')
plt.ylabel('Frequency')
plt.title('Histogram of Integral Estimates')
plt.show()

# req:1.3

mu,std = norm.fit(auc)
print(mu,std)
    

