# CARP_Podcast_Segmentation

## Intro

This project is created for classifying and hence filtering non-related to theme of the podcast segments. For classification I used CARP technique which is described in this [research paper](https://arxiv.org/pdf/2305.08377)

## Description

1. Reading parts of podcast transcript from output.yaml
2. Extracting podcast theme using theme_extractor.py
3. Classifying related/non-related transcript parts using async code (which allows batching) in CARP_classification.py
4. Removing non-related segments if there are more than M occurences in a row.

## Technologies Used

- openai API

## Installation and Setup (Python 3.11)
```bash
git clone git@github.com:nikitazuevblago/CARP_Podcast_Segmentation.git
cd CARP_Podcast_Segmentation
pip install -r requirements.txt
```
Then create .env file and put your openai api key in OPENAI_API_KEY variable.

After you can use this environment for interacting with **main.ipynb**

## Result 
List with relevant podcast segments according to GPT vision.

#### Example:
[...'Allow me to say that the SpaceX launch',
 'of human beings to orbit on May 30th, 2020',
 'was seen by many as the first step',
 'in a new era of human space exploration.',
 'These human spaceflight missions were a beacon of hope',
 'to be excited about the future.',
 'Let me ask about Crew Dragon demo two.'...]


## File structure
- **main.ipynb** - notebook using all modules and containing all overall logic of the project
- **theme_extractor.py** - extracting the theme of the podcast using GPT model
- **CARP_classification.ipynb** - script for classification, here you can find the implementation of CARP technique in modified prompt
- **output.yaml** - example of random podcast transcript
- **requirements.txt** - file with all libs