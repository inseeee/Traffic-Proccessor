# MVP v0 Report

## Purpose and description

MVP v0 provides a runnable technical foundation consisting of:

- **Backend API** (`swp_project`): FastAPI server that accepts traffic statistics via HTTP POST and stores them (PostgreSQL) https://github.com/LimpingCoronation/swp_project#.  
- **Traffic Processor** (`Traffic-Processor`): Python script that generates mock packet counters (`in_packets`, `out_packets`) and sends them to the backend every second. https://github.com/TimLih-h/Traffic-Processor/blob/main/tp.py

Together they demonstrate a minimal data flow for network traffic monitoring.

## Deployment URL / runnable artifact

We failed to obtain university VM due to infinite subscription loading error, and could not resolve the problem with technical support before the deadline, but the MVP v0 can be ran localy.


## Public video demonstration

[Demo video](https://drive.google.com/file/d/1KZb48pca0WREjlQR2O6zNYwMon6ceqjj/view?usp=drive_link)

## Relationship to prototype and proposed MVP v1 stories

- **Prototype**: Figma mock shows the prototype of web-interface of the product. Only navigation and states examples with no functionality
- **MVP v1 stories** (proposed):  
  - US-01: Basic Packet Counting
  - US-02: Web Dashboard
  - US-03: Deploy TP as a Virtual Machine

- **MVP v0 relevance**:  
  - US-01 is partially implemented.  
  - US-02 is **not** implemented (only prototype).  
  - US-03 is **not** implemented (for the mentioned above reasons)
  - The foundation establishes the API contract and a working data sender.

## Current limitations, placeholders, and mocks
  
- **Mock data** – Traffic-Processor sends random integers instead of real packet counts.  
- **No persistent storage** – backend accepts data but may lose it on restart.  
- **No visualisation** – only API endpoints and raw database tables.
## Local setup instructions

See repositories description for detailed steps.  
Quick start:
```bash
#Backend
cd swp_project
cp .env_template .env
#edit .env variables
docker-compose up -d --build

#Traffic Processor
cd Traffic-Processor
pip install -r requirements.txt   # or requests library
python tp.py   # set SERVER_URL to your backend URL
```
## Repeatable smoke‑check scenario

1. Open the backend URL: `https://swp-project.onrender.com`
2. Navigate to `/docs` (Swagger UI).
3. Use the Traffic‑Processor script (or curl) to send a POST request.

### Steps

1. **Health check** – visit `/ping`
   *Expected result:* HTTP 200 OK, text `TP online`

2. **Swagger UI** – ensure the interactive documentation loads without errors.

3. **Submit mock data** – run the Traffic‑Processor and visit `/packets` 
*Expected result:* HTTP 200 or 201 response, packets information
