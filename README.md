# March Madness Likelihood

We all remember Cinderella stories from NCAA Men's Basketball Tournaments, but can we look at the entiriety of the tournament and say that one year really was much crazier than any others? Sure, there are years like in 2010 where the four 1 seeds all made it into the Final Four. Still with 2^63 bracket combinations, any one outcome still has an incredible tiny probability of occuring.  However, just computing one individual outcome's likelihood does not show the complete picture. This project aims to answer the question how crazy each year really was and how that excitement relates to every possible bracket.

To measure any sort of likelihood, I made a statistical model to compute a teams probability based on their and their opponent's seed. Then I will calculate the probability of all brackets from 1985 onward and estimate the number of outcomes that were more likely than what occured. 

## Estimating a Team's Probability of Winning ##

First I counted all games from

![Game_Counts](trevorfiez.github.io/trevorfiez/March-Madness-Likelihood/game_counts.png)

![Unsooth_Probs](trevorfiez.github.io/trevorfiez/March-Madness-Likelihood/raw.png)

![Smooth_Probs](trevorfiez.github.io/trevorfiez/March-Madness-Likelihood/smoothed_real.png)

## Error Bound for Number of Brackets Less Likely Than Real Outcome ##



## Current Results ##



## To-Do ##

- Compile previous tournement results
- Calculate better seed vs. seed 
- Eventually get team vs team probs from fivethirteight projections, compare vs. previous statistics.
- Run for like a billion iterations

