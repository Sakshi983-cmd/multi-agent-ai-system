# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1M-U0OwwIiLSAzMJIihr00ceVOon53P_f
"""

import datetime

# Memory share kia
shared_memory = []

def classify_format(input_text):
    text = input_text.lower()
    if input_text.strip().startswith('{') and input_text.strip().endswith('}'):
        return "JSON"
    elif "@" in input_text and ("\n" in input_text or "\r\n" in input_text):
        return "Email"
    else:
        return "Plain Text"

def classify_intent(text):
    text = text.lower()
    intent_keywords = {
        "Invoice": ["invoice", "bill", "payment due", "amount due", "payment"],
        "Complaint": ["complaint", "issue", "problem", "not working", "failure", "error", "bad service"],
        "RFQ": ["rfq", "request for quote", "quote", "pricing", "price", "quotation"],
        "Regulation": ["regulation", "policy", "compliance", "law", "rule", "guideline"],
        "Order": ["order", "purchase", "buy", "shipment", "delivery"],
        "Support": ["support", "help", "assist", "technical assistance", "customer service"],
    }
    for intent, keywords in intent_keywords.items():
        for kw in keywords:
            if kw in text:
                return intent
    return "Unknown"

def json_agent(json_payload):
    # placeholder: extract/reformat
    return {"status": "Processed JSON Agent", "details": json_payload}

def email_agent(email_text):
    # extract sender, urgency etc.
    sender = "unknown_sender@example.com"  # example
    urgency = "normal"  # example
    return {"status": "Processed Email Agent", "sender": sender, "urgency": urgency}

def plain_text_agent(text):
    #  simple processing
    return {"status": "Processed Plain Text Agent"}

def classifier_agent(input_text):
    fmt = classify_format(input_text)
    intent = classify_intent(input_text)

    # Routing based on format
    if fmt == "JSON":
        result = json_agent(input_text)
    elif fmt == "Email":
        result = email_agent(input_text)
    else:
        result = plain_text_agent(input_text)

    # share memory se login krenge
    log_entry = {
        "Source": fmt,
        "Intent": intent,
        "Time": datetime.datetime.now().isoformat(),
        "Extracted": result,
    }
    shared_memory.append(log_entry)

    return log_entry

if __name__ == "__main__":
    # Sample inputs to test
    sample_email = """From: user@example.com
Subject: Request for Quote

Hello, I would like to request a quote for 100 units of product X."""

    sample_json = '{"order_id": "12345", "amount": 2500, "status": "pending"}'

    sample_text = "I have an issue with my recent payment invoice."

    print(classifier_agent(sample_email))
    print(classifier_agent(sample_json))
    print(classifier_agent(sample_text))
