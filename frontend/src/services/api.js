import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const sendQuery = async (query) => {
  const { data } = await API.post("/chat", {
    query,
  });

  return data;
};