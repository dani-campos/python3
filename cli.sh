#! /usr/bin/env bash

export COMMAND="$1"

function docker_run {
  docker run -i --rm -v "`pwd`:/authorizer" authorizer-python "$@"
}

function docker_run_test {
  docker run -i --rm authorizer-python-test
}

case "$COMMAND" in
  build)
    docker build -t authorizer-python . -f app.Dockerfile
    docker build -t authorizer-python-test . -f test.Dockerfile
    ;;
  run)
    docker_run
    ;;
  test)
    docker_run_test
    ;;
esac
