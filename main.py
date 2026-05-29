
import json
import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

# Modular Core Package Imports
from core.scanner import InstaLiveScanner
from core.analyzer import IntelAnalyzer
from core.reporter import IntelReporter

console = Console()

def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = (
        "[bold red]🕵️‍♂️ INSTA OSINT FRAMEWORK v3.5 (MODULAR) 🕵️‍♂️[/bold red]\n"
        "[bold white]Industrial-Grade Open Source Intelligence Framework[/bold white]\n"
        "[dim cyan]Architecture Split System Ready[/dim cyan]"
    )
    console.print(Panel(banner, expand=False, border_style="red", title_align="center"))

def show_loading_animation(task_name):
    with Progress(SpinnerColumn(spinner_name="dots"), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description=f"[bold yellow]{task_name}...[/bold yellow]", total=None)
        time.sleep(1.2)

def analyze_json_target(file_path):
    if not os.path.exists(file_path):
        console.print(f"\n[bold red]❌ Error:[/bold red] File '[yellow]{file_path}[/yellow]' root Folder mein nahi mili!")
        Prompt.ask("\n[bold white]Press Enter to return to Menu[/bold white]")
        return

    show_loading_animation("Parsing Local Database Subsystems")
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    # Local fallback bio data keyword extraction calculation
    bio_text = data.get("profile", {}).get("biography", "")
    if not bio_text and "keyword_analysis" in data:
        # custom backup map mapping
        kw_data = data.get("keyword_analysis")
    else:
        kw_data = IntelAnalyzer.extract_behavioral_keywords(bio_text)
        
    IntelReporter.render_dashboard(data, "TARGET LOCAL DATABASE RECORD", keywords_data=kw_data)
    Prompt.ask("[bold white]Investigation complete. Press Enter to return to Menu[/bold white]")

def live_target_scan():
    target = Prompt.ask("\n[bold red]🕵️‍♂️ Enter Target Username for Real Live Scan[/bold red]")
    if not target:
        return
        
    session_user = Prompt.ask("[bold white]Enter bypass Agent Username (Or Press Enter for Anonymous Mode)[/bold white]", default="")
    scanner = InstaLiveScanner()
    
    if session_user:
        show_loading_animation("Syncing Authentication Parameters")
        auth = scanner.setup_session(session_user)
        console.print(f"[dim yellow]{auth['msg']}[/dim yellow]\n")

    show_loading_animation(f"Intercepting Live Instagram Telemetry for @{target}")
    result = scanner.execute_live_intel(target)
    
    if result.get("status") == "error":
        console.print(f"\n[bold red]❌ Interception Blocked:[/bold red] {result.get('msg')}\n")
    else:
        console.print(f"\n[bold green]✅ Network Mapping Completed for @{target}![/bold green]")
        # Dynamic processing inside analytics hub
        bio = result.get("profile", {}).get("biography", "")
        kw_data = IntelAnalyzer.extract_behavioral_keywords(bio)
        
        IntelReporter.render_dashboard(result, "LIVE METADATA DUMP INTERCEPT", keywords_data=kw_data)
        
    Prompt.ask("\n[bold white]Press Enter to return to Menu[/bold white]")

def main_menu():
    while True:
        display_banner()
        console.print("[bold white]Select Operation Mode:[/bold white]")
        console.print(" [1] 📂 Parse Local JSON Intel File ([yellow]coding_with_naveen_20260529_123706.json[/yellow])")
        console.print(" [2] 🌐 Real-Time Live Profile Tracker (Instaloader Hub)")
        console.print(" [3] ❌ Terminate Session\n")
        
        choice = Prompt.ask("[bold red]OSINT-CLI >> [/bold red]", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            target_file = "coding_with_naveen_20260529_123706.json"
            analyze_json_target(target_file)
        elif choice == "2":
            live_target_scan()
        elif choice == "3":
            console.print("\n[bold red]Shutting down Framework safely. Stay Anonymous.[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
  
