## Overview

This is a scrapy project to collect data from the urge website. 

## Spiders

Two spiders have been included in the project, `the-urge` and `the-urge-api`; the first one being a crawling spider that starts from the main page and extracts the 
links in a two directional manner and collects the data using xpaths and post processing. The second one is an alternative solution spider that parses the json objects from the website api.

- #### the-urge
This spider crawls theurge website, starting from the homepage it finds the listing pages and finally scrapes the product page. Xpath configuration for the spider 
is handled on a yaml file `yaml_configs/the-urge.yml`, which includes the fields to be scraped as well as the xpaths for link extraction. 

- #### the-urge-api
This spider was added as an alternate solution to overcome the difficulties of working with xpaths and infinite scrolling. It basically sends requests to 
the website api and parses the response json objects while handling the pagination. <em>The item pipeline `TheurgeScraperPipeline` must be turned of when running this spider.</em>

## Extensions
Two extensions have been added to the project, one is to count the request and response latencies for each scraped product and the other one to keep track of the 
number of scraped items for each category. Both of those are heavly influenced from the book `Learning Scrapy`.
- #### latencies
This one keeps track of the `response.meta['schedule_time']` and `response.meta['received_time']` to calculate the latencies. Runs every time an item is scraped. 
Example log:<br />
`[the-urge] INFO: Request latency: 25.89, Response latency: 0.13`
- #### categories
This one counts the number of products scraped per category. Runs periodically using the scrapy setting `LOGSTATS_INTERVAL`. Example log:<br />
`[the-urge] INFO: Total number of distinct categories scraped: 18, Category counts: shoes-sneakers-high_top_sneakers: 1, bags-satchels_&_cross_body_bags: 1, bags-tote_&_shopper_bags: 1, bags-shoulder_bags: 1, accessories-wallets-cardholders-bags: 1, shoes-flatforms-flats: 1, shoes-boots-ankle_boots: 1, shoes-sneakers: 1, shoes-flats: 1, shoes-heels-wedges: 1, shoes: 1, clothing-maternity-dresses: 1, clothing-plus_size-lingerie: 1, clothing-sleepwear-pyjamas-two-piece_sets: 1, clothing-jumpsuits_&_playsuits-jumpsuits: 1, clothing-activewear-sports_jackets: 1, grooming-suncare-self_tanning: 19, grooming-suncare-after_sun: 1`

## Item pipeline
The `theurge_scraper.pipelines.TheurgeScraperPipeline` is used to post process the items scraped by the-urge crawler. E.g. Parse currency from price. 

## Feed Output
The spiders are setup to send a stop signal after 300 products and the output will be saved in 20 product chunks of `jl` files to the `products` folder as the scraping goes on.
Those can be changed using the following scrapy settings: `CLOSESPIDER_ITEMCOUNT`, `FEED_EXPORT_BATCH_ITEM_COUNT`, `FEEDS`.

## Unit tests
Contracts have been added to each spider and can be run with `scrapy check <spider_name>`.

