"""Common utility functions"""

from types import NoneType
from typing import Dict, Optional, Type, Union, get_args, get_origin, TypeVar

T = TypeVar("T")


def unwrap(wrapped: Optional[T], default: T = None) -> T:
    """Unwrap function for Optionals."""
    if wrapped is None:
        return default

    return wrapped


def coalesce(*args):
    """Coalesce function for multiple unwraps."""
    return next((arg for arg in args if arg is not None), None)


def filter_none_values(collection: Union[dict, list]) -> Union[dict, list]:
    """Remove None values from a collection."""

    if isinstance(collection, dict):
        return {
            k: filter_none_values(v) for k, v in collection.items() if v is not None
        }
    elif isinstance(collection, list):
        return [filter_none_values(i) for i in collection if i is not None]
    else:
        return collection


def merge_dict(dict1: Dict, dict2: Dict) -> Dict:
    """Merge 2 dictionaries"""
    for key, value in dict2.items():
        if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
            merge_dict(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge an arbitrary amount of dictionaries"""
    result = {}
    for dictionary in dicts:
        result = merge_dict(result, dictionary)

    return result

def deep_merge_config(base_dict: dict, override_dict: dict) -> dict:
    """
    Merge Dict but filter not none.
    """
    merged = base_dict.copy()
    for key, value in override_dict.items():
        if value is not None: # Only merge not None
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = deep_merge_config(merged[key], value)
            else:
                merged[key] = value
    return merged


def flat_map(input_list):
    """Flattens a list of lists into a single list."""

    return [item for sublist in input_list for item in sublist]


def is_list_type(type_hint) -> bool:
    """Checks if a type contains a list."""

    if get_origin(type_hint) is list:
        return True

    # Recursively check for lists inside type arguments
    type_args = get_args(type_hint)
    if type_args:
        return any(is_list_type(arg) for arg in type_args)

    return False


def unwrap_optional_type(type_hint) -> Type:
    """
    Unwrap Optional[type] annotations.
    This is not the same as unwrap.
    """

    if get_origin(type_hint) is Union:
        args = get_args(type_hint)
        if NoneType in args:
            for arg in args:
                if arg is not NoneType:
                    return arg

    return type_hint


def calculate_rope_alpha(base_seq_len: int, target_seq_len: int):
    """
    Converts a given max sequence length to a rope alpha value.

    Args:
        base_seq_len: The model's configured sequence length.
        target_seq_len: The user-specified max sequence length.
    """

    # Get the ratio of the model's max sequence length to the target
    ratio = target_seq_len / base_seq_len

    # Default to a 1 alpha if the sequence length is ever less
    # than or equal to 1
    if ratio <= 1.0:
        alpha = 1
    else:
        alpha = -0.13436 + 0.80541 * ratio + 0.28833 * ratio**2
    return alpha
