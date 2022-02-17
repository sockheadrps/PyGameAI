from rich.table import Table
from rich.console import Console
from math import sqrt


def make_table(duration, won, lost, reward, str_multiplier, hp, robot_hp, hits):
	table = Table("Stats", min_width= 1000)
	table.add_column("Duration")
	table.add_column("Won")
	table.add_column("lost")
	table.add_column("Reward")
	table.add_column("str_multiplier")
	table.add_column("health")
	table.add_column("Robot health")
	table.add_column("Hit robot:")

	table.add_row("", str(duration), str(won), str(lost), str(reward), str(str_multiplier), str(hp), str(robot_hp), str(hits))
	console = Console()
	console.print(table)
