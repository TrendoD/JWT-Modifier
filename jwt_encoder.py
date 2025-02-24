import jwt
from typing import Dict, Any, Optional

class JWTEncoder:
    @staticmethod
    def create_token_none_alg(header: Dict[str, Any], payload: Dict[str, Any]) -> str:
        """
        Create a JWT using 'none' algorithm
        """
        try:
            # Ensure algorithm is set to 'none'
            header['alg'] = 'none'
            return jwt.encode(payload, None, algorithm='none', headers=header)
        except Exception as e:
            raise ValueError(f"Error creating JWT: {str(e)}")

    @staticmethod
    def create_token_hs(header: Dict[str, Any], payload: Dict[str, Any], 
                       secret_key: str, algorithm: str = 'HS256') -> str:
        """
        Create a JWT using HMAC algorithm
        """
        try:
            # Ensure correct algorithm is set in header
            header['alg'] = algorithm
            return jwt.encode(payload, secret_key, algorithm=algorithm, headers=header)
        except Exception as e:
            raise ValueError(f"Error creating JWT: {str(e)}")

    @staticmethod
    def create_token_rs(header: Dict[str, Any], payload: Dict[str, Any],
                       private_key: str, algorithm: str = 'RS256') -> str:
        """
        Create a JWT using RSA algorithm
        """
        try:
            # Ensure correct algorithm is set in header
            header['alg'] = algorithm
            return jwt.encode(payload, private_key, algorithm=algorithm, headers=header)
        except Exception as e:
            raise ValueError(f"Error creating JWT: {str(e)}")

    @staticmethod
    def update_token(original_token: str, new_header: Optional[Dict[str, Any]] = None,
                    new_payload: Optional[Dict[str, Any]] = None,
                    key: Optional[str] = None, algorithm: Optional[str] = None) -> str:
        """
        Update an existing token with new header and/or payload
        """
        try:
            # If no new header/payload provided, use existing ones
            if not new_header or not new_payload:
                old_header = jwt.get_unverified_header(original_token)
                old_payload = jwt.decode(original_token, options={"verify_signature": False})
                
            header = new_header if new_header is not None else old_header
            payload = new_payload if new_payload is not None else old_payload
            
            # Determine algorithm
            if not algorithm:
                algorithm = header.get('alg', 'HS256')

            # Create new token based on algorithm
            if algorithm.lower() == 'none':
                return JWTEncoder.create_token_none_alg(header, payload)
            elif algorithm.startswith('HS'):
                return JWTEncoder.create_token_hs(header, payload, key, algorithm)
            elif algorithm.startswith('RS'):
                return JWTEncoder.create_token_rs(header, payload, key, algorithm)
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
                
        except Exception as e:
            raise ValueError(f"Error updating JWT: {str(e)}")