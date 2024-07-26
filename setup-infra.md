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