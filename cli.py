import click
import json
from typing import Optional, List
from pathlib import Path
from utils import AchievementDatabase
from exporters import ExportManager
from exceptions import DatabaseError, ValidationError

@click.group()
def cli():
    """Achievement Database Management CLI"""
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def add(file: str):
    """Add achievement from JSON file"""
    try:
        with open(file) as f:
            data = json.load(f)
        db = AchievementDatabase()
        db.add_achievement(data)
        click.echo(f"Successfully added achievement {data['id']}")
    except (ValidationError, DatabaseError) as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--role', help='Role type to filter by')
@click.option('--tags', multiple=True, help='Tags to filter by')
@click.option('--output', type=click.Path(), help='Output file path')
def query(role: Optional[str], tags: Optional[List[str]], output: Optional[str]):
    """Query achievements with filters"""
    try:
        db = AchievementDatabase()
        results = db.query_achievements(role_type=role, tags=tags)
        
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            click.echo(json.dumps(results, indent=2))
    except DatabaseError as e:
        click.echo(f"Error: {str(e)}", err=True)