# March-Madness-Likelihood

A perfect bracket is practically impossible to predict. With 63 individual games there are 2^63 different bracket combinations, which is an almost overwhelming number.
Any specific bracket outcome then has a extremely small probability of occuring. However, just computing one individual outcome's
likelihood does not show the complete picture. Even though there are always upsets in every tournement, most of the time the favored team wins.
Think of how many 1 seeds reach the final four or how few 13-16 seeds ever win a game. Therefore, there must be a ton of outcomes that are
almost completely implausible. 

The main goal of this project is to estimate how many outcomes were more or less likely than what actually occured.
Along the way, I will generate a easy to use csv file of previous march madness results which includes seeds, team names, region, and scores which currently does not exist.
Using simple statistics I will be able to quantify which years were the least and most likely across the whole tournement and how likely those outcomes
were compared to every single possible outcome. To directly count the number of brackets that are more or less likely is intractable
so I will estimate the number of brackets that are worse. To do this I will model the outcome as a Bournoulli random variable where 
I am estimating the number of brackets that were less likely than the actual outcome.

I am going to use some sort of heuristic based off of the team's seed to estimate the probability a team will win. While a model that
takes into account the strength of each team would be better, it is currently out of the scope of this project.

While many people have talked about craziest moments in march madness, or the greatest cinderella stories, to my knowledge, no one has
compared the entire bracket of each year to each other. This project will be able to begin to quantify which years were craziest, and how
crazy the outcome actually was.

## Error Bound for Number of Brackets Less Likely Than Real Outcome ##



## Current Results ##



## To-Do ##

- Compile previous tournement results
- Calculate better seed vs. seed 
- Eventually get team vs team probs from fivethirteight projections, compare vs. previous statistics.
- Run for like a billion iterations

