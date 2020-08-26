"""
Cookie Clicker Simulator
"""
import math

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor

codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._tot_cookies = 0.0
        self._cur_cookie = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "\nTotal Number of Cookies " + str(self._tot_cookies) \
               + "\n Current Number of Cookies " + str(self._cur_cookie) \
               + "\n Current Time " + str(self._current_time) \
               + "\n Current CPS " + str(self._current_cps)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cur_cookie

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history_list[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """

        cookies_make = (cookies - self._cur_cookie)


        if cookies_make < 0:
            return 0.0
        else:
            return math.ceil(cookies_make / self.get_cps())

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """

        if time > 0.0:
            self._cur_cookie = self.get_cookies() + time * self.get_cps()
            self._tot_cookies += time * self.get_cps()
            self._current_time = self.get_time() + time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """

        if self._cur_cookie >= cost:
            self._cur_cookie = self.get_cookies() - cost
            self._current_cps = self.get_cps() + additional_cps
            self._history_list.append((self._current_time, item_name, cost, self._tot_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    this_build = build_info.clone()
    clicker = ClickerState()

    while clicker.get_time() <= duration:
        value = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(),
                         this_build)
        if value == None:
            break
        cost = this_build.get_cost(value)
        update_cps = this_build.get_cps(value)
        time_to_wait = clicker.time_until(cost)
        if (clicker.get_time() + time_to_wait) > duration:
            break
        clicker.wait(time_to_wait)
        clicker.buy_item(value, cost, update_cps)
        this_build.update_item(value)
    time_left = duration - clicker.get_time()
    clicker.wait(time_left)
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """

    values = build_info.build_items()

    mmin = float("inf")
    item = None

    for valk in values:
        cost = build_info.get_cost(valk)
        if cost - cookies <= 0:
            if cost < mmin:
                mmin = cost
                item = valk
                continue
            else:
                continue
        time = (cost - cookies) / cps
        if cost < mmin and time <= time_left:
            mmin = cost
            item = valk
    return item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """

    values = build_info.build_items()

    mmax = 0
    item = None

    for val in values:
        cost = build_info.get_cost(val)
        if cost - cookies <= 0:
            if cost > mmax:
                mmax = cost
                item = val
                continue
            else:
                continue
        time = (cost - cookies) / cps
        if cost > mmax and time <= time_left:
            mmax = cost
            item = val
    return item


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """

    values = build_info.build_items()

    mmax = 0
    item = None
    for val in values:
        cost = build_info.get_cost(val)
        cps_ = build_info.get_cps(val)
        if cost - cookies <= 0:
            if cps_ / cost > mmax:
                mmax = cps_ / cost
                item = val
            continue
        time = math.ceil((cost - cookies) / cps)
        if cps_ / cost > mmax and time <= time_left:
            mmax = cps_ / cost
            item = val
    return item


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print(strategy_name, ":", state)

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)


# run()