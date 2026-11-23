import os
import subprocess
from datetime import datetime, timezone

import pytest


class Repo:
    """A throwaway git repository with dated commits."""

    def __init__(self, path):
        self.path = str(path)
        os.makedirs(self.path, exist_ok=True)
        self._git("init", "-q", "-b", "main")
        self._git("config", "user.name", "Test")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "commit.gpgsign", "false")

    def _git(self, *args, env=None):
        return subprocess.run(["git", "-C", self.path, *args], check=True, capture_output=True, text=True,
                              env={**os.environ, **(env or {})}).stdout

    def commit(self, files, message, when, author="test@example.com", delete=()):
        for name, content in files.items():
            full = os.path.join(self.path, name)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as fh:
                fh.write(content)
            self._git("add", name)
        for name in delete:
            self._git("rm", "-q", name)
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S+0000")
        env = {"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp,
               "GIT_AUTHOR_EMAIL": author, "GIT_COMMITTER_EMAIL": author}
        self._git("commit", "-q", "--allow-empty", "-m", message, env=env)
        return self._git("rev-parse", "HEAD").strip()

    def tag(self, name, when):
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S+0000")
        self._git("tag", "-a", name, "-m", name, env={"GIT_COMMITTER_DATE": stamp})


def day(y, m, d, h=12):
    return datetime(y, m, d, h, tzinfo=timezone.utc)


@pytest.fixture
def repo(tmp_path):
    return Repo(tmp_path / "repo")
