### Deps

You may need to run this command for pandas being able to load excel files.
```
pip3 install openpyxl 
```

You may need to run this for database connection
```
pip3 install psycopg2-binary
```

### Running

If you are running this file from this directory you will likely need to change this line
```
data_dir = "../data/"
```

to
```
data_dir = "../../data/"   
```

```
python3 etl.py
```

