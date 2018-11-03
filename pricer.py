# Default number of steps to use.
# Feel free to change this value and see how it affects your score.
N_STEPS = 200


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
    disc_factor = np.exp(-rate*delta_t)
    
    returns = [spot * u ** (steps - i) * d ** i for i in reversed(range(steps+1))]
    backward = np.array(returns) - strike
    backward[backward < 0] = 0
    
    p_star = (1 - d) / (u - d)
    for n in reversed(range(N)):
        backward = [backward[i] * (1 - p_star) + backward[i+1] * p_star for i range(n+1)]
    
    return backward[0]


