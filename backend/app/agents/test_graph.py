import asyncio
from app.agents.graph import agent_graph, AgentState
from langchain_core.messages import HumanMessage

async def main():
    print("Starting AgentSphere Workflow...")
    initial_state = AgentState(
        messages=[HumanMessage(content="Start weekly campaign")],
        trend_data={},
        content="",
        brand_approved=False,
        review_approved=False,
        engagement_score=0.0,
        human_approved=False,
        scheduled_time="",
        published=False
    )
    
    async for output in agent_graph.astream(initial_state):
        for node_name, state in output.items():
            print(f"--- {node_name.upper()} ---")
            if "content" in state:
                print(f"Content: {state['content']}")
            if "engagement_score" in state:
                print(f"Engagement Score: {state['engagement_score']}")
            print()

if __name__ == "__main__":
    asyncio.run(main())
