from typing import List, Callable, Union

def listify(func: Callable[[any], any]) -> Callable[[List[any]], List[any]]:
    """Wrapper for making a function compatible with lists of objects.

    Args:
        func (Callable[[any], any]): the function to wrap

    Returns:
        Callable[[List[any]], List[any]]: the wrapped function that can handle lists of objects
    """    
    def wrapper(lst: Union[List[any], any]) -> Union[List[any], any]:
        if isinstance(lst, list):
            return [func(elem) for elem in lst]
        else:
            return func(lst)
    return wrapper
