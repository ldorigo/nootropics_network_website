## The goal

To investigate usage patterns of nootropic drugs through analysis of discussions on a social forum (Reddit) and compare these to the pattern of connections between Wiki pages of these drugs. This comparison would allow investigating the differencxe in the types of networks that arise from an encyclopaedic source vs. social discussion about the same topic.
	
## What we have

We have list of all psychoactive drugs that can be considered as cognitive enhancers:

- How?
  - Get a hierarchy of all psychoactive substances from Wikipedia
			https://en.wikipedia.org/wiki/Category:Drugs_by_psychological_effect  
   - Manually remove irrelevant categories and pages
  - Get
    - all in and out links
	- Content
	- Redirects (synonyms)
		

## What do we still need
	
* Clean data (remove categories from substance names)
* Sentiment

  * Define sentiment / effect measures for categories:
  
    * Positive / negative
    * (optional) Effect type (e.g. memory, endurance, anxiety)
    * Attach sentiment / effect as link attribute
 
* Find communities (Wikipedia + Reddit)

    * Compare with Wikipedia categories (measure overlap)
    
* Evaluation
* Notebook
* Web page 
  

		

## What we want to do

- Compare communities from Louvain to categories from Wikipedia
    - By psychological effect
    - By physiological effect
    - By mechanism of action
	
- Sentiment analysis
	- Score per 
		- Message
		- Thread

We will use the information obtained from text analysis (e.g. connotations, word frequencies) as attributes in our networks, and then use the network for further analysis.

We will compare the network from Wiki to the network from Reddit
	Redit will (maybe) tell us which substances are used together
Wiki will group in other ways (e.g. by psychological effect)