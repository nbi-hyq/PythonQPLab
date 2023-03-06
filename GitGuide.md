# Guide to git

This is a guide on how to set up and use git.

## Getting started

To get started with this git project follow the following steps (This is for windows, Mac or Linux may vary slightly)

1. Create a GitHub user if you don't have one
2. Get added to the github repository
3. Install the Git Bash: https://git-scm.com/downloads
4. Add an SSH agent to your computer if you have not already (in your first commit you may have to define your name and email first)
    1. Login to GitHub
    2. In the top right corner click your profile picture and choose "Settings"
    3. Now choose SSH and GPG keys in the left menu
    4. Open GitBash and type: ```ssh-keygen -t ed25519 -C "your_email@example.com"```
    5. Press enter
    6. Next write a password and press enter, just press enter without writing anything to use Git on your computer without a password
    7. Repeat password
    8. Next write: ```eval "$(ssh-agent -s)"```
    9. Next write: ```ssh-add ~/.ssh/id_ed25519```
    10. Next write: ```clip < ~/.ssh/id_ed25519.pub```
    11. On GitHub click "New SSH Key"
    12. Give it a title and in the "Key" field press CTRL-V
    13. Click Add SSH Key
5. Open Git Bash on your computer and navigate to the folder in which to put the project, can be done with: cd "path/to/my/folder"
6. Next write: ```git clone git@github.com:nbi-hyq/PythonQPLab.git```

## Committing changes

When working on a git project you will only make local changes to your computer, to update the repository do the following

1. If any files should stay local and not be added, then add them to the .gitignore in the main project folder
2. Open Git Bash and navigate to your project folder
3. Write: ```git add .```
4. Write: ```git commit -m "My update message"```
5. Write: ```git push```

### Branching

To avoid breaking everyones code when changing the project you should always create your own branch before working on the project. Then when it is tested and ready for other people to use merge it with the master branch. To create a branch do the following

1. Open Git Bash and navigate to your project folder
2. Write: ```git checkout -b "Name of Branch"```
3. Write: ```git push -u origin "Name of Branch"```

To merge a branch with the master branch do the following

1. Open Git Bash and navigate to your project folder
2. Write: ```git checkout master```
3. Write: ```git pull```
4. Write: ```git merge "Name of Branch"```
5. Write: ```git push```