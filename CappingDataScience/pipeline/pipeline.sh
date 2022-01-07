echo 'Starting pipeline' && python3 etl/etl.py && python3 cleansing/cleansing.py && python3 featureEngineering/featureEngineering.py && echo 'Pipeline finished'
