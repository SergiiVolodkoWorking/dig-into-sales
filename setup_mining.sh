echo "Starting bootstrapping"

# Check for Homebrew, install if we don't have it
if test ! $(which brew); then
    echo "Installing homebrew..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

brew update

echo "Installing environment"

brew install python3
brew install geckodriver

echo "Installing dependencies"
pip3 install pandas
pip3 install selenium
pip3 install tqdm

echo "Setup completed!"