from workflow_loader import WorkflowLoader
from workflow_router import WorkflowRouter
from workflow_engine import WorkflowEngine


EXCEL_PATH = "data/workflows.xlsx"


def test_workflow_loader():

    loader = WorkflowLoader(EXCEL_PATH)

    workflows = loader.load()

    assert len(workflows) == 10

    print("PASS: Workflow loader loaded 10 workflows")


def test_workflow_router():

    router = WorkflowRouter(EXCEL_PATH)

    test_cases = {
        "Which products need restocking?": "WF001",
        "Check vendor product prices": "WF002",
        "Process vendor spreadsheet": "WF003",
        "Generate product description": "WF004",
        "Where is my order?": "WF005",
        "Find duplicate products": "WF006",
        "Create a marketing campaign brief": "WF007",
        "Classify SEO keywords": "WF008",
        "Assign tasks to employees": "WF009",
        "Generate workflow performance report": "WF010"
    }

    for request, expected_workflow in test_cases.items():

        workflow = router.route(request)

        assert workflow is not None

        assert workflow["workflow_id"] == expected_workflow

        print(
            f"PASS: Router -> {expected_workflow}"
        )


def test_workflow_engine():

    router = WorkflowRouter(EXCEL_PATH)

    engine = WorkflowEngine()

    test_requests = [
        "Which products need restocking?",
        "Check vendor product prices",
        "Process vendor spreadsheet",
        "Generate product description",
        "Where is my order?",
        "Find duplicate products",
        "Create a marketing campaign brief",
        "Classify SEO keywords",
        "Assign tasks to employees",
        "Generate workflow performance report"
    ]

    for request in test_requests:

        workflow = router.route(request)

        assert workflow is not None

        result = engine.execute(workflow)

        assert result is not None

        assert result["status"] in [
            "completed",
            "order_not_found"
        ]

        print(
            f"PASS: Engine -> "
            f"{workflow['workflow_id']}"
        )


if __name__ == "__main__":

    print("=" * 60)
    print("RUNNING WORKFLOW TESTS")
    print("=" * 60)

    test_workflow_loader()

    test_workflow_router()

    test_workflow_engine()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)