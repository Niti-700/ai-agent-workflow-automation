# AI Agent Workflow Automation

An AI-powered workflow automation system that reads business workflows from Excel, understands a user's request, selects the appropriate workflow using an LLM, executes the workflow through a reusable tool, handles conditions and errors, and returns the final result.

## Architecture

```text
User Request
     ↓
AI Agent (Gemini)
     ↓
Identify Workflow
     ↓
Excel Workflow Definition
     ↓
Tool Calling
     ↓
Workflow Engine
     ↓
CSV / Excel / Calculation / Validation Tools
     ↓
Conditions & Error Handling
     ↓
Final Result
```

## Key Features

* Reads business workflows dynamically from Excel.
* Uses Gemini LLM for natural-language workflow identification.
* Uses function/tool calling to execute the selected workflow.
* Uses a reusable workflow execution architecture.
* Displays:

  * Selected workflow
  * Workflow steps
  * Tool call
  * Execution result
  * Final agent response
* Supports condition and error handling.
* Uses CSV/Excel files as business data sources.
* Simulates business tools/APIs where real APIs are unavailable.
* Adding a new workflow to the Excel source does not require changes to the AI agent or routing logic.

## Project Structure

```text
AI Agent Workflow/
│
├── data/
│   ├── workflows.xlsx
│   ├── inventory.csv
│   ├── product_prices.csv
│   ├── vendor_prices.csv
│   ├── vendor_products.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── keywords.csv
│   ├── employees.csv
│   ├── tasks.csv
│   └── execution_logs.csv
│
├── tools/
│   ├── csv_tool.py
│   ├── calculator.py
│   ├── excel_tool.py
│   └── validation_tool.py
│
├── workflow_loader.py
├── workflow_router.py
├── workflow_engine.py
├── agent.py
├── main.py
├── test_workflows.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Workflows

The Excel file contains 10 business workflows:

| ID    | Workflow                      |
| ----- | ----------------------------- |
| WF001 | Inventory Restock Check       |
| WF002 | Product Price Validation      |
| WF003 | Vendor File Processing        |
| WF004 | Product Description Generator |
| WF005 | Customer Order Status         |
| WF006 | Duplicate Product Detection   |
| WF007 | Marketing Campaign Brief      |
| WF008 | SEO Keyword Classification    |
| WF009 | Employee Task Assignment      |
| WF010 | Workflow Performance Report   |

The workflows are stored in:

```text
data/workflows.xlsx
```

The Excel structure contains:

* Workflow ID
* Workflow Name
* Trigger
* Inputs
* Steps
* Decision Logic
* Tools Required
* Expected Output

## How It Works

### 1. User Request

The user provides a natural-language request such as:

```text
Which products need restocking?
```

### 2. Workflow Loading

`workflow_loader.py` reads the workflows from Excel.

The workflow definitions are passed to the AI agent dynamically.

### 3. AI Workflow Identification

Gemini analyzes the user's request and selects the most appropriate workflow.

Example:

```text
User Request:
Which products need restocking?

Selected Workflow:
WF001 - Inventory Restock Check
```

### 4. Tool Calling

The AI agent calls the reusable:

```text
execute_workflow
```

tool with the selected workflow ID and original user request.

### 5. Workflow Execution

The workflow engine executes the required business logic and uses the required data/tools.

### 6. Conditions and Errors

The system handles conditions such as:

* Order not found
* Missing required columns
* Invalid vendor records
* Price differences
* Duplicate products
* Workflow failures

### 7. Final Response

The tool result is sent back to Gemini, which produces the final user-friendly response.

## Example

### Request

```text
Which products need restocking?
```

### Agent Selection

```text
Workflow: WF001
Name: Inventory Restock Check
```

### Execution

The system reads:

```text
data/inventory.csv
```

and identifies products below their minimum stock level.

### Result

```text
Laptop Stand → Reorder 5
Keyboard → Reorder 5
Webcam → Reorder 3
```

## Error Handling Example

Request:

```text
Where is order ORD-1001?
```

The order does not exist in the provided dataset.

The workflow returns:

```text
Order ORD-1001 not found.
```

The system handles the condition without crashing and returns the result to the AI agent.

## Technology Stack

* Python
* Gemini LLM
* Gemini Function / Tool Calling
* Pandas
* OpenPyXL
* Python-dotenv
* Excel
* CSV
* VS Code

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "AI Agent Workflow"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit `.env` to GitHub.

A sample configuration is provided in:

```text
.env.example
```

## Run the AI Agent

```bash
python agent.py
```

Example:

```text
Enter your request: Which products need restocking?
```

The system will:

1. Analyze the request using Gemini.
2. Select the appropriate workflow.
3. Call the workflow execution tool.
4. Execute the workflow.
5. Return the final result.

## Run Tests

```bash
python test_workflows.py
```

The test suite validates:

* Excel workflow loading
* Workflow routing
* Workflow execution
* All 10 workflows

## Scalability

The AI agent is not implemented as 10 separate chatbots.

All workflows are loaded dynamically from:

```text
data/workflows.xlsx
```

The AI agent uses one reusable workflow execution tool:

```text
execute_workflow
```

Therefore, adding a new workflow does not require changes to the AI agent or workflow-selection prompt.

For workflows requiring unique business logic, a corresponding workflow-engine handler can be added while keeping the agent architecture unchanged.

## Design Decisions

### Excel as Workflow Source

Excel was selected because the assessment requires business workflows to be maintained in an Excel file. It also allows workflow definitions to be updated without modifying the AI agent.

### Gemini LLM

Gemini is used for natural-language understanding and workflow selection.

### Tool Calling

Function/tool calling provides a clear separation between:

```text
AI Decision
```

and:

```text
Actual Workflow Execution
```

The AI decides which workflow should execute, while Python performs the actual business operation.

### Deterministic Workflow Execution

Business logic is executed in Python rather than allowing the LLM to directly modify business data. This makes workflow execution predictable and easier to test and validate.

## Security

API keys are stored in environment variables.

The following files are excluded from Git:

```text
.env
.venv/
__pycache__/
*.pyc
```

## Assessment Demonstration

The Loom demonstration covers:

1. Project architecture
2. Excel workflow source
3. Workflow loading
4. AI workflow identification
5. Gemini tool calling
6. Workflow execution
7. Conditions and error handling
8. Successful workflow examples
9. Adding a new workflow
10. Technical design decisions

## Author

Niti Bhatia

AI / AI Automation Developer Assessment Project
