import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    OpenAIChatCompletionsModel,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    set_tracing_disabled,
)
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
# --------------input types---user propmt checker-------------
class CheckJobRequest(BaseModel):
    is_illegal:bool
    reasoning: str

# input guardrails agent ----- input analyzr
input_guardrail_agent = Agent(
    name="Input Guardrail Check Agent",
    instructions="Check if the user is asking for an illegal or unethical job.",
    model=model,
    output_type=CheckJobRequest
)

# -------------Input Guardrail Function--------------
@input_guardrail
async def illegal_job_guardrail(
    # ctx,agent,input):
    ctx:RunContextWrapper[None],agent:Agent,input:str | list[TResponseInputItem] 
    )->GuardrailFunctionOutput:
    result = await Runner.run(input_guardrail_agent,input,context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_illegal
    )
    
#   output guardrails agents   
# -----------output types  agent response checker
class JobResponse(BaseModel):
    response: str

class CheckOutput(BaseModel):
    is_fake_job: bool
    reasoning: str
    
output_guardrail_agent = Agent(
    name="Output Guardrail Checker",
    instructions="Check if the response contains a fake or unethical job suggestion.",
    output_type=CheckOutput,
    model=model
)

# -------------Input Guardrail Function--------------
@output_guardrail
async def fake_job_output_guardrail(
    # ctx,agent,input):
    ctx:RunContextWrapper[None],agent:Agent,output:JobResponse 
    )->GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent,output.response,context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_fake_job,

    )

# main agent----------

job_finder_agent = Agent(
    name="Job Finder Agent",
    instructions="You are a helpful assistant that finds suitable jobs based on user input.",
    model=model,
    input_guardrails=[illegal_job_guardrail],
    output_guardrails=[fake_job_output_guardrail],
    output_type=JobResponse
)

async def main():
    try:
      result =  await Runner.run(
          starting_agent=job_finder_agent,
          input="Show me software engineering jobs in Karachi that offer remote work.",
      )
      print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("❌ Illegal job guardrail tripped – Input blocked.")
    except OutputGuardrailTripwireTriggered:
        print("❌ Output Guardrail Tripped – Fake job response")
    
if __name__ == "__main__":
    asyncio.run(main())