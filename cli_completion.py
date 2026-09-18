from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

Completer = Callable[[], Iterable[str]]
SUPPORTED_SHELLS = ("bash", "zsh", "fish")


@dataclass(frozen=True, slots=True)
class Option:
    name: str
    description: str = ""
    values: tuple[str, ...] = field(default_factory=tuple)
    completer: Completer | None = None


@dataclass(frozen=True, slots=True)
class Command:
    name: str
    description: str = ""
    options: tuple[Option, ...] = field(default_factory=tuple)
    subcommands: tuple[Command, ...] = field(default_factory=tuple)


def generate_completion(
    shell: str,
    app_name: str,
    commands: tuple[Command, ...],
) -> str:
    match shell.lower():
        case "bash":
            return _generate_bash(app_name, commands)
        case "zsh":
            return _generate_zsh(app_name, commands)
        case "fish":
            return _generate_fish(app_name, commands)
        case _:
            raise ValueError(f"unsupported shell: {shell}")


def current_shell(*, environment: Mapping[str, str] | None = None) -> str | None:
    """Return the supported shell named by SHELL, when one is available."""
    shell = (environment or os.environ).get("SHELL", "")
    name = Path(shell).name.casefold()
    return name if name in SUPPORTED_SHELLS else None


def completion_path(
    shell: str,
    app_name: str,
    *,
    home: Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> Path:
    """Return the conventional user completion path for *shell*."""
    user_home = home or Path.home()
    values = environment or os.environ
    match shell.casefold():
        case "fish":
            config_home = Path(values.get("XDG_CONFIG_HOME", user_home / ".config"))
            return config_home / "fish" / "completions" / f"{app_name}.fish"
        case "bash":
            data_home = Path(values.get("XDG_DATA_HOME", user_home / ".local" / "share"))
            return data_home / "bash-completion" / "completions" / app_name
        case "zsh":
            return _zsh_function_path(user_home, values) / f"_{app_name}"
        case _:
            raise ValueError(f"unsupported shell: {shell}")


def _zsh_function_path(home: Path, environment: Mapping[str, str]) -> Path:
    """Find Zsh's first user-level function directory without reading shell config."""
    shell_environment = {**os.environ, **environment, "HOME": str(home)}
    try:
        completed = subprocess.run(
            ["zsh", "-fc", "print -rl -- $fpath"],
            text=True,
            capture_output=True,
            check=True,
            timeout=5,
            env=shell_environment,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        completed = None
    if completed is not None:
        for value in completed.stdout.splitlines():
            candidate = Path(value)
            if candidate.is_relative_to(home):
                return candidate
    data_home = Path(environment.get("XDG_DATA_HOME", home / ".local" / "share"))
    return data_home / "zsh" / "site-functions"


def install_completion(
    shell: str,
    app_name: str,
    commands: tuple[Command, ...],
    *,
    home: Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> tuple[Path, bool]:
    """Install completion once, returning its path and whether it was created."""
    target = completion_path(shell, app_name, home=home, environment=environment)
    script = generate_completion(shell, app_name, commands)
    if target.exists():
        created = False
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        created = True
    if created or target.read_text(encoding="utf-8") != script:
        target.write_text(script, encoding="utf-8")
    _install_shell_loader(shell, target, home=home)
    return target, created


def _install_shell_loader(shell: str, completion: Path, *, home: Path | None = None) -> None:
    """Add a single idempotent completion loader to the shell startup file."""
    user_home = home or Path.home()
    match shell.casefold():
        case "bash":
            startup = user_home / ".bashrc"
            loader = f'[[ -r "{completion}" ]] && source "{completion}"'
        case "zsh":
            startup = user_home / ".zshrc"
            loader = f'[[ -r "{completion}" ]] && source "{completion}"'
        case _:
            return
    marker = f"# {completion.name} completion"
    block = f"\n{marker}\n{loader}\n"
    content = startup.read_text(encoding="utf-8") if startup.exists() else ""
    if marker not in content:
        startup.parent.mkdir(parents=True, exist_ok=True)
        startup.write_text(content.rstrip() + block, encoding="utf-8")


def install_completions(
    app_name: str,
    commands: tuple[Command, ...],
) -> tuple[tuple[str, Path, bool], ...]:
    """Install completion for every supported shell."""
    return tuple(
        (shell, *install_completion(shell, app_name, commands)) for shell in SUPPORTED_SHELLS
    )


def is_completion_installed(
    shell: str | None,
    app_name: str,
    *,
    home: Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> bool:
    """Return whether a completion file exists for the selected shell."""
    return (
        shell is not None
        and completion_path(shell, app_name, home=home, environment=environment).is_file()
    )


def complete_values(
    commands: tuple[Command, ...],
    command_name: str | tuple[str, ...],
    option_name: str,
) -> tuple[str, ...]:
    path = (command_name,) if isinstance(command_name, str) else command_name
    command = _find_command(commands, path)

    if command is None:
        return ()

    option = next(
        (option for option in command.options if option.name == option_name),
        None,
    )

    if option is None:
        return ()

    if option.completer is not None:
        return tuple(dict.fromkeys(str(value) for value in option.completer()))

    return option.values


def handle_completion(
    argv: list[str],
    app_name: str,
    commands: tuple[Command, ...],
) -> bool:
    if not argv or argv[0] != "completion":
        return False

    if len(argv) == 1:
        for shell, path, created in install_completions(app_name, commands):
            message = "Installed" if created else "Completion already exists"
            print(f"{shell}: {message}: {path}")
        return True

    if len(argv) >= 4 and argv[1] == "values":
        values = complete_values(
            commands=commands,
            command_name=tuple(argv[2:-1]),
            option_name=argv[-1],
        )

        print("\n".join(values))
        return True

    raise SystemExit(
        f"Usage:\n  {app_name} completion\n  {app_name} completion values <command> <option>"
    )


def _find_command(
    commands: tuple[Command, ...],
    path: tuple[str, ...],
) -> Command | None:
    if not path:
        return None
    current = next((command for command in commands if command.name == path[0]), None)
    for name in path[1:]:
        if current is None:
            return None
        current = next((command for command in current.subcommands if command.name == name), None)
    return current


def _generate_bash(
    app_name: str,
    commands: tuple[Command, ...],
) -> str:
    function_name = f"_{_sanitize(app_name)}_completion"

    visible_commands = tuple(command for command in commands if command.name != "completion")
    root_commands = " ".join(command.name for command in visible_commands)

    command_cases = []

    for command in visible_commands:
        available = [
            *(subcommand.name for subcommand in command.subcommands),
            *(option.name for option in command.options),
        ]

        value_cases = []

        for option in command.options:
            if option.completer is not None:
                source = f"$({app_name} completion values {command.name} {option.name})"

                value_cases.append(
                    f"""            {option.name})
                COMPREPLY=( $(compgen -W "{source}" -- "$cur") )
                return
                ;;"""
                )

            elif option.values:
                values = " ".join(option.values)

                value_cases.append(
                    f"""            {option.name})
                COMPREPLY=( $(compgen -W "{values}" -- "$cur") )
                return
                ;;"""
                )

        command_cases.append(
            f"""        {command.name})
            case "$prev" in
{chr(10).join(value_cases)}
            esac

            COMPREPLY=( $(compgen -W "{" ".join(available)}" -- "$cur") )
            return
            ;;"""
        )

    return f"""\
{function_name}() {{
    local cur prev command

    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"

    if (( COMP_CWORD == 1 )); then
        COMPREPLY=( $(compgen -W "{root_commands}" -- "$cur") )
        return
    fi

    command="${{COMP_WORDS[1]}}"

    case "$command" in
{chr(10).join(command_cases)}
    esac
}}

complete -F {function_name} {app_name}
"""


def _generate_zsh(
    app_name: str,
    commands: tuple[Command, ...],
) -> str:
    function_name = f"_{_sanitize(app_name)}"

    visible_commands = tuple(command for command in commands if command.name != "completion")
    root_commands = " ".join(
        _zsh_entry(command.name, command.description) for command in visible_commands
    )

    command_cases = []

    for command in visible_commands:
        entries = [
            *(
                _zsh_entry(
                    subcommand.name,
                    subcommand.description,
                )
                for subcommand in command.subcommands
            ),
            *(
                _zsh_entry(
                    option.name,
                    option.description,
                )
                for option in command.options
            ),
        ]

        value_cases = []

        for option in command.options:
            if option.completer is not None:
                value_cases.append(
                    f"""                {option.name})
                    local -a values
                    values=("${{(@f)$({app_name} completion values {command.name} {option.name})}}")
                    _describe "value" values
                    return
                    ;;"""
                )

            elif option.values:
                values = " ".join(option.values)

                value_cases.append(
                    f"""                {option.name})
                    _values "value" {values}
                    return
                    ;;"""
                )

        command_cases.append(
            f"""        {command.name})
            case "$words[CURRENT-1]" in
{chr(10).join(value_cases)}
            esac

            _values "{command.name}" {" ".join(entries)}
            ;;"""
        )

    fallback_function = f"{function_name}_fallback"
    return f"""\
#compdef {app_name}

{function_name}() {{
    if (( CURRENT == 2 )); then
        _values "command" {root_commands}
        return
    fi

    case "$words[2]" in
{chr(10).join(command_cases)}
    esac
}}

{fallback_function}() {{
    local command="${{words[2]}}"
    case "$command" in
{chr(10).join(_zsh_compctl_case(app_name, command) for command in visible_commands)}
    esac
    reply=({" ".join(command.name for command in visible_commands)})
}}

if (( $+functions[compdef] )); then
    compdef {function_name} {app_name}
else
    compctl -K {fallback_function} {app_name}
fi
"""


def _zsh_compctl_case(app_name: str, command: Command) -> str:
    options = " ".join(option.name for option in command.options)
    subcommands = " ".join(subcommand.name for subcommand in command.subcommands)
    values = f"{options} {subcommands}".strip()
    return f"""        {command.name})
            reply=({values})
            ;;"""


def _generate_fish(
    app_name: str,
    commands: tuple[Command, ...],
) -> str:
    lines = [
        f"complete -c {app_name} -f",
    ]

    for command in commands:
        if command.name == "completion":
            continue

        line = f"complete -c {app_name} -n '__fish_use_subcommand' -a '{command.name}'"

        if command.description:
            line += f" -d '{_escape_fish(command.description)}'"

        lines.append(line)

        command_condition = f"__fish_seen_subcommand_from {command.name}"

        for subcommand in command.subcommands:
            line = f"complete -c {app_name} -n '{command_condition}' -a '{subcommand.name}'"

            if subcommand.description:
                line += f" -d '{_escape_fish(subcommand.description)}'"

            lines.append(line)

        for option in command.options:
            line = f"complete -c {app_name} -n '{command_condition}' -a '{option.name}'"

            if option.description:
                line += f" -d '{_escape_fish(option.description)}'"

            lines.append(line)

            value_condition = (
                f"{command_condition}; and test (commandline -opc)[-1] = '{option.name}'"
            )

            if option.completer is not None:
                values = f"({app_name} completion values {command.name} {option.name})"

                lines.append(f'complete -c {app_name} -n "{value_condition}" -a "{values}"')

            elif option.values:
                values = " ".join(option.values)

                lines.append(f"complete -c {app_name} -n \"{value_condition}\" -a '{values}'")

    return "\n".join(lines) + "\n"


def _zsh_entry(
    name: str,
    description: str,
) -> str:
    if not description:
        return name

    description = description.replace("'", "")
    return f"'{name}[{description}]'"


def _escape_fish(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _sanitize(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)
