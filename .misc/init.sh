#!/bin/sh

confirm_action() {
  local prompt_message="$1"
  while true; do
    printf  "$prompt_message (Y/n): "
    read user_input
    if [ "$user_input" = "Y" ] || [ "$user_input" = "y" ]; then
      return 0
    elif [ "$user_input" = "N" ] || [ "$user_input" = "n" ]; then
      echo "Cancelled"
      exit 0  # User cancelled
    else
      echo "Invalid input. Please type 'Y' or 'n'."
    fi
  done
}

replace_project_name() {
  local project_name="$1"
  if [ "$(uname)" = "Darwin" ]; then
    sed -i '' "s/django-playground-maker/$project_name/g" pyproject.toml
  else
    sed -i "s/django-playground-maker/$project_name/g" pyproject.toml
  fi
}

default_project_name=$(basename "$(dirname "$(dirname "$(realpath "$0")")")")

printf "Enter your project name [$default_project_name]: "
read project_name
project_name=${project_name:-$default_project_name}

confirm_action "Your project name is \"$project_name\". Is this correct?"

replace_project_name "$project_name"
echo "Project name changed to \"$project_name\""
echo "# $project_name\n\nThis is a Django project created with [django-playground-maker](https://github.com/paikwiki/django-playground-maker)." > README.md

printf "Enter your superuser password: "
read password
echo "SUPERUSER_PASSWORD=$password" > .env

echo "--------------------"
echo "Continue to:"
echo "  - create a new virtual environment in .venv"
echo "  - install dependencies in the virtual environment with poetry"
confirm_action "Continue?"

if [ -d ".venv" ]; then
  echo "Error: '.venv' directory already exists. Please remove it before proceeding."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
poetry install
echo "--------------------"

confirm_action "Do you want to remove .git and create a new .git?"
rm -rf .git
git init
git add .
git commit -m "1st commit"

echo "Project initialized successfully."
echo "Remove this script by running \"rm .misc/init.sh\""
echo "--------------------"

echo "Done."
