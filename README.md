# 🤖 Multi-Agent AI System

A sophisticated modular AI system integrating multiple intelligent agents for contextual retrieval, summarization, and task coordination. Built with LangChain, FastAPI, MLflow, and deployed on Azure cloud infrastructure.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.0.346-orange.svg)
![Azure](https://img.shields.io/badge/Azure-Cloud-blue.svg)

## 🚀 Features

### Core Capabilities
- **Multi-Agent Architecture**: Specialized agents for different document types and intents
- **Intelligent Routing**: Automatic format detection and intent classification
- **Contextual Processing**: Advanced text processing with LangChain LLM integration
- **Real-time Processing**: FastAPI-based REST API with background task handling
- **Memory Management**: Shared memory system for conversation context

### Supported Document Types
- 📧 **Email Processing**: Extract sender, subject, urgency, and entities
- 📊 **JSON Processing**: Structured data extraction and validation
- 📝 **Plain Text**: Summarization and content analysis
- 🔍 **Intent Classification**: Automatic detection of user requirements

### Intelligent Agents
- **JSON Agent**: Handles structured data processing
- **Email Agent**: Email content extraction and analysis
- **Text Agent**: General text processing and summarization
- **Summarization Agent**: Advanced content summarization
- **Classifier Agent**: Smart routing and intent detection

## 🏗 System Architecture
## 🏗 System Architecture

### 🔄 End-to-End Process Flow

```mermaid
graph TD
    A[📥 Client Request] --> B[🌐 FastAPI Server]
    B --> C[🔍 Classifier Agent]
    C --> D{Format Detection}
    D -->|JSON| E[📊 JSON Agent]
    D -->|Email| F[📧 Email Agent]
    D -->|Plain Text| G[📝 Text Agent]
    D -->|Other| H[🔧 Generic Agent]
    
    E --> I[💾 Shared Memory]
    F --> I
    G --> I
    H --> I
    
    I --> J[📈 MLflow Tracking]
    I --> K[🔄 Context Manager]
    J --> L[📊 Analytics Dashboard]
    K --> M[🧠 Memory Storage]
    
    I --> N[📤 Response Aggregator]
    N --> O[📨 Client Response]
    
    style A fill:#4CAF50
    style O fill:#2196F3
    style I fill:#FF9800
