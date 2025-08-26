def run_postgres_setup_inline():
    print("Running postgres setup inline")
    import subprocess
    import sys
    from pathlib import Path
    import click

    project_root = Path(__file__).resolve().parents[0] 
    sql_file = project_root / "db" / "local_postgres_db_setup.sql"
    container_name = "humblebridge-db-1"
    target_path = "/tmp/schema_setup.sql"

    click.echo(f"SQL file: {sql_file}")

    if not sql_file.exists():
        click.echo(f" ERROR: SQL file does not exist: {sql_file}")
        sys.exit(1)
    elif not sql_file.is_file():
        click.echo(f" ERROR: Expected a file, but found a directory: {sql_file}")
        sys.exit(1)

    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        click.echo(" ERROR: Docker is not running. Please start Docker first.")
        sys.exit(1)

    click.echo(f"📦 Copying {sql_file} to {container_name}:{target_path} ...")
    try:
        subprocess.run(["docker", "cp", str(sql_file), f"{container_name}:{target_path}"], check=True)
    except subprocess.CalledProcessError:
        click.echo(f"ERROR: Failed to copy SQL file. Does the container '{container_name}' exist and is running?")
        sys.exit(1)

    click.echo("🔧 Executing SQL in container...")
    try:
        subprocess.run(
            ["docker", "exec", "-i", container_name, "psql", "-U", "addy_rw", "-d", "humble_dev", "-f", target_path],
            check=True
        )
        click.echo(" SUCCESS: Database setup script executed successfully.")
    except subprocess.CalledProcessError:
        click.echo("ERROR: Failed to execute SQL inside the container.")
        sys.exit(1)
        
        
if __name__ == "__main__":
    run_postgres_setup_inline()