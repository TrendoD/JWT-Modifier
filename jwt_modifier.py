#!/usr/bin/env python3
import pyperclip
from jwt_decoder import JWTDecoder
from jwt_encoder import JWTEncoder
from input_handler import InputHandler
from ui_formatter import UIFormatter
import time

class JWTModifier:
    def __init__(self):
        self.ui = UIFormatter()
        self.input_handler = InputHandler()
        self.decoder = JWTDecoder()
        self.encoder = JWTEncoder()

    def run(self):
        try:
            self.ui.display_header("JWT MODIFIER")
            
            # Get initial JWT input
            jwt_token = self.input_handler.get_jwt_input()
            
            # Decode and display JWT info
            header, payload, algorithm = self.decoder.decode_without_verification(jwt_token)
            self.ui.display_jwt_details(header, payload, jwt_token.split('.')[2])
            
            # Process based on algorithm
            if algorithm.lower() == 'none':
                self.handle_none_algorithm(header, payload)
            elif algorithm.startswith('HS'):
                self.handle_hs_algorithm(jwt_token, header, payload, algorithm)
            elif algorithm.startswith('RS'):
                self.handle_rs_algorithm(jwt_token, header, payload, algorithm)
            else:
                self.ui.display_error(f"Algorithm {algorithm} not supported")
                
        except KeyboardInterrupt:
            self.ui.display_warning("Program terminated by user")
        except Exception as e:
            self.ui.display_error(str(e))

    def show_main_menu(self, header: dict, payload: dict, key: str = None, algorithm: str = None):
        current_header = header.copy()
        current_payload = payload.copy()
        
        while True:
            self.ui.clear_screen()
            options = {
                "1": "View JWT",
                "2": "Modify Header",
                "3": "Modify Payload",
                "4": "Generate New JWT",
                "5": "Exit"
            }
            
            self.ui.display_header("MAIN MENU")
            self.ui.display_menu(options)
            
            choice = self.input_handler.get_menu_choice(options)
            
            if choice == "1":
                self.ui.display_jwt_details(current_header, current_payload, "...")
                # Pause to show details
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.ui.clear_screen()
                self.ui.display_header("MODIFY HEADER")
                new_header = self.input_handler.modify_json(current_header, "header")
                if new_header != current_header:
                    current_header = new_header
                    algorithm = current_header.get('alg', algorithm)
                    self.ui.display_success("Header updated!")
                    time.sleep(1)  # Show success message briefly
            elif choice == "3":
                self.ui.clear_screen()
                self.ui.display_header("MODIFY PAYLOAD")
                new_payload = self.input_handler.modify_json(current_payload, "payload")
                if new_payload != current_payload:
                    current_payload = new_payload
                    self.ui.display_success("Payload updated!")
                    time.sleep(1)  # Show success message briefly
            elif choice == "4":
                new_jwt = self.encoder.update_token(None, current_header, current_payload, key, algorithm)
                self.ui.display_new_jwt(new_jwt)
                pyperclip.copy(new_jwt)
                input("\nPress Enter to continue...")
            else:  # Exit
                break

    def handle_none_algorithm(self, header: dict, payload: dict):
        self.ui.display_success("'none' algorithm detected. Direct modification allowed.")
        time.sleep(1)  # Show message briefly
        self.show_main_menu(header, payload, None, 'none')

    def handle_hs_algorithm(self, jwt_token: str, header: dict, payload: dict, algorithm: str):
        self.ui.display_warning(f"{algorithm} algorithm detected. Secret key required for verification.")
        
        while True:
            try:
                secret_key = self.input_handler.get_secret_key()
                if self.decoder.verify_hs_token(jwt_token, secret_key):
                    self.ui.display_success("Verification Successful! Valid JWT.")
                    time.sleep(1)  # Show success message briefly
                    self.show_main_menu(header, payload, secret_key, algorithm)
                    break
                else:
                    self.ui.display_error("Invalid secret key. Verification failed.")
                    if not self.input_handler.confirm_action("Try again?"):
                        break
            except KeyboardInterrupt:
                break

    def handle_rs_algorithm(self, jwt_token: str, header: dict, payload: dict, algorithm: str):
        self.ui.display_warning(f"{algorithm} algorithm detected. Public key required for verification.")
        
        while True:
            try:
                public_key_path = self.input_handler.get_file_path("Enter path to public key file")
                with open(public_key_path, 'r') as f:
                    public_key = f.read()
                
                if self.decoder.verify_rs_token(jwt_token, public_key):
                    self.ui.display_success("Verification Successful! Valid JWT.")
                    time.sleep(1)  # Show success message briefly
                    
                    private_key_path = self.input_handler.get_file_path("Enter path to private key file")
                    with open(private_key_path, 'r') as f:
                        private_key = f.read()
                    
                    self.show_main_menu(header, payload, private_key, algorithm)
                    break
                else:
                    self.ui.display_error("Invalid public key. Verification failed.")
                    if not self.input_handler.confirm_action("Try again?"):
                        break
            except FileNotFoundError:
                self.ui.display_error("Key file not found.")
                if not self.input_handler.confirm_action("Try again?"):
                    break
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.ui.display_error(f"Error: {str(e)}")
                if not self.input_handler.confirm_action("Try again?"):
                    break

if __name__ == "__main__":
    modifier = JWTModifier()
    modifier.run()