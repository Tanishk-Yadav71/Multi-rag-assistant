import { useState, useEffect } from "react";
import { sendQuery } from "../services/api";

export const useChat = () => {
  const [sessions, setSessions] = useState({});
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (Object.keys(sessions).length === 0) {
      createNewSession();
    }
  }, []);

  const createNewSession = () => {
    const newId = `session_${Date.now()}`;
    const newSession = {
      id: newId,
      title: "New Research Session",
      messages: [],
    };
    
    setSessions((prev) => ({
      ...prev,
      [newId]: newSession,
    }));
    setActiveSessionId(newId);
    setError("");
  };

  const askQuestion = async (query) => {
    if (!activeSessionId) return;

    try {
      setLoading(true);
      setError("");

      const userMessage = { role: "user", content: query };

      setSessions((prev) => {
        const currentSession = prev[activeSessionId];
        const updatedTitle = currentSession.messages.length === 0 
          ? query.slice(0, 30) + (query.length > 30 ? "..." : "")
          : currentSession.title;

        return {
          ...prev,
          [activeSessionId]: {
            ...currentSession,
            title: updatedTitle,
            messages: [...currentSession.messages, userMessage],
          },
        };
      });

      const response = await sendQuery(query);

      const assistantMessage = { role: "assistant", ...response };

      setSessions((prev) => ({
        ...prev,
        [activeSessionId]: {
          ...prev[activeSessionId],
          messages: [...prev[activeSessionId].messages, assistantMessage],
        },
      }));

    } catch (err) {
      setError("Unable to connect to backend.");
      console.error("Agent Pipeline Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const currentSession = sessions[activeSessionId];
  const messages = currentSession ? currentSession.messages : [];

  return {
    sessions: Object.values(sessions),  
    activeSessionId,
    setActiveSessionId,
    createNewSession,
    messages,
    loading,
    error,
    askQuestion,
  };
};