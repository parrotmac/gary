import argparse
import gzip
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import boto3
import botocore
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv()


def require_bucket_credentials():
    envvars = {
        "CAMINO_ARTIFACT_S3_ACCESS_KEY": os.getenv("CAMINO_ARTIFACT_S3_ACCESS_KEY"),
        "CAMINO_ARTIFACT_S3_SECRET_KEY": os.getenv("CAMINO_ARTIFACT_S3_SECRET_KEY"),
        "CAMINO_ARTIFACT_S3_BUCKET_NAME": os.getenv("CAMINO_ARTIFACT_S3_BUCKET_NAME"),
        "CAMINO_ARTIFACT_S3_ENDPOINT": os.getenv("CAMINO_ARTIFACT_S3_ENDPOINT"),
    }
    is_missing = False
    for envvar, value in envvars.items():
        if value is None:
            is_missing = True
            sys.stderr.write(f"Missing required envvar {envvar}\n")
    if is_missing:
        sys.exit(1)
    return envvars


def new_s3_connection():
    creds = require_bucket_credentials()
    session = boto3.session.Session()
    client = session.client(
        "s3",
        config=botocore.config.Config(s3={"addressing_style": "virtual"}),
        region_name="sfo3",
        endpoint_url="https://sfo3.digitaloceanspaces.com",
        aws_access_key_id=creds["CAMINO_ARTIFACT_S3_ACCESS_KEY"],
        aws_secret_access_key=creds["CAMINO_ARTIFACT_S3_SECRET_KEY"],
    )
    bucket_name = creds["CAMINO_ARTIFACT_S3_BUCKET_NAME"]
    return client, bucket_name

def clone_database_from_pgdump_archive(list_sources, from_db, args, database_url):
    client, bucket_name = new_s3_connection()
    list_kwargs = {
        "Bucket": bucket_name,
    }
    if list_sources or from_db:
        list_kwargs["Prefix"] = f"{list_sources or from_db}"
    items = client.list_objects(**list_kwargs)["Contents"]

    if args._list:
        for obj in items:
            print("Object: {}".format(obj["Key"]))
    if (
        args._from
    ):  # To use a specific file, specify the full name of the file instead of just e.g. 'development'
        item = items[-1]
        item_key = item["Key"]
        temp_dir = tempfile.mkdtemp(prefix="db-clone-")
        destination_path = Path(temp_dir) / item_key
        client.download_file(
            Bucket=bucket_name,
            Key=item_key,
            Filename=str(destination_path),
        )
        if args.verbose:
            print(f"Downloaded {item_key} to {destination_path}")
        restore_sql = gzip.decompress(destination_path.read_bytes())
        result = subprocess.run(
            ["/usr/bin/env", "bash", "-c", f"psql {database_url}"],
            input=restore_sql,
            check=True,
            capture_output=True,
        )
        if args.verbose:
            print(result.stdout.decode())

def clone_database_from_live_instance(from_db, database_url, remote_db_envvar):
    try:
        if remote_db_envvar:
            remote_db_url = os.getenv(remote_db_envvar)
        else:
            remote_db_url = json.loads(Path(".secrets/database-credentials.json").read_bytes())["by_key"][from_db]

        subprocess.run(
            [
                "/usr/bin/env",
                "bash",
                "-c",
                f"pg_dump {remote_db_url} | psql {database_url}",
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            stdin=sys.stdin,
        )
    except KeyError:
        print(f"Database {from_db} not found in database-credentials.json")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading database-credentials.json: {e}")
        sys.exit(1)

secret_files = [
    ("database-credentials.json", ".secrets/database-credentials.json"),
    (".env", ".env"),
]

def main():
    parser = argparse.ArgumentParser(description="Development tooling.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output.")
    component_sp = parser.add_subparsers(dest="component")

    secrets_parser = component_sp.add_parser("secrets", help="Manage secrets.")
    secrets_action_parser = secrets_parser.add_subparsers(
        dest="action", help="Secrets action."
    )
    secrets_action_parser.add_parser("get", help="Get secrets from 1Password.")
    secrets_action_parser.add_parser("upload", help="Upload secrets to 1Password.")

    database_parser = component_sp.add_parser("database", help="Manipulate databases.")
    database_action_parser = database_parser.add_subparsers(
        dest="action", help="Database action."
    )
    database_cloner = database_action_parser.add_parser(
        "clone", help="Clone a database locally."
    )
    database_cloner.add_argument(
        "--from", dest="_from", type=str, help="Which database to clone."
    )
    database_cloner.add_argument(
        "--list", dest="_list", type=str, help="List available clone sources."
    )
    database_cloner.add_argument(
        "--using-archive-strategy",
        dest="_using_pgdump_archive",
        action="store_true",
        help="Restore from a pgdump archive instead of a live instance.",
    )
    database_cloner.add_argument(
        "--remote-db-envvar",
        dest="_remote_db_envvar",
        type=str,
        help="The environment variable containing the remote database URL. Skips the database-credentials.json file.",
    )

    args = parser.parse_args()

    match args.component:
        case "database":
            database_url = os.getenv("DATABASE_URL")
            if database_url is None:
                sys.stderr.write(f"Missing DATABASE_URL envvar\n")
                sys.exit(1)
            if args.verbose:
                print(f"DATABASE_URL: {database_url}")
            match args.action:
                case "clone":
                    if args._using_pgdump_archive:
                        list_sources = args._list
                        from_db = args._from
                        clone_database_from_pgdump_archive(list_sources, from_db, args, database_url)
                    else:
                        from_db = args._from
                        remote_db_envvar = args._remote_db_envvar
                        clone_database_from_live_instance(from_db, database_url, remote_db_envvar)

        case "secrets":
            match args.action:
                case "upload":
                    if input(
                        "Are you sure you want to upload secrets to 1Password? [y/N] "
                    ).lower() != "y":
                        print("Aborting.")
                        sys.exit(1)

                    for secret_file, secret_path in secret_files:
                        f = Path(secret_path).read_bytes()
                        try:
                            subprocess.run(
                                [
                                    "/usr/bin/env",
                                    "bash",
                                    "-c",
                                    f"op --account my.1password.com --vault Gary document edit {secret_file}",
                                ],
                                check=True,
                                input=f
                            )
                        except subprocess.CalledProcessError:
                            print(f"Failed to get {secret_file}, creating a new document...")
                            f.seek(0)
                            subprocess.run(
                                [
                                    "/usr/bin/env",
                                    "bash",
                                    "-c",
                                    f"op --account my.1password.com --vault Gary document create {secret_file}",
                                ],
                                check=True,
                                input=f,
                            )
                            print(f"Successfully uploaded {secret_file} to 1Password.")

                case "get":
                    for secret_file, secret_path in secret_files:
                        leading_dir = os.path.dirname(secret_path)
                        if leading_dir and not os.path.exists(leading_dir):
                            os.makedirs(leading_dir)
                        try:
                            subprocess.run(
                                [
                                    "/usr/bin/env",
                                    "bash",
                                    "-c",
                                    f"op --account my.1password.com --vault Gary document get {secret_file} > {secret_path}",
                                ],
                                check=True,
                            )
                        except subprocess.CalledProcessError:
                            print(f"Failed to get {secret_file}")
                            sys.exit(1)
                case _:
                    secrets_parser.print_help()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
