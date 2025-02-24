from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.box import ROUNDED
import json
import os
from typing import Dict, Any

class UIFormatter:
    def __init__(self):
        self.console = Console()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self, title: str) -> None:
        """Display a header with the given title"""
        self.clear_screen()
        self.console.print(Panel.fit(
            title,
            border_style="bold blue",
            padding=(1, 2),
            box=ROUNDED
        ))

    def display_json(self, data: Dict[str, Any], title: str) -> None:
        """Display formatted JSON data with a title"""
        json_str = json.dumps(data, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai")
        
        self.console.print(Panel(
            syntax,
            title=f"[bold]─ {title} ─[/bold]",
            border_style="blue",
            padding=(1, 2),
            box=ROUNDED
        ))

    def display_menu(self, options: Dict[str, str]) -> None:
        """Display a menu with numbered options"""
        table = Table(show_header=False, box=None)
        
        for key, value in options.items():
            table.add_row(f"[bold blue][{key}][/bold blue]", value)
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")

    def display_jwt_details(self, header: Dict[str, Any], payload: Dict[str, Any], signature: str) -> None:
        """Display complete JWT details"""
        self.clear_screen()
        self.display_header("JWT DETAILS")
        self.console.print("\n[bold green]✓ Valid JWT Format[/bold green]\n")
        
        # Display header
        self.display_json(header, "HEADER")
        
        # Display payload
        self.display_json(payload, "PAYLOAD")
        
        # Display signature
        self.console.print(Panel(
            signature,
            title="[bold]─ SIGNATURE ─[/bold]",
            border_style="blue",
            padding=(1, 2),
            box=ROUNDED
        ))
        
        self.console.print(f"\nAlgorithm: [bold]{header.get('alg', 'none')}[/bold]")

    def display_success(self, message: str) -> None:
        """Display a success message"""
        self.console.print(f"\n[bold green]✓ {message}[/bold green]")

    def display_error(self, message: str) -> None:
        """Display an error message"""
        self.console.print(f"\n[bold red]✗ {message}[/bold red]")

    def display_warning(self, message: str) -> None:
        """Display a warning message"""
        self.console.print(f"\n[bold yellow]! {message}[/bold yellow]")

    def display_input_prompt(self, message: str) -> None:
        """Display an input prompt"""
        self.console.print(f"\n[bold blue]> {message}[/bold blue]")

    def display_new_jwt(self, jwt_token: str) -> None:
        """Display a newly generated JWT token"""
        self.clear_screen()
        self.display_header("GENERATE NEW JWT")
        
        self.console.print("\nNew JWT:")
        self.console.print(Panel(
            jwt_token,
            border_style="green",
            padding=(1, 2),
            box=ROUNDED
        ))
        
        self.display_success("JWT copied to clipboard!")