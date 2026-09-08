# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
import asyncio
import shlex
from typing import Tuple
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())
def git():
    REPO_LINK = config.UPSTREAM_REPO

    if not REPO_LINK:
        LOGGER(__name__).warning("UPSTREAM_REPO is not configured.")
        return

    # Build authenticated URL only when GIT_TOKEN is available
    if config.GIT_TOKEN:
        repo_path = REPO_LINK.replace("https://github.com/", "").rstrip("/")
        UPSTREAM_REPO = (
            f"https://x-access-token:{config.GIT_TOKEN}"
            f"@github.com/{repo_path}"
        )
    else:
        UPSTREAM_REPO = REPO_LINK

    try:
        repo = Repo()
        LOGGER(__name__).info("Git repository found.")

    except InvalidGitRepositoryError:
        LOGGER(__name__).info("Git repository not found. Initializing...")
        repo = Repo.init()

    except GitCommandError as e:
        LOGGER(__name__).error(f"Git error: {e}")
        return

    # Make sure origin exists and points to the correct repository
    try:
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
            origin.set_url(UPSTREAM_REPO)
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)

        LOGGER(__name__).info("Git remote configured successfully.")

        # Fetch latest upstream
        origin.fetch(config.UPSTREAM_BRANCH)

        # Checkout/update branch
        if config.UPSTREAM_BRANCH in repo.heads:
            repo.heads[config.UPSTREAM_BRANCH].checkout()
        else:
            repo.create_head(
                config.UPSTREAM_BRANCH,
                origin.refs[config.UPSTREAM_BRANCH],
            ).checkout()

        # Pull latest changes
        try:
            origin.pull(config.UPSTREAM_BRANCH)
        except GitCommandError:
            LOGGER(__name__).warning(
                "Pull failed, resetting to FETCH_HEAD..."
            )
            repo.git.reset("--hard", "FETCH_HEAD")

        LOGGER(__name__).info(
            "Fetching updates from upstream repository..."
        )

    except GitCommandError as e:
        LOGGER(__name__).error(f"GitHub fetch/update failed: {e}")

    # Install requirements
    try:
        install_req("pip3 install --no-cache-dir -r requirements.txt")
    except Exception as e:
        LOGGER(__name__).error(
            f"Failed to install requirements: {e}"
        )
