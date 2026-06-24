import DatabaseBadge from "./DatabaseBadge";
import SourceList from "./SourceList";

const ChatMessage = ({ message }) => {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div
          className="
            max-w-2xl
            bg-blue-500
            text-black
            px-5
            py-4
            rounded-3xl
            rounded-br-md
            shadow-lg
          "
        >
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div
      className="
        bg-white/3
        backdrop-blur-xl
        border border-white/10
        rounded-3xl
        p-6
        shadow-xl
      "
    >
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-medium">
          Agentic Multi-RAG
        </h3>

        <DatabaseBadge database={message.database} />
      </div>

      <div className="text-gray-200 whitespace-pre-wrap leading-8">
        {message.answer}
      </div>

      <SourceList sources={message.sources} />
    </div>
  );
};

export default ChatMessage;