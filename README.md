# Saarthi- Guiding you home

Relocating to a new city can be overwhelming, presenting challenges like navigating unfamiliar neighborhoods, searching for housing, and accessing essential amenities. Key issues include the lack of centralized resources, difficulty assessing neighborhood safety, and the absence of real-time service insights. On top of this, adapting to new cultures, managing physical and emotional stress, and handling financial costs add further complexity.


## Project Overview
Saarthi helps users make informed decisions during relocation by integrating multiple data sources into one easy-to-use platform. The project aims to tackle common challenges in the relocation process, including:
   1. Unfamiliar neighborhoods
   2. Difficulty assessing neighborhood safety and amenities
   3. Cultural adaptation and managing stress
   4. Real-time service and neighborhood data
Powered by Large Language Models (LLMs) and a Neo4j knowledge graph, Saarthi provides insights on crime rates, demographics, nearby restaurants, parks, and more.

## Project Goals
Saarthi aims to address the complexities of relocating by offering an intelligent assistant that simplifies apartment searching and neighborhood discovery. Key features include:

1. Apartment Recommendation System: AI-powered suggestions based on user preferences, budget, and requirements.
2. Neighborhood Insights: Contextual information about various neighborhoods to aid users in making informed relocation decisions.
3. Dynamic User Interaction: An engaging and personalized interface for better user experience and satisfaction.


## **The Journey of Saarthi**

Building Saarthi was a journey filled with conundrums—decisions that shaped the project at every stage. Some choices proved invaluable, while others highlighted areas for growth. This iterative process required strategic planning and execution to bring our vision to life.

### **Project Phases**
1. **Data Collection and Preparation**  
   Curated and cleaned data to ensure accuracy and consistency, forming the foundation for reliable insights.

2. **Knowledge Graph Development**  
   Leveraged **Neo4j** to model relationships and build a robust, connected knowledge base for the chatbot.

3. **AI Model Integration**  
   Combined **RAG** and large language models (**LLMs**) to create an interactive, context-aware experience.

4. **Frontend Development**  
   Designed and implemented a sleek, intuitive interface using **Streamlit** to bring Saarthi to life.

5. **Feedback, Analytics, and Future Enhancements**  
   Focused on incorporating user feedback and analytics to ensure continuous improvement and relevance for our users.


## Tech Stack

### Programming Languages & Frameworks
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LLMs](https://img.shields.io/badge/LLMs-AI%20Driven-blue?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-36A6F0?style=for-the-badge&logo=langchain&logoColor=white)

### Cloud Platforms
![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)

### Databases
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FCC624?style=for-the-badge&logoColor=black)
![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)

### Data Orchestration & Transformation
![dbt-cloud](https://img.shields.io/badge/dbt%20Cloud-FF694B?style=for-the-badge&logo=dbt&logoColor=white)

### Technical Architecture:
![architecture-diagram](https://github.com/RutujaMore1706/Sarathi-Relocation-Guide/blob/main/sarathi-architecture-diagram.png)

### Project structure:

```
📦 
├─ .DS_Store
├─ Chatbot
│  ├─ .gitignore
│  ├─ __pycache__
│  │  ├─ get_context_data.cpython-312.pyc
│  │  ├─ guardrails_manager.cpython-311.pyc
│  │  └─ saarthi_guards.cpython-312.pyc
│  ├─ chat_context_streamlit.py
│  ├─ get_apartments.py
│  ├─ get_context_data.py
│  ├─ get_similar_groups.py
│  ├─ get_transformed_apartment_data.py
│  ├─ requirements.txt
│  ├─ saarthi_analytics.py
│  ├─ saarthi_conversation.db
│  ├─ saarthi_feedback.py
│  ├─ saarthi_guards.py
│  ├─ saarthi_main_app.py
│  └─ saarthi_recommend.py
├─ DataCollection
│  ├─ boston_groups.csv
│  ├─ boston_groups.json
│  ├─ boston_openSpace_data.csv
│  ├─ cleaned_boston_groups.csv
│  ├─ cleaned_boston_openSpace.csv
│  ├─ cleaned_boston_utilities_data.csv
│  ├─ cleaned_rentsmart_data.csv
│  ├─ get_csv_rentsmart.py
│  ├─ get_csv_utility.py
│  ├─ get_meetup.py
│  ├─ get_openSpace.py
│  ├─ lat_long_park.py
│  ├─ meetup_groups_transformation.py
│  ├─ openSpace_transformation.py
│  ├─ openspace_csv_gold.csv
│  ├─ openspace_latlong.csv
│  ├─ rentsmart_data_after_date.csv
│  ├─ rentsmart_transformations.py
│  └─ utilities_transformation.py
├─ Neo4j
│  ├─ __pycache__
│  │  └─ graph_structure_entity_linking.cpython-310.pyc
│  ├─ connect.py
│  ├─ data_load_neo4j.py
│  ├─ graph_structure_entity_linking.py
│  └─ snowflakeconnect.py
├─ README.md
├─ Saarthi Chatbot
│  ├─ chat_context_streamlit.py
│  ├─ get_apartments.py
│  ├─ get_context_data.py
│  ├─ get_similar_groups.py
│  ├─ get_transformed_apartment_data.py
│  ├─ requirements.txt
│  ├─ saarthi_analytics.py
│  ├─ saarthi_feedback.py
│  ├─ saarthi_guards.py
│  ├─ saarthi_main_app.py
│  └─ saarthi_recommend.py
├─ SnowFlakeTasks
│  ├─ CDC Task - Snowflake.html
│  ├─ CDC Task - Snowflake_files
│  │  ├─ 10381-3f66c784b06384b62b99.js.download
│  │  ├─ 43542-7740bec1b1c4542ae06f.js.download
│  │  ├─ 45739-dcf0c23b4aaf0de91275.js.download
│  │  ├─ 62524-8ebf93e4d0265fdf136a.js.download
│  │  ├─ 6326-9f8ff34ee058beca4da5.js.download
│  │  ├─ 73045-ac1eab408ec0dbf5e548.js.download
│  │  ├─ 85391-0dce631c3ee2e738ca07.js.download
│  │  ├─ 89915-112efe7f4aa809e00f6d.js.download
│  │  ├─ 91126-bc5e4fe7f4ddbdbf9ef2.js.download
│  │  ├─ core-js-592492ca0f6bdea9d881.js.download
│  │  ├─ datadog-05d135b0a44708954a95.js.download
│  │  ├─ generated-styles.241021-2-19a5f77f18.css
│  │  ├─ index-a1f7c9008bca05f5567c.js.download
│  │  ├─ initialization-3a2a3d236c389fcf02a1.js.download
│  │  ├─ lezer-7ebaeb628b84eee7610d.js.download
│  │  ├─ lodash-c720f727dcb0397194fb.js.download
│  │  ├─ moment-0ab6b083739678163fca.js.download
│  │  ├─ numeracy-7f57a7648ca26e8beaaf.js.download
│  │  ├─ prefetcher-352eff9a47eb4b77c375.js.download
│  │  ├─ react-19b00cb97480d06be906.js.download
│  │  ├─ redux-431e39e67c2707c32af3.js.download
│  │  ├─ snowflakeSqlLanguageServer-922d71b2f99cbc2f366c.js.download
│  │  └─ styles-c83d9d209d4fc4ea9b40.css
│  ├─ Consolidated Table Creation - Snowflake.html
│  ├─ Consolidated Table Creation - Snowflake_files
│  │  ├─ 10381-3f66c784b06384b62b99.js.download
│  │  ├─ 43542-7740bec1b1c4542ae06f.js.download
│  │  ├─ 45739-dcf0c23b4aaf0de91275.js.download
│  │  ├─ 62524-8ebf93e4d0265fdf136a.js.download
│  │  ├─ 6326-9f8ff34ee058beca4da5.js.download
│  │  ├─ 73045-ac1eab408ec0dbf5e548.js.download
│  │  ├─ 85391-0dce631c3ee2e738ca07.js.download
│  │  ├─ 89915-112efe7f4aa809e00f6d.js.download
│  │  ├─ 91126-bc5e4fe7f4ddbdbf9ef2.js.download
│  │  ├─ core-js-592492ca0f6bdea9d881.js.download
│  │  ├─ datadog-05d135b0a44708954a95.js.download
│  │  ├─ generated-styles.241021-2-19a5f77f18.css
│  │  ├─ index-a1f7c9008bca05f5567c.js.download
│  │  ├─ initialization-3a2a3d236c389fcf02a1.js.download
│  │  ├─ lezer-7ebaeb628b84eee7610d.js.download
│  │  ├─ lodash-c720f727dcb0397194fb.js.download
│  │  ├─ moment-0ab6b083739678163fca.js.download
│  │  ├─ numeracy-7f57a7648ca26e8beaaf.js.download
│  │  ├─ prefetcher-352eff9a47eb4b77c375.js.download
│  │  ├─ react-19b00cb97480d06be906.js.download
│  │  ├─ redux-431e39e67c2707c32af3.js.download
│  │  ├─ snowflakeSqlLanguageServer-922d71b2f99cbc2f366c.js.download
│  │  └─ styles-c83d9d209d4fc4ea9b40.css
│  ├─ Snowflake CDC Streams - Snowflake.html
│  └─ Snowflake CDC Streams - Snowflake_files
│     ├─ 10381-3f66c784b06384b62b99.js.download
│     ├─ 43542-7740bec1b1c4542ae06f.js.download
│     ├─ 45739-dcf0c23b4aaf0de91275.js.download
│     ├─ 62524-8ebf93e4d0265fdf136a.js.download
│     ├─ 6326-9f8ff34ee058beca4da5.js.download
│     ├─ 73045-ac1eab408ec0dbf5e548.js.download
│     ├─ 85391-0dce631c3ee2e738ca07.js.download
│     ├─ 89915-112efe7f4aa809e00f6d.js.download
│     ├─ 91126-bc5e4fe7f4ddbdbf9ef2.js.download
│     ├─ core-js-592492ca0f6bdea9d881.js.download
│     ├─ datadog-05d135b0a44708954a95.js.download
│     ├─ generated-styles.241021-2-19a5f77f18.css
│     ├─ index-a1f7c9008bca05f5567c.js.download
│     ├─ initialization-3a2a3d236c389fcf02a1.js.download
│     ├─ lezer-7ebaeb628b84eee7610d.js.download
│     ├─ lodash-c720f727dcb0397194fb.js.download
│     ├─ moment-0ab6b083739678163fca.js.download
│     ├─ numeracy-7f57a7648ca26e8beaaf.js.download
│     ├─ prefetcher-352eff9a47eb4b77c375.js.download
│     ├─ react-19b00cb97480d06be906.js.download
│     ├─ redux-431e39e67c2707c32af3.js.download
│     ├─ snowflakeSqlLanguageServer-922d71b2f99cbc2f366c.js.download
│     └─ styles-c83d9d209d4fc4ea9b40.css
├─ Streamlit
│  ├─ Page1.py
│  ├─ app.py
│  ├─ get_similar_groups.py
│  └─ get_transformed_apartment_data.py
├─ data_prep
│  ├─ __pycache__
│  │  └─ fetch_restaurant.cpython-311.pyc
│  ├─ csv_cleaning.py
│  ├─ fetch_restaurant.py
│  ├─ meetup_groups_transformation.py
│  ├─ openSpace_transformation.py
│  ├─ prep_clean
│  │  ├─ yelp_cleaned_cvs.csv
│  │  ├─ yelp_cleaned_fenway.csv
│  │  ├─ yelp_cleaned_indian.csv
│  │  ├─ yelp_cleaned_korean.csv
│  │  ├─ yelp_cleaned_mexican.csv
│  │  ├─ yelp_restaurants_cleaned.csv
│  │  └─ yelp_zipcode.csv
│  ├─ prep_flow
│  │  └─ basi_cleaning_yelp_restaurant.tfl
│  ├─ rentsmart_transformations.py
│  ├─ utilities_transformation.py
│  ├─ yelp_data.csv
│  ├─ yelp_data_cvs.csv
│  ├─ yelp_data_indian.csv
│  ├─ yelp_data_korean.csv
│  └─ yelp_data_mexican.csv
├─ pipelines
│  ├─ .gitignore
│  ├─ README.md
│  ├─ analyses
│  │  └─ .gitkeep
│  ├─ dbt_project.yml
│  ├─ macros
│  │  └─ .gitkeep
│  ├─ models
│  │  ├─ bronze
│  │  │  ├─ br_boston_groups.sql
│  │  │  ├─ br_boston_openspace.sql
│  │  │  ├─ br_boston_utilities.sql
│  │  │  ├─ br_yelp_food.sql
│  │  │  └─ br_zillow_apartments.sql
│  │  ├─ gold
│  │  │  ├─ apartments.sql
│  │  │  ├─ meetup_groups.sql
│  │  │  ├─ open_space_ground.sql
│  │  │  ├─ restaurants.sql
│  │  │  └─ utilities.sql
│  │  ├─ silver
│  │  │  ├─ sl_boston_groups.sql
│  │  │  ├─ sl_boston_openspace.sql
│  │  │  ├─ sl_boston_utilities.sql
│  │  │  ├─ sl_yelp_food.sql
│  │  │  ├─ sl_yelp_food_tests.yml
│  │  │  └─ sl_zillow_apartments.sql
│  │  └─ sources.yml
│  ├─ package-lock.yml
│  ├─ packages.yml
│  ├─ seeds
│  │  ├─ .gitkeep
│  │  └─ zip_codes.csv
│  ├─ snapshots
│  │  └─ .gitkeep
│  └─ tests
│     └─ .gitkeep
├─ requirements.txt
└─ sarathi-architecture-diagram.png
```

## How to run?

#### **1. Clone the Repository**

#### **2. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt

```

#### **4. Configure DBT**
- Add your profiles.yml configuration for Snowflake:
```bash
my_dbt_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your_account>
      user: <your_username>
      password: <your_password>
      role: <your_role>
      database: saarthi
      warehouse: <your_warehouse>
      schema: boston
      threads: 4
      client_session_keep_alive: False

```

#### **5. Run DBT Models**
```bash
cd pipelines
dbt run
```

#### **6. Launch the Streamlit Application**
```bash
streamlit run saarthi_main_app.py
```

#### **7. Generate DBT Documentation**
```bash
dbt docs generate
dbt docs serve
```

## References:
- ChatGPT: https://chat.openai.com/
- OpenAI CLIP: https://towardsdatascience.com/quick-fire-guide-to-multi-modal-ml-with-openais-clip-2dad7e398ac0
- neo4j:  https://neo4j.com/docs/



