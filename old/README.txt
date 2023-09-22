Martin Marcos Mutt Datta Exam


Python version: 3.11.5
OS: MacOS Ventura

Environment Setup

There are 2 main ways to do this:

1. Mounting the image via docker:


/to install postgres into a docker container, fisrt download the image

docker pull postgres


/create the docker container

docker run --name MuttPOSTGRES -e POSTGRES_PASSWORD=@Mutt1234 -e POSTGRES_DB=MuttDB -p 5432:5432 -d postgres


/you can check the connection using

server name: localhost or 0.0.0.0
port: 5432
username: postgres
password: @Mutt1234


/you can check the container by

docker ps


2. Creating the container from a docker-compose.yml file


/using the attached file, mount the image into a container by using this commnad inside the docker-compose folder:

docker-compose up -d


/you can check the connection using

server name: localhost or 0.0.0.0
port: 5432
username: postgres
password: Mutt@2023


/you can check the container by

docker ps





Creation of CRON running:

/run the bash command

crontab -e


/then modify the file in order to aggreagate the following command lines:

0 3 * * * /usr/bin/python3 /Users/martinmarcos/ML Martin Marcos/Mutt Data Exam/GetCoinInfoForDay.py 'bitcoin'
0 3 * * * /usr/bin/python3 /Users/martinmarcos/ML Martin Marcos/Mutt Data Exam/GetCoinInfoForDay.py 'ethereum'
0 3 * * * /usr/bin/python3 /Users/martinmarcos/ML Martin Marcos/Mutt Data Exam/GetCoinInfoForDay.py 'cardano'


/save the CRON file by pressing esc and then type:

:wq







