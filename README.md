# Cloud Computing Team Members

| Bangkit ID | Name | Learning Path | University | Contact |
| ----- | ----- | ----- | ----- | ----- |
|C128BSY3290|Shoffan Darul Mufti|Cloud Computing|Politeknik Negeri Jakarta|https://www.linkedin.com/in/shoffanda/|
|C102BSY3325|Jonathan Christian|Cloud Computing|Institut Bisnis dan Informatika Kwik Kian Gie|https://www.linkedin.com/in/jonathan-christian-7b2009272/|

## API for ARUNA

Bangkit 2023 Capstone Project <br>

We're using Python Flask for developing this API and deploy it on Google CLoud Platform.

## GCP Architecture
![gcp_architecture](assets/gcp-architecture.png)

### Base URL
https://aruna-r3wznanhga-et.a.run.app/

### Documentation
[Aruna API Documentation](https://pandarl.notion.site/Aruna-API-Documentation-c63074cec06241ef870e79f623ce5f86?pvs=4)

## Replicate our work

1. Create new Google Cloud project
2. Install Cloud Run API, Cloud Build API, & Cloud SQL API
3. Install and init Google Cloud SDK
4. Create MySQL instance on Google Cloud SQL
5. Give your MySQL instance to public access (you can use many ways to connect Cloud Run to Cloud SQL. For easier understanding, we're going to use public IP)
6. Connect to the instance and create the databases using commands below
```plaintext
CREATE TABLE articles (
id_articles INT NOT NULL AUTO_INCREMENT,
PRIMARY KEY(id_articles),
name VARCHAR(255),
description VARCHAR(1000),
image VARCHAR(255)
);
CREATE TABLE contact_persons (
id_cp INT NOT NULL AUTO_INCREMENT,
PRIMARY KEY(id_cp),
id_articles INT,
name VARCHAR(255),
phone VARCHAR(20),
contact_link VARCHAR(255),
FOREIGN KEY (id_articles) REFERENCES articles(id_articles)
);
```
7. You may fill the database with some data
8. Clone this repo and go inside the folder
9. Run commands below
```plaintext
gcloud builds submit --tag gcr.io/<YOUR-GCP-PROJECT>/Flask-API
gcloud run deploy aruna \
--image=gcr.io/<YOUR-GCP-PROJECT>/Flask-API \
--set-env-vars=DB_HOST=<DB-IP>,DB_USER=<DB-USER>,DB_PASS=<DB-PASS>,DB_NAME=<DB-NAME> \
--region=asia-southeast2 \
--project=<YOUR-GCP-PROJECT>
```
10. Done
