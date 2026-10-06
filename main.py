from workflow_router import WorkflowRouter
from workflow_engine import WorkflowEngine


EXCEL_PATH = "data/workflows.xlsx"


def main():

    print("=" * 60)
    print("AI AGENT WORKFLOW")
    print("=" * 60)

    user_request = input("\nEnter your request: ")

    router = WorkflowRouter(EXCEL_PATH)

    workflow = router.route(user_request)

    if workflow is None:
        print("\nNo suitable workflow found.")
        return

    print("\nWorkflow Selected:")
    print(f"ID: {workflow['workflow_id']}")
    print(f"Name: {workflow['workflow_name']}")

    engine = WorkflowEngine()

    result = engine.execute(workflow, user_request)

    print("\nExecution Result:")
    print(result)


if __name__ == "__main__":
    main()