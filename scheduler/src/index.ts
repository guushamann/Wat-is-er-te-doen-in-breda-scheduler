import express from "express";
import cors from "cors";
import fs from "fs";
import path from "path";
import cron from "node-cron";
import axios from "axios";

const app = express();
app.use(express.json());
app.use(cors());

const DATA_DIR = path.join(__dirname, "../data");
const SCHEDULES_FILE = path.join(DATA_DIR, "schedules.json");
const LOGS_FILE = path.join(DATA_DIR, "logs.json");

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Initialize files if they don't exist
if (!fs.existsSync(SCHEDULES_FILE)) {
  fs.writeFileSync(SCHEDULES_FILE, "[]");
}
if (!fs.existsSync(LOGS_FILE)) {
  fs.writeFileSync(LOGS_FILE, "[]");
}

interface Schedule {
  id: string;
  url: string;
  cronExpression: string;
  enabled: boolean;
}

interface Log {
  id: string;
  timestamp: string;
  status: "success" | "error";
  response: string;
}

// Load schedules from file
function loadSchedules(): Schedule[] {
  const data = fs.readFileSync(SCHEDULES_FILE, "utf-8");
  return JSON.parse(data);
}

// Save schedules to file
function saveSchedules(schedules: Schedule[]): void {
  fs.writeFileSync(SCHEDULES_FILE, JSON.stringify(schedules, null, 2));
}

// Load logs from file
function loadLogs(): Log[] {
  const data = fs.readFileSync(LOGS_FILE, "utf-8");
  return JSON.parse(data);
}

// Save log to file
function saveLog(log: Log): void {
  const logs = loadLogs();
  logs.push(log);
  fs.writeFileSync(LOGS_FILE, JSON.stringify(logs, null, 2));
}

// Active cron jobs map
const cronJobs = new Map<string, cron.ScheduledTask>();

// Start a job
function startJob(schedule: Schedule): void {
  if (cronJobs.has(schedule.id)) {
    stopJob(schedule.id);
  }

  if (schedule.enabled) {
    const task = cron.schedule(schedule.cronExpression, async () => {
      try {
        console.log("executing job:", schedule);
        const response = await axios.post(schedule.url);
        saveLog({
          id: schedule.id,
          timestamp: new Date().toISOString(),
          status: "success",
          response: `${response.status} ${response.statusText}`,
        });
      } catch (error: any) {
        saveLog({
          id: schedule.id,
          timestamp: new Date().toISOString(),
          status: "error",
          response: error.message,
        });
      }
    });
    console.log("started schedule for job:", schedule);
    cronJobs.set(schedule.id, task);
  }
}

// Stop a job
function stopJob(id: string): void {
  const job = cronJobs.get(id);
  if (job) {
    job.stop();
    cronJobs.delete(id);
  }
}

// Initialize all jobs from schedules
function initializeJobs(): void {
  const schedules = loadSchedules();
  schedules.forEach(startJob);
}

// API Routes
app.get("/schedules", (req, res) => {
  const schedules = loadSchedules();
  res.json(schedules);
});

app.post("/schedules", (req, res) => {
  const schedule: Schedule = req.body;
  const schedules = loadSchedules();

  if (schedules.some((s) => s.id === schedule.id)) {
    return res.status(400).json({ error: "Schedule ID already exists" });
  }

  if (!cron.validate(schedule.cronExpression)) {
    return res.status(400).json({ error: "Invalid cron expression" });
  }

  schedules.push(schedule);
  saveSchedules(schedules);
  startJob(schedule);
  res.status(201).json(schedule);
});

app.get("/logs", (req, res) => {
  const logs = loadLogs();
  res.json(logs);
});

// Initialize jobs on startup
initializeJobs();

const PORT = process.env.PORT || 8085;
app.listen(PORT, () => {
  console.log(`Scheduler service running on port ${PORT}`);
});
