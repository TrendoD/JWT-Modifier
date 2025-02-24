# JWT Modifier

A command-line tool for analyzing and modifying JWTs. I created this tool just to help me solve CTF challenges in the future. If you find any bugs or have questions about this tool, feel free to DM me directly.

## Features

- **JWT Analysis**
  - Decode and view JWT contents
  - Detect algorithm used (none, HS256, RS256)
  - Format output for better readability

- **JWT Modification**
  - Modify header fields (algorithm, type, etc.)
  - Edit payload content
  - Add/remove fields
  - Generate new tokens

- **Algorithm Support**
  - "none" algorithm: Direct modification
  - HS256: Secret key verification
  - RS256: Public/private key pair handling

## Quick Start

1. **Setup**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run**
   ```bash
   python jwt_modifier.py
   ```

3. **Usage Example**
   ```bash
   # For RS256 tokens, have your keys ready:
   # - Public key for verification (publ.pem)
   # - Private key for signing (priv.pem)

   # If you need to generate a key pair:
   python generate_keys.py
   ```

## Commands

- `View JWT`: Display current token details
- `Modify Header`: Change algorithm or add fields
- `Modify Payload`: Edit claims or add admin privileges
- `Generate New JWT`: Create token with your modifications
- `Exit`: Quit program

## Dependencies

- PyJWT
- cryptography
- rich (for CLI formatting)
- pyperclip (for clipboard operations)
