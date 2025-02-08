import { useState, useEffect } from "react";
import {
  Container,
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  IconButton,
  AppBar,
  Toolbar,
} from "@mui/material";
import { PlayArrow, Pause } from "@mui/icons-material";
import axios from "axios";
import { format } from "date-fns";

interface Job {
  id: string;
  url: string;
  cronExpression: string;
  enabled: boolean;
}

interface Log {
  id: string;
  timestamp: string;
  status: string;
  response: string;
}

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [logs, setLogs] = useState<Log[]>([]);
  const apiUrl =
    import.meta.env.VITE_SCHEDULER_API_URL || "http://localhost:3000";

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get(`${apiUrl}/schedules`);
        setJobs(response.data);
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };

    const fetchLogs = async () => {
      try {
        const response = await axios.get(`${apiUrl}/logs`);
        setLogs(response.data);
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    };

    fetchJobs();
    fetchLogs();
    const interval = setInterval(() => {
      fetchJobs();
      fetchLogs();
    }, 8085);

    return () => clearInterval(interval);
  }, []);

  const toggleJob = async (job: Job) => {
    try {
      await axios.post(`${apiUrl}/schedules`, {
        ...job,
        enabled: !job.enabled,
      });
    } catch (error) {
      console.error("Error toggling job:", error);
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Job Scheduler Dashboard</Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Box sx={{ display: "flex", gap: 4 }}>
          <Paper sx={{ p: 2, flexBasis: "50%" }}>
            <Typography variant="h6" gutterBottom>
              Scheduled Jobs
            </Typography>
            <List>
              {jobs.map((job) => (
                <ListItem
                  key={job.id}
                  secondaryAction={
                    <IconButton edge="end" onClick={() => toggleJob(job)}>
                      {job.enabled ? <Pause /> : <PlayArrow />}
                    </IconButton>
                  }
                >
                  <ListItemText
                    primary={job.id}
                    secondary={
                      <>
                        {job.url}
                        <br />
                        Cron: {job.cronExpression}
                        <br />
                        <Chip
                          label={job.enabled ? "Enabled" : "Disabled"}
                          color={job.enabled ? "success" : "default"}
                          size="small"
                        />
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>

          <Paper sx={{ p: 2, flexBasis: "50%" }}>
            <Typography variant="h6" gutterBottom>
              Execution Logs
            </Typography>
            <List>
              {[...logs]
                .sort(
                  (a, b) =>
                    new Date(b.timestamp).getTime() -
                    new Date(a.timestamp).getTime()
                )
                .map((log, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={`Job: ${log.id}`}
                      secondary={
                        <>
                          Time:{" "}
                          {format(
                            new Date(log.timestamp),
                            "yyyy-MM-dd HH:mm:ss"
                          )}
                          <br />
                          Status:{" "}
                          <Chip
                            label={log.status}
                            color={
                              log.status === "success" ? "success" : "error"
                            }
                            size="small"
                          />
                          <br />
                          Response: {log.response}
                        </>
                      }
                    />
                  </ListItem>
                ))}
            </List>
          </Paper>
        </Box>
      </Container>
    </Box>
  );
}

export default App;
