from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
print("Hello World")

MODEL = "claude-sonnet-5-5"

response = client.messages.create(
    model=MODEL,
    max_tokens=300,
    output_config={"effort":"low"},
    messages=[{"role":"user",
               "content":"""A customer asks: can I return
               a jacket after 20 days? Our policy allows
               returns within 30 days. Answer the customer
               in two sentences.
               """}],
)

response_json = response.model_dump_json(indent=2, exclude_none=True)
print(response_json)

resposne_text = response.content[0].text
print(resposne_text)
print("stop_reason:", response.stop_reason)
print("usage:", response.usage.input_tokens,
      response.usage.output_tokens)