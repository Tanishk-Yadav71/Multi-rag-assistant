const colors = {
  papers: "bg-purple-500/20 text-purple-300",
  docs: "bg-green-500/20 text-green-300",
  notes: "bg-yellow-500/20 text-yellow-300",
  comparison_mode: "bg-pink-500/20 text-pink-300",
  literature_review_mode: "bg-cyan-500/20 text-cyan-300",
  web_research_mode: "bg-red-500/20 text-red-300",
  reflection_research_mode: "bg-red-500/20 text-red-300",
};

const DatabaseBadge = ({ database }) => {
  return (
    <span
      className={`
        px-3 py-1 rounded-full text-xs border
        ${colors[database] ||
          "bg-blue-500/20 text-blue-300"}
      `}
    >
      {database}
    </span>
  );
};

export default DatabaseBadge;