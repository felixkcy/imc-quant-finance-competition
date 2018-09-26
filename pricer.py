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

    raise NotImplementedError


