from workflow_loader import WorkflowLoader


class WorkflowRouter:

    def __init__(self, excel_path):
        self.loader = WorkflowLoader(excel_path)
        self.workflows = self.loader.load()

    def route(self, user_request):

        request = user_request.lower()

        keyword_mapping = {
            "WF001": ["restock", "restocking", "low stock", "inventory"],
            "WF002": ["price", "vendor price", "price difference"],
            "WF003": ["vendor file", "vendor spreadsheet", "process spreadsheet", "clean file"],
            "WF004": ["product description", "seo content", "product content", "seo title"],
            "WF005": ["order status", "where is my order", "where is order", "order", "shipment", "tracking"],
            "WF006": ["duplicate", "duplicates", "duplicate products"],
            "WF007": ["campaign brief", "marketing campaign", "campaign"],
            "WF008": ["keyword", "keywords", "search intent"],
            "WF009": ["assign task", "employee", "developer", "task assignment"],
            "WF010": [
    "performance report",
    "failing workflows",
    "which workflows are failing",
    "workflows are failing",
    "failure rate",
    "execution time",
    "workflow performance",
    "performance"
]
        }

        for workflow_id, keywords in keyword_mapping.items():

            for keyword in keywords:

                if keyword in request:
                    return self.workflows[workflow_id]

        return None


if __name__ == "__main__":

    router = WorkflowRouter("data/workflows.xlsx")

    test_request = "Which products need restocking?"

    workflow = router.route(test_request)

    if workflow:

        print("Selected Workflow:")
        print(workflow["workflow_id"])
        print(workflow["workflow_name"])

    else:

        print("No matching workflow found.")