"""
stop_words is a list that cannot form a meaningful noun with any word. These words were taken from the
internet and none of them are nouns, etc. which could skew the learning
"""

stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "any", "are", "as",
              "at",
              "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did",
              "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has",
              "have",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
              "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's",
              "its",
              "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or",
              "other",
              "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's",
              "should", "so", "some", "such", "the", "than", "that", "that's", "their", "theirs", "them",
              "themselves",
              "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
              "those",
              "through", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're",
              "we've",
              "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
              "whom",
              "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
              "yourself", "yourselves", "Mr", "Ms", "and", "the", "to"]

"""
prepositions is a list that we use to check if the previous words to the current word is a preposition.
This provides us with a context indicating that this could be a noun, more specifically, a location.
"""
prepositions = ["the", "in", ".", "of", "and", "to", "from"]

"""
followed by is a list to set context for nouns that could be a location based on what follows it.
"""

followed_by = ["s", ".", "in", "and", "is", "has", "to"]

"""
substr is a list of possible substrings that could belong to certain "regexes" of locations. This will affect both
TP and FP but in the larger picture, this is a very powerful feature.
"""

substr = ["land", "lands", "shire", "fax", "berg", "tan", "ia", "is", "ne"]

"""
location_tenders are a list of possible previous words that could lead to a location. Especially words which have
directions right in front of a noun has a high percentange of being a location tender.
"""

location_tenders = ["South", "North", "West", "East", "San", "New", "Sri"]

"""
Non location nouns are words that have a chance of being classified as locations if present in a similar context. This 
list is added as a seperate feature to allow the ML algorithm to identify such features.
"""

nonlocation_nouns = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January",
                     "February",
                     "March",
                     "April", "May", "June", "July", "August", "October", "September", "November", "December", "BBC",
                     "FBI",
                     "Middle",
                     "Mid", "ONGC", "Lacroix", "EC", "GDP", "VW", "ADB", "LSE", "LPG", "FTSE", "ECB", "IPCL", "SEC",
                     "IMF",
                     "Renault", "IPC", "FT",
                     "LVMH", "AMR", "KSE", "KFB", "United Bank", "United", "ODPM", "Sarbanes-Oxley", "Wal-Mart",
                     "WorldCom",
                     "Citigroup", "Reliance",
                     "Yukos", "JP", "BA", "EC", "VW", "Volkswagen", "MS", "GW", "Ford", "Technology"]
