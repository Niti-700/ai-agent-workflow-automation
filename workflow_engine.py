import re
from difflib import SequenceMatcher

from tools.csv_tool import read_csv

from tools.calculator import (
    calculate_reorder_quantity,
    calculate_percentage_difference
)

from tools.validation_tool import (
    validate_required_columns,
    find_missing_values
)


class WorkflowEngine:

    def execute(self, workflow, inputs=None):

        print("\n" + "=" * 60)
        print("WORKFLOW EXECUTION")
        print("=" * 60)

        workflow_id = workflow["workflow_id"]

        print(f"Workflow ID: {workflow_id}")
        print(f"Workflow: {workflow['workflow_name']}")

        # Convert user input to text
        user_request = str(inputs or "")

        # ==========================================================
        # WF001 - Inventory Restock Check
        # ==========================================================

        if workflow_id == "WF001":

            print("\nLoading inventory data...")

            df = read_csv("data/inventory.csv")

            if df is None:
                return {"status": "failed"}

            required_columns = [
                "SKU",
                "Product",
                "Current_Stock",
                "Minimum_Stock"
            ]

            missing_columns = validate_required_columns(
                df,
                required_columns
            )

            if missing_columns:
                print(f"Missing columns: {missing_columns}")
                return {"status": "failed"}

            restock_items = []

            for _, row in df.iterrows():

                if row["Current_Stock"] < row["Minimum_Stock"]:

                    reorder_quantity = calculate_reorder_quantity(
                        row["Current_Stock"],
                        row["Minimum_Stock"]
                    )

                    restock_items.append({
                        "SKU": row["SKU"],
                        "Product": row["Product"],
                        "Current Stock": row["Current_Stock"],
                        "Minimum Stock": row["Minimum_Stock"],
                        "Reorder Quantity": reorder_quantity
                    })

            print("\nRestock List:")
            print("-" * 60)

            for item in restock_items:
                print(
                    f"{item['Product']} | "
                    f"Current: {item['Current Stock']} | "
                    f"Minimum: {item['Minimum Stock']} | "
                    f"Reorder: {item['Reorder Quantity']}"
                )

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "restock_items": restock_items
            }

        # ==========================================================
        # WF002 - Product Price Validation
        # ==========================================================

        if workflow_id == "WF002":

            print("\nLoading product and vendor prices...")

            product_df = read_csv("data/product_prices.csv")
            vendor_df = read_csv("data/vendor_prices.csv")

            if product_df is None or vendor_df is None:
                return {"status": "failed"}

            merged_df = product_df.merge(
                vendor_df,
                on="SKU",
                how="inner"
            )

            results = []

            for _, row in merged_df.iterrows():

                difference = calculate_percentage_difference(
                    row["Internal_Price"],
                    row["Vendor_Price"]
                )

                status = "FLAGGED" if difference > 10 else "OK"

                results.append({
                    "SKU": row["SKU"],
                    "Product": row["Product"],
                    "Internal Price": row["Internal_Price"],
                    "Vendor Price": row["Vendor_Price"],
                    "Difference %": round(difference, 2),
                    "Status": status
                })

            print("\nPrice Validation Results:")
            print("-" * 60)

            for item in results:
                print(
                    f"{item['Product']} | "
                    f"Difference: {item['Difference %']}% | "
                    f"{item['Status']}"
                )

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "price_validation": results
            }

        # ==========================================================
        # WF003 - Vendor File Processing
        # ==========================================================

        if workflow_id == "WF003":

            print("\nProcessing vendor file...")

            df = read_csv("data/vendor_products.csv")

            if df is None:
                return {"status": "failed"}

            required_columns = [
                "SKU",
                "Product",
                "Category",
                "Price"
            ]

            missing_columns = validate_required_columns(
                df,
                required_columns
            )

            if missing_columns:
                print(f"Missing columns: {missing_columns}")
                return {"status": "failed"}

            missing_rows = find_missing_values(
                df,
                ["SKU", "Product"]
            )

            valid_df = df.dropna(
                subset=["SKU", "Product"]
            )

            invalid_rows = missing_rows.to_dict(
                orient="records"
            )

            print(f"\nTotal rows: {len(df)}")
            print(f"Valid rows: {len(valid_df)}")
            print(f"Invalid rows: {len(missing_rows)}")

            print("\nInvalid Rows:")
            for row in invalid_rows:
                print(row)

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "valid_rows": len(valid_df),
                "invalid_rows": len(missing_rows),
                "invalid_records": invalid_rows
            }

        # ==========================================================
        # WF004 - Product Description / SEO Content Generator
        # ==========================================================

        if workflow_id == "WF004":

            print("\nGenerating SEO product content...")

            # Try to extract product from request
            product = None

            known_products = [
                "wireless bluetooth headphones",
                "laptop stand",
                "wireless mouse",
                "keyboard",
                "usb cable",
                "webcam"
            ]

            request_lower = user_request.lower()

            for item in known_products:
                if item in request_lower:
                    product = item.title()
                    break

            # If product is not supplied, use a safe example
            # and explicitly record that product details were missing.
            missing_data = []

            if product is None:
                product = "Wireless Bluetooth Headphones"
                missing_data.append("specific product details")

            category = "Electronics"
            audience = "Young professionals"

            description = (
                f"{product} is a practical {category.lower()} solution "
                f"designed for {audience}. It offers a convenient option "
                f"for everyday use and is suitable for modern lifestyles."
            )

            short_description = (
                f"{product} designed for convenient everyday use."
            )

            seo_title = (
                f"{product} | Premium {category} for Everyday Use"
            )

            meta_description = (
                f"Discover {product}, a practical {category.lower()} "
                f"choice designed for everyday use by {audience}."
            )

            keywords = [
                product.lower(),
                "premium electronics",
                "everyday electronics",
                "best electronics"
            ]

            print("\nSEO Content:")
            print("-" * 60)

            print(f"Product: {product}")
            print(f"\nDescription:\n{description}")
            print(f"\nShort Description:\n{short_description}")
            print(f"\nSEO Title:\n{seo_title}")
            print(f"\nMeta Description:\n{meta_description}")
            print(f"\nKeywords: {keywords}")

            if missing_data:
                print(
                    "\nMissing information: "
                    + ", ".join(missing_data)
                )

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "description": description,
                "short_description": short_description,
                "seo_title": seo_title,
                "meta_description": meta_description,
                "keywords": keywords,
                "missing_data": missing_data
            }

        # ==========================================================
        # WF005 - Customer Order Status
        # ==========================================================

        if workflow_id == "WF005":

            print("\nSearching customer orders...")

            df = read_csv("data/orders.csv")

            if df is None:
                return {"status": "failed"}

            # Extract order ID from user request.
            order_match = re.search(
                r"\bORD[- ]?\d+\b",
                user_request,
                re.IGNORECASE
            )

            if order_match:
                order_id = order_match.group(0).upper()
                order_id = order_id.replace(" ", "")
            else:
                order_id = "ORD001"

            # Support ORD-1001 and ORD1001 formats
            result = df[
                df["Order_ID"]
                .astype(str)
                .str.upper()
                .str.replace("-", "", regex=False)
                == order_id.replace("-", "")
            ]

            if result.empty:

                print(f"Order {order_id} not found.")

                return {
                    "workflow_id": workflow_id,
                    "workflow_name": workflow["workflow_name"],
                    "status": "order_not_found",
                    "order_id": order_id,
                    "message": (
                        f"No order was found for {order_id}. "
                        "Please provide another order ID."
                    )
                }

            order = result.iloc[0]

            print("\nOrder Details:")
            print("-" * 60)

            print(f"Order ID: {order['Order_ID']}")
            print(f"Product: {order['Product']}")
            print(f"Status: {order['Status']}")
            print(f"Tracking: {order['Tracking_Number']}")

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "order_id": order["Order_ID"],
                "product": order["Product"],
                "order_status": order["Status"],
                "tracking_number": order["Tracking_Number"]
            }

        # ==========================================================
        # WF006 - Duplicate Product Detection
        # ==========================================================

        if workflow_id == "WF006":

            print("\nChecking for duplicate products...")

            df = read_csv("data/products.csv")

            if df is None:
                return {"status": "failed"}

            if "Product" not in df.columns:
                return {"status": "failed"}

            df["Normalized_Product"] = (
                df["Product"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            duplicates = []

            # Exact duplicate names
            grouped = df.groupby("Normalized_Product")

            for product_name, group in grouped:

                if len(group) > 1:

                    skus = group["SKU"].astype(str).tolist()

                    duplicates.append({
                        "Product": product_name.title(),
                        "SKUs": skus,
                        "Similarity": 1.0,
                        "Confidence": "High",
                        "Match_Type": "Exact name match"
                    })

            # Similar product names
            product_rows = df[
                ["SKU", "Product", "Normalized_Product"]
            ].to_dict(orient="records")

            checked_pairs = set()

            for i in range(len(product_rows)):

                for j in range(i + 1, len(product_rows)):

                    first = product_rows[i]
                    second = product_rows[j]

                    pair = tuple(
                        sorted([
                            str(first["SKU"]),
                            str(second["SKU"])
                        ])
                    )

                    if pair in checked_pairs:
                        continue

                    checked_pairs.add(pair)

                    if (
                        first["Normalized_Product"]
                        == second["Normalized_Product"]
                    ):
                        continue

                    similarity = SequenceMatcher(
                        None,
                        first["Normalized_Product"],
                        second["Normalized_Product"]
                    ).ratio()

                    if similarity >= 0.85:

                        duplicates.append({
                            "Product": (
                                f"{first['Product']} / "
                                f"{second['Product']}"
                            ),
                            "SKUs": [
                                first["SKU"],
                                second["SKU"]
                            ],
                            "Similarity": round(
                                similarity,
                                2
                            ),
                            "Confidence": "High",
                            "Match_Type": "Name similarity"
                        })

            print("\nLikely Duplicate Products:")
            print("-" * 60)

            for item in duplicates:
                print(
                    f"{item['Product']} | "
                    f"SKUs: {item['SKUs']} | "
                    f"Confidence: {item['Confidence']}"
                )

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "duplicates": duplicates
            }

        # ==========================================================
        # WF007 - Marketing Campaign Brief
        # ==========================================================

        if workflow_id == "WF007":

            print("\nCreating marketing campaign brief...")

            request_lower = user_request.lower()

            # Infer product/theme from request
            if "collection" in request_lower:
                product = "New Collection"
            else:
                product = "New Product Collection"

            # Structured defaults
            campaign_goal = "Increase product awareness"
            audience = "Target customers interested in the new collection"
            promotion = "Launch promotion"
            campaign_dates = "To be confirmed"

            missing_data = []

            # Assessment workflow says goal and dates should be requested
            if not any(
                word in request_lower
                for word in [
                    "awareness",
                    "sales",
                    "conversion",
                    "launch",
                    "engagement"
                ]
            ):
                missing_data.append("campaign goal")

            if not any(
                word in request_lower
                for word in [
                    "october",
                    "november",
                    "december",
                    "january",
                    "february",
                    "march",
                    "april",
                    "may",
                    "june",
                    "july",
                    "august",
                    "september",
                    "date"
                ]
            ):
                missing_data.append("campaign dates")

            brief = {
                "Campaign Goal": campaign_goal,
                "Product": product,
                "Target Audience": audience,
                "Promotion": promotion,
                "Campaign Dates": campaign_dates,
                "Key Message": (
                    f"Discover the new {product.lower()} "
                    "and explore what makes it special."
                ),
                "Suggested Channels": [
                    "Instagram",
                    "LinkedIn",
                    "Email Marketing"
                ],
                "Content Ideas": [
                    "Product announcement post",
                    "Feature highlight",
                    "Launch email",
                    "Customer-focused social post"
                ],
                "Call To Action": "Explore Collection"
            }

            print("\nMarketing Campaign Brief:")
            print("-" * 60)

            for key, value in brief.items():
                print(f"{key}: {value}")

            if missing_data:
                print(
                    "\nInformation to confirm: "
                    + ", ".join(missing_data)
                )

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "campaign_brief": brief,
                "missing_data": missing_data
            }

        # ==========================================================
        # WF008 - SEO Keyword Classification + Page Mapping
        # ==========================================================

        if workflow_id == "WF008":

            print("\nClassifying SEO keywords...")

            df = read_csv("data/keywords.csv")

            if df is None:
                return {"status": "failed"}

            if "Keyword" not in df.columns:
                print("Missing Keyword column.")
                return {"status": "failed"}

            df = df.dropna(subset=["Keyword"])

            df["Keyword"] = (
                df["Keyword"]
                .astype(str)
                .str.strip()
            )

            df = df.drop_duplicates(
                subset=["Keyword"]
            )

            results = []

            for keyword in df["Keyword"]:

                keyword_lower = keyword.lower()

                if any(
                    word in keyword_lower
                    for word in [
                        "buy",
                        "purchase",
                        "order",
                        "shop",
                        "price"
                    ]
                ):
                    intent = "Transactional"
                    page = "Product / Pricing Page"
                    priority = "High"

                elif any(
                    word in keyword_lower
                    for word in [
                        "best",
                        "review",
                        "top",
                        "compare",
                        "cheap"
                    ]
                ):
                    intent = "Commercial"
                    page = "Comparison / Category Page"
                    priority = "High"

                elif any(
                    word in keyword_lower
                    for word in [
                        "amazon",
                        "login",
                        "website",
                        "official"
                    ]
                ):
                    intent = "Navigational"
                    page = "Brand / Website Page"
                    priority = "Medium"

                else:
                    intent = "Informational"
                    page = "Blog / Guide Page"
                    priority = "Medium"

                results.append({
                    "Keyword": keyword,
                    "Intent": intent,
                    "Mapped Page": page,
                    "Priority": priority
                })

            print("\nSEO Keyword Classification:")
            print("-" * 60)

            for item in results:
                print(
                    f"{item['Keyword']} | "
                    f"{item['Intent']} | "
                    f"{item['Mapped Page']} | "
                    f"{item['Priority']}"
                )

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "classified_keywords": results
            }

        # ==========================================================
        # WF009 - Employee Task Assignment
        # ==========================================================

        if workflow_id == "WF009":

            print("\nAssigning tasks to employees...")

            employees_df = read_csv("data/employees.csv")
            tasks_df = read_csv("data/tasks.csv")

            if employees_df is None or tasks_df is None:
                return {"status": "failed"}

            assignments = []

            print("\nTask Assignments:")
            print("-" * 60)

            for _, task in tasks_df.iterrows():

                required_skills = [
                    skill.strip().lower()
                    for skill in str(
                        task["Required_Skills"]
                    ).split("|")
                ]

                candidates = []

                for _, employee in employees_df.iterrows():

                    employee_skills = [
                        skill.strip().lower()
                        for skill in str(
                            employee["Skills"]
                        ).split("|")
                    ]

                    matching_skills = [
                        skill
                        for skill in required_skills
                        if skill in employee_skills
                    ]

                    workload = float(
                        employee["Current_Workload"]
                    )

                    if (
                        len(matching_skills) > 0
                        and workload < 80
                    ):

                        candidates.append({
                            "Employee_ID": employee["Employee_ID"],
                            "Employee_Name": employee["Employee_Name"],
                            "Skill_Score": len(matching_skills),
                            "Workload": workload,
                            "Matching_Skills": matching_skills
                        })

                if not candidates:

                    print(
                        f"{task['Task_ID']} | "
                        f"{task['Task']} | ESCALATED"
                    )

                    assignments.append({
                        "Task_ID": task["Task_ID"],
                        "Task": task["Task"],
                        "Status": "Escalated"
                    })

                    continue

                candidates.sort(
                    key=lambda x: (
                        -x["Skill_Score"],
                        x["Workload"]
                    )
                )

                selected = candidates[0]

                print(
                    f"{task['Task_ID']} | "
                    f"{task['Task']} | "
                    f"{selected['Employee_Name']} | "
                    f"{selected['Workload']}%"
                )

                assignments.append({
                    "Task_ID": task["Task_ID"],
                    "Task": task["Task"],
                    "Priority": task["Priority"],
                    "Deadline": task["Deadline"],
                    "Employee_ID": selected["Employee_ID"],
                    "Employee": selected["Employee_Name"],
                    "Matching_Skills": selected["Matching_Skills"],
                    "Workload": selected["Workload"],
                    "Status": "Assigned"
                })

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "assignments": assignments
            }

        # ==========================================================
        # WF010 - Workflow Performance Report
        # ==========================================================

        if workflow_id == "WF010":

            print("\nGenerating workflow performance report...")

            df = read_csv("data/execution_logs.csv")

            if df is None:
                return {"status": "failed"}

            required_columns = [
                "Execution_ID",
                "Workflow_ID",
                "Status",
                "Execution_Time_Seconds",
                "Error",
                "Failed_Step"
            ]

            missing_columns = validate_required_columns(
                df,
                required_columns
            )

            if missing_columns:
                print(f"Missing columns: {missing_columns}")
                return {"status": "failed"}

            total_executions = len(df)

            successful = len(
                df[df["Status"].str.lower() == "success"]
            )

            failed = len(
                df[df["Status"].str.lower() == "failed"]
            )

            success_rate = (
                successful / total_executions * 100
                if total_executions > 0
                else 0
            )

            failure_rate = (
                failed / total_executions * 100
                if total_executions > 0
                else 0
            )

            average_execution_time = (
                df["Execution_Time_Seconds"].mean()
                if total_executions > 0
                else 0
            )

            workflow_summary = (
                df.groupby("Workflow_ID")
                .agg(
                    Executions=("Execution_ID", "count"),
                    Average_Time=(
                        "Execution_Time_Seconds",
                        "mean"
                    ),
                    Failures=(
                        "Status",
                        lambda x: (
                            x.str.lower() == "failed"
                        ).sum()
                    )
                )
                .reset_index()
            )

            workflow_summary["Failure_Rate"] = (
                workflow_summary["Failures"]
                / workflow_summary["Executions"]
                * 100
            )

            print("\nPerformance Summary:")
            print("-" * 60)

            print(f"Total Executions: {total_executions}")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            print(f"Success Rate: {success_rate:.2f}%")
            print(f"Failure Rate: {failure_rate:.2f}%")
            print(
                f"Average Execution Time: "
                f"{average_execution_time:.2f} seconds"
            )

            failed_df = df[
                df["Status"].str.lower() == "failed"
            ]

            print("\nFrequent Errors:")
            print("-" * 60)

            if failed_df.empty:

                frequent_errors = {}

                print("No errors found.")

            else:

                frequent_errors = (
                    failed_df["Error"]
                    .value_counts()
                    .to_dict()
                )

                for error, count in frequent_errors.items():
                    print(f"{error}: {count}")

            print("\nSlow Workflows:")
            print("-" * 60)

            slow_workflows = workflow_summary[
                workflow_summary["Average_Time"] > 5
            ]

            if slow_workflows.empty:

                print("No workflows above 5 seconds.")

            else:

                for _, row in slow_workflows.iterrows():

                    print(
                        f"{row['Workflow_ID']} | "
                        f"Average: "
                        f"{row['Average_Time']:.2f}s"
                    )

            recommendations = []

            if failure_rate > 10:
                recommendations.append(
                    "Failure rate is above 10%. "
                    "Investigate failed workflows."
                )

            if average_execution_time > 5:
                recommendations.append(
                    "Average execution time is above "
                    "5 seconds. Optimize slow workflows."
                )

            if not recommendations:
                recommendations.append(
                    "Overall workflow performance is healthy."
                )

            print("\nRecommendations:")
            print("-" * 60)

            for recommendation in recommendations:
                print(f"- {recommendation}")

            return {
                "workflow_id": workflow_id,
                "workflow_name": workflow["workflow_name"],
                "status": "completed",
                "total_executions": total_executions,
                "successful": successful,
                "failed": failed,
                "success_rate": round(success_rate, 2),
                "failure_rate": round(failure_rate, 2),
                "average_execution_time": round(
                    average_execution_time,
                    2
                ),
                "frequent_errors": frequent_errors,
                "recommendations": recommendations
            }

        # ==========================================================
        # Unknown workflow
        # ==========================================================

        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow["workflow_name"],
            "status": "workflow_loaded"
        }