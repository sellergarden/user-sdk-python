import inspect
from functools import wraps

from sellergarden_sdk import ExecEnvironment
from sellergarden_sdk.helpers import (
    AppKVStore,
    BotEventType,
    DigikalaSellerAPI,
    helper_classes,
)
from sellergarden_sdk.pre_process import validate_injectable
from sellergarden_sdk.widgets import components

registered_functions = {"apis": [], "schedules": [], "widgets": [], "bots": []}


def Api(endpoint=None):
    """
    API decorator that injects dependencies into the API function.
    It uses an `ExecEnvironment` object for API key and DB URL, and only passes
    required dependencies to the user function.
    """
    if endpoint != None and not endpoint.startswith("/"):
        raise ValueError("Endpoint should start with a forward slash '/'.")

    def decorator(func):
        """
        Decorator function that wraps the API function.
        """
        # Check all args of the function are injectables except first one which is api post data
        func_params = list(inspect.signature(func).parameters.items())[1:]
        # Check all args of the function are injectables.
        validate_injectable(func_params, helper_classes)

        # add function to triggers
        registered_functions["apis"].append({"name": func, "endpoint": endpoint})

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Running API endpoint '{func.__name__}'...")
            # Extract environment object
            environment = kwargs.get("environment")

            if not isinstance(environment, ExecEnvironment):
                raise ValueError(
                    "Environment object is required to initialize injectables"
                )

            # Automatically inject dependencies based on the function signature.
            resolved_injectables = {}
            func_params = list(inspect.signature(func).parameters.items())[1:]
            for arg_name, param in func_params:
                if param.annotation == DigikalaSellerAPI:
                    injectable_instance = DigikalaSellerAPI(environment)
                    resolved_injectables[arg_name] = injectable_instance
                elif param.annotation == AppKVStore:
                    injectable_instance = AppKVStore(environment)
                    resolved_injectables[arg_name] = injectable_instance

            # Drop the `environment` from kwargs before passing to user function
            if "environment" in kwargs:
                del kwargs["environment"]

            # API execution with injectables
            return func(*args, **{**kwargs, **resolved_injectables})

        return wrapper

    return decorator


def Widget(widget_id):
    """
    Widget decorator that injects dependencies into the widget building function.
    It uses an `ExecEnvironment` object for API key and DB URL, and only passes
    required dependencies to the user function.
    """

    def decorator(func):
        """
        Decorator function that wraps the widget building function.
        """
        # Check environment variables to see if the code is running in pre-process mode
        # Skip the first parameter (widget) and check the rest for injectables
        func_params = list(inspect.signature(func).parameters.items())[1:]
        # Check all args of the function are injectables.
        validate_injectable(func_params, helper_classes)

        # add function to triggers
        registered_functions["widgets"].append({"name": func, "widget_id": widget_id})

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Running widget '{func.__name__}'...")
            # Create a new instance of Widget and inject it as the first argument
            widget_instance = components.WidgetComponent(widget_id)

            # Extract environment object
            environment = kwargs.get("environment")

            if not isinstance(environment, ExecEnvironment):
                raise ValueError(
                    "Environment object is required to initialize injectables"
                )

            # Automatically inject dependencies, skipping the first parameter (widget)
            resolved_injectables = {}
            func_params = list(inspect.signature(func).parameters.items())[
                1:
            ]  # Skip widget parameter
            for arg_name, param in func_params:
                if param.annotation == DigikalaSellerAPI:
                    injectable_instance = DigikalaSellerAPI(environment)
                    resolved_injectables[arg_name] = injectable_instance
                elif param.annotation == AppKVStore:
                    injectable_instance = AppKVStore(environment)
                    resolved_injectables[arg_name] = injectable_instance

            # Drop the `environment` from kwargs before passing to the user function
            if "environment" in kwargs:
                del kwargs["environment"]

            # Call the original function with widget as the first argument, and injectables for the rest
            try:
                widget = func(
                    widget_instance, *args, **{**kwargs, **resolved_injectables}
                )
                return widget.render()
            except:
                return "<b style='color: red;'>An error occurred while rendering the widget</b>"

        return wrapper

    return decorator


def Schedule(cron_expression, retry_on_failure=True, timeout=None):
    """
    Scheduler decorator that injects dependencies into the task function.
    It uses an `ExecEnvironment` object for API key and DB URL, and only passes
    required dependencies to the user function.
    """

    def decorator(func):
        """
        Decorator function that wraps the scheduled task function.
        """
        # Check environment variables that if code is running in pre-process mode
        print("registering scheduled task...")
        # Check all args of the function are injectables.
        func_params = list(inspect.signature(func).parameters.items())
        # Check all args of the function are injectables.
        validate_injectable(func_params, helper_classes)

        # add function to triggers
        registered_functions["schedules"].append(
            {
                "name": func,
                "cron_expression": cron_expression,
                "retry_on_failure": retry_on_failure,
                "timeout": timeout,
            }
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract environment object
            environment = kwargs.get("environment")

            if not isinstance(environment, ExecEnvironment):
                raise ValueError(
                    "Environment object is required to initialize injectables"
                )

            # Automatically inject dependencies based on the function signature.
            resolved_injectables = {}
            for arg_name, param in inspect.signature(func).parameters.items():
                if param.annotation == DigikalaSellerAPI:
                    injectable_instance = DigikalaSellerAPI(environment)
                    resolved_injectables[arg_name] = injectable_instance
                elif param.annotation == AppKVStore:
                    injectable_instance = AppKVStore(environment)
                    resolved_injectables[arg_name] = injectable_instance

            # Drop the `environment` from kwargs before passing to user function
            if "environment" in kwargs:
                del kwargs["environment"]

            if retry_on_failure:
                print(f"Retry on failure is enabled.")
            if timeout:
                print(f"Task will timeout after {timeout} seconds.")

            # Task execution with injectables
            try:
                func(*args, **{**kwargs, **resolved_injectables})
            except Exception as e:
                if retry_on_failure:
                    print(f"Error: {e}, retrying task...")
                else:
                    print(f"Error: {e}, not retrying.")

        return wrapper

    return decorator


def Bot(event_type: BotEventType):
    """
    Bot decorator that registers a function to listen on a specific event type.
    """

    def decorator(func):
        """
        Decorator function that wraps the event handler function.
        """
        # Check environment variables that if code is running in pre-process mode
        print("registering bot event handler...")
        # Check all args of the function are injectables.
        func_params = list(inspect.signature(func).parameters.items())
        # Check all args of the function are injectables.
        validate_injectable(func_params, helper_classes)

        # add function to triggers
        registered_functions["schedulers"].append(
            {
                "name": func,
                "event_type": event_type,
            }
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Call the original function with the provided arguments
            func(*args, **kwargs)

        return wrapper

    return decorator
