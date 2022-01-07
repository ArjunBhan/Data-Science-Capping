FROM  postgres:13.2

#Set the TimeZone 
RUN apt-get update -y
RUN apt-get install -y tzdata
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure tzdata

CMD ["postgres"]
