# This is the user-interface branch

This branch runs within a docker container, but we mount the files for now. 

run: 

    docker build -t react-frontend.
    docker run -it -p 3000:3000 react-frontend


run this:

    docker build -t react-runtime .
    docker run -it -p 3000:3000 -v ./doc-manager-ui:/usr/src/app react-runtime

