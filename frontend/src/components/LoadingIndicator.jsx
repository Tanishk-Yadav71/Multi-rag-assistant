const LoadingIndicator = () => {
return ( <div className="mt-8">

  <div
    className="
      bg-white/3
      backdrop-blur-xl
      border border-white/10
      rounded-3xl
      p-6
    "
  >

    <div className="flex items-center gap-4">

      <div className="flex gap-1">

        <div
          className="
            w-2 h-2
            bg-blue-400
            rounded-full
            animate-bounce
          "
        />

        <div
          className="
            w-2 h-2
            bg-blue-400
            rounded-full
            animate-bounce
            [animation-delay:0.15s]
          "
        />

        <div
          className="
            w-2 h-2
            bg-blue-400
            rounded-full
            animate-bounce
            [animation-delay:0.3s]
          "
        />

      </div>

      <span className="text-gray-400">
        Agent is researching...
      </span>

    </div>

  </div>

</div>

);
};

export default LoadingIndicator;
