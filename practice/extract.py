import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# MESSAGE = [{"role":"user", "content":"Extract the return request from this customer email: {email}"}]
MODEL = "claude-sonnet-5-5"
MAX_TOKENS=200
SYSTEM= ""
# OUTPUT_CONFIG={"effort":"low","format":{"type":"json_schema", "schema":SCHEMA}}
SCHEMA = {
    "type":"object",
    "properties":{
        "order_id":{"type":"string"},
        "item":{"type":"string"},
        "reason":{
            "type":"string",
            "enum":["too_small", "too_big", "damaged", "other"]
        }
        },
    "required":["order_id","item", "reason"],
    "additionalProperties":False
}
EMAILS=["Hi, I want to return the blue jacket from order 1893. It arrived last week but it is too small. ALex",
        "Hello, the shoes I got are damaged. Please tell me how to send them back.  Thanks, Sam"]

def extract(email):
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        output_config={"effort":"low",
                       "format":
                           {"type":"json_schema", 
                            "schema":SCHEMA}},
        system=SYSTEM,
        messages=[{"role":"user", "content":f"Extract the return request from this customer email: {email}"}],
        ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        response=stream.get_final_message().content
        # print(response)
        return response
    
for email in EMAILS:
    extract(email)
    print("\n===============================")
    # response = json.loads(extract(email.co), indent=2)