$ brew install pyenv 
$ echo 'eval "$(pyenv init --path)"' >> ~/.zprofile 
$ echo 'eval "$(pyenv init -)"' >> ~/.zshrc

pyenv -v :
pyenv 2.3.9

pyenv install 3.11.1

WARNING: The Python lzma extension was not compiled. Missing the lzma lib?