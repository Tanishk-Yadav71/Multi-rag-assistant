const SourceList = ({ sources }) => {
  if (!sources?.length) return null;

  return (
    <div className="mt-8">
      <h4
        className="
        text-xs
        uppercase
        tracking-widest
        text-gray-500
        mb-4
      "
      >
        Sources
      </h4>

      <div className="space-y-3">
        {sources.map((source, index) => (
          <div
            key={index}
            className="
            bg-black/20
            border border-white/5
            rounded-xl
            px-4 py-3
            text-sm
            text-gray-300
          "
          >
            {source}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SourceList;