# GeneticAlgo
A genetic algorithm for search of optimal NBA lineups on Draft Kings.

To use simply download the LineupGenerator.py file then download the CSV list of available players for the contest you're entering. Place both in the same directory.

To run, open the command prompt and navigate to the directory where you saved the files. Then type "python lineupgenerator.py" and press enter. You should run the program 5-10 times to avoid getting stuck in a local maximum. 

This strategy is most likely to be effective in games where you can win by placing in the top 50%. It is very unlikely to be successful the high paying contests. It may also be best to enter several lineups each night. 

This has NOT been backtested and it is unclear how it will perform, but it does appear to have face vailidity in that it generates lineups that are predicted to score a lot of points and stay under the salary cap. I am not responsible for any decisions to bet real money. 

How it works:
Genetic algorithms are a type of search algorithm that mimics evolution by natural selection. In this case, an inital population of lineups are generated. A ftiness function determines which of the lineups are best based on their average points and whether they stay under the salary cap or not. The top N lineups are kept for mating and mutation. During mating two of the best performing lineups are crossed, giving some players from each of the two "parent" lineups to the child lineup. There is also a small chance that an individual "gene" (player in this case) can be replaced at random from the general population. This is called mutation. After mating/mutation has occurred the lineups are scored again. The top N of this generation are kept. This loop continues 500 times (although this is a tuneable parameter). 
