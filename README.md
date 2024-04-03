# assignment3bdl
Big Data Laboratory CS5830 Assignment3 Submission

File Structure

dags

|---task1.py

|---task2.py

data

|---year

    |---csv files for year
    
extracted_data

|---index.json(json file of tuples of year and quantity key value pairs)

logs(logs of each run of airflow)

output

|---data.zip(zip file of data downloaded)

|---processed.csv(csv processed for visualization)

vizs(visualisaitions)

|---HourlyDewPointTemperature

    |---year1
    
        |---visualization1
        
        |---visualization2
        
        ..
        
    |---year2
    
        |---visualization1
        
        |---visualization2
        
    .
    
    .
    
|---HourlyDryBulbTemperature

    |---year1
    
        |---visualization1
        
        |---visualization2
        
    .
    
    .
    
|---HourlyPrecipitation

    |---year1
    
        |---visualization1
        
        |---visualization2
        
    .
    
    .
    
|---.env

|---docker-compose.yaml




