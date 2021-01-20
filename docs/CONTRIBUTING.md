Contributing
============
We happily welcome outside contributions to this repo! Here
are a few guidelines on how to contribute.

PRs/Issues
----------
If you want to discuss a potential new feature or an existing problem, please
open an issue so we can discuss in greater detail.

To open a PR, you'll first have to get yourself a copy of this repo. The easiest
way to do that is to make a public fork. GitHub's UI for PRs from public forks
will recognize branches in your forked repo.

[Here](https://stackoverflow.com/questions/10065526/github-how-to-make-a-fork-of-public-repository-private)
are some instructions on how to open a PR if you're working off of a private
fork. Please be careful not to leak any private code into the public repo. Make
sure you branch off using `upstream/main` (i.e. the `main` branch of a remote
pointing to this repo).

Our preferred branch naming convention is `<your-name>-<feature>` (e.g.
`hans-golang-support`).

Style
-----
We set up Github Actions to run `pylint` on code coming into the `main` branch.
PRs into `main` will be checked by this Github Actions hook. Please be sure to
fix up any linting errors.
