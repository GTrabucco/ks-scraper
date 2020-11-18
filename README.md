# ks-scraper

# Team class examples
Team data is located in data/teams

Retrieves all the gambling data specified in the Team Class for the Celtics<br/>
`team = Team("Celtics")`<br/>

Retrieves all the gambling data for the Celtics in the 2018 season<br/>
`team = Team("Celtics", season='2018')`<br/>

Retrieves all the gambling data for the Celtics between 1/10/2017 - 11/11/2018.<br/>
DATES MUST BE IN YYYY-MM-DD FORMAT<br/>
`team = Team("Celtics", start_date='2017-1-10', end_date='2018-11-11')`<br/>

Retrieves all the gambling data for the Celtics between 1/1/2015 - 11/11/2018. <br/>
DATES MUST BE IN YYYY-MM-DD FORMAT<br/>
`team = Team("Celtics", end_date='2016-11-11')`<br/>

Retrieves all the gambling data for the Celtics 11/11/2018 - their latest game<br/> 
DATES MUST BE IN YYYY-MM-DD FORMAT<br/>
`team = Team("Celtics", start_date='2018-11-11')`<br/>



# Scenario class example

A Scenario is defined as a trend that produces a specific set of Matchups ex. home favorites after a loss<br/>
Scenario data is located in data/scenarios<br/>
All the same season and date specifications demo'd in the Team class examples can be used with the Scenario class<br/>

Retrieves all the gambling data specified in the Scenario class for the Scenario: tS(assists-14>=turnovers,N=4)=4<br/>
`scenario = Scenario("tS(assists-14>=turnovers,N=4)=4")`



# League class example
League data is located in data/master<br/>
All the same season and date specifications demo'd in the Team class examples can be used with the Scenario class<br/>

Retrieves all the NBA Matchups since 1/1/2015<br/>
`league = League()`

