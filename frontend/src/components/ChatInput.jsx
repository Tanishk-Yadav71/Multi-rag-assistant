import { useState } from "react";

const ChatInput = ({ onSubmit, loading }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = () => {
    if (!query.trim() || loading) return;
    onSubmit(query);
    setQuery("");
  };

  return (
    <div
      className="
        glass-panel
        rounded-2xl
        shadow-2xl
        p-1.5
        transition-all
        duration-300
        focus-within:border-white/20
        focus-within:ring-1
        focus-within:ring-white/10
      "
    >
      <div className="flex items-center gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          placeholder="Ask papers, docs, notes, or literature reviews..."
          className="
            flex-1
            bg-transparent
            px-4
            py-3.5
            outline-none
            text-sm
            text-white
            placeholder:text-gray-500
          "
        />

        <button
          disabled={loading}
          onClick={handleSubmit}
          className="
            flex items-center gap-2
            px-5 py-3
            rounded-xl
            text-sm
            font-mediu
            transition-all
            duration-300
            bg-linear-to-r from-blue-500 to-indigo-500
            hover:from-blue-400 hover:to-indigo-400
            disabled:from-gray-800 disabled:to-gray-800
            disabled:text-gray-500
            disabled:cursor-not-allowed
            text-black font-medium 
            shadow-lg shadow-blue-500/10
          "
        >
          {loading ? (
            <>
              <div
                className="
                  w-3.5 h-3.5
                  border-2
                  border-gray-500
                  border-t-transparent
                  rounded-full
                  animate-spin
                "
              />
              <span className="text-gray-500 text-xs">Researching</span>
            </>
          ) : (
            <>
              <span className="text-white">Ask</span>
              <span className="text-white transform transition-transform group-hover:translate-x-1">→</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;