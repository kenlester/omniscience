import sys
import json
import importlib

def main():
    """
    A generic utility to run a function from a module with input from a file.

    Usage:
        python run_function.py <module_name> <function_name> <input_filepath>

    - <module_name>: The name of the module to import (e.g., 'extractor_swarm.agent').
    - <function_name>: The name of the function to call within the module.
    - <input_filepath>: The path to a JSON file containing the input data.
                        The data will be passed as the first argument to the function.

    The script prints the function's return value to stdout as a JSON string.
    """
    if len(sys.argv) != 4:
        print("Usage: python run_function.py <module_name> <function_name> <input_filepath>")
        sys.exit(1)

    module_name = sys.argv[1]
    function_name = sys.argv[2]
    input_filepath = sys.argv[3]

    try:
        # Read the input data from the specified file
        with open(input_filepath, 'r') as f:
            input_data = json.load(f)

        # Dynamically import the module
        module = importlib.import_module(module_name)

        # Get the function from the module
        function_to_run = getattr(module, function_name)

        # Run the function, passing the loaded JSON object as keyword arguments
        result = function_to_run(**input_data)

        # Print the result as a JSON string to stdout
        print(json.dumps(result, indent=2))

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_filepath}'")
        sys.exit(1)
    except (ModuleNotFoundError, AttributeError):
        print(f"Error: Could not find function '{function_name}' in module '{module_name}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
