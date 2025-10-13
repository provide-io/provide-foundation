# How to Build a CLI Application

`provide.foundation` makes building powerful, production-ready Command-Line Interfaces (CLIs) simple and declarative.

## The Core Concept

You define CLI commands as standard Python functions and use the `@register_command` decorator to expose them. The framework handles the rest: parsing arguments, generating help text, and dispatching to the correct function.

## A Minimal CLI

Here’s a complete, runnable CLI application.

```python
# my_cli.py
from provide.foundation import logger, pout, setup_telemetry
from provide.foundation.hub import Hub, register_command

@register_command
def greet(name: str, excited: bool = False):
    """
    Greets someone by name.

    :param name: The name of the person to greet.
    :param excited: If true, adds an exclamation mark for excitement.
    """
    greeting = f"Hello, {name}{'!' if excited else '.'}"
    logger.info("greeting_sent", name=name, was_excited=excited)
    pout(greeting, color="cyan")

if __name__ == "__main__":
    # Configure logging
    setup_telemetry()

    # The Hub discovers registered commands and builds the CLI
    hub = Hub()
    cli = hub.create_cli(name="my-cli", description="A demonstration CLI.")

    # Run the application
    cli()```

### How it Works

1.  `@register_command`: This decorator tells the `Hub` that the `greet` function is a CLI command.
2.  **Function Signature**: The framework inspects the function's parameters (`name`, `excited`) and type hints (`str`, `bool`) to automatically create CLI arguments and options.
    *   Parameters without default values (`name: str`) become **required arguments**.
    *   Parameters with default values (`excited: bool = False`) become **optional flags**.
3.  **Docstring**: The docstring is automatically used to generate the help text.
4.  `hub.create_cli()`: This method finds all registered commands and assembles them into a single, runnable `click` application.

### Running the CLI

```bash
# Get automatically generated help
$ python my_cli.py --help
Usage: my-cli [OPTIONS] COMMAND [ARGS]...

  A demonstration CLI.

Options:
  --help  Show this message and exit.

Commands:
  greet  Greets someone by name.

# Run the 'greet' command
$ python my_cli.py greet World
Hello, World.

# Use the optional flag
$ python my_cli.py greet "Awesome Developer" --excited
Hello, Awesome Developer!

# Get help for a specific command
$ python my_cli.py greet --help
Usage: my-cli greet [OPTIONS] NAME

  Greets someone by name.

Arguments:
  NAME  The name of the person to greet.  [required]

Options:
  --excited   If true, adds an exclamation mark for excitement.
  --help      Show this message and exit.
```
