# citibike-nyc
padpy1920

```
mkdir data

curl https://s3.amazonaws.com/tripdata/201{7,8}{01,02,03,04,05,06,07,08,09,10,11,12}-citibike-tripdata.csv.zip -o "./data/citibike-tripdata201#1_#2.csv.zip"
curl https://s3.amazonaws.com/tripdata/2019{01,02,03,04,05,06,07,08,09,10}-citibike-tripdata.csv.zip -o "./data/citibike-tripdata2019_#1.csv.zip" 

cd data
unzip '*.zip'
citibike-tripdata201*
```
