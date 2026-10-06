import os
import json

from dotenv import load_dotenv
from google import genai

from workflow_loader import WorkflowLoader
from workflow_engine import WorkflowEngine


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

EXCEL_PATH = "data/workflows.xlsx"


def load_workflows():
    loader = WorkflowLoader(EXCEL_PATH)
    return loader.load()


def execute_workflow(workflow_id, user_request):
    """
    Tool executed by the AI agent after it selects a workflow.
    """

    workflows = load_workflows()
    workflow = workflows.get(workflow_id)

    if workflow is None:
        return {
            "status": "error",
            "message": f"Workflow {workflow_id} not found."
        }

    print("\n" + "=" * 60)
    print("TOOL CALL")
    print("=" * 60)
    print("Tool: execute_workflow")
    print(f"Workflow ID: {workflow_id}")
    print(f"Workflow Name: {workflow['workflow_name']}")

    print("\nSteps Executed:")
    print("-" * 60)

    steps = str(workflow["steps"])

    for step in steps.split("\n"):
        if step.strip():
            print(f"✓ {step.strip()}")

    print("\nExecuting workflow logic...")

    engine = WorkflowEngine()

    result = engine.execute(workflow, user_request)

    return {
        "workflow_id": workflow_id,
        "workflow_name": workflow["workflow_name"],
        "execution_result": result
    }


def run_agent(user_request):

    workflows = load_workflows()

    workflow_context = []

    for workflow_id, workflow in workflows.items():

        workflow_context.append({
            "workflow_id": workflow_id,
            "workflow_name": workflow["workflow_name"],
            "trigger": workflow["trigger"],
            "inputs": workflow["inputs"],
            "steps": workflow["steps"],
            "decision_logic": workflow["decision_logic"],
            "tools_required": workflow["tools_required"],
            "expected_output": workflow["expected_output"]
        })

    # Tool declaration given to Gemini
    execute_workflow_tool = {
        "type": "function",
        "name": "execute_workflow",
        "description": (
            "Execute the selected business workflow using the "
            "workflow engine. Use this after identifying the "
            "best workflow for the user's request."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "workflow_id": {
                    "type": "string",
                    "description": "The selected workflow ID, such as WF001."
                },
                "user_request": {
                    "type": "string",
                    "description": "The original user request."
                }
            },
            "required": [
                "workflow_id",
                "user_request"
            ]
        }
    }

    prompt = f"""
You are an AI workflow automation agent.

Your job is to understand the user's request, identify the
best workflow from the Excel-defined workflows, and then
call the execute_workflow tool.

Available workflows:

{json.dumps(workflow_context, indent=2)}

User request:

{user_request}

Choose the single most appropriate workflow.

Then call execute_workflow with:
- workflow_id
- user_request
"""

    print("\nAI Agent is analyzing the request...")

    # First interaction: Gemini decides which tool to call
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=prompt,
        tools=[execute_workflow_tool]
    )

    function_call = None

    for step in interaction.steps:

        if step.type == "function_call":
            function_call = step
            break

    if function_call is None:

        print("\nAgent did not call a workflow tool.")

        if interaction.output_text:
            print(interaction.output_text)

        return

    print("\n" + "=" * 60)
    print("AI AGENT SELECTED TOOL")
    print("=" * 60)

    print(f"Tool: {function_call.name}")
    print(f"Arguments: {function_call.arguments}")

    arguments = function_call.arguments

    workflow_id = arguments["workflow_id"]
    original_request = arguments["user_request"]

    # Execute the tool locally
    tool_result = execute_workflow(
        workflow_id,
        original_request
    )

    # Send tool result back to Gemini
    final_interaction = client.interactions.create(
        model="gemini-3.8-flash",
        previous_interaction_id=interaction.id,
        input=[
            {
                "type": "function_result",
                "name": function_call.name,
                "call_id": function_call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            tool_result,
                            default=str
                        )
                    }
                ]
            }
        ]
    )

    print("\n" + "=" * 60)
    print("FINAL AGENT RESPONSE")
    print("=" * 60)

    print(final_interaction.output_text)


if __name__ == "__main__":

    print("=" * 60)
    print("AI AGENT WORKFLOW AUTOMATION")
    print("=" * 60)

    user_request = input("\nEnter your request: ")

    try:
        run_agent(user_request)

    except Exception as e:

        print("\nAgent Error:")
        print(type(e).__name__)
        print(e)