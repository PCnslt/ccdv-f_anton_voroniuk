import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()



MODEL="claude-sonnet-5-5"
MAX_TOKENS=100
SYSTEM="""
You are ShopAssist, an online store's support assistant.
Returns are accepted within 30 days of delivery.
Answer in one or two sentences.
"""
MESSAGES=[{"role":"user","content":"Can I still return the jacket from order 1893"}]
ORDERS = {
    "1893":{
        "item":"jacket",
        "status":"delivered",
        "delivered_days_ago":20
    }
}

TOOLS=[{
    "name":"lookup_order",
    "description":"""
                    Look up an order by its ID. Returns the 
                    item, the status and how many days ago
                    it was delivered.
                 """,
    "input_schema":{
        "type":"object",
        "properties":{
            "order_id":{
                "type":"string",
                "description": "The order ID, like 4 digit integer"
            }
        },
        "required":["order_id"]
    }
}]

def lookup_order(order_id):
    return ORDERS.get(order_id,{"error":"order not found.."})

with client.messages.stream(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    output_config={"effort":"low"},
    system=SYSTEM,
    tools=TOOLS,
    messages=MESSAGES,
    ) as stream:
    for text in stream.text_stream:
        print(text,end="",flush=True)
    final_message=stream.get_final_message()
    print("==============================")
    print(f"1st output: {final_message.content}")
print(f"\n\nStop Reason: {final_message.stop_reason}")
print(f"Input Tokens: {final_message.usage.input_tokens}")
print(f"Output Tokens: {final_message.usage.output_tokens}")

for block in final_message.content:
    if block.type == "tool_use":
        print("Claude asks for: ", block.name, block.input)
        result = lookup_order(**block.input)
        print("our code returns:", result)
        MESSAGES.append({"role":"assistant", "content":final_message.content})
        MESSAGES.append({"role":"user", 
                         "content":[{
                                "type":"tool_result",
                                "tool_use_id":block.id,
                                "content": json.dumps(result)
        }]})
        
# print(MESSAGES)

print("Response to customer:========")
with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        output_config={"effort":"low"},
        system=SYSTEM,
        tools=TOOLS,
        messages=MESSAGES,
    ) as stream:
    for text in stream.text_stream:
        print(text,end="",flush=True)
    final_response = stream.get_final_message()
            
print(f"\n\nStop Reason: {final_response.stop_reason}")
print(f"Input Tokens: {final_response.usage.input_tokens}")
print(f"Output Tokens: {final_response.usage.output_tokens}")