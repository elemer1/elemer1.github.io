#!/bin/bash

# Publish script
# Double-click or run this script to push all changes to GitHub.

cd "$(dirname "$0")"

echo "======================================"
echo "  Publishing to GitHub Pages"
echo "======================================"
echo ""

# Auto-format Chinese typography (spacing, punctuation) in markdown and homepage.
# Front matter and HTML files in _html/ are not touched.
if command -v node >/dev/null 2>&1; then
    if [ ! -d node_modules ]; then
        echo "Installing formatter dependencies (one-time)..."
        npm install --silent
    fi
    echo "Formatting Chinese typography..."
    node scripts/format.mjs _markdown/*.md index.html
    echo ""
else
    echo "Warning: node is not installed; skipping auto-formatting."
    echo "Install Node.js to enable Chinese typography auto-formatting."
    echo ""
fi

# Bail out if there is nothing to publish
if [[ -z $(git status -s) ]]; then
    echo "No changes to publish."
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 0
fi

# Show files that will be published
echo "The following files will be published:"
echo "--------------------------------------"
git status -s
echo "--------------------------------------"
echo ""

# Stage all changes
echo "Staging files..."
git add .

# Commit with a timestamped message
COMMIT_MSG="Update content - $(date '+%Y-%m-%d %H:%M:%S')"
echo "Committing: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Push to GitHub
echo "Pushing to GitHub..."
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "  Published successfully"
    echo "======================================"
    echo ""
    echo "Your site will update in 1-2 minutes."
    echo "Visit: https://elemer.net"
else
    echo ""
    echo "======================================"
    echo "  Publish failed"
    echo "======================================"
    echo ""
    echo "Check your network connection or Git configuration."
fi

echo ""
echo "Press any key to exit..."
read -n 1
