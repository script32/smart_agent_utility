# Smart Agents Utility

**Field Operations Smarter, Geospatially Powered**

---

## What is Smart Agents Utility?

Smart Agents Utility is an intelligent multi-agent system designed for companies that manage **linear assets** such as **electricity**, **water**, **gas**, and **telecom**.  
It merges **Semantic Kernel**, **geospatial databases**, and **Azure AI** into a unified field operations platform.

---

## Key Features

- **Multi-Agent Orchestration** (Semantic Kernel 1.28+)
- **Geospatial Intelligence** (PostGIS + OpenStreetMap)
- **Smart Fault Reporting** and **Crew Dispatch**
- **Regulatory AI Integration** (Azure AI Foundry Agents)
- **Real-Time Map Visualization** (dynamic maps on demand)
- **Chainlit Frontend** for instant conversations
- **Azure Container Apps Deployment** for full scalability

---

## Use Cases

| Industry     | Application Example                                        |
|--------------|-------------------------------------------------------------|
| Electricity  | Outage localization, dispatch of emergency crews           |
| Water        | Leak detection mapping, maintenance prioritization          |
| Gas          | Risk zone analysis for pipelines                             |
| Telecom      | Storm damage mapping and fiber restoration planning          |
| Smart Cities | Unified field services coordination across all utilities     |

---

## Why Smart Agents Utility is Innovative

- Combines **natural language** understanding with **geospatial** operations.
- **Multi-agent specialization** (Field, Crew, Geo, Reporting, Regulatory).
- Instant generation of **visual maps** within conversations.
- Fully extendable for **multi-utility** field operations.
- **Azure-native** scalable deployment.

---

## Technologies Used

- Python 3.11+
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel) 1.28+
- Chainlit (Frontend for conversational AI)
- PostgreSQL + PostGIS (geospatial database)
- Azure AI Foundry (agent orchestration, regulatory knowledge)
- Azure Container Apps (deployment)
- Folium (for OpenStreetMap-based map generation)

---

## How to Deploy

### Local Development

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your .env file:

```bash
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_AI_FOUNDATION_AGENT_ID=your-agent-id
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432
POSTGRES_DB=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
```

5. Run the API:

```bash
uvicorn app.main:app --reload
```
6. (Optional) Run the Chat Frontend:

```bash
chainlit run app/app_chainlit.py
```

## Deploy to Azure Container Apps

1. Build the container:

```bash
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Push to Azure Container Registry.

3. Deploy to Azure Container Apps.

4. Set environment variables in Container App settings.


## Azure AI Foundry Integration

- Create an Agent in Azure AI Foundry.

- Obtain your assistant_id and set it as AZURE_AI_FOUNDATION_AGENT_ID.

- Smart Agents Utility will route advanced regulatory or technical questions to this Foundry agent automatically.

 ## License

 This project is licensed under the MIT License.
See the LICENSE file for details.


## Video
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/kb8b04hwXZ4/0.jpg)](https://www.youtube.com/watch?v=kb8b04hwXZ4)