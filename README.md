# SPbU Data Mining 2021
-------------------------------
## Scraping

Scraper is based on selenium framework and firefox webdriver.  
To avoid restrictions from robots.txt different user-agents and free http proxies were used.

__Date range__: 05.11.2014 - 20.03.2016

## Data preprocessing

Preprocessing steps:
 - removing html tags
 - removing urls
 - removing punctuation
 - removing texts by length

tags:
 - политика
 - помощь
 - дети
 - девушки
 - отношения
 - рассказ
 - стихи
 - юмор

## EDA
Plots are in the `reports/figures` folder.  

## Features

I have chosen [fastText embeddings from DeepPavlov](http://docs.deeppavlov.ai/en/master/features/pretrained_vectors.html#fasttext) trained on Twitter data due to the same domain as user-generated texts.

Original embeddings were pruned with this [lib](https://github.com/avidale/compress-fasttext).  
Pruned embeddings and all CSVs are available at my [Google Drive](https://drive.google.com/drive/folders/1OPgFRBn6zJzclqWtj2ssgEIldvZ3RUD0?usp=sharing).  

## Tested Models

### Classification
 - SVC results without stemming/lemmatization ~ 0.8.  
 - LogisticRegression results without stemming/lemmatization ~ 0.75.  
 - LDA (discriminant analysis) results without stemming/lemmatization ~ 0.73.  

### Topic modeling
- LDA catched only four topics: юмор, политика, отношения, помощь; and unexpected one - computers.

### Clustering
 - Kmeans and other clustering algorithms show very poor scores, so there is no need to mention these results.
