from scipy.stats import expon, uniform

def exp_unif_renorm(x, N , min , max , a, b, tau, A):
    return a * N * (expon.cdf(x, A, tau)*tau/(expon.cdf(max , loc = A , scale = tau) - expon.cdf(min , loc = A , scale = tau))) + b * N * uniform.cdf(x, min, max)

params = [436397.9784100306,0.07951815220977412,2.1290150790533152e-06, 0.0]