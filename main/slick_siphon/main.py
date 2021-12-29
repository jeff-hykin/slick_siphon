def siphon(*, when, is_true_for,):
    original_function = is_true_for
    if not hasattr(original_function, "__name__") or not hasattr(original_function, "__module__"):
        raise Exception(f'\n\n\nSorry siphon only works on functions that have both a .__name__ and .__module__\nthis happended when calling @siphon(\n    when={when},\n    is_true_for={is_true_for},\n)\n')
    parent_module_name     = original_function.__module__
    parent_module          = __import__(parent_module_name, fromlist = [parent_module_name])
    name_of_child_function = original_function.__name__
    if not hasattr(parent_module, name_of_child_function):
        raise Exception(f'\n\n\nSorry siphon looks up the original function using the is_true_for.__name__ and is_true_for.__module__\nI did that but it looks like the module doesnt have the name, so Im unable to find the original function\nthe this happended when calling @siphon(\n    when={when},\n    is_true_for={is_true_for},\n)\n    __module__: {parent_module}\n    __name__:{name_of_child_function}\n')
    def level_2_wrapper(target_func_after_siphoning):
        def level_1_wrapper(*args, **kwargs):
            # check condition
            if when(*args, **kwargs):
                return target_func_after_siphoning(*args, **kwargs)
            else:
                return original_function(*args, **kwargs)
        # force the module and name to match (allowing for double-siphoning the same function)
        level_1_wrapper.__module__ = parent_module_name
        level_1_wrapper.__name__ = name_of_child_function
        # mutate the original value to be the level_1_wrapper value
        setattr(parent_module, name_of_child_function, level_1_wrapper)
        return level_1_wrapper
    return level_2_wrapper
