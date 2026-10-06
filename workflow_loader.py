import pandas as pd
from pathlib import Path


class WorkflowLoader:
    def __init__(self, excel_path):
        self.excel_path = Path(excel_path)
        self.workflows = {}

    def load(self):
        df = pd.read_excel(self.excel_path, sheet_name="Workflows")

        for _, row in df.iterrows():
            workflow_id = row["Workflow_ID"]

            self.workflows[workflow_id] = {
                "workflow_id": workflow_id,
                "workflow_name": row["Workflow_Name"],
                "trigger": row["Trigger"],
                "inputs": row["Inputs"],
                "steps": row["Steps"],
                "decision_logic": row["Decision_Logic"],
                "tools_required": row["Tools_Required"],
                "expected_output": row["Expected_Output"],
            }

        return self.workflows

    def get_workflow(self, workflow_id):
        return self.workflows.get(workflow_id)


if __name__ == "__main__":
    loader = WorkflowLoader("data/workflows.xlsx")

    workflows = loader.load()

    print(f"Loaded {len(workflows)} workflows")

    for workflow_id, workflow in workflows.items():
        print(f"{workflow_id}: {workflow['workflow_name']}")