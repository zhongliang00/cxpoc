from parse_messages import parse_messages
import json


tools = [
  {
      "type": "function",
      "function": {
          "name": "has_late_payments",
          "description": "Check if the user has late payments",
          "parameters": {
              "type": "object",
              "properties": {
                  "email": {
                      "type": "string",
                      "description": "The customer's email address",
                  },
              },
              "required": ["email"],
              "additionalProperties": False,
          },
      }
  },
  {
      "type": "function",
      "function": {
          "name": "reply_customer",
          "description": "Respond to the customer or ask questions",
          "parameters": {
              "type": "object",
              "properties": {
                  "text": {
                      "type": "string",
                      "description": "The text to respond with",
                  },
              },
              "required": ["text"],
              "additionalProperties": False,
          },
      }
  },
  {
      "type": "function",
      "function": {
          "name": "lookup_order_id",
          "description": "Get's information about the provided order id",
          "parameters": {
              "type": "object",
              "properties": {
                  "order_id": {
                      "type": "string",
                      "description": "The order id",
                  },
              },
              "required": ["order_id"],
              "additionalProperties": False,
          },
      }
  },
  {
      "type": "function",
      "function": {
          "name": "query_faq",
          "description": "Get information from FAQs",
          "parameters": {
              "type": "object",
              "properties": {
                  "question": {
                      "type": "string",
                      "description": "What is your question?",
                  },
              },
              "required": ["question"],
              "additionalProperties": False,
          },
      }
  },
  {
      "type": "function",
      "function": {
          "name": "exit",
          "description": "",
          "parameters": {
              "type": "object",
              "properties": {
                  "is_error": {
                      "type": "boolean",
                      "description": "Is exiting due to error"
                  },
                  "reason": {
                      "type": "string",
                      "description": "Exit reason",
                  },
              },
              "required": ["is_error"],
              "additionalProperties": False,
          },
      }
  },
]

def mock_internal_call_tool(name: str, kwargs: dict):
    args = list(kwargs.values())[0]
    result = ''
    match name:
        case "has_late_payments":
            result = f":sys: has_late_payments({args}) returned '{False}'"
        case "reply_customer":
            result = f":ai: {args}"
        case "lookup_order_id":
            result = f":sys: lookup_order_id({args}) returned 'REJECTED: HIGH_RISK_POTENTIAL_FRAUD'"
        case "query_faq":
            result = f":sys: Most relevant FAQ: Order ID can be found in the user tab, scroll down and look for order, then click the relevant order and see the id"
        case "exit":
            print(f"exiting! {kwargs}")
    return parse_messages(result)

def call_tool(message_history: list, function):
    name = function.name
    kwargs = json.loads(function.arguments)
    message_history.extend(mock_internal_call_tool(name, kwargs))
