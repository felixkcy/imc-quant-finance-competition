from math import exp, log, sqrt
from scipy.stats import norm
import numpy as np
import unittest
from pricer import pricer

FLOAT_PRECISION = 4


class TestPricer(unittest.TestCase):

    def test_returns_scalar(self):
        """Result is a scalar number
        Inputs: spot = 100
                strike = 100
                tau = 1.0
                rate = 0.0
                vola = 0.1
        """

        p = pricer(spot=100., strike=100., tau=1., rate=0., vola=.1)
        self.assertIsInstance(
            p, float,
            "\nThe pricer needs to return a scalar number! Maybe you return the root node of your tree as an array?"
        )

    def test_is_finite(self):
        """Price is finite
        Inputs: spot = 100
                strike = 100
                tau = 1.0
                rate = 0.0
                vola = 0.1
        """

        p = pricer(spot=100., strike=100., tau=1., rate=0., vola=.1)

        self.assertFalse(np.isnan(p), "The pricer return NaN!")

    def test_otmlimit(self):
        """Out of the money limit
        Inputs: spot = 1
                strike = 100
                tau = 1.0
                rate = 0.0
                vola = 0.1

        A call option with a strike much larger than the
        spot should have a value of zero. Think about it: the call option gives you
        the right to buy the stock at the strike price. But if this price is much
        higher than what you pay in the market, this right is worth nothing.
        """

        otmprice = pricer(spot=1., strike=100., tau=1., rate=0., vola=.1)
        self.assertAlmostEqual(otmprice, 0., FLOAT_PRECISION)

    def test_itmlimit_no_rates(self):
        """In the money limit with zero rate
        Inputs: spot = 100
                strike = 1
                tau = 1.0
                rate = 0.0
                vola = 0.1

        If the call option gives you the right to buy the stock at a price much lower than the current
        market price (spot), the call option price is simply the price of a forward. In this example
        we set the rates to zero which means the forward price is just spot - strike.
        """

        spot = 100.0
        strike = 1.0
        rate = 0.0
        tau = 1.0

        itmprice = pricer(spot=spot, strike=strike, tau=tau, rate=rate, vola=.1)
        ref = spot - strike * exp(-rate * tau)
        self.assertAlmostEqual(itmprice, ref, FLOAT_PRECISION)

    def test_itmlimit(self):
        """In the money limit with rate
        Inputs: spot = 100
                strike = 1
                tau = 1.0
                rate = 0.05
                vola = 0.1

        If the call option gives you the right to buy the stock at a price much lower than the current
        market price (spot), the call option price is simply the price of a forward. In this example
        we use a rate of 5% and the forward price is spot - strike*exp(-rate * tau).

        Maybe you forget to discount when working backwards in the tree?
        """

        spot = 100.0
        strike = 1.0
        rate = 0.05
        tau = 1.0

        itmprice = pricer(spot=spot, strike=strike, tau=tau, rate=rate, vola=.1)
        ref = spot - strike * exp(-rate * tau)
        self.assertAlmostEqual(itmprice, ref, FLOAT_PRECISION)

    def test_convergence(self):
        """Convergence test
        Inputs: spot = 99.0
                strike = 100
                tau = 1.0
                rate = 0.02
                vola = 0.6
                steps = 10, 50, 300

        Your binomial tree approximates the true price of the option calculated using the
        analytical Black Scholes formula. By increasing the number of steps, the estimate
        should get closer to the correct value.
        """

        def bscall(spot, strike, tau, rate, vola):
            """Call price calculated using analytical BS formula."""

            d1 = (log(spot / strike) +
                  (rate + 0.5 * vola * vola) * tau) / (vola * sqrt(tau))
            d2 = d1 - vola * sqrt(tau)

            return spot * norm.cdf(d1) - strike * exp(
                -rate * tau) * norm.cdf(d2)

        kwargs = {
            "spot": 99.,
            "strike": 100.,
            "tau": 1.,
            "rate": .02,
            "vola": .6
        }

        refprice = bscall(**kwargs)
        errors = []
        for steps in [10, 50, 300]:
            kwargs["steps"] = steps
            theo = pricer(**kwargs)
            errors.append(abs(theo - refprice))

        self.assertGreater(
            errors[1],
            errors[2],
            msg="Error for step=50 should be higher than error for step=300")
        self.assertGreater(
            errors[0],
            errors[1],
            msg="Error for step=10 should be higher than error for step=50")


if __name__ == "__main__":
    unittest.main()
