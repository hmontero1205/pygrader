# Creating a Private Fork

You might want to create a private fork of `pygrader` in which to implement your course's grading scripts.
The [repository](https://github.com/hmontero1205/pygrader) is public and GitHub does not allow the creation of private forks for public repositories.

Here is how you might go about it:

 1. Create a bare clone of the repository.
    (This is temporary and will be removed so just do it wherever.)
    ```bash
    git clone --bare git@github.com:hmontero1205/pygrader.git
    ```

 2. [Create a new private repository on GitHub](https://help.github.com/articles/creating-a-new-repository/) and name it `pygrader`.

 3. Mirror-push your bare clone to your new `pygrader` repository.
    > Replace `<your_username_or_org>` with your actual GitHub username/org in the url below.
    
    ```bash
    cd pygrader.git
    git push --mirror git@github.com:<your_username_or_org>/pygrader.git
    ```

 4. Remove the temporary local repository you created in step 1.
    ```bash
    cd ..
    rm -rf pygrader.git
    ```
    
 5. You can now clone your `pygrader` repository on your machine.
    ```bash
    git clone git@github.com:<your_username_or_org>/pygrader.git
    ```
   
 6. If you want, add the original repo as remote to fetch (potential) future changes.
    Make sure you also disable push on the remote (likely you're not allowed anyway).
    ```bash
    git remote add upstream git@github.com:hmontero1205/pygrader.git
    git remote set-url --push upstream DISABLE
    ```
    You can list all your remotes with `git remote -v`. You should see:
    ```
    origin	git@github.com:<your_username_or_org>/pygrader.git (fetch)
    origin	git@github.com:<your_username_or_org>/pygrader.git (push)
    upstream	git@github.com:hmontero1205/pygrader.git (fetch)
    upstream	DISABLE (push)
    ```
    When you want to pull changes from `upstream` you can just fetch the remote and rebase on top of your work.
    ```bash
      git fetch upstream
      git rebase upstream/master
      ```
      And solve any conflicts.

Then follow [adaptme.md](./adaptme.md) for adapting this repo to your own needs.
