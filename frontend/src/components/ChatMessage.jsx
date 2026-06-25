import DatabaseBadge from "./DatabaseBadge";
import SourceList from "./SourceList";

// Premium Markdown Formatter Helper
const renderContent = (text) => {
  if (!text) return null;

  // Detect if the block is a Markdown table
  const lines = text.trim().split("\n");
  const isTable = lines.length >= 2 && 
                  lines[0].trim().startsWith("|") && 
                  lines[1].trim().includes("---");

  if (isTable) {
    // Separate table rows, filtering out formatting delimiter lines (e.g., |---|---|)
    const tableRows = lines.filter(line => line.trim().startsWith("|") && !line.includes("---"));
    
    if (tableRows.length > 0) {
      // Parse out cells from the first row as headers
      const headers = tableRows[0].split("|").map(cell => cell.trim()).filter(cell => cell !== "");
      const dataRows = tableRows.slice(1).map(row => 
        row.split("|").map(cell => cell.trim()).filter(cell => cell !== "")
      );

      return (
        <div className="overflow-x-auto my-4 rounded-xl border border-white/10 glass-panel">
          <table className="w-full text-left border-collapse text-sm">
            <thead>
              <tr className="border-b border-white/10 bg-white/2">
                {headers.map((header, idx) => (
                  <th key={idx} className="px-5 py-3 font-semibold text-gray-300 tracking-wide uppercase text-xs">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {dataRows.map((row, rowIdx) => (
                <tr key={rowIdx} className="hover:bg-white/1 transition-colors">
                  {row.map((cell, cellIdx) => (
                    <td key={cellIdx} className="px-5 py-3.5 text-gray-300 font-light leading-relaxed">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }
  }

  // Fallback to regular formatted text if it's not a table
  return <div className="whitespace-pre-wrap leading-8 font-light text-gray-100">{text}</div>;
};

const ChatMessage = ({ message }) => {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div
          className="
            max-w-2xl
            bg-linear-to-r from-blue-600 to-indigo-600
            text-white
            px-6
            py-4
            rounded-3xl
            rounded-br-sm
            shadow-xl
            text-sm
            leading-relaxed
          "
        >
          {message.content || message.answer}
        </div>
      </div>
    );
  }

  return (
    <div
      className="
        glass-panel
        rounded-3xl
        p-6
        shadow-xl
        transition-all
        duration-300
        hover:border-white/15
      "
    >
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <h3 className="font-medium text-sm tracking-wide text-gray-300 uppercase">
            Agentic Multi-RAG
          </h3>
        </div>

        <DatabaseBadge database={message.database} />
      </div>

      {/* Renders tables natively using our smart parsing block */}
      <div className="text-[15px]">
        {renderContent(message.answer)}
      </div>

      <SourceList sources={message.sources} />
    </div>
  );
};

export default ChatMessage;