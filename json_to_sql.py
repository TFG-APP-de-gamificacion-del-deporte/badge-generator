import json

def process_badges(badges, parent_id=None, depth=0):
    """
    Recursively process badges and generate SQL insert statements.
    
    Args:
        badges (list): List of badge dictionaries.
        parent_id (int): ID of the parent badge (None for root badges).

    Returns:
        list: List of SQL insert statements.
    """
    sql_statements = []
    
    for badge in badges:
        badge_id = badge["id"]
        name = badge["name"].replace("'", "''")  # Escape single quotes
        image = badge["image"].replace("'", "''")
        description = badge["description"].replace("'", "''")
        parent = "null" if parent_id == None else parent_id

        # Calculate experience value based on depth
        # y = 1.9^(x+4) + 100(x+4) -400
        x = depth + 4
        exp = -400 + 100*x + (1.9 ** x)
        exp = round(exp)

        # Root badges (categories) don't have exp
        if depth == 0:
          exp = 0

        sql = f"INSERT INTO badge (id, name, description, image, parent_badge_id, exp) VALUES ({badge_id}, '{name}', '{description}', '{image}', {parent}, {exp});"
        sql_statements.append(sql)

        # Recursively process children badges
        if "children" in badge and badge["children"]:
            sql_statements.extend(process_badges(badge["children"], parent_id=badge_id, depth=depth + 1))

    return sql_statements

def generate_sql_script(json_file, output_file):
    """
    Generate an SQL script from a JSON file describing badges.

    Args:
        json_file (str): Path to the JSON file.
        output_file (str): Path to the output SQL file.
    """
    with open(json_file, "r") as f:
        badges = json.load(f)

    sql_statements = []

    # Process top-level badge categories
    for category in badges:
        sql_statements.extend(process_badges([category]))

    # Write SQL statements to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(sql_statements))

if __name__ == "__main__":
    # Define input and output files
    json_file = "badges.json"
    output_file = "insert_badges.sql"

    # Generate the SQL script
    generate_sql_script(json_file, output_file)
    print(f"SQL script generated and saved to {output_file}")
