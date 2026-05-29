
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class IntelReporter:
    @staticmethod
    def render_dashboard(data, title_source, keywords_data=None):
        profile = data.get("profile", {})
        analysis = data.get("account_analysis", {})
        stats = data.get("profile_stats", {})

        # 1. Identity Panel Box
        overview = (
            f"[bold cyan]🎯 Target Username :[/bold cyan] {profile.get('username')}\n"
            f"[bold cyan]📛 Full Identity    :[/bold cyan] {profile.get('full_name', 'N/A')}\n"
            f"[bold cyan]🔗 Profile URL     :[/bold cyan] {profile.get('profile_url')}\n"
            f"[bold cyan]📝 Biography       :[/bold cyan] [dim white]{profile.get('biography', 'No Bio Data')}[/dim white]\n"
            f"[bold cyan]🛡️ Verification    :[/bold cyan] {'✅ Verified Account' if analysis.get('verified') else '❌ Unverified Identity'}\n"
            f"[bold cyan]💼 Account Type    :[/bold cyan] {'Business/Creator' if analysis.get('business_account') else 'Personal Account'}\n"
            f"[bold cyan]🔒 Privacy Guard   :[/bold cyan] {'🔒 Private (High Restriction)' if analysis.get('private') else '🔓 Public (Accessible)'}"
        )
        console.print(Panel(overview, title=f"[bold red]🔍 {title_source}[/bold red]", border_style="yellow"))

        # 2. Metrics Table
        stats_table = Table(title="📈 METRICS SYSTEMS", border_style="cyan", title_style="bold magenta")
        stats_table.add_column("Followers (Reach)", justify="center", style="bold green")
        stats_table.add_column("Following (Network)", justify="center", style="bold yellow")
        stats_table.add_column("Total Posts (Activity)", justify="center", style="bold blue")
        stats_table.add_row(stats.get("followers"), stats.get("following"), stats.get("posts"))
        console.print(stats_table)

        # 3. Dynamic Keyword Weights Render
        if keywords_data and keywords_data.get("keywords"):
            kw_table = Table(title="🔤 EXTRACTED KEYWORD WEIGHTS", border_style="green", title_style="bold green")
            kw_table.add_column("Keyword Token", justify="left", style="bold white")
            kw_table.add_column("Frequency Count", justify="center", style="bold yellow")
            
            for item in keywords_data.get("keywords", []):
                kw_table.add_row(f"📍 {item[0]}", str(item[1]))
            console.print(kw_table)
          
