# Function Plugins Util

Adds the ability to plug functions into any label/functions

# Documentation:

## Functions:

### `submod_utils.getAndRunFunctions()`:
Gets and runs functions within the key provided

##### IN:
- key - Key to retrieve functions from
  - If `None`, we'll assume the function that called this method
  - (Default: `None`)

(**NOTE:** This does not need to be called manually, labels will always automatically call this. If you want to be able to plug into a *function*, then it must be called manually)

### `submod_utils.registerFunction()`:
Registers a function to the function_plugins dict

**NOTE:** Does **NOT** allow overwriting of existing functions in the dict

**NOTE:** Function must be callable

**NOTE:** This can also be done via the function decorator:
```python
@store.submod_utils.functionplugin(key, args=[], auto_error_handling=True, priority=DEF_PRIORITY)
```

##### IN:
- key - key to add the function to
- _function - function to add
- args - list of args (must be in order) to pass to the function
  - (Default: `[]`)
- auto_error_handling - Whether or not the function plugin caller should handle errors automatically
  - NOTE: This should only be set to False for functions which `renpy.call` or `renpy.jump`
  - (Default: `True`)
- priority - the priority level to run this function (the lower the number, the earlier it runs)
  - (Defualt: `0`)

##### OUT:
- `True` if the function was registered successfully
- `False` otherwise

### `submod_utils.getArgs()`:
Gets args for the given function at the given key

##### IN:
- key - key to retrieve the function from
- _function - function to retrieve args from

##### OUT:
- `list` of args if the function is present
- If function is not present, `None` is returned

### `submod_utils.setArgs()`:
Sets args for the given function at the key

##### IN:
- key - key that the function's function dict is stored in
- _function - function to set the args
- args - list of args (must be in order) to pass to the function (Default: `[]`)

##### OUT:
- `True` if args were set successfully
- `False` if not

### `submod_utils.unregisterFunction()`:
Unregisters a function from the function_plugins dict

##### IN:
- key - key the function we want to unregister is in
- _function - function we want to unregister

#### OUT:
- `True` if function was unregistered successfully
- `False` otherwise

## Global variables:

### `submod_utils.last_label`:
- The last label we were on

### `submod_utils.current_label`:
- The current label we're on

### `submod_utils.DEF_PRIORITY`:
- Default priority level for function plugins (0)

### `submod_utils.JUMP_CALL_PRIORITY`:
- Priority for functions which will call or jump to labels (999)

### `submod_utils.PRIORITY_SORT_KEY`:
- Lambda expression to sort function plugins by priority level

## Additional Note:
- Errors which happen via plugged in functions will *not* crash MAS, they will be logged into the `mas_log.txt` file.