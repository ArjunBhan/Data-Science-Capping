### Running

The frontend requires a HTTP server to run.

You can set one up easily with by running the following in this directory
```
python3 -m http.server
```

Then visit

```
http://127.0.0.1:8000
```

The frontend requires the API to be running. Currently the frontend expects the API to be at nicholasblaskey.com. This can be changed with APIURL variables at the top of all JavaScript files if you wish to run it locally instead.