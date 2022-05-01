# Campaign Performance Analysis - Solution

For task description please see below. I only implemented scenario 1, but scenario 2
isn't hard to implement as the data is sorted by timestamp, so it's possible to do all
needed calculation in real time(if you need this, I could add this). 

**Requirements:**
Application requires docker and docker-compose to be installed and started.

**Installation:**
To start a service run:
```bash
docker-compose up --build
```

The data will be read, report will be calculated and written to docker postgres instance. 
After the statistics application has finished saving the reports and exits, 
you can query the reports from postgres by running:

```
psql postgresql://user:password@localhost:5432/stats

stats=# select * from page_loads;
stats=# select * from clicks;
stats=# select * from unique_user_clicks;
stats=# select * from click_through_rate;
```

`click_through_rate` is implemented using a time window, when we check if there are `ReferralPageLoad` 
events in this time window, that have the same `user_id` and `customer_id` as in `ReferralRecommendClick`. 
We can think of this click as being directly related to the page load event. You can change window size by 
changing `CLICK_THROUGH_WINDOW_SECONDS` env in `docker-compose.yaml`, default is 300 seconds
(there should be some time that the user visits the page and thinks about whether to click on the link)
Сhanging this window, you can get a different number of related events. But it seems that in the given data for almost all `ReferralRecommendClick` events, there are 
`ReferralPageLoad` events within 600 seconds.

TODO: add some tests

# Task description

We would like to know if users find the reward attractive enough to recommend this product on our [recommendation page](referral.png). Each customer has a custom recommendation landing page. We have multiple customers and each has a different customer_id, the example in the page is IONOS. Customer is a company that offers the product and needs referral marketing, user is a person who wants to potentially buy the product and interacts with the page. 

We collect data everytime a user visits one of the recommendation pages (`ReferralPageLoad` event) and clicks on the "Recommend IONOS" button (`ReferralRecommendClick` event).

Your task is to build a data pipeline that reads the events and answers these questions:

- `page_loads`: How many `ReferralPageLoad` events happened for each customer for each hour?
- `clicks`: How many `ReferralRecommendClick` events happened for each customer for each hour?
- `unique_user_clicks`: How many unique users did `ReferralRecommendClick` for each customer for each hour?
- `click_through_rate`: How many `ReferralRecommendClick` events directly related to `ReferralPageLoad` happened for each customer for each hour?
Feel free to make an assumption on how to relate the events to each other, it can be subsequent based on the time window
or based on a combination of fields in the event. Please explain your assumption in your submission.  

For the sake of this task, assume that the events were collected into log files and ordered by timestamp. 
You can find a sample in `aklamio_challenge.json` Every line is a valid json https://jsonlines.org/ 

Data looks like this:
`event_id | customer_id | user_id | fired_at | event_type | ip | email`

## Scenario 1

You can read all the data into memory. Assume that all data is available at the processing time. All you need to do is read all the data,
clean it up and calculate the aggregations asked above. 
Scheduling is out of scope.

## Scenario 2 (optional)

Assume there is too much data and we cannot read it all into the memory. You need to read the data line by line to memory and
update the aggregations upon reading each line. For this case, you can omit deduplication of events.

## Write to postgres/ model the report lines

Decide on how you would want to model the reports and create queries to create the tables and update them to the postgres instance we provide. 

# General Requirements

- You have used a minimum amount of libraries doing some data processing written in Python (pandas is fine but no fully fledged framework like flask please)
- In a state that you consider production ready
- No sensitive data included
- Please submit it in a link to a git repository or the git repository as .zip together with the commit history
