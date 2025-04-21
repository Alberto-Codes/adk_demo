import sqlfluff


def lint_sql(sql_code: str) -> dict:
    """Lints SQL code using sqlfluff and reports violations.

    Args:
        sql_code (str): The SQL code string to lint.

    Returns:
        dict: A dictionary containing the status and the linting report or an error message.
            Example success (no violations):
                {
                    "status": "success",
                    "report": "No linting violations found."
                }
            Example success (violations found):
                {
                    "status": "success",
                    "report": "[Linter violations...]"
                }
            Example error:
                {
                    "status": "error",
                    "error_message": "Failed to lint SQL: [Error details...]"
                }
    """
    try:
        # Lint the SQL code using sqlfluff
        # Using the 'ansi' dialect as a default
        linted_result = sqlfluff.lint(sql_code, dialect="teradata")

        # Check if linted_result is a list of violations
        if isinstance(linted_result, list) and not linted_result:
            report = "No linting violations found."
        elif isinstance(linted_result, list):
            # Format violations for readability (optional, adjust as needed)
            report = "\n".join([str(v) for v in linted_result])
        else:
            # Handle unexpected result format
            report = str(linted_result)

        return {"status": "success", "report": report}
    except Exception as e:
        # Catch potential errors during linting
        error_message = f"Failed to lint SQL: {e}"
        return {"status": "error", "error_message": error_message}


def fix_sql(sql_code: str) -> dict:
    """Attempts to fix SQL code using sqlfluff.

    Args:
        sql_code (str): The SQL code string to fix.

    Returns:
        dict: A dictionary containing the status and the fixed SQL code or an error message.
            Example success:
                {
                    "status": "success",
                    "report": "SELECT column1, column2\nFROM my_table\nWHERE condition = TRUE;"
                }
            Example error:
                {
                    "status": "error",
                    "error_message": "Failed to fix SQL: [Error details...]"
                }
    """
    try:
        # Fix the SQL code using sqlfluff
        # Using the 'ansi' dialect as a default
        fixed_sql = sqlfluff.fix(sql_code, dialect="teradata")
        return {"status": "success", "report": fixed_sql}
    except Exception as e:
        # Catch potential errors during fixing
        error_message = f"Failed to fix SQL: {e}"
        # Check if the error is due to linting issues and include them if possible
        # Although fix implies linting first, the error might manifest differently
        if hasattr(e, "violations"):
            error_message += f"\nViolations preventing fix: {e.violations}"
        return {"status": "error", "error_message": error_message}


def parse_sql(sql_code: str) -> dict:
    """Parses SQL code using sqlfluff.

    Args:
        sql_code (str): The SQL code string to parse.

    Returns:
        dict: A dictionary containing the status and the parsed SQL code or an error message.
            Example success:
                {
                    "status": "success",
                    "report": "Parsed SQL structure..."
                }
            Example error:
                {
                    "status": "error",
                    "error_message": "Failed to parse SQL: [Error details...]"
                }
    """
    try:
        # Parse the SQL code using sqlfluff
        # Using the 'ansi' dialect as a default
        parsed_sql = sqlfluff.parse(sql_code, dialect="teradata")
        return {"status": "success", "report": parsed_sql}
    except Exception as e:
        # Catch potential errors during parsing
        error_message = f"Failed to parse SQL: {e}"
        return {"status": "error", "error_message": error_message}
