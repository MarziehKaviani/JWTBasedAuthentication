from datetime import datetime

from pydantic import BaseModel, Field

from common.utils import BaseTime


class Event(BaseModel):
    """
    The base event.

    Parameters
    -----------
    - name `(str)`: The name or type of the event.
    - timestamp `(datetime, optional)`: Timestamp of when the event occurred.
    - source `(str, optional)`: Source or origin of the event.
    - serializer_format `(str, optional)`: supported formats are protobuf & flatbuffers. protobuf is defualt.
    """

    name: str
    timestamp: datetime = Field(
        default_factory=lambda: BaseTime().now())
    source: str
    serializer_format: str = 'protobuf'
