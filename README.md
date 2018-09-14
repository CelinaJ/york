# Web Scraping Google Search Results

There are three different versions of codes where all three of them serve to acquire and store the number of search results obtained from self-generated google queries. To be more specific, the queries are clauses in the form of 

```
"I am [adjective] because I [verb]" 
```

while the adjectives and verbs come from ```adjectives.txt``` and ```verbs.txt```. The number of search results are then stored in respective results.txt files.

## Getting Started

To run any of the python files, simply type the following command in terminal:

```
python3 main.py adjectives.txt verbs.txt
```

## main.py

This program first generates queries in the form of

```
"I am [adjective] because "
```

where the adjectives come from ```adjectives.txt```. Then it takes the google suggestions for the above query and google their search results respectively. The number of search results are then stored in ```results_main.txt```. Next, the program generates queries in the form of:

```
"I am [adjective] because I [verb]" 
```

where the adjectives and verbs are taken from ```adjectives.txt``` and ```verbs.txt```. The queries are then being searched on google, and the number of search results generated using the clauses are recorded in ```results_main.txt``` also. Note there is an example file for ```results_main.txt```, and it was generated by running ```main.py``` and stopping it after a few hours.

## main_multi2.py

This program performs exactly like ```main.py``` except that it uses multiple local processes to google queries concurrently. The default number of processes was set to 6, and it could be changed by modifying the code on ```line 120```. Note that the search results are stored in the file ```results_multi2.txt```, and that there is also an example file that was generated by running ```main_multi2.py``` for a few hours.

## Acknowledgments

The get_num_searches(query) function in class Google was taken from https://github.com/infinitecold/EntityElection.git.
