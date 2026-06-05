from typing import Dict, TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

# Initialize LLMs
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, openai_api_key=settings.OPENAI_API_KEY)
creative_llm = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=settings.OPENAI_API_KEY)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    trend_data: Dict
    content: str
    brand_approved: bool
    review_approved: bool
    engagement_score: float
    human_approved: bool
    scheduled_time: str
    published: bool

def trend_agent(state: AgentState):
    # Analyze trends
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Social Media Trend Analyst. Based on the user's input, identify 3 trending topics and 5 hashtags."),
        ("human", "{input}")
    ])
    chain = prompt | llm
    user_input = state["messages"][-1].content
    response = chain.invoke({"input": user_input})
    
    # Parse mock response
    return {"trend_data": {"analysis": response.content, "topic": "AI Trends"}}

def content_agent(state: AgentState):
    # Generate content
    trend_analysis = state.get("trend_data", {}).get("analysis", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Social Media Content Creator. Create a viral post based on this trend analysis: {trend}"),
        ("human", "Create a post for LinkedIn.")
    ])
    chain = prompt | creative_llm
    response = chain.invoke({"trend": trend_analysis})
    
    return {"content": response.content}

def brand_voice_agent(state: AgentState):
    # Check brand voice
    content = state.get("content", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Brand Guardian. Analyze the following content and ensure it aligns with our professional, innovative brand tone. Reply with 'APPROVED' or provide suggested edits."),
        ("human", "{content}")
    ])
    chain = prompt | llm
    response = chain.invoke({"content": content})
    
    is_approved = "APPROVED" in response.content.upper()
    return {"brand_approved": is_approved, "messages": [AIMessage(content=f"Brand Guardian: {response.content}")]}

def review_agent(state: AgentState):
    # Compliance and Toxicity Review
    content = state.get("content", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Compliance and Trust & Safety Reviewer. Check for toxicity, spam, and factual errors. Reply with 'PASSED' if safe."),
        ("human", "{content}")
    ])
    chain = prompt | llm
    response = chain.invoke({"content": content})
    
    is_approved = "PASSED" in response.content.upper()
    return {"review_approved": is_approved, "messages": [AIMessage(content=f"Reviewer: {response.content}")]}

def engagement_agent(state: AgentState):
    # Predict engagement
    return {"engagement_score": 8.5}

def approval_workflow_agent(state: AgentState):
    # Pause for human approval
    # In a real deployed app, LangGraph would use a checkpoint to pause here
    return {"human_approved": True}

def scheduler_agent(state: AgentState):
    return {"scheduled_time": "2026-06-06T10:00:00Z"}

def publishing_agent(state: AgentState):
    if state.get("human_approved"):
        return {"published": True}
    return {"published": False}

def analytics_agent(state: AgentState):
    return {"messages": [AIMessage(content="Analytics tracked successfully.")]}

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("trend_agent", trend_agent)
    workflow.add_node("content_agent", content_agent)
    workflow.add_node("brand_voice_agent", brand_voice_agent)
    workflow.add_node("review_agent", review_agent)
    workflow.add_node("engagement_agent", engagement_agent)
    workflow.add_node("approval_workflow_agent", approval_workflow_agent)
    workflow.add_node("scheduler_agent", scheduler_agent)
    workflow.add_node("publishing_agent", publishing_agent)
    workflow.add_node("analytics_agent", analytics_agent)
    
    workflow.set_entry_point("trend_agent")
    workflow.add_edge("trend_agent", "content_agent")
    workflow.add_edge("content_agent", "brand_voice_agent")
    workflow.add_edge("brand_voice_agent", "review_agent")
    workflow.add_edge("review_agent", "engagement_agent")
    workflow.add_edge("engagement_agent", "approval_workflow_agent")
    workflow.add_edge("approval_workflow_agent", "scheduler_agent")
    workflow.add_edge("scheduler_agent", "publishing_agent")
    workflow.add_edge("publishing_agent", "analytics_agent")
    workflow.add_edge("analytics_agent", END)
    
    return workflow.compile()

agent_graph = build_graph()
