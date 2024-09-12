import inspect


def validate_injectable(
    func_params: list[tuple[str, inspect.Parameter]], helper_classes: list
) -> list:
    """
    Validate if all parameters of a function are injectables.
    """
    for arg_name, param in func_params:
        # The annotation of the function parameter must be an injectable class.
        found = False
        for injectable in helper_classes:
            if param.annotation == injectable or arg_name == injectable.__name__:
                found = True
                break
        if not found:
            raise ValueError(
                f"Parameter '{arg_name}' should be an injectable or have a valid annotation."
            )
