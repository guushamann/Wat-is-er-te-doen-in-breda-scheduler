# Docker Job Scheduler System

A containerized job scheduler system consisting of three services:

1. **Scheduler Service** (Node.js + TypeScript)

   - Manages job schedules stored in JSON
   - Executes jobs based on cron expressions
   - Maintains execution logs
   - Exposes REST API for schedule management

2. **Test Job Service** (Python)

   - Simple web service with one endpoint
   - Simulates job execution with delay
   - Returns either success (200) or error (500)

3. **Web Interface** (React + TypeScript + Vite)
   - Displays scheduled jobs
   - Shows execution logs
   - Provides interface for managing schedules

## Project Structure

```
.
├── docker-compose.yml
├── scheduler/
│   ├── Dockerfile
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
├── test-job/
│   ├── Dockerfile
│   └── app.py
└── web-interface/
    ├── Dockerfile
    ├── src/
    ├── package.json
    └── vite.config.ts
```

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository
2. Run the system:
   ```bash
   docker-compose up --build
   ```

## Services

### Scheduler Service

- Port: 3000
- API Endpoints:
  - GET /schedules - List all scheduled jobs
  - POST /schedules - Create new schedule
  - GET /logs - View execution logs

### Test Job Service

- Port: 5000
- Endpoint: POST /execute

### Web Interface

- Port: 8087
- Access the dashboard at http://localhost:8087

## Schedule Format

Schedules are stored in JSON format:

```json
{
  "id": "job1",
  "url": "http://test-job:8086/execute",
  "cronExpression": "*/5 * * * *",
  "enabled": true
}
```

## Log Format

Execution logs are stored in JSON format:

```json
{
  "id": "job1",
  "timestamp": "2024-01-20T10:00:00Z",
  "status": "success",
  "response": "200 OK"
}
```

## Development

To modify the services:

1. Scheduler Service:

   ```bash
   cd scheduler
   npm install
   npm run dev
   ```

2. Test Job Service:

   ```bash
   cd test-job
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

3. Web Interface:
   ```bash
   cd web-interface
   npm install
   npm run dev
   ```
