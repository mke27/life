# Best Life

By [Maya Ellis](https://github.com/mke27), [Areti Makropoulos](https://github.com/aremakropoulos), [Max Robinson](https://github.com/maxr21), [Zoya Siddiqui](https://github.com/zoyasiddiqui336)

## About

We created this project through Northeastern University's Summer 2025 Dialogue of Civilizations in Leuven, Belgium focused on data and software in the realm of international government and politics. Best Life provides insight in Europeon Union member states on how a user can improve their own or others' quality of life based on a set of priorities. Focused on key life factors of health, education, safety, and environment to guide decisions of relocation, policy development, or activism focus. Well informed decisions are made simple with a centralized platform that allows an effective assessment of how to pursue the best possible quality of life for all.

## To build this project

- git clone https://github.com/mke27/life.git
- Set up the `.env` file in the `api` folder based on the `.env.template` file.
- Run the following docker commands in the root directory:
  - docker compose build
  - docker compose up -d
- Open localhost:8501 in your browser

- The repo is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets
  - `./ml-src` - folder for storing ML models
- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. This file is used to run the app and API in Docker containers.

## Uses

There are three different personas in the application which are a prospective university student, a policymaker, and an activist. Each persona has features tailored to their use, creating a more personalized experience so that there satisfaction is maximized.

With the persona of a prospective university student their interaction with the application is to aid in the choice of relocating for further education as they embark on a new chapter of their lives. They are able to view recommendations of countries based on their preferences regarding the factors of education, health, safety, and environment. Saving their preference values and comparing the recommended countries predicted quality of life scores. Additionally, top university information based on their country of choice simplifies the challenging action of moving for further education to a country that best suites them.

The next persona of a policymaker is able to learn more about recent policy and view countries similar to theirs to make better informed decisions to improve the overall quality of life of the people in their country. As a policymaker they are able to view recent policy news and filter it based off of his focus on education, health, safety, or environment. Also, they are able to view the countries most similar to their own and compare the predicted quality of life in order to gain insights for their own policy decisions.

Lastly, the activist persona can maximize their impact in EU member states. They are able to countries with the largest need for improvement in the key factors of health, education, environment, or safety to learn more about where they should expand their reach in. They are also able to view predicted quality of life scores by countries to be able to recognize declines and address them before they occur. Activism is stronger together, so they are also able to view organizations in countries that address their area of interest to be able learn more about them and expand their outreach.

## Team Contribution Overview
### Maya Ellis

### Areti Makropoulos
Areti contributed significantly on developing the database, REST API, an UI layers of the application. In creating the database layer, she focused on designing well structured entities and relationships aligned with our application's needs, as well as generating mock data to support development. Additionally, she collaborated with Maya on the design of the REST API and implemented the UI for the application ensuring a smooth personalized performance. 

### Max Robinson

### Zoya Siddiqui
Zoya worked primarily on developing our time-series autoregressive model that was used to predict future quality of life for the next five years. She also procured, cleaned, and performed EDA on most of the data used for the ML models.

To learn more about specific individual contributions and our overall app development process, you can read [our team blog.](https://maxr21.github.io/belgiumsquad/)

## Future Considerations

One point to improve on is the factors we use to judge each country's 'health', 'education', 'environment' and 'safety' score. It is somewhat arbitrary at the moment and would be better if we had constructed a metric that combined many statistics collected on a Nation's safety. For example, we currently only look at life expectancy to guage the health score. If we combined hospital waiting times, number of doctors per person we could already get a better sense of how well a nation provides healthcare.

Furthermore, it would be interesting to compare our current autoregressive model with a boosting model that also takes into account the health, education, environement and safety scores. Constructing an autoregressive model for each factor individually and then using all those scores in another autoregressive model that predicts quality of life.
