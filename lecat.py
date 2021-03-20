import pandas as pd
import numpy as np

def parse_lexicon(lexicon):
    """ Reshape lexicon from wide to long 
    Parameters
    ----------
    lexicon : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: Type, dtype: float64
            Name: Category, dtype: float64
            Name: Query, dtype: float64
            Name: Query1, dtype: object
            Name: Queryx, dtype: object
        Search queries, types and categories        

    Returns
    ----------
    parsed_lexicon : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: Type, dtype: object
            Name: Category, dtype: object
            Name: Query, dtype: object
        Long form lexicon
    """

    # preallocate our parsed dataframe
    parsed_lexicon = pd.DataFrame(columns = ['Type', 'Category', 'Query'])

    # iterate over each row in lexicon
    for index, row in lexicon.iterrows():

        # extract columns
        this_type = row['Type']
        this_category = row['Category']
        these_queries = row[lexicon.keys().str.startswith('Query')]
        
        for query in these_queries:
            if pd.isna(query):
                continue
            # append our collected data
            parsed_lexicon = parsed_lexicon.append(
                {'Type':this_type, 'Category':this_category, 'Query':query},
                ignore_index=True)
        
    return(parsed_lexicon)

def run_search(strings, query, this_type, this_category, column, regex = '\\bquery\\b'):
    """ Search for query in strings 
    Parameters
    ----------
    strings         : pandas.Series
        Series of strings to search.
    query           : str
        Term to seach for.
    this_type       : str
        Query type.
    this_category   : str
        Query category.
    regex           : str
        Query search regular expression.

    Returns
    ----------

    result : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: [query], dtype: int64
        Counts of query in string
        
    """
    # correctly add backslash to special characters
    query = query.replace("([{\\[()|?$^*+.\\\\])", "\\$1")
    regex = regex.replace('query', query)
    counts = strings.str.count(regex)

    # put counts into dataframe 
    result = pd.DataFrame({query: counts})
    result = result.set_index(strings)

    return(result)

def run_lecat_analysis(parsed_lexicon, corpus, regex_expression, column):
    """ Run search against all lexicon entries 
    Parameters
    ----------
    parsed_lexicon : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: Type, dtype: float64
            Name: Category, dtype: float64
            Name: Query, dtype: float64
    Long form lexicon from parse_lexicon.
    corpus         : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: [column], dtype: object
        DataFrame with at least 1 column with column name matching column parameter.
    regular_expression : str
        Regular expression for search.
    column          : str
        Column name to search for. Must be column name in corpus.

    Returns
    ----------
    result : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: [query_1], dtype: int64
            Name: [query_2], dtype: int64
            Name: [query_n], dtype: int64
    """
    # preallocate result dataframe
    result = pd.DataFrame(np.nan, index = corpus.description, columns = parsed_lexicon.Query)

    # run search for each query
    for index, row in parsed_lexicon.iterrows():
        
        # get features
        this_query = row['Query']
        these_strings = corpus[column]
        this_type = row['Type']
        this_category = row['Category']

        # search
        result[this_query] = run_search(these_strings, this_query, this_type, this_category, column, regex_expression)

    return(result)

def create_unique_total_diagnostics(parsed_lexicon, lecat_result):
    """ 
    Count the total occurences [total] and the number of corpus elements
    containing each query [unique].
    Parameters
    ----------
    parsed_lexicon : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: Type, dtype: float64
            Name: Category, dtype: float64
            Name: Query, dtype: float64
    Long form lexicon from parse_lexicon.
    lecat_result : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: [query_1], dtype: int64
            Name: [query_2], dtype: int64
            Name: [query_n], dtype: int64
    Output from run_lecat_analysis

    Returns
    ----------
    result : pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: Type, dtype: float64
            Name: Category, dtype: float64
            Name: Query, dtype: float64
    """
    totals = []
    uniques = []
    Types = []
    Categories = []
    Queries = []

    for query in lecat_result:
        # tally up counts
        n_total = sum(lecat_result[query])
        n_unique = lecat_result[query].astype(bool).sum(axis=0)
        
        # TODO: fix cases where multiple of same query
        Type = parsed_lexicon.Type[parsed_lexicon.Query == query].values[0]
        Category = parsed_lexicon.Category[parsed_lexicon.Query == query].values[0]

        # add counts to lists
        totals.append(n_total)
        uniques.append(n_unique)
        Types.append(Type)
        Categories.append(Category)
        Queries.append(query)

    # put lists into a pretty dataframe
    data = {'Query': Queries,
            'Type': Types, 
            'Category': Categories, 
            'unique': uniques, 
            'total': totals}

    result = pd.DataFrame(data)

    return(result)