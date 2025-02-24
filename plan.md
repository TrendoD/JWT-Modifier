# JWT Modifier Project Plan

## Project Objective
Create a Python-based JWT Modifier application similar to jwt.io that allows users to:
1. Extract and view JWT contents (header and payload)
2. Modify JWT based on the algorithm and keys used
3. Provide a clean, intuitive interface for easy navigation

## Core Features

### 1. JWT Analysis
- Accept JWT input from the user
- Decode JWT to display header and payload in a readable format
- Detect the algorithm used (None, HS256, RS256, etc.)

### 2. JWT Modification Based on Algorithm
- **For "none" algorithm**:
  - Allow direct modification of JWT contents (header and payload)
  - Generate a new JWT based on these modifications

- **For "HS" algorithms (HMAC-SHA)**:
  - Prompt user to input the secret key
  - Verify JWT with the provided secret key
  - If verification succeeds, allow JWT modification
  - If verification fails, display error message and prompt for re-input or exit option

- **For "RS" algorithms (RSA)**:
  - Prompt user to input the public key
  - Verify JWT using the public key
  - If verification succeeds, request private key and allow modification
  - If verification fails, display error message and prompt for re-input or exit option

### 3. User Flow
- **On application launch**:
  - Request JWT input
  - Display JWT contents (header and payload) in a readable format
  - Detect the algorithm used

- **Based on algorithm**:
  - Execute the appropriate verification flow (as described in point 2)
  - If verification fails, still display JWT contents but disallow modification
  - Provide options to re-input keys or exit

- **After successful verification**:
  - Allow user to modify header and payload
  - Generate a new JWT with a valid signature
  - Display the new JWT

### 4. User Interface Requirements
- **Clean and Intuitive CLI (Command Line Interface)**:
  - Use colors to differentiate between header, payload, and signature
  - Display well-formatted JSON (with proper indentation)
  - Provide clear instructions at each step
  - Implement an intuitive navigation menu
  - Support proper error handling with descriptive messages
  - Ensure all text is properly aligned and formatted
  - Add option to copy JWT to clipboard

## Program Structure

### 1. Main Module
```
jwt_modifier.py - Main script that users will run
```

### 2. Functional Components
```
jwt_decoder.py - Functions for decoding and verifying JWT
jwt_encoder.py - Functions for encoding and signing JWT
input_handler.py - Manages user input and validation
ui_formatter.py - Manages terminal UI display and formatting
```

## Detailed Program Flow

1. **Program Start**
   ```
   $ python jwt_modifier.py
   ╔════════════════════════════════════╗
   ║           JWT MODIFIER             ║
   ╚════════════════════════════════════╝
   
   Enter your JWT:
   > eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
   ```

2. **Displaying JWT Information**
   ```
   ╔════════════════════════════════════╗
   ║           JWT DETAILS              ║
   ╚════════════════════════════════════╝
   
   ✓ Valid JWT Format
   
   ┌─ HEADER ─────────────────────────┐
   │ {                                │
   │   "alg": "HS256",                │
   │   "typ": "JWT"                   │
   │ }                                │
   └──────────────────────────────────┘
   
   ┌─ PAYLOAD ────────────────────────┐
   │ {                                │
   │   "sub": "1234567890",           │
   │   "name": "John Doe",            │
   │   "iat": 1516239022              │
   │ }                                │
   └──────────────────────────────────┘
   
   ┌─ SIGNATURE ──────────────────────┐
   │ SflKxwRJSMeKKF2QT4fwpMeJf36POk6y │
   │ JV_adQssw5c                      │
   └──────────────────────────────────┘
   
   Algorithm: HS256
   ```

3. **Verification Based on Algorithm**
   - For HS256:
   ```
   HS256 algorithm detected. Secret key required for verification.
   
   Enter secret key (or type 'exit' to quit):
   > your-256-bit-secret
   
   ✓ Verification Successful! Valid JWT.
   ```

4. **JWT Modification**
   ```
   ╔════════════════════════════════════╗
   ║             MAIN MENU              ║
   ╚════════════════════════════════════╝
   
   [1] View JWT
   [2] Modify Header
   [3] Modify Payload
   [4] Generate New JWT
   [5] Exit
   
   Select an option (1-5):
   > 3
   
   ╔════════════════════════════════════╗
   ║          MODIFY PAYLOAD            ║
   ╚════════════════════════════════════╝
   
   Current Payload:
   {
     "sub": "1234567890",
     "name": "John Doe",
     "iat": 1516239022
   }
   
   Enter new payload (JSON format):
   > {"sub": "1234567890", "name": "Jane Doe", "iat": 1516239022, "admin": true}
   
   ✓ Payload updated!
   ```

5. **Generating New JWT**
   ```
   ╔════════════════════════════════════╗
   ║         GENERATE NEW JWT           ║
   ╚════════════════════════════════════╝
   
   Header:
   {
     "alg": "HS256",
     "typ": "JWT"
   }
   
   Payload:
   {
     "sub": "1234567890",
     "name": "Jane Doe",
     "iat": 1516239022,
     "admin": true
   }
   
   New JWT:
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkphbmUgRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhZG1pbiI6dHJ1ZX0.cAOIAifu3fykvhkHpbuhbvtH807-Z2rI1FS3vX1XMjY
   
   JWT copied to clipboard!
   
   [1] Return to Main Menu
   [2] Exit
   
   Select an option (1-2):
   > 
   ```

## Technical Implementation Plan

### Technologies and Libraries
1. **Python 3.6+** - Main programming language
2. **PyJWT** - Library for JWT encoding/decoding
3. **cryptography** - Library for cryptographic operations (RSA)
4. **rich** - Library for enhanced terminal UI
5. **pyperclip** - For clipboard operations

### Code Structure
```python
# jwt_modifier.py
import json
import jwt
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
import pyperclip

# Main function
def main():
    console = Console()
    console.print(Panel.fit("JWT MODIFIER", border_style="bold blue"))
    
    # Get JWT input
    jwt_token = input_jwt()
    
    # Decode and display JWT
    header, payload, alg = decode_jwt(jwt_token)
    display_jwt_info(header, payload, alg)
    
    # Verify based on algorithm
    if alg.lower() == "none":
        console.print("[bold green]'none' algorithm detected. Direct modification allowed.[/bold green]")
        proceed_to_modification(header, payload, None, alg)
    elif alg.startswith("HS"):
        verify_and_modify_hs(jwt_token, header, payload, alg)
    elif alg.startswith("RS"):
        verify_and_modify_rs(jwt_token, header, payload, alg)
    else:
        console.print(f"[bold red]Algorithm {alg} not supported yet.[/bold red]")
    
# Implementation of other functions...
```

### Validation and Error Handling
- JWT format validation
- JSON input validation during modification
- Error handling during decode/encode
- Handling incorrect inputs

## Testing Scenarios
- Verify different algorithms
- Test header and payload modifications
- Test with invalid JWTs
- Test with correct/incorrect keys

## Implementation Notes
- Focus on clean, intuitive interface design
- Ensure clear error messages and user guidance
- Implement proper JSON formatting for readability
- Use colors and UI elements consistently
- Optimize for command-line usability

This plan provides a comprehensive framework for developing a Python-based JWT Modifier that replicates jwt.io functionality while offering a clean, intuitive interface for users to analyze and modify JWTs based on different algorithms and key requirements.