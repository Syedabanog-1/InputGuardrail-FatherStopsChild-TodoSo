import rich
import asyncio
from pydantic import BaseModel
from connection import config
from agents import (
    Agent, Runner, trace, input_guardrail,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered
)

# Output model for father's inspection
class FatherResponse(BaseModel):
    reply: str
    isBelow26: bool

# Sub agent: Child controlling the AC
ac_child = Agent(
    name="AC Child",
    instructions="""
        You are an obedient child controlling the AC.
        If asked to set temperature below 26°C, respond clearly that it's below 26°C and set 'isBelow26' to true.
        Otherwise, say it's okay and set 'isBelow26' to false.
    """,
    output_type=FatherResponse
)

# Guardrail function: Father's rule check
@input_guardrail
async def father_guardrail(ctx, agent, input):
    result = await Runner.run(ac_child, input, run_config=config)
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.reply,
        tripwire_triggered=result.final_output.isBelow26
    )
# Main agent: Father
father_agent = Agent(
    name="Father",
    instructions="You are a caring father. Do not allow AC temperature below 26°C.",
    input_guardrails=[father_guardrail]
)
# Main execution
async def main():
    with trace("FatherStopsChild"):
        try:
            result = await Runner.run(father_agent, "Set the AC to 23°C please", run_config=config)
            print(" Father approves: Temperature is acceptable.")
        except InputGuardrailTripwireTriggered:
            print(" Father says: Don't set AC below 26°C!")

if __name__ == "__main__":
    asyncio.run(main())
