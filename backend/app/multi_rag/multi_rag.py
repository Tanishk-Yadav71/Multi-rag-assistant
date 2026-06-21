import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from agent.retrieval_agent import (
    choose_tool
)


def ask_question(query):

    result = choose_tool(
        query
    )

    return result


if __name__ == "__main__":

    while True:

        query = input(
            "\nAsk a question (or type 'exit'): "
        )

        if query.lower() == "exit":
            break

        result = ask_question(
            query
        )
        print(type(result))
        print(result)
        print("\nDatabase Used:")
        print(
            result["database"]
        )

        print("\nAnswer:")
        print(
            result["answer"]
        )

        if result["sources"]:

            print("\nSources:")

            for source in result["sources"]:

                print(
                    "-",
                    source
                )