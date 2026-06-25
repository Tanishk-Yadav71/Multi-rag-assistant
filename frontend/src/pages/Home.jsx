import { useEffect, useRef } from "react";
import ChatInput from "../components/ChatInput";
import ChatMessage from "../components/ChatMessage";
import LoadingIndicator from "../components/LoadingIndicator";
import { useChat } from "../hooks/useChat";

const Home = () => {
  const {
    sessions,
    activeSessionId,
    setActiveSessionId,
    createNewSession,
    messages,
    loading,
    error,
    askQuestion,
  } = useChat();

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="h-screen gradient-bg text-white flex overflow-hidden">
      
      <aside className="w-72 border-r border-white/5 bg-black/20 backdrop-blur-md flex flex-col">
        <div className="p-6 border-b border-white/5">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500 shadow-lg" />
            <h2 className="text-lg font-semibold tracking-tight">
              Research Intel
            </h2>
          </div>
          <p className="text-xs text-gray-500 mt-1 font-medium tracking-wider uppercase">
            Multi-Agent Pipeline
          </p>
        </div>
        <div className="p-4">
          <button
            onClick={createNewSession}
            className="
              w-full
              rounded-xl
              bg-white/5
              hover:bg-white/10
              border border-white/10
              text-white
              text-sm
              font-medium
              py-3
              transition-all
              duration-300
              cursor-pointer
              hover:scale-[1.01]
              active:scale-[0.99]
            "
          >
            + New Research Session
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-2">
          <div className="text-xs uppercase tracking-widest text-gray-500 font-bold mb-4 px-2">
            Recent Analysis
          </div>

          <div className="space-y-1.5">
            {sessions.map((session) => {
              const isActive = session.id === activeSessionId;
              return (
                <div 
                  key={session.id} 
                  onClick={() => setActiveSessionId(session.id)}
                  className={`
                    p-3 rounded-xl border transition-all duration-200 cursor-pointer text-sm
                    ${isActive 
                      ? "bg-blue-500/10 border-blue-500/30 text-white font-medium" 
                      : "bg-white/2 hover:bg-white/5 border-transparent text-gray-400 hover:text-white"
                    }
                  `}
                >
                  <div className="truncate">{session.title}</div>
                </div>
              );
            })}
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col h-full bg-transparent">

        <header className="border-b border-white/5 px-8 py-5 bg-black/10 backdrop-blur-sm flex items-center justify-between">
          <div>
            <h1 className="text-xl font-medium tracking-tight text-gray-200">
              Research Intelligence Engine
            </h1>
            <p className="text-xs text-gray-500 mt-0.5">
              Cross-referencing indexed semantic memory pools
            </p>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto px-8 py-8">
          {messages.length === 0 && (
            <div className="max-w-2xl mx-auto text-center mt-32">
              <h2 className="text-4xl font-light tracking-tight mb-3 text-white">
                Demystify Your Data Architecture
              </h2>
              <p className="text-sm text-gray-400 max-w-md mx-auto leading-relaxed">
                Query papers, literature reviews, operational notes, or documentation structures instantly.
              </p>

              <div className="flex flex-wrap justify-center gap-2.5 mt-8 max-w-xl mx-auto">
                {[
                  "Vision Transformers Review",
                  "Compare ViT vs Swin",
                  "FastAPI Best Practices",
                  "Agentic AI Consensus"
                ].map((promptText, idx) => (
                  <button 
                    key={idx}
                    onClick={() => askQuestion(promptText)}
                    className="px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-xs text-gray-300 transition-all duration-200 cursor-pointer"
                  >
                    {promptText}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="max-w-4xl mx-auto space-y-8">
            {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}

            {loading && <LoadingIndicator />}

            {error && (
              <div className="bg-red-500/5 border border-red-500/20 rounded-2xl p-4 text-sm text-red-400 flex items-center gap-3">
                <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                {error}
              </div>
            )}
            
            <div ref={bottomRef} />
          </div>
        </div>

        <div className="border-t border-white/5 bg-[#0b0e15] bg-opacity-80 backdrop-blur-md p-6">
          <div className="max-w-3xl mx-auto">
            <ChatInput onSubmit={askQuestion} loading={loading} />
            <p className="text-[10px] text-center text-gray-600 mt-3 tracking-wide">
              Agentic system synthesizes content dynamically from connected vector spaces.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;