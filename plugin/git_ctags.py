import pathlib
import os
import subprocess
import logging


CACHE_DIR = pathlib.Path("~/.cache/gitctags").expanduser()
USER_HOME = pathlib.Path.home()

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def find_git(f):
    p = pathlib.Path(f)
    if not p.exists():
        return None
    while p != p.parent and p != USER_HOME:
        if p.joinpath(".git").exists():
            return p
        p = p.parent
    return None


def is_tags_fresh(repo_dir, cache_path, head):
    if not repo_dir.joinpath("tags").exists():
        logging.debug("no tags in repo")
        return False
    cached_head = cache_path.read_bytes() if cache_path.exists() else None
    logging.debug("cached head is %s", cached_head)
    if head != cached_head:
        return False
    return True


def ensure_tags_fresh(repo_dir):
    os.chdir(repo_dir)
    head = subprocess.check_output("git rev-parse HEAD", shell=True).strip()
    logging.debug("repo head is %s", head)
    cache_file = str(repo_dir).replace("/", "%").replace(" ", "!")
    cache_path = pathlib.Path(f"{CACHE_DIR}/{cache_file}")
    logging.debug("cache path is %s", cache_path)

    if is_tags_fresh(repo_dir, cache_path, head):
        logging.info("tags is fresh")
        return

    subprocess.Popen("ctags")
    cache_path.write_bytes(head)
    logging.info("new tags generated for %s", head)


def run(f):
    logging.debug("inputed file is %s", f)
    repo_dir = find_git(f)
    logging.debug("repo dir is %s", repo_dir)
    if repo_dir is None:
        logging.info("%s not in a git repo", f)
        return
    ensure_tags_fresh(repo_dir)


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s"
    )
    #  run("/Users/georgexsh/workspace/wasteland/tmp/test_qr2.py")
    #  run("/Users/georgexsh/workspace/djv/duozhuayu/apps/web/app.py")
    run("/Users/georgexsh/workspace/wasteland/ttbridge/ttbridge/ttclient.py")


if __name__ == "__main__":
    main()