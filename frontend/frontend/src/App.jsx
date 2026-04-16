import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/jobs?limit=20`);
      const data = await res.json();
      setJobs(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const searchJobs = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `${API}/jobs/search?title=${encodeURIComponent(title)}`
      );
      const data = await res.json();
      setJobs(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Job Data Dashboard</h1>

      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search job title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ padding: "8px", marginRight: "10px" }}
        />
        <button onClick={searchJobs}>Search</button>
        <button onClick={fetchJobs} style={{ marginLeft: "10px" }}>
          Reset
        </button>
      </div>

      {loading && <p>Loading...</p>}

      <div>
        {jobs.map((job) => (
          <div
            key={job.job_id}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "10px",
              borderRadius: "8px",
            }}
          >
            <h3>{job.job_title}</h3>
            <p><strong>Company:</strong> {job.company_name}</p>
            <p><strong>Location:</strong> {job.job_location}</p>
            <p><strong>Country:</strong> {job.job_country}</p>
            <p><strong>Salary:</strong> {job.salary_year_avg || "N/A"}</p>
            <p><strong>Remote:</strong> {job.job_work_from_home ? "Yes" : "No"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}