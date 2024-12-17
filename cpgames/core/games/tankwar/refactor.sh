PYPATH=$(find . -type f -name "*.py")
autoflake -i --remove-all-unused-imports --ignore-init-module-imports $PYPATH
autopep8 -i --max-line-length 500 $PYPATH
isort $PYPATH
