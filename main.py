import asyncio
import aiohttp
from rich import print
from rich.progress import Progress
from rich.table import Table
from rich.console import Console

class PasswordGenerator:
    def __init__(self):
        self.generate_password_url = 'https://bot-hosting.net/api/newPassword'
        self.font_url = 'https://cdn.jsdelivr.net/npm/fork-awesome@1.1.7/fonts/forkawesome-webfont.woff2?v=1.1.7'
        self.headers = {
            'authority': 'bot-hosting.net',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization': 'YOUR AUTH TOKEN FROM BOT-HOSTING.NET',  # ---> Token<---
            'origin': 'https://bot-hosting.net',
            'referer': 'https://bot-hosting.net/panel/settings',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'cookie': '_ga=GA1.1.1490463030.1730505490; _lr_env_src_ats=false; ncmp.domain=bot-hosting.net; na-unifiedid_cst=TyylLI8srA%3D%3D; na-unifiedid=%7B%22TDID%22%3A%22dd4ff050-2e73-4131-9b7b-72096db06684%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-10-02T18%3A01%3A05%22%7D; cf_clearance=_SstwP9ckc5gtFecNKnOy8P5wJBvS3qN5uxAVLGXp6M-1730659424-1.2.1.1-N0JCf9CzlOuE4Lmcg8TFhlLdqIHE15pKE0IWOhf.YT5endhlXsO9_Rc3IhnWL4KJ3cJIv_mx8fauCOS3pfN08lNavLwLxOAOZuAc6fq3ybQ73xypDEvzHIc4a5axqWkyRT8UiFeqs8gyYXi0.uqaBiguYSHeueHCEGxPxJfP84H.HhePL6lA75U28ZxYX4jgVImiG7JGqEK.V36Pd0M9buxMD_qfY7F6U.zAznkufiIXcd7diTqIFsGJmMUQ9BJAlfbKqPRZsJTnilh8TXTv3RhZEVm_qasBe6ppJxxsnkGwPc_uE6BvDLqKUjaNwiV_0Tp20mJanRBPOI_poE69tvv5LvEfg75SyJi0KOHSnkvuxyG4uXU0zaGvRi9DSOyS7QkknXvfVwvx0w_uAZybO1nq.yEoV5_KS9jCVBmFy0n5aQhWh4.qltbwQvzqhVi9; _lr_retry_request=true; _ga_S0VHSF9NEZ=GS1.1.1730659432.3.0.1730659433.0.0.0; cto_bundle=nmvWzl92ZFN5N0lJWFY1Um1XeUtBZXBrMmFub2xJQkRpVXd1JTJGOExhNTBWTGRaMUljaGt1VnZpN2ZLaE1yNkNlelpQa2V6SnNkT1hqV254RlZDTFA4M3BiZWZJeWVUYkRqOE1EJTJCd3ZKZjhZQzFXZEVPRFRZQWFJbHZhcldjdlRqczRzM1VuJTJCdW5rUHZiUDdSWnlxQyUyQmZZMVZkQSUzRCUzRA; cto_bidid=XOAANF93Q0ladkdKcEFFa055cnNjVzFxdGFQN1A5JTJCNWdITUtTa0RlclkzcDlHNnlJbUZRQlJYblklMkZqZEM2NUdLR2VWUWJrMU5EJTJGRXhKWkNzVEhXVG41OUdiVEJtR3paQ2d5aGJHYWVDOCUyRkRaZVBGRVV0aDgyUk5aaHJXb2o4ZFFDdHRq',  # Add your cookie man
        }
        self.console = Console()
        self.table = Table(show_header=True, header_style="bold magenta")
        self.table.add_column("REQUEST FROM SERVER MESSAGE:")
        self.table.add_column("STATUS OF REQUESTS")
        self.table.add_column("RESULTS OF SERVER")

    async def generate_password(self, session, task_id, progress_task, progress):
        try:
            async with session.post(self.generate_password_url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    password = data.get('password', 'No password provided')
                    self.table.add_row(f"Task {task_id}", "[green]Success[/green]", f"[V]{password}")
                else:
                    self.table.add_row(f"Task {task_id}", "[yellow]Failed[/yellow]", f"Status Code: {response.status}")
        except Exception as e:
            self.table.add_row(f"Task {task_id}", "[red]Failed[/red]", f"Error: {e}")
        finally:
            progress.update(progress_task, advance=1)

    async def download_font(self, session):
        try:
            async with session.get(self.font_url, headers={'Referer': ''}) as response:
                if response.status == 200:
                    font_data = await response.read()
                    with open("forkawesome-webfont.woff2", "wb") as f:
                        f.write(font_data)
                    print("[green]Font downloaded successfully.[/green]")
                else:
                    print("[yellow]Failed to download font.[/yellow]")
        except Exception as e:
            print(f"[red]Error downloading font:[/red] {e}")

    async def run_tasks(self):
        async with aiohttp.ClientSession() as session:
            with Progress() as progress:
                progress_task = progress.add_task("[cyan]Generating passwords...", total=100)
                tasks = [self.generate_password(session, i, progress_task, progress) for i in range(1, 101)]
                await asyncio.gather(*tasks)
                self.console.print(self.table)
                if any("Success" in row[1] for row in self.table.rows):
                    await self.download_font(session)

async def main():
    generator = PasswordGenerator()
    await generator.run_tasks()

asyncio.run(main())
