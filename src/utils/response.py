from typing import Optional, Union, List

from fastapi.responses import UJSONResponse as Response


class UJSONResponse(Response):
    def __init__(
            self,
            message: str,
            status_code: int,
            data: Optional[Union[dict, List[dict]]] = None):
        response = dict(
            message=message,
            status_code=status_code,
            data=data,
        )
        super().__init__(response, status_code)
