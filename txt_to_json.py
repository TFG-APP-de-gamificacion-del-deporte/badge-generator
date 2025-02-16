import json

def parse_tree_to_json(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    def build_tree(lines: list[str], parent_indent=-1, current_id=1, catID=-1):
        """Recursively builds the tree structure."""
        result = []
        while lines:
            line = lines[0]
            # Calculate the indentation level
            stripped_line = line.lstrip()
            current_indent = len(line) - len(stripped_line)
            
            if current_indent <= parent_indent:
                break  # This line belongs to a higher-level node
            
            # Consume the current line
            lines.pop(0)
            
            # Create a node
            if current_indent == 0:
                # Category nodes have negative id's
                node = {
                    "id": catID,
                    "name": stripped_line.strip().lower(),
                    "achieved": False,
                    "image": "",
                    "description": "",
                    "children": [],
                }
                catID -= 1
            else:
                node = {
                    "id": current_id,
                    "name": stripped_line.strip(),
                    "achieved": False,
                    "image": f"/image/badge/{current_id}.svg",
                    "description": "",
                    "children": [],
                }
                current_id += 1
            
            # Build children nodes
            node["children"], current_id = build_tree(lines, current_indent, current_id)
            
            # Add the node to the result
            result.append(node)
        
        return result, current_id

    # Parse the lines into a tree structure
    tree, _ = build_tree(lines)

    return tree


def main():
    TXT_FILE = "badges.txt"
    json_tree = parse_tree_to_json(TXT_FILE)

    def write_json_to_file(json_data, output_file):
        with open(output_file, 'w') as file:
            json.dump(json_data, file, indent=2)

    OUTPUT_JSON_FILE = "badges.json"
    write_json_to_file(json_tree, OUTPUT_JSON_FILE)


if __name__ == "__main__":
    main()