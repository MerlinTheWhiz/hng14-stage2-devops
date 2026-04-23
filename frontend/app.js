const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

const API_URL = process.env.API_URL || "http://localhost:8000";
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    const status = err.response ? err.response.status : 500;
    const msg = err.response?.data?.detail || "something went wrong";
    res.status(status).json({ error: msg });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    const status = err.response ? err.response.status : 500;
    const msg = err.response && err.response.data && err.response.data.detail ? err.response.data.detail : "something went wrong";
    res.status(status).json({ error: msg });
  }
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});
