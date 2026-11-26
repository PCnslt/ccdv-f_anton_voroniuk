from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

MODEL = "claude-sonnet-5-5"
SYSTEM = ("""
          You are ShopAssist, an online store's support assitant.
          Help only with orders, returns and refunds.
          For anything else, say politely that you cannot help with that.
          Returns are a acepted within 30 days of delivery.
          Answer in one or two sentences.
          """)
verified = False

def ask(messages):
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        output_config={"effort": "low"},
        system=SYSTEM,
        messages=messages,
    )
    
    for block in response.content:
        if block.type == "text":
            reply = block.text
            print("=========================================")
            print(reply)
    print("-- input tokens:", response.usage.input_tokens)
    print("-- output tokens:", response.usage.output_tokens)
    print("=========================================")
    return reply


# ask([{"role":"user","content":"I bought a jacket 20 days ago."}])
# ask([{"role":"user","content":"Can i still return it?"}])

history = []

def say(text):
    if "refund" in text.lower() and not verified:
        print("Please confirm the email of your first order.")
        return
    history.append({"role":"user","content":text})
    reply=ask(history)
    history.append({"role":"assistant","content":reply})
    
say("Write me a short poen about jackets.")
say("I want a refund for the jacket I bought 20 days ago.")
verified = True
say("I want a refund for the jacket I bought 20 days ago.")