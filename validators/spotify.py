class SpotifyError(Exception):
    def __init__(self, message, status_code: int):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.status_code = status_code
        self.message = message


def raise_error(response_data):
    error = response_data.get('error', None)
    
    if error is not None:
        raise SpotifyError(error.get('message', None), error.get('status', 500))
