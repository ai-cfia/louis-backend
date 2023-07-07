FROM postgres:15.2
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN apt-get -y install postgresql-server-dev-15
RUN pip install pgxnclient
RUN pgxn install vector