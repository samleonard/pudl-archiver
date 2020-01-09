# PUDL Scrapers


# Output location

Logs are collected:
`[your home]/Downloads/pudl/scrape/`

Data from the scrapers is stored: 
`[your home]/Downloads/pudl/scrape/[source_name]/[today #]`


# Running the scrapers

The general pattern: is `scrapy crawl [source_name]` for one of the supported.
Typically and additional "year" argument is available,
if the form `scrapy crawl [source_name] -a year=[year]`.  


See below for exact commands and available arguments.


## CEMS

To collect all the data:

`scrapy crawl cems`

To collect a specific year (eg, 2007):

`scrapy crawl cems -a year=2007`


## EIA860

To collect all the data:

`scrapy crawl eia860`

To collect a specific year (eg, 2007):

`scrapy crawl eia860 -a year=2007`


## EIA861

To collect all the data:

`scrapy crawl eia923`

To collect a specific year (eg, 2007):

`scrapy crawl eia861 -a year=2007`


## EIA923

To collect all the data:

`scrapy crawl eia923`

To collect a specific year (eg, 2007):

`scrapy crawl eia923 -a year=2007`


## FERC Form 1

To collect all the data:

`scrapy crawl ferc1`

To collect a specific year (eg, 2007):

`scrapy crawl ferc1 -a year=2007`


## IPM NEEDS6

To collect all the data:

`scrapy crawl ipm`

No additional arguments are supported.
