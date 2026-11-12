"""
  Run this file at first, in order to see what is it printng. Instead of the print() use the respective log level
"""
############################### LOGGER
import csv
import math
import random
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
from loguru import logger


class Bandit(ABC):
    ##==== DO NOT REMOVE ANYTHING FROM THIS CLASS ====##

    @abstractmethod
    def __init__(self, p):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def pull(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def experiment(self):
        pass

    @abstractmethod
    def report(self):
        # store data in csv
        # print average reward (use f strings to make it informative)
        # print average regret (use f strings to make it informative)
        pass

#--------------------------------------#


class Visualization():

    def plot1(self):
        # Visualize the performance of each bandit: linear and log
        pass

    def plot2(self):
        # Compare E-greedy and thompson sampling cummulative rewards
        # Compare E-greedy and thompson sampling cummulative regrets
        pass

#--------------------------------------#


class EpsilonGreedy(Bandit):

    def __init__(self, p):
        self.p = p
        self.n_bandits = len(p)

        self.counts = [0] * self.n_bandits
        self.estimates = [0.0] * self.n_bandits

        self.rewards = []
        self.chosen_bandits = []
        self.regrets = []

    def __repr__(self):
        return "EpsilonGreedy"

    def pull(self):
        t = len(self.rewards) + 1

        if 0 in self.counts:
            return self.counts.index(0)

        epsilon = 1 / t

        if random.random() < epsilon:
            # Explore: select a random advertisement
            return random.randrange(self.n_bandits)

        # Exploit: select the best estimated advertisement
        return max(
            range(self.n_bandits),
            key=lambda i: self.estimates[i]
        )

    def update(self, bandit, reward):
        self.counts[bandit] += 1

        n = self.counts[bandit]
        self.estimates[bandit] += (
            reward - self.estimates[bandit]
        ) / n

        self.rewards.append(reward)
        self.chosen_bandits.append(bandit + 1)

        regret = max(self.p) - self.p[bandit]
        self.regrets.append(regret)

    def experiment(self, trials=20000):
        for _ in range(trials):
            bandit = self.pull()
            reward = random.gauss(self.p[bandit], 1.0)
            self.update(bandit, reward)

    def report(self):
        cumulative_reward = sum(self.rewards)
        cumulative_regret = sum(self.regrets)

        average_reward = (
            cumulative_reward / len(self.rewards)
        )
        average_regret = (
            cumulative_regret / len(self.regrets)
        )

        logger.info(f"Cumulative reward: {cumulative_reward:.2f}")
        logger.info(f"Cumulative regret: {cumulative_regret:.2f}")
        logger.info(f"Average reward: {average_reward:.2f}")
        logger.info(f"Average regret: {average_regret:.2f}")

        with open("epsilon_greedy_rewards.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Bandit", "Reward", "Algorithm"])

            for bandit, reward in zip(
                self.chosen_bandits, self.rewards
            ):
                writer.writerow(
                    [bandit, reward, "Epsilon Greedy"]
                )

#--------------------------------------#

class ThompsonSampling(Bandit):
    pass




def comparison():
    # think of a way to compare the performances of the two algorithms VISUALLY and 
    pass

if __name__=='__main__':
   
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
