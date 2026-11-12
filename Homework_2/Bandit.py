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



class Visualization:
    """Visualize and compare the bandit algorithms."""

    def __init__(self, epsilon_greedy, thompson_sampling):
        self.algorithms = [epsilon_greedy, thompson_sampling]

    @staticmethod
    def cumulative(values):
        """Calculate cumulative sums."""
        result = []
        total = 0

        for value in values:
            total += value
            result.append(total)

        return result

    def plot1(self):
        """Plot learning performance on linear and log scales."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        for algorithm in self.algorithms:
            trials = range(1, len(algorithm.rewards) + 1)
            cumulative_rewards = self.cumulative(
                algorithm.rewards
            )

            average_rewards = [
                total / t
                for t, total in zip(trials, cumulative_rewards)
            ]

            for ax in axes:
                ax.plot(
                    trials, average_rewards,
                    label=repr(algorithm)
                )

        axes[0].set_title("Learning Process - Linear Scale")
        axes[1].set_title("Learning Process - Log Scale")
        axes[1].set_xscale("log")

        for ax in axes:
            ax.set_xlabel("Trial")
            ax.set_ylabel("Average Reward")
            ax.legend()
            ax.grid(True)

        plt.tight_layout()
        plt.savefig("learning_process.png", dpi=150)
        plt.close(fig)

    def plot2(self):
        """Compare cumulative rewards and cumulative regrets."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        for algorithm in self.algorithms:
            cumulative_rewards = self.cumulative(
                algorithm.rewards
            )
            cumulative_regrets = self.cumulative(
                algorithm.regrets
            )

            axes[0].plot(
                cumulative_rewards,
                label=repr(algorithm)
            )

            axes[1].plot(
                cumulative_regrets,
                label=repr(algorithm)
            )

        axes[0].set_title("Cumulative Rewards")
        axes[1].set_title("Cumulative Regrets")

        for ax in axes:
            ax.set_xlabel("Trial")
            ax.legend()
            ax.grid(True)

        axes[0].set_ylabel("Cumulative Reward")
        axes[1].set_ylabel("Cumulative Regret")

        plt.tight_layout()
        plt.savefig("cumulative_comparison.png", dpi=150)
        plt.close(fig)


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
    """Thompson Sampling with a Gaussian reward model."""

    def __init__(self, p):
        self.p = p
        self.n_bandits = len(p)

        # Known reward precision (variance = 1)
        self.precision = 1.0

        # Normal prior: mean = 0, precision = 1
        self.posterior_means = [0.0] * self.n_bandits
        self.posterior_precisions = [1.0] * self.n_bandits

        self.counts = [0] * self.n_bandits
        self.rewards = []
        self.chosen_bandits = []
        self.regrets = []

    def __repr__(self):
        return "ThompsonSampling"

    def pull(self):
        # Sample an estimated reward from each posterior
        samples = []

        for i in range(self.n_bandits):
            mean = self.posterior_means[i]
            std = math.sqrt(
                1 / self.posterior_precisions[i]
            )

            sample = random.gauss(mean, std)
            samples.append(sample)

        # Choose the advertisement with the highest sample
        return samples.index(max(samples))

    def update(self, bandit, reward):
        self.counts[bandit] += 1

        # Update the Gaussian posterior
        old_precision = self.posterior_precisions[bandit]
        old_mean = self.posterior_means[bandit]

        new_precision = old_precision + self.precision

        new_mean = (
            old_precision * old_mean
            + self.precision * reward
        ) / new_precision

        self.posterior_precisions[bandit] = new_precision
        self.posterior_means[bandit] = new_mean

        # Store results
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

        average_reward = cumulative_reward / len(self.rewards)
        average_regret = cumulative_regret / len(self.regrets)

        logger.info(
            f"Cumulative reward: {cumulative_reward:.2f}"
        )
        logger.info(
            f"Cumulative regret: {cumulative_regret:.2f}"
        )
        logger.info(
            f"Average reward: {average_reward:.2f}"
        )
        logger.info(
            f"Average regret: {average_regret:.4f}"
        )

        with open("thompson_sampling_rewards.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Bandit", "Reward", "Algorithm"])

            for bandit, reward in zip(
                self.chosen_bandits, self.rewards
            ):
                writer.writerow(
                    [bandit, reward, "Thompson Sampling"]
                )




def comparison():


    # Experiment settings
    bandit_rewards = [1, 2, 3, 4]
    trials = 20000

    # Set a random seed for reproducible results
    random.seed(42)

    # Initialize both algorithms
    epsilon = EpsilonGreedy(bandit_rewards)
    thompson = ThompsonSampling(bandit_rewards)

    # Run experiments
    epsilon.experiment(trials)
    thompson.experiment(trials)

    # Display results
    logger.info("===== Epsilon Greedy Results =====")
    epsilon.report()

    logger.info("===== Thompson Sampling Results =====")
    thompson.report()

    # Generate the two required visualizations
    visualization = Visualization(epsilon, thompson)
    visualization.plot1()
    visualization.plot2()

    # How often does each algorithm choose a suboptimal ad?

    ads = ["Ad 1", "Ad 2", "Ad 3"]
    x = range(3)
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))

    # Epsilon Greedy advertisement selections
    ax.bar(
        [i - width / 2 for i in x],
        epsilon.counts[:3],
        width,
        label="Epsilon Greedy",
        color="royalblue"
    )

    # Thompson Sampling advertisement selections
    ax.bar(
        [i + width / 2 for i in x],
        thompson.counts[:3],
        width,
        label="Thompson Sampling",
        color="orange"
    )

    # Customize the chart
    ax.set_xticks(list(x))
    ax.set_xticklabels(ads)
    ax.set_title("Suboptimal Advertisement Selections")
    ax.set_xlabel("Advertisement")
    ax.set_ylabel("Number of Selections")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("selection_comparison.png", dpi=150)
    plt.close(fig)

    # Save combined results to CSV
    with open("bandit_rewards.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bandit", "Reward", "Algorithm"])

        for algorithm in [epsilon, thompson]:
            for bandit, reward in zip(
                algorithm.chosen_bandits,
                algorithm.rewards
            ):
                writer.writerow(
                    [bandit, reward, repr(algorithm)]
                )

    logger.info("Comparison completed successfully!")

if __name__=='__main__':
    comparison()

   
