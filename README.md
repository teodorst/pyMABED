# pyMABED

pyMABED is a Python 3 implementation of MABED (for more information about MABED, see https://github.com/AdrienGuille/MABED/ or the references below)

Contributors:
- Adrien Guille
- Nicolas Dugué

## MABED

MABED (Mention-Anomaly-Based Event Detection) is a statistical method for automatically detecting significant events that most interest Twitter users from the stream of tweets they publish. In contrast with existing methods, it doesn't only focus on the textual content of tweets but also leverages the frequency of social interactions that occur between users (i.e. mentions). MABED also differs from the literature in that it dynamically estimates the period of time during which each event is discussed rather than assuming a predefined fixed duration for all events.

##Requirements 

	pip install pandas
	pip install nltk
	pip install numpy
	pip install networkx

## References

	Adrien Guille and Cécile Favre (2015) 
	Event detection, tracking, and visualization in Twitter: a mention-anomaly-based approach.
	Springer Social Network Analysis and Mining,
	vol. 5, iss. 1, art. 18, DOI: 10.1007/s13278-015-0258-0


	Adrien Guille and Cécile Favre (2014) 
	Mention-Anomaly-Based Event Detection and Tracking in Twitter.
	In Proceedings of the 2014 IEEE/ACM International Conference on
	Advances in Social Network Mining and Analysis (ASONAM 2014),
	pp. 375-382, DOI: 10.1109/ASONAM.2014.6921613
