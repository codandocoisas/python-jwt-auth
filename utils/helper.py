import uuid
from database.database_models import User

async def generate_uuid() -> uuid.uuid4:
    """
    UUID must be an unique identifier when user is being registered.
    once user creation is requested, this function will be charged on creating
    an unique uuid for the user
    """
    random_uuid = uuid.uuid4()
    id_exists = await User.get_by_id(random_uuid)
    
    while id_exists:
        random_uuid = uuid.uuid4()
        id_exists = await User.get_by_id(random_uuid)
    
    return random_uuid
    
    
    