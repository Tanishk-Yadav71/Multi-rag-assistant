const askQuestion = async (query) => {
  try {
    setLoading(true);
    setError("");

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: query,
      },
    ]);

    const response = await sendQuery(query);

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        ...response,
      },
    ]);
  } catch {
    setError("Unable to connect to backend.");
  } finally {
    setLoading(false);
  }
};