# Lakehouse Infrastructure

one of the main things I've just figured out is that at the very least you'll need

- **object storage**: the lakehouse is usually built on top of object storage and that will be the physical location that the data and metadata files will live in.

- **Catalog**: The catalog has the keys to the city! it's how you'll be able to enjoy all the cool features like acid compliance, schema evolution etc. it's basically how you figure out what files to read from and whenever a user makes a request, this is probably a naive way to think of it but that's how i'm chosing to describe it for now as I build up momentum.

- **A Query Engine**: Lakehouses are usually "bring your own query engine" so once you have your tables, you want something your analysts can use to read your data and also something that can be used to write data too.


One big gotcha at this point is that if you're designing a lakehouse you'd want to take some time thinking about how data in your lakehouse would be assessed and based on that decide what catalog to use for example, I've heard a lot of good things about nessie but until I can confirm it can expose a rest catalog nessie might just be limiting since you'll typically only enjoy connection to spark and dremio, even pyiceberg doesn't seem to support the nessie catalog (Again, that's what I think I know right now, this might be incorrect.)

I'm going to be using a sql catalog for now since it reduces the burden of technologies I'll need to get familliar with. I'm hoping an engine like trino will be good enough and will support sql based catalogs...I'll find out shortly anyways!


## What's my Stack Looking like

for now I'll be working with:

- Docker and docker-compose to manage all the tools that needs to come together
- pyiceberg and pyarrow for writing to my iceberg table and managing it's inital setup
- minio for object storage but a relatively light setup without any kind of replication
- trino as my query engine
- Postgres for catalog duties!
- Superset for visualization

I would love to test the rest catalog but I think I already have too much tech to figure out right now so I'll consider it a nice to have, same goes for streamlit!


# Experince Notes

So I really don't know what I'm doing yet...lol...I just know a little bit of docker and have been able to piece the services together, I'm not yet sure if I'm doing the catalog thing right but I can connect to minio (didn't know port 9000 was for api and 9001 has to be configured to use handle the UI before now, you do that with the command in the compose file).

Another wierd thing quick googling didn't really give me answers to is setting up trino, I had to keep looking at the logs, googling the errors and asking chat-gpt what I may be missing.

Next, I'll work on a `pyiceberg` script to load the catalog, create a namespace and create my tables...

# Finding a stable setup that works!

So I was able to find a setup that I'm very comfortable with. what I found interesting was that I had to pick a catalog that would work well with as many systems as possible and Hive Metastore seemed to be like the way to go but boy did I see a headache coming my way?

Most of the example setups I found were a hell to work with, it's either they didn't startup properly and then crashed or they just fall apart once you try to do anything with Iceberg, I knew I had one last line of setup to fall back to, but I was too complex in my opinion and I genuinely don't want someone to pick this up a few months from now and find it extremely difficult to pull my setup apart. 

Complex setups are so easy to get locked into, usually there's a bit of hardcoding or assumptions about service names, ports, etc harcoded all over configuration files that makes them very hard to work with

## Setup Components

- **oltp service**: This is a postgres service representing an oltp system, you can think of it as a database connected to the backend of an app, so users intereactions will lead to the creation of data in this system.

- **trino service**: This service is a query engine that can connect to other db systems, trino let's me do federated queries without necessarily having all my data in a central datawarehouse. to register a new source that trino can read from (and write to) you basicailly need to create a new catalog property file describing how trino can connect to that source and read from it. in this setup, trino will connect to my postgres oltp service and an iceberg setup.

- **metastore_db service**: This is a postgres database that will serve as a backend to hold the metadata manage by my hive metastore db. in most lakehouse setups, mariadb is commonly used here but I'm sticking to something I'm already comfortable/familliar with just incase I need to go low level for any reason (none for now tbh, just keeping the stack as familliar as possible.)

- **hive-metastore service**: Iceberg table format is usually driven by two core components (as far as I know so far) - an object storage component and a metadata manager which is also called a catalog. this catalog can be a glue catalog, SQL catalog, Hive catalog, Nessie, Rest, etc. there are clearly many types of metadata managers that can serve this purpose, for our setup here, I'm chosing to go with hive and I'm going with a starburst image of hive metastore that seemed to work best for my setup.


- **minio service***: this is an open source object storage project that integrates well with S3 and will be my object storage layer for my Iceberg tables.

- **mc-job**: This service is really just a script that is executed once minio is stood up. it basically creates a bucket which represents my lakehouse

In The setup described above, note that I'm not persisting data in any service and I'm only mounting the catalog directory for trino so there's a risk here that everytime you teardown this setup you'll loose data between sessions, I've lazily left the old compose file in the dumps folder, I may eventually reconsider volume mounting for the oltp and minio services at least.


Once I connected to trino via my SQL client (DataGrip in my case) I ran the follwing queries to see how it came together:

```sql

show catalogs;

CREATE SCHEMA datalake.lakehouse
WITH (location = 's3a://datalake/lakehouse');
```

the command created a folder in my datalake bucket called lakehouse to represent the schema I created.

I'll work on using Pyiceberg next to take things to the next level!!