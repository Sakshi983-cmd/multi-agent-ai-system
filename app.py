# -*- coding: utf-8 -*-
"""app.py - Enhanced Multi-Agent AI System"""

import os
import datetime
import json
from typing import Dict, List, Any

# LangChain imports
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI

# FastAPI imports
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

# MLflow imports
import mlflow

# Configuration
class Config:
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

# Initialize MLflow
mlflow.set_tracking_uri(Config.MLFLOW_TRACKING_URI)
mlflow.set_experiment("multi-agent-ai-system")

# Initialize FastAPI
app = FastAPI(title="Multi-Agent AI System", version="1.0.0")

# Enhanced shared memory
class SharedMemory:
    def __init__(self):
        self.memory = []
        self.conversation_memory = ConversationBufferMemory()
    
    def add_entry(self, entry: Dict[str, Any]):
        entry["timestamp"] = datetime.datetime.now().isoformat()
        self.memory.append(entry)
        
        # MLflow tracking
        with mlflow.start_span():
            mlflow.log_metric("memory_entries", len(self.memory))

shared_memory = SharedMemory()

# LangChain LLM initialization
llm = AzureChatOpenAI(
    deployment_name="gpt-4",
    openai_api_key=Config.AZURE_OPENAI_API_KEY,
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
    temperature=0.1,
    max_tokens=2000
)

# Enhanced Classification
def classify_format_enhanced(input_text: str) -> str:
    text = input_text.strip()
    
    if text.startswith('{') and text.endswith('}'):
        return "JSON"
    elif '@' in text and any(keyword in text.lower() for keyword in ['subject:', 'from:', 'to:', 'cc:']):
        return "Email"
    elif text.startswith('<') and text.endswith('>'):
        return "XML"
    else:
        return "Plain Text"

def classify_intent_enhanced(text: str) -> str:
    text_lower = text.lower()
    
    intent_mapping = {
        "Invoice": ["invoice", "bill", "payment due", "amount due"],
        "Complaint": ["complaint", "issue", "problem", "not working"],
        "RFQ": ["rfq", "request for quote", "quote", "pricing"],
        "Regulation": ["regulation", "policy", "compliance", "law"],
        "Order": ["order", "purchase", "buy", "shipment"],
        "Support": ["support", "help", "assist", "technical"],
        "Summarization": ["summarize", "summary", "brief", "tl;dr"],
        "Data Extraction": ["extract", "parse", "data from", "information"]
    }
    
    for intent, keywords in intent_mapping.items():
        if any(keyword in text_lower for keyword in keywords):
            return intent
    
    return "Unknown"

# Enhanced Agents
class JSONAgent:
    def process(self, json_text: str) -> Dict[str, Any]:
        try:
            json_data = json.loads(json_text)
            return {
                "status": "Processed by JSON Agent",
                "extracted_data": json_data,
                "data_type": "structured",
                "confidence": 0.95
            }
        except:
            return {"status": "Error", "message": "Invalid JSON"}

class EmailAgent:
    def process(self, email_text: str) -> Dict[str, Any]:
        lines = email_text.split('\n')
        sender = "unknown"
        subject = "No Subject"
        
        for line in lines:
            if line.lower().startswith('from:'):
                sender = line.split(':', 1)[1].strip()
            elif line.lower().startswith('subject:'):
                subject = line.split(':', 1)[1].strip()
        
        return {
            "status": "Processed by Email Agent",
            "sender": sender,
            "subject": subject,
            "urgency": "normal",
            "entities": ["email"]
        }

class PlainTextAgent:
    def __init__(self):
        self.llm = llm
    
    def process(self, text: str) -> Dict[str, Any]:
        summary_prompt = PromptTemplate(
            input_variables=["text"],
            template="Summarize this text in 2-3 sentences: {text}"
        )
        
        summary_chain = LLMChain(llm=self.llm, prompt=summary_prompt)
        summary = summary_chain.run(text=text)
        
        return {
            "status": "Processed by Text Agent",
            "summary": summary,
            "length": len(text),
            "processed_chars": len(text)
        }

class SummarizationAgent:
    def __init__(self):
        self.llm = llm
    
    def process(self, text: str) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Create a concise summary of this text: {text}"
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        summary = chain.run(text=text)
        
        return {
            "status": "Processed by Summarization Agent",
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary)
        }

# Agent Coordinator
class AgentCoordinator:
    def __init__(self):
        self.json_agent = JSONAgent()
        self.email_agent = EmailAgent()
        self.text_agent = PlainTextAgent()
        self.summary_agent = SummarizationAgent()
    
    def route_agent(self, input_text: str, format_type: str, intent: str) -> Dict[str, Any]:
        # Route based on format first
        if format_type == "JSON":
            return self.json_agent.process(input_text)
        elif format_type == "Email":
            return self.email_agent.process(input_text)
        elif intent == "Summarization":
            return self.summary_agent.process(input_text)
        else:
            return self.text_agent.process(input_text)

# Pydantic Models
class ProcessRequest(BaseModel):
    text: str
    user_id: str = "default"
    priority: str = "normal"

class ProcessResponse(BaseModel):
    status: str
    format: str
    intent: str
    result: Dict[str, Any]
    timestamp: str
    processing_time: float

# Initialize coordinator
coordinator = AgentCoordinator()

@app.post("/process", response_model=ProcessResponse)
async def process_text(request: ProcessRequest, background_tasks: BackgroundTasks):
    start_time = datetime.datetime.now()
    
    # Classify input
    format_type = classify_format_enhanced(request.text)
    intent = classify_intent_enhanced(request.text)
    
    # Route to appropriate agent
    result = coordinator.route_agent(request.text, format_type, intent)
    
    # Calculate processing time
    processing_time = (datetime.datetime.now() - start_time).total_seconds()
    
    # Log to shared memory
    log_entry = {
        "user_id": request.user_id,
        "format": format_type,
        "intent": intent,
        "result": result,
        "processing_time": processing_time
    }
    
    background_tasks.add_task(shared_memory.add_entry, log_entry)
    
    # MLflow logging
    with mlflow.start_span():
        mlflow.log_metric("processing_time_seconds", processing_time)
        mlflow.log_param("format_type", format_type)
        mlflow.log_param("intent_type", intent)
    
    return ProcessResponse(
        status="success",
        format=format_type,
        intent=intent,
        result=result,
        timestamp=datetime.datetime.now().isoformat(),
        processing_time=processing_time
    )

@app.get("/memory")
async def get_memory(limit: int = 10):
    return {
        "total_entries": len(shared_memory.memory),
        "recent_entries": shared_memory.memory[-limit:] if shared_memory.memory else []
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "memory_entries": len(shared_memory.memory)
    }

# Main execution
if __name__ == "__main__":
    import uvicorn
    
    # Test the enhanced system
    sample_email = """From: user@example.com
Subject: Request for Quote

Hello, I would like to request a quote for 100 units of product X."""

    sample_json = '{"order_id": "12345", "amount": 2500, "status": "pending"}'

    sample_text = "Please summarize this document about AI advancements."

    # Test cases
    test_cases = [sample_email, sample_json, sample_text]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        format_type = classify_format_enhanced(test_case)
        intent = classify_intent_enhanced(test_case)
        result = coordinator.route_agent(test_case, format_type, intent)
        
        print(f"Format: {format_type}")
        print(f"Intent: {intent}")
        print(f"Result: {result}")
    
    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
