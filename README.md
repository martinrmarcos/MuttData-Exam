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


/you can create the required table structures with the available TablesCreation.sql, they can be queried by:

select* from coin_price_usd
select* from maxmin_monthly_usd





///To end the docker containers you can use:

docker stop MuttDBdockercompose
docker rm MuttDBdockercompose







Creation of CRON running:

/run the bash command

crontab -e


/then modify the file in order to aggreagate the following command lines:

0 3 * * * /usr/bin/python3 <the_files_path>/GetCoinInfoForDay.py 'bitcoin'
0 3 * * * /usr/bin/python3 <the_files_path>/GetCoinInfoForDay.py 'ethereum'
0 3 * * * /usr/bin/python3 <the_files_path>/GetCoinInfoForDay.py 'cardano'

in my case:

0 3 * * * /usr/bin/python3 /Users/martinmarcos/ML Martin Marcos/Mutt Data Exam/GetCoinInfoForDay.py 'bitcoin'
0 3 * * * /usr/bin/python3 /Users/martinmarcos/ML Martin Marcos/Mutt Data Exam/GetCoinInfoForDay.py 'ethereum'
0 3 * * * /usr/bin/python3 /Users/martinmarcos/ML Martin Marcos/Mutt Data Exam/GetCoinInfoForDay.py 'cardano'


/save the CRON file by pressing esc and then type:

:wq





/APP functionality: GetCoinInfoForDay.py

/the app can receive one, two, three or four variables.

GetCoinInfoForDay.py coin date(YYY-mm-dd) to_date(YYY-mm-dd) y(y: to upload to SQL)

1 Variable: if you just enter the coin desired, the app will give you the information for that coin for todaysdate
2 variables: if you add a date, the app will fetch the data for that day
3 variables: if you add another date, the app will fetch information available between both dates entered
4 variables: if you add an 'y' after both dates entered, the app will upload the bulk import just performed and add it to the POSTGRESSQL




/SQL queries:

you can find both queries requested on the SQL folder


Query1.sql: Get the average price for each coin by month.

Query2allcoins.sql: Calculate for each coin, on average, how much its price has increased after it had dropped consecutively for more than 3 days. In the same result set include the current market cap in USD (obtainable from the JSON-typed column). Use any time span that you find best.



/Plots:


Plots can be found on the Plots.ipynb and the images inside the folder Plots


/In the file: Finance meets Data Science.ipynb

     you can find all the tasks related to that section
 
 
/on the file 'UnitTestingForApp.ipynb' you will find a test that goes through all the basic functionality of the app and its error messages






















