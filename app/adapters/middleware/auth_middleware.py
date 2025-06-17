from functools import wraps
from flask import request, jsonify
import requests
import os
from typing import Optional, Dict, Any

class AuthMiddleware:
    """Middleware para validación de tokens JWT"""
    
    def __init__(self, auth_service_url: Optional[str] = None):
        self.auth_service_url = auth_service_url or os.getenv(
            'AUTH_SERVICE_URL', 
            'http://localhost:5001/auth/validate-token'
        )
    
    def _extract_token(self) -> Optional[str]:
        """Extrae el token JWT del header Authorization"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        # Verificar que el header tenga el formato "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        
        return parts[1]
    
    def _validate_token(self, token: str) -> Dict[str, Any]:
        """Valida el token contra el servicio de autenticación"""
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                self.auth_service_url,
                headers=headers,
                timeout=5  # Timeout de 5 segundos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"valid": False, "error": f"Auth service returned {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"valid": False, "error": f"Auth service unavailable: {str(e)}"}
    
    def require_auth(self, f):
        """Decorador que requiere autenticación válida"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extraer token
            token = self._extract_token()
            if not token:
                return jsonify({
                    "error": "Token de autorización requerido",
                    "message": "Debe proporcionar un token Bearer en el header Authorization"
                }), 401
            
            # Validar token
            validation_result = self._validate_token(token)
            
            if not validation_result.get("valid", False):
                error_message = validation_result.get("error", "Token inválido")
                return jsonify({
                    "error": "Token no válido",
                    "message": error_message
                }), 401
            
            # Agregar información del usuario al contexto de Flask para uso posterior
            from flask import g
            g.user_id = validation_result.get("user_id")
            g.auth_data = validation_result
            
            return f(*args, **kwargs)
        
        return decorated_function

# Instancia global del middleware
auth_middleware = AuthMiddleware()

# Decorador de conveniencia
def require_auth(f):
    """Decorador de conveniencia para requerir autenticación"""
    return auth_middleware.require_auth(f) 