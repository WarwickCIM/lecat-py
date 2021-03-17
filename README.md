# LE-CAT (py)
Version 0.1.0

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LE-CAT is a Lexicon-based Categorization and Analysis Tool developed by the Centre for Interdisciplinary Methodologies in collaboration with the Media of Cooperation Group at the University of Siegen.

The tool allows you to apply a set of word queries associated with a category (a lexicon) to a data set of textual sources (the corpus). LE-CAT determines the frequency of occurrence for each query and category in the corpus, as well as the relations between categories (co-occurrence) by source.

This repository contains a *work in progress* implmenetation of LE-CAT written in Python. A more extensive implementation in R can be found [here](https://github.com/warwickcim/lecat).

## Usage

Load in pandas and numpy.

```python
import pandas as pd
import numpy as np
```

Import the lecat functions.

```python
from lecat import parse_lexicon, run_search, run_lecat_analysis, create_unique_total_diagnostics
```

Read in corpus and lexicon. 

```python
corpus = pd.read_excel(r"sample_data\Corpus.xlsx")
lexicon = pd.read_excel(r"sample_data\Lexicon.xlsx")
```

Parse the lexicon file. The parse_lexicon function converts the wide lexicon file format to a table with one row per query.

```python
parsed_lexicon = parse_lexicon(lexicon)
```

|   | Type        | Category | Query          |   |
|---|-------------|----------|----------------|---|
| 0 | technology  | Apple    | iphone         |   |
| 1 | technology  | Apple    | iPad           |   |
| 2 | technology  | Apple    | imac           |   |
| 3 | influencers | CIM      | Noortje Marres |   |
| 4 | influencers | CIM      | James Tripp    |   |

The lexicon can then be passed to the lecat analysis function. The corpus, our preferred regular expression and the column we wish to search are also passed to run_lecat_analysis. The regular expression needs to include the word query.

```python
run_lecat_analysis(parsed_lexicon, corpus, 'query', 'description')
```

The run_lecat_analsysis function counts up the number of query matches and returns a dataframe.

| Query                                              | iphone | iPad | imac | Noortje Marres | James Tripp |
|----------------------------------------------------|--------|------|------|----------------|-------------|
| description                                        |        |      |      |                |             |
| In this iphone and ipad delivered lecture James... | 1      | 0    | 0    | 0              | 0           |
| An interesting interview                           | 0      | 0    | 0    | 0              | 0           |
| Apple has launched a series of iphones, ipads a... | 1      | 0    | 1    | 0              | 0           |

The Query column shown above is the index for each row.

The create_unique_total_diagnostics function allows us to summarise the total number of query occurences and also the number of corpus items each query occurs in.

```python
create_unique_total_diagnostics(parsed_lexicon, result)
```

A nicely formatted table is returned.

|   | Query          | Type Category | unique | total |   |
|---|----------------|---------------|--------|-------|---|
| 0 | iphone         | technology    | Apple  | 2     | 2 |
| 1 | iPad           | technology    | Apple  | 0     | 0 |
| 2 | imac           | technology    | Apple  | 1     | 1 |
| 3 | Noortje Marres | influencers   | CIM    | 0     | 0 |
| 4 | James Tripp    | influencers   | CIM    | 0     | 0 |

## Contributing

Please feel free to either open a pull request or contact [James Tripp](mailto:james.tripp@warwick.ac.uk) with contributions. All contributions, questions and suggestions are warmly welcomed.