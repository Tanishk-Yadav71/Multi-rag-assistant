from fastapi import APIRouter

from app.api.schemas import QueryRequest, QueryResponse 

from app.agent.retrieval_agent import (
    choose_tool
)

router = APIRouter()


@router.post(
    "/chat",
    response_model=QueryResponse
)
def chat(
    request: QueryRequest
):

    result = choose_tool(
        request.query
    )

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
        database=result["database"]
    )