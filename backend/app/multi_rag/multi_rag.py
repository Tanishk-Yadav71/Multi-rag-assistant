import os
import sys
try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
except NameError:
    pass

from agent.retrieval_agent import choose_tool


def ask_question(query: str) -> dict:
    """Invokes the agentic routing layer to answer the query."""
    try:
        return choose_tool(query)
    except Exception as e:
        return {
            "answer": f"An unexpected processing error occurred: {str(e)}",
            "database": "None (Pipeline Error)",
            "sources": []
        }


if __name__ == "__main__":
    print("--- Agentic Multi-RAG CLI Initialized ---")
    
    while True:
        try:
            query = input("\nAsk a question (or type 'exit'): ").strip()
            
            if not query:
                continue

            if query.lower() in ("exit", "quit"):
                print("Exiting pipeline runner. Goodbye!")
                break

            result = ask_question(query)

            database_used = result.get("database", "Unknown")
            answer = result.get("answer", "No answer generated.")
            sources = result.get("sources", [])

            print(f"\n[Database Used]: {database_used}")
            print(f"[Answer]:\n{answer}")

            if sources:
                print("\n[Sources]:")
                for source in sources:
                    print(f" - {source}")
                    
        except KeyboardInterrupt:
            # Catch Ctrl+C gracefully
            print("\nExiting pipeline runner via interrupt.")
            break