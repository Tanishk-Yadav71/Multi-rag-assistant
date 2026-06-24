import ChatInput from "../components/ChatInput";
import ChatMessage from "../components/ChatMessage";
import LoadingIndicator from "../components/LoadingIndicator";

import { useChat } from "../hooks/useChat";

const Home = () => {
const {
messages,
loading,
error,
askQuestion,
} = useChat();

return ( <div className="h-screen bg-[#0b0e1500] text-white flex overflow-hidden">

  {/* Sidebar */}
  <aside className="w-72 border-r border-white/5 bg-[#0f131d00] flex flex-col">

    <div className="p-6 border-b border-white/5">
      <h2 className="text-xl font-semibold">
        Agentic Multi-RAG
      </h2>

      <p className="text-xs text-gray-400 mt-1">
        Research Assistant
      </p>
    </div>

    <div className="p-4">
      <button
        className="
          w-full
          rounded-xl
          bg-blue-500
          hover:bg-blue-400
          text-black
          font-medium
          py-3
          transition
        "
      >
        + New Chat
      </button>
    </div>

    <div className="flex-1 overflow-y-auto px-3">
      <div className="text-xs uppercase tracking-widest text-gray-500 mb-3">
        Recent Chats
      </div>

      <div className="space-y-2">
        <div className="p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer text-sm">
          Vision Transformer
        </div>

        <div className="p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer text-sm">
          FastAPI Docs
        </div>

        <div className="p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer text-sm">
          BCNF Notes
        </div>
      </div>
    </div>
  </aside>

  {/* Main Area */}
  <main className="flex-1 flex flex-col">

    {/* Header */}
    <header className="border-b border-white/5 px-8 py-5 bg-[#10131a00]">
      <h1 className="text-2xl font-light">
        Research Intelligence
      </h1>

      <p className="text-sm text-gray-400 mt-1">
        Agentic Multi-RAG Research Assistant
      </p>
    </header>

    {/* Messages */}
    <div className="flex-1 overflow-y-auto px-8 py-8">

      {messages.length === 0 && (
        <div className="max-w-3xl mx-auto text-center mt-24">

          <h2 className="text-5xl font-light mb-4">
            Ask Anything
          </h2>

          <p className="text-gray-400">
            Search papers, docs, notes, literature reviews,
            and compare research models.
          </p>

          <div className="flex flex-wrap justify-center gap-3 mt-8">

            <button className="px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 text-sm">
              Vision Transformers Review
            </button>

            <button className="px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 text-sm">
              Compare ViT vs Swin
            </button>

            <button className="px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 text-sm">
              FastAPI Best Practices
            </button>

            <button className="px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 text-sm">
              Agentic AI Papers
            </button>

          </div>
        </div>
      )}

      <div className="max-w-5xl mx-auto space-y-8">

        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message}
          />
        ))}

        {loading && (
          <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
            <LoadingIndicator />
          </div>
        )}

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-300">
            {error}
          </div>
        )}

      </div>
    </div>

    {/* Input */}
    <div className="border-t border-white/5 bg-[#10131a] p-6">

      <div className="max-w-4xl mx-auto">
        <ChatInput
          onSubmit={askQuestion}
          loading={loading}
        />
      </div>

    </div>
  </main>
</div>

);
};

export default Home;
