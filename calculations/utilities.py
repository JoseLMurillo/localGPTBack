from nanoid import generate

#UTILITIES
def id_generator(size: int = 21) -> str:
    """
    Generate id with nanoid with a defined size.
    :param Size: Number of characters. default 21
    """
    return generate(size= size)