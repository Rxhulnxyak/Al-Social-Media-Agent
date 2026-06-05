from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.agents.graph import agent_graph, AgentState
from langchain_core.messages import HumanMessage
from typing import Optional

router = APIRouter()

class CampaignRequest(BaseModel):
    topic: str
    platform: str
    brand_tone: Optional[str] = "Professional"

@router.post("/generate")
async def generate_campaign(request: CampaignRequest, background_tasks: BackgroundTasks):
    # For a real application, we would use background tasks or websockets to stream progress
    
    initial_state = AgentState(
        messages=[HumanMessage(content=f"Create a campaign about {request.topic} for {request.platform} with a {request.brand_tone} tone.")],
        trend_data={},
        content="",
        brand_approved=False,
        review_approved=False,
        engagement_score=0.0,
        human_approved=False,
        scheduled_time="",
        published=False
    )
    
    # We will run this synchronously for demonstration purposes
    try:
        final_state = await agent_graph.ainvoke(initial_state)
        return {
            "status": "success",
            "content": final_state.get("content"),
            "engagement_score": final_state.get("engagement_score"),
            "approved": final_state.get("brand_approved") and final_state.get("review_approved")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
