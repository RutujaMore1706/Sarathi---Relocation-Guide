# Saarthi- Guiding you home

Relocating to a new city can be overwhelming, presenting challenges like navigating unfamiliar neighborhoods, searching for housing, and accessing essential amenities. Key issues include the lack of centralized resources, difficulty assessing neighborhood safety, and the absence of real-time service insights. On top of this, adapting to new cultures, managing physical and emotional stress, and handling financial costs add further complexity.

To address these challenges, we developed **Saarthi**, an intelligent chatbot designed to simplify the relocation experience. Powered by a **Retrieval-Augmented Generation (RAG)** system, Saarthi integrates advanced AI with a **Neo4j knowledge graph** to deliver accurate and contextual information about crime rates, demographics, restaurants, parks, and more.

---

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
![image](https://github.com/user-attachments/assets/cf53504b-1508-4510-ace7-afa75b684c57)

![image](https://github.com/user-attachments/assets/2394cc94-b1ad-4058-b6a4-a54cef29b251)


##
### ⚙️ Setup Guide

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

---

