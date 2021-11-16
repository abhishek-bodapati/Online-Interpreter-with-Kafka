# Online-Interpreter-with-Kafka

- Works only for Python language.
- Apache Kafka used for queueing the requests and responses from client and server respectively.
- Used websockets for server-client communication. 

## Clone

```
https://github.com/abhishek-bodapati/Online-Interpreter-with-Kafka.git && cd Online-Interpreter-with-Kafka
```

## Setup
- Install and start [Apache Zookeeper](https://zookeeper.apache.org) and [Apache Kafka](https://kafka.apache.org/) services
```
npm install
```
## Run

- Run the below commands in new terminal tabs

```
python server.py
```
```
python consumer.py
```
```
npm start
```
- Open [http://localhost:3000](http://localhost:3000) in the browser.
