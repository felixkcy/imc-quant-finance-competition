import numpy as np
from scipy.special import comb

# Default number of steps to use.
# Feel free to change this value and see how it affects your score.
N_STEPS = 400


def pricer(spot, strike, tau, rate, vola, steps=N_STEPS):
    """
    This is where all the action is.
    You should return the price of the call option
    :param spot:
    :param strike:
    :param tau:
    :param rate:
    :param vola:
    :param steps: The number of steps for your model. It should be set to the
    default value N_STEPS
    You can try different values of N_STEPS (each one being a different model).
    :return: price of the call option
    :rtype: float
    """

    delta_t = tau / steps
    u = np.exp(vola*np.sqrt(delta_t))
    d = 1 / u
    p = (np.exp(rate*delta_t) - d) / (u - d)
    disc_factor = np.exp(-rate*tau)
    
    tmp_arr = np.arange(steps+1)
    returns = spot * np.power(u, steps-tmp_arr) * np.power(d, tmp_arr)
    backward = np.array(returns) - strike
    backward[backward < 0] = 0
    p_star = (np.exp(rate*delta_t) - d) / (u - d)
    q_star = 1 - p_star
    price_arr = comb(steps, tmp_arr) * backward * np.power(p_star, steps-tmp_arr) * np.power(q_star, tmp_arr)
    price = np.sum(price_arr) * disc_factor
    
    return price


