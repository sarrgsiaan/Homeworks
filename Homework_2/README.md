# Homework 2 — A/B Testing

## Objective

This project compares two multi-armed bandit algorithms, Epsilon Greedy and Thompson Sampling, to identify the best advertisement among four available options.

## Experiment Setup

- Bandit expected rewards: `[1, 2, 3, 4]`
- Number of trials: 20,000 per algorithm
- Reward distribution: Gaussian with standard deviation 1
- Epsilon Greedy: epsilon decays as `1/t`
- Thompson Sampling: Gaussian posterior with known reward precision of 1
- Random seed: 42

## Algorithms

### Epsilon Greedy

Epsilon Greedy balances exploration and exploitation. It randomly explores with a probability that decreases over time and otherwise selects the advertisement with the highest estimated average reward.

### Thompson Sampling

Thompson Sampling uses Bayesian probability distributions to represent uncertainty about each advertisement's expected reward. The algorithm samples from these distributions and selects the advertisement with the highest sampled value.

## Visualizations

The experiment generates three visualizations:

1. `learning_process.png` — average reward over time, using linear and logarithmic trial scales.
2. `cumulative_comparison.png` — cumulative rewards and regrets for both algorithms.
3. `selection_comparison.png` — comparison of suboptimal advertisement selections.

## Results

In the experiment using random seed 42:

| Metric | Epsilon Greedy | Thompson Sampling |
|---|---:|---:|
| Cumulative reward | 79,983.64 | 79,988.46 |
| Cumulative regret | 20 | 37 |
| Suboptimal selections | 10 | 17 |

Epsilon Greedy achieved lower cumulative regret and fewer suboptimal selections. Thompson Sampling achieved slightly higher observed cumulative reward.

These findings describe one experiment and do not establish that either algorithm is consistently superior.

## Bonus — Suggested Improved Implementation Plan

To make the comparison more reliable, I propose the following improvements:

1. **Repeat the experiment:** Run both algorithms across multiple random seeds to reduce dependence on a single simulation.
2. **Measure variability:** Calculate the mean and standard deviation of cumulative rewards and regrets across repeated experiments.
3. **Compare exploration strategies:** Test different epsilon decay schedules and prior precision values.
4. **Improve fairness:** Use shared simulated reward observations where appropriate so both algorithms are evaluated under comparable conditions.
5. **Add automated tests:** Verify the posterior updates, reward calculations, and CSV outputs.

These improvements would provide a more statistically reliable comparison between the two algorithms.

## How to Run

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Run the complete experiment:

```bash
python Bandit.py
```

The program generates CSV results and the three visualization files. 