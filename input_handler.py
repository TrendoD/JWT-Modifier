import json
from typing import Dict, Any, Tuple, Optional
import re

class InputHandler:
    @staticmethod
    def validate_jwt_format(token: str) -> bool:
        """
        Validate if the string matches JWT format (three base64-encoded sections separated by dots)
        """
        jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]*$'
        return bool(re.match(jwt_pattern, token))

    @staticmethod
    def validate_json_input(json_str: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Validate if the string is valid JSON
        Returns: (is_valid, parsed_json, error_message)
        """
        try:
            parsed = json.loads(json_str)
            if not isinstance(parsed, dict):
                return False, None, "Input must be a JSON object"
            return True, parsed, None
        except json.JSONDecodeError as e:
            return False, None, f"Invalid JSON: {str(e)}"

    @staticmethod
    def get_menu_choice(options: Dict[str, str]) -> str:
        """
        Get user's menu choice and validate it
        """
        valid_choices = list(options.keys())
        while True:
            choice = input(f"\nSelect an option ({'-'.join(valid_choices)}): ").strip()
            if choice in valid_choices:
                return choice
            print(f"Invalid choice. Please select from: {', '.join(valid_choices)}")

    @staticmethod
    def get_jwt_input() -> str:
        """
        Get JWT input from user and validate format
        """
        while True:
            token = input("\nEnter your JWT: ").strip()
            if InputHandler.validate_jwt_format(token):
                return token
            print("Invalid JWT format. Please try again.")

    @staticmethod
    def get_secret_key() -> str:
        """
        Get secret key input from user
        """
        while True:
            key = input("\nEnter secret key (or type 'exit' to quit): ").strip()
            if key.lower() == 'exit':
                raise KeyboardInterrupt("User requested exit")
            if key:
                return key
            print("Secret key cannot be empty. Please try again.")

    @staticmethod
    def modify_header(current_header: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interactive header modification with specific field options
        """
        header = current_header.copy()
        while True:
            print("\nCurrent header:")
            print(json.dumps(header, indent=2))
            
            options = {
                "1": "Modify algorithm (alg)",
                "2": "Modify type (typ)",
                "3": "Add new field",
                "4": "Remove field",
                "5": "Save and return",
                "6": "Cancel modifications"
            }
            
            print("\nHeader modification options:")
            for key, value in options.items():
                print(f"[{key}] {value}")
            
            choice = InputHandler.get_menu_choice(options)
            
            if choice == "1":
                print("\nAvailable algorithms: none, HS256, RS256")
                alg = input("Enter new algorithm: ").strip().upper()
                header["alg"] = alg
            elif choice == "2":
                typ = input("\nEnter new type (default 'JWT'): ").strip().upper()
                header["typ"] = typ or "JWT"
            elif choice == "3":
                key = input("\nEnter field name: ").strip()
                if key:
                    value = input("Enter field value: ").strip()
                    try:
                        # Try to parse as JSON in case it's a boolean/number/null
                        parsed_value = json.loads(value.lower())
                        header[key] = parsed_value
                    except json.JSONDecodeError:
                        # If not valid JSON, treat as string
                        header[key] = value
            elif choice == "4":
                if len(header) > 0:
                    print("\nAvailable fields:")
                    for i, key in enumerate(header.keys(), 1):
                        print(f"[{i}] {key}")
                    field_choice = input("\nEnter field number to remove: ").strip()
                    try:
                        field_idx = int(field_choice) - 1
                        if 0 <= field_idx < len(header):
                            key_to_remove = list(header.keys())[field_idx]
                            del header[key_to_remove]
                            print(f"\nRemoved field: {key_to_remove}")
                    except (ValueError, IndexError):
                        print("Invalid selection")
            elif choice == "5":
                return header
            else:  # Cancel
                return current_header
            
            print("\n✓ Header updated")

    @staticmethod
    def modify_payload(current_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interactive payload modification with specific field options
        """
        payload = current_payload.copy()
        while True:
            print("\nCurrent payload:")
            print(json.dumps(payload, indent=2))
            
            options = {
                "1": "Modify existing field",
                "2": "Add new field",
                "3": "Remove field",
                "4": "Save and return",
                "5": "Cancel modifications"
            }
            
            print("\nPayload modification options:")
            for key, value in options.items():
                print(f"[{key}] {value}")
            
            choice = InputHandler.get_menu_choice(options)
            
            if choice == "1":
                if len(payload) > 0:
                    print("\nAvailable fields:")
                    for i, (key, value) in enumerate(payload.items(), 1):
                        print(f"[{i}] {key}: {value}")
                    field_choice = input("\nEnter field number to modify: ").strip()
                    try:
                        field_idx = int(field_choice) - 1
                        if 0 <= field_idx < len(payload):
                            key_to_modify = list(payload.keys())[field_idx]
                            value = input(f"Enter new value for '{key_to_modify}': ").strip()
                            try:
                                # Try to parse as JSON in case it's a boolean/number/null
                                parsed_value = json.loads(value.lower())
                                payload[key_to_modify] = parsed_value
                            except json.JSONDecodeError:
                                # If not valid JSON, treat as string
                                payload[key_to_modify] = value
                    except (ValueError, IndexError):
                        print("Invalid selection")
            elif choice == "2":
                key = input("\nEnter field name: ").strip()
                if key:
                    value = input("Enter field value: ").strip()
                    try:
                        # Try to parse as JSON in case it's a boolean/number/null
                        parsed_value = json.loads(value.lower())
                        payload[key] = parsed_value
                    except json.JSONDecodeError:
                        # If not valid JSON, treat as string
                        payload[key] = value
            elif choice == "3":
                if len(payload) > 0:
                    print("\nAvailable fields:")
                    for i, key in enumerate(payload.keys(), 1):
                        print(f"[{i}] {key}")
                    field_choice = input("\nEnter field number to remove: ").strip()
                    try:
                        field_idx = int(field_choice) - 1
                        if 0 <= field_idx < len(payload):
                            key_to_remove = list(payload.keys())[field_idx]
                            del payload[key_to_remove]
                            print(f"\nRemoved field: {key_to_remove}")
                    except (ValueError, IndexError):
                        print("Invalid selection")
            elif choice == "4":
                return payload
            else:  # Cancel
                return current_payload
            
            print("\n✓ Payload updated")

    @staticmethod
    def modify_json(current_json: Dict[str, Any], section: str) -> Dict[str, Any]:
        """
        Interactive JSON modification
        """
        if section.lower() == "header":
            return InputHandler.modify_header(current_json)
        elif section.lower() == "payload":
            return InputHandler.modify_payload(current_json)
        
        # Fallback to direct JSON input
        while True:
            print(f"\nCurrent {section}:")
            print(json.dumps(current_json, indent=2))
            
            print(f"\nEnter new {section} (JSON format) or press Enter to cancel:")
            json_str = input("> ").strip()
            
            if not json_str:
                return current_json
                
            is_valid, parsed_json, error = InputHandler.validate_json_input(json_str)
            if is_valid:
                return parsed_json
            print(error)

    @staticmethod
    def confirm_action(prompt: str) -> bool:
        """
        Get user confirmation for an action
        """
        while True:
            response = input(f"\n{prompt} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            if response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'")

    @staticmethod
    def get_file_path(prompt: str) -> str:
        """
        Get file path input from user
        """
        while True:
            path = input(f"\n{prompt}: ").strip()
            if path:
                return path
            print("File path cannot be empty. Please try again.")