OBJECTIVE
*********

The objective of this code is to simulate a guardrail mechanism where a father agent prevents a child agent from setting the AC temperature below 26°C. If the child tries to set the AC to a temperature below this threshold, the father_guardrail is triggered, and the request is rejected.

 Execution Flow
 **************

1- Output Model Definition (FatherResponse):

A Pydantic model that defines the expected structure of the child agent’s output:

2-AC Child Agent (ac_child):

This agent receives temperature instructions and checks if it's below 26°C.

If yes, it replies accordingly and sets isBelow26 = True.

Otherwise, it sets isBelow26 = False.

3- Input Guardrail (father_guardrail):

Before the father's agent processes the user request, this guardrail is triggered.

It runs the ac_child agent with the user’s input.

If the output from the child says the temperature is below 26°C, it returns tripwire_triggered = True.

4- Father Agent (father_agent):

This is the main agent.

It has a guardrail (father_guardrail) to stop any input that violates his rule (AC < 26°C).

If the child tries to set the AC to below 26°C, the input is rejected via InputGuardrailTripwireTriggered.

5- Execution (main() function):

Uses the Runner.run() method to run the father_agent with a test input like "Set the AC to 23°C please".

If the guardrail is triggered (AC < 26°C), it prints a warning from the father.

Otherwise, it prints approval.

 Example Output Behavior
 ************************

Scenario 1: Input = "Set the AC to 23°C please"

ac_child → reply = "Setting AC to 23°C", isBelow26 = True

father_guardrail → tripwire_triggered = True

father_agent → Raises InputGuardrailTripwireTriggered

Output:

Father says: Don't set AC below 26°C!

Scenario 2: Input = "Set the AC to 28°C please"

ac_child → reply = "Setting AC to 28°C", isBelow26 = False

father_guardrail → tripwire_triggered = False

father_agent → Proceeds

Output:

Father approves: Temperature is acceptable.



https://github.com/user-attachments/assets/35480d75-2ca1-4d68-8832-321a9edd5b4b

<img width="1613" height="906" alt="ChildAgent-Generation" src="https://github.com/user-attachments/assets/bf7eb950-59c2-412a-a999-6d9e5714b192" />
<img width="1610" height="905" alt="Father-Guardrail-Generation" src="https://github.com/user-attachments/assets/7e1e6e93-8c3b-4fe9-846d-884d980449dd" />
<img width="1609" height="925" alt="Trigerred-True" src="https://github.com/user-attachments/assets/37ef4a14-f4c8-4df5-97c7-519a525f1db5" />
<img width="1612" height="904" alt="FatherStopsChild-code-output" src="https://github.com/user-attachments/assets/a3ba64ea-bbae-4856-a082-d7ef7d2ab544" />
<img width="1616" height="906" alt="FatherStopsChild-Trigerred-True" src="https://github.com/user-attachments/assets/c3a2059c-fc5b-4ba8-bd51-4c2a27119c21" />








