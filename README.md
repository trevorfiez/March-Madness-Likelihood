# March Madness Likelihood

We all remember Cinderella stories from NCAA Men's Basketball Tournaments, but can we look at the entiriety of the tournament and say that one year really was much crazier than any others? Sure, there are years like in 2010 where the four 1 seeds all made it into the Final Four. Still with 2^63 bracket combinations, any one outcome still has an incredible tiny probability of occuring.  However, just computing one individual outcome's likelihood does not show the complete picture. This project aims to answer the question how crazy each year really was and how that excitement relates to every possible bracket.

To measure any sort of likelihood, I made a statistical model to compute a teams probability based on their and their opponent's seed. Then I will calculate the probability of all brackets from 1985 onward and estimate the number of outcomes that were more likely than what occured. 

## Estimating a Team's Probability of Winning ##

First I counted all games from every tournement from 1979. The winning percentage for each seed vs each seed is shown below. Where there were cases when a match-up had never occured, I set the winning probability to be 0.5. 

![Unsooth_Probs](https://trevorfiez.github.io/March-Madness-Likelihood/raw.png)

As you can see there are a lot of areas that might be statitical anomolies because there has not been enough games. For example, should a 9 seed really be favored over a 4 seed? To better illustrate the lack of data the number of matchups for each seed vs. each seed is shown below. 

![Game_Counts](https://trevorfiez.github.io/March-Madness-Likelihood/game_counts.png)

To fix this and to simulate the results for matchups that have not been played, I biased the actual data with a previous proxy count. I keep track of both the wins and losses for each matchup. The initial win count then is 8 - (lossing_seed - winning_seed). The initial count of all the games is then set to 16. I would then go through all the games again and add the actual results to these counts to compute the probability of any team beating another.

![Smooth_Probs](https://trevorfiez.github.io/March-Madness-Likelihood/smoothed_real.png)

## Error Bound for Number of Brackets Less Likely Than Real Outcome ##



## Current Results ##



## To-Do ##

- Compile previous tournement results
- Calculate better seed vs. seed 
- Eventually get team vs team probs from fivethirteight projections, compare vs. previous statistics.
- Run for like a billion iterations

