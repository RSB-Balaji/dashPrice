import numpy as np
import matplotlib.pyplot as plt

def gbm(mu, sigma, S0, t, seed):
    np.random.seed(seed)
    Z_sim = np.random.normal(size = t-1)    
    log_returns = []
    T = np.linspace(0., 1., t)
    for i in range(len(Z_sim)):
        log_returns.append(np.exp((mu-0.5*sigma**2)*T[i] + sigma*Z_sim[i]))
    cum_returns = [1]+list(np.cumprod(log_returns))
    sample_path = [S0*i for i in cum_returns]
    #plot
    return T,sample_path

def plot_path(T, path1, path2):
    plt.plot(T, path1, 'b', label="Actual")
    plt.plot(T, path2, 'r', label="Predicted")
    #plt.title("Geometric Brownian motion mu:{} sigma:{}".format(mu, sigma))
    plt.xlabel("Timesteps:{}".format(len(T)))
    plt.legend()
    plt.show(block=True)

if __name__ == '__main__':
    # number of timesteps
    n = 1000
    t,path1 = gbm(0.0003, 0.005, 100, n, 5)
    t,path2 = gbm(0.0005, 0.003, 100, n, 5)
    plot_path(t, path1, path2)