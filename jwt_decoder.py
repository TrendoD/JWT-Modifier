import jwt
from typing import Tuple, Dict, Any, Optional
from jwt.exceptions import InvalidTokenError, InvalidSignatureError

class JWTDecoder:
    @staticmethod
    def decode_without_verification(token: str) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
        """
        Decode JWT without verifying the signature to extract header and payload
        """
        try:
            # Split the token into parts
            header_segment, payload_segment, _ = token.split('.')
            
            # Decode header and payload
            header = jwt.get_unverified_header(token)
            payload = jwt.decode(token, options={"verify_signature": False})
            algorithm = header.get('alg', 'none')
            
            return header, payload, algorithm
            
        except Exception as e:
            raise ValueError(f"Invalid JWT format: {str(e)}")

    @staticmethod
    def verify_hs_token(token: str, secret_key: str) -> bool:
        """
        Verify JWT signed with HMAC algorithm
        """
        try:
            jwt.decode(token, secret_key, algorithms=["HS256", "HS384", "HS512"])
            return True
        except InvalidSignatureError:
            return False
        except InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    @staticmethod
    def verify_rs_token(token: str, public_key: str) -> bool:
        """
        Verify JWT signed with RSA algorithm
        """
        try:
            jwt.decode(token, public_key, algorithms=["RS256", "RS384", "RS512"])
            return True
        except InvalidSignatureError:
            return False
        except InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")