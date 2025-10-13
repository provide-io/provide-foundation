import datetime
import logging
import sys
from pathlib import Path

import attrs
import click
from dateutil.relativedelta import relativedelta
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

# Use a module-level logger
logger = logging.getLogger(__name__)


@attrs.define(frozen=True, slots=True)
class OriginalCommit:
    """Represents a commit from the source repository."""

    hexsha: str
    committed_datetime: datetime.datetime
    message: str


def setup_logging(level: str) -> None:
    """Configures the root logger for the application."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    # Configure root logger
    logging.basicConfig(level=log_level, handlers=[handler])


def get_source_commits(
    repo_path: Path, branch_name: str | None
) -> tuple[str, list[OriginalCommit]]:
    """
    Retrieves all commits from a specific branch in the source repository.

    Args:
        repo_path: The path to the source Git repository.
        branch_name: The name of the branch to read from. If None, uses the
                     active branch.

    Returns:
        A tuple containing the branch name used and a list of `OriginalCommit`
        objects, sorted from oldest to newest.
    """
    try:
        source_repo = Repo(repo_path)
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        logger.error(f"Error: Source path '{repo_path}' is not a valid Git repository.")
        raise click.Abort() from e

    if branch_name is None:
        try:
            branch_to_use = source_repo.active_branch.name
            logger.info(f"No branch specified. Using active branch: '{branch_to_use}'")
        except TypeError:  # Happens in detached HEAD state
            logger.error(
                "Source repository is in a detached HEAD state. "
                "Please specify a branch with --branch."
            )
            raise click.Abort()
    else:
        branch_to_use = branch_name
        logger.info(f"Using specified source branch: '{branch_to_use}'")

    logger.info(f"Reading commits from branch '{branch_to_use}' in '{repo_path}'...")
    try:
        commits_rev_chron = list(source_repo.iter_commits(branch_to_use))
    except GitCommandError as e:
        logger.error(f"Failed to read commits from branch '{branch_to_use}'.")
        logger.error(f"Please ensure the branch exists in '{repo_path}'. Details: {e}")
        raise click.Abort() from e

    if not commits_rev_chron:
        logger.warning(f"Branch '{branch_to_use}' has no commits. Nothing to do.")
        return branch_to_use, []

    source_commits = [
        OriginalCommit(
            hexsha=c.hexsha,
            committed_datetime=c.committed_datetime,
            message=c.message.split("\n")[0],
        )
        for c in commits_rev_chron
    ]

    # Reverse to get chronological order (oldest first)
    sorted_commits = sorted(source_commits, key=lambda c: c.committed_datetime)
    logger.info(f"Found {len(sorted_commits)} commits on branch '{branch_to_use}'.")
    return branch_to_use, sorted_commits


def create_snapshot_commits(
    source_path: Path,
    dest_path: Path,
    branch_to_process: str,
    commits: list[OriginalCommit],
) -> None:
    """
    Creates commits in 7-day increments in the destination repository using
    a fast, Git-native approach.
    """
    if not commits:
        return

    dest_repo = Repo.init(dest_path)
    logger.info(f"Initialized new empty repository at '{dest_path}'.")

    # Add the source repo as a remote to fetch its objects
    try:
        source_remote = dest_repo.create_remote("source", source_path.as_uri())
        logger.info(f"Fetching branch '{branch_to_process}' from '{source_path}'...")
        source_remote.fetch(branch_to_process)
        logger.info("Fetch complete.")
    except GitCommandError as e:
        logger.error(f"Failed to fetch from source repository: {e}")
        raise click.Abort() from e

    first_commit_date = commits[0].committed_datetime
    today = datetime.datetime.now(first_commit_date.tzinfo)

    current_span_start = first_commit_date
    commit_idx = 0

    while current_span_start <= today and commit_idx < len(commits):
        span_end_date = current_span_start + relativedelta(days=7)
        logger.info("-" * 70)
        logger.info(
            f"Processing 7-day span: {current_span_start.strftime('%Y-%m-%d')} to "
            f"{span_end_date.strftime('%Y-%m-%d')}"
        )

        commits_in_span = []
        while (
            commit_idx < len(commits)
            and commits[commit_idx].committed_datetime < span_end_date
        ):
            commits_in_span.append(commits[commit_idx])
            commit_idx += 1

        if commits_in_span:
            last_commit_in_span = commits_in_span[-1]
            logger.info(
                f"Found {len(commits_in_span)} commits in this span. "
                f"Using state from the last one: '{last_commit_in_span.hexsha[:7]}'"
            )

            # Get the corresponding commit object now present in the destination repo
            source_commit_obj = dest_repo.commit(last_commit_in_span.hexsha)

            # This is the key performance improvement:
            # Read the commit's tree directly into the index without touching
            # the working directory.
            logger.info(
                f"Reading tree '{source_commit_obj.tree.hexsha[:7]}' into index..."
            )
            dest_repo.git.read_tree(source_commit_obj.tree.hexsha)

            # Generate a detailed, multi-line commit message
            subject_line = (
                f"feat: Snapshot for 7-day period starting "
                f"{current_span_start.strftime('%Y-%m-%d')}"
            )
            body_lines = [
                f"This commit consolidates {len(commits_in_span)} original commits.",
                "",
                "Original commits included in this snapshot:",
            ]
            for c in commits_in_span:
                body_lines.append(f"- {c.hexsha[:7]}: {c.message}")

            commit_message = "\n\n".join([subject_line, "\n".join(body_lines)])

            logger.info(f"Creating commit with subject: \"{subject_line}\"")

            timestamp = int(span_end_date.timestamp())
            offset_delta = span_end_date.utcoffset()
            if offset_delta:
                total_seconds = offset_delta.total_seconds()
                hours = int(total_seconds / 3600)
                minutes = int(abs(total_seconds % 3600) / 60)
                offset_string = f"{hours:+03d}{minutes:02d}"
                commit_date_str = f"{timestamp} {offset_string}"
            else:
                commit_date_str = str(timestamp)

            logger.info(
                f"Setting commit date to end of span: '{commit_date_str}' "
                f"({span_end_date.isoformat()})"
            )

            # Commit directly from the populated index
            new_commit = dest_repo.index.commit(
                commit_message,
                commit_date=commit_date_str,
                author_date=commit_date_str,
            )
            logger.info(f"✨ Created new commit: {new_commit.hexsha[:7]}")

        else:
            logger.info("No commits found in this time span.")

        current_span_start = span_end_date

    # Clean up by removing the temporary remote
    logger.info("-" * 70)
    dest_repo.delete_remote(source_remote)
    logger.info("Removed temporary 'source' remote.")


@click.command()
@click.argument(
    "source_repo_path",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.argument(
    "destination_repo_path",
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option(
    "--branch",
    default=None,
    help="The source branch to read commits from. Defaults to the current active branch.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    default="INFO",
    help="Set the logging level.",
)
def cli(
    source_repo_path: Path,
    destination_repo_path: Path,
    branch: str | None,
    log_level: str,
) -> None:
    """
    Reorganizes a Git repository's history into 7-day snapshots.

    SOURCE_REPO_PATH: Path to the existing Git repository to analyze.
    DESTINATION_REPO_PATH: Path where the new repository will be created.
    """
    setup_logging(log_level)

    if destination_repo_path.exists() and any(destination_repo_path.iterdir()):
        logger.error(
            f"Error: Destination path '{destination_repo_path}' already "
            "exists and is not empty."
        )
        raise click.Abort()

    branch_to_process, source_commits = get_source_commits(
        source_repo_path, branch_name=branch
    )
    create_snapshot_commits(
        source_repo_path,
        destination_repo_path,
        branch_to_process,
        source_commits,
    )
    logger.info("✅ Reorganization complete.")
    logger.info(f"New repository created at: {destination_repo_path.resolve()}")


if __name__ == "__main__":
    cli()
