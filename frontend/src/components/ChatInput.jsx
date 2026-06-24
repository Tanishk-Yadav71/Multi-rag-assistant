import { useState } from "react";

const ChatInput = ({
onSubmit,
loading,
}) => {
const [query, setQuery] = useState("");

const handleSubmit = () => {
if (!query.trim() || loading) return;

onSubmit(query);
setQuery("");

};

return ( <div
   className="
     bg-white/3
     backdrop-blur-2xl
     border border-white/10
     rounded-3xl
     shadow-xl
     p-2
   "
 > <div className="flex items-center gap-3">

    <input
      value={query}
      onChange={(e) =>
        setQuery(e.target.value)
      }
      onKeyDown={(e) =>
        e.key === "Enter" &&
        handleSubmit()
      }
      placeholder="Ask papers, docs, notes, or literature reviews..."
      className="
        flex-1
        bg-transparent
        px-5
        py-4
        outline-none
        text-white
        placeholder:text-gray-500
      "
    />

    <button
      disabled={loading}
      onClick={handleSubmit}
      className="
        flex items-center gap-2
        px-6 py-4
        rounded-2xl
        font-medium
        transition-all
        duration-300
        bg-blue-500
        hover:bg-blue-400
        disabled:bg-gray-700
        disabled:cursor-not-allowed
        text-black
      "
    >
      {loading ? (
        <>
          <div
            className="
              w-4 h-4
              border-2
              border-black
              border-t-transparent
              rounded-full
              animate-spin
            "
          />
          Thinking
        </>
      ) : (
        <>
          Ask
          <span>→</span>
        </>
      )}
    </button>

  </div>
</div>

);
};

export default ChatInput;
