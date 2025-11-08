def get_auth_header():
    return  {
        "Access-Control-Allow-Origin": "*",  # Allow from any origin
        "Access-Control-Allow-Methods": "GET, OPTIONS",  # Allow specific methods
        "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allow specific headers
    }
    
def post_auth_header():
    return  {
        "Access-Control-Allow-Origin": "*",  # Allow from any origin
        "Access-Control-Allow-Methods": "POST, OPTIONS",  # Allow specific methods
        "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allow specific headers
    }

def put_auth_header():
    return  {
        "Access-Control-Allow-Origin": "*",  # Allow from any origin
        "Access-Control-Allow-Methods": "PUT, OPTIONS",  # Allow specific methods
        "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allow specific headers
    }

def delete_auth_header():
    return  {
        "Access-Control-Allow-Origin": "*",  # Allow from any origin
        "Access-Control-Allow-Methods": "DELETE, OPTIONS",  # Allow specific methods
        "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allow specific headers
    }