import configparser
import os

class GitRepository(object):
    """A git repository"""
    worktree = None
    gitdir = None
    conf = None
    def __init__(self, path, force=False):
        assert path is not None
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)
        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = self.repo_file("config")
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        if not force:
            vers = int(sefl.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported resitoryformatversion %s" % vers)

    def repo_file(self, *path, mkdir=False):
        """Same as repo_path, but create dirname(*path) if absent.
        For example, repo_file(r, "refs", "remotes", "origin", "HEAD")
        will create .git/refs/remotes/origi."""
        if self.repo_dir(*path[:-1], mkdir=mkdir):
            return self.repo_path(*path)

    def repo_path(self, *path):
        """Compute path under repo's gitdir."""
        return os.path.join(self.gitdir, *path)

    def repo_dir(self, *path, mkdir=False):
        """Same as repo_path, but mkdir *path if absent if mkdir."""
        path = self.repo_path(*path)
        if os.path.exists(path):
            if (os.path.isdir(path)):
                return path
            else:
                raise Exception("Not a directory %s" % path)
        if mkdir:
            os.makedirs(path)
            return path
        else:
            return None

    @classmethod
    def repo_create(cls, path):
        """Create a new repository at path."""
        repo = GitRepository(path, True)
        # First, we make sure the path either does't exit or
        # is an empty dir
        if os.path.exists(repo.worktree):
            if not os.path.isdir(repo.worktree):
                raise Exception("%s is not a directory" % path)
            if os.lisdir(repo.worktree):
                raise Exception("%s is not empty!" % path)
        else:
            os.makedirs(repo.worktree)
        assert(repo.repo_dir("branches", mkdir=True))
        assert(repo.repo_dir("objects", mkdir=True))
        assert(repo.repo_dir("refs", "tags", mkdir=True))
        assert(repo.repo_dir("refs", "heads", mkdir=True))
        # .git/description
        with open(repo.repo_file("description"), "w") as f:
            f.write("Unnamed repository; edit this file 'description' to name the repository.\n")
        # .git/HEAD
        with open(repo.repo_file("HEAD"), "w") as f:
            f.write("ref: refs/head/master\n")
        with open(repo.repo_file("config"), "w") as f:
            config = repo.repo_default_config()
            config.write(f)
        return repo

    @classmethod
    def repo_default_config(cls):
        ret = configparser.ConfigParser()
        ret.add_section("core")
        ret.set("core", "repositoryformatversion", "0")
        ret.set("core", "filemode", "false")
        ret.set("core", "bare", "false")
        return ret
