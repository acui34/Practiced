# Practiced: A Cloud-based Smart Pratice Planning System for Self-starter Musicians

Personal Final Project for Fall 2020 COMS 6998 Cloud Commputing & Big Data

## Motivation

Many self-starter musicians, like myself, always suffering fromm the following problems:

- With limited professional guides, self-start musicians may be confused about what to do to get started.
- There are too many articles and videos online, but there’s no clear pathway on what songs people should choose.
- Without any regular reminder by a teacher or friends, people may forget to practice and then give up silently.

However, music is great and people should not be stopped by these reasons. To help the self-starter musician community, 'Practiced', a cloud-based smart pratice planning system is presented to:

- Help people find songs they are interested and suitable for their level
- Provide personal and conversational guidance
- Remind people to practice regularly and build good habits

## Use Cases

* Search songs 
  - Search by artist, genre, song name
  - See song information, difficulty and predicted practice time
  - Fuzzy search by a rough idea
  - Search by voice
* Personal account
  - Register for a secured new account
  - Log in/ log out to keep the experience personal
* Practice List
  - Add a song to practice list
  - Record daily practice 
  - Finish practicing a song
* Personal Coach
  - Conversational song suggestion
* Reminder
  - Subscribe to email daily reminder
  - Receive daily practice reminder to build a habit


## Key Design Decisions

* **Efficient Search**: Maintain song keywords (name, artist, tags) in ES for fuzzy search and recommendation.
* **Cost Effective**: Maintain detailed song information in DynamoDB.
* **Personalized Experience and Account Safety**: User management system with Cognito.
* **Flexible Record**: After a song is finished, the record will stay at the bottom. In this way, users can build a sense of accomplishment along the way.
* **Easy Update**: Code versioning with CodePipeline and CodeCommit.
* **Smart Prediction**: ML model deployed on Sagemaker to predict practice time

## Solution Architecture

<img src='/images/practiced-architecture.png'/>

## File Structure

This repo mainly contains the backend code and fake data generated to populate the database.

Frontend code can be found [here](https://github.com/acui34/CloudFinalFrontend).