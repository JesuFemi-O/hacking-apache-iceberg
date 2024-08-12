## Table Formats

Fine, Iceberg is a table format. It’s an abstraction over files in object storage that lets you enjoy things like ACID-compliant transactions, schema evolution, and even time travel!! That’s just insane. So, I can basically write files to a bucket in S3, and if the structure changes, I can still read all of my data without breaking a sweat? I can even roll back to a particular version of my data?

All the gibberish Precious used to say about Databricks is starting to come together. Finally, lakehouse experience without Databricks pricing and maybe I can even avoid Spark? Well, we’ll find out soon enough!

## Iceberg Catalog

So basically, there’s something called a catalog, which is how the Iceberg table format figures out what files to look at when you make a read request. It also uses the catalog to handle writes, incoming data, and any changes. So, if you’re serious about implementing a lakehouse, you should know at the very moment that the catalog is what makes Iceberg smart, and it’d be wise of you to also befriend the catalog.

The next question in my head was about whether the catalog was just some sort of object you have to use with Iceberg. You know how if you’re spinning up Kafka, you need Zookeeper, yea? Yeah, but then it turns out there are numerous catalogs you can use with Iceberg. You don’t have to be tied to any particular one, and I honestly think that’s cool. I don’t yet know if I can start with one catalog and just migrate to another one yet, but we’ll find out soon, I guess.

## Working With Iceberg Tables

So there’s this thing called PyIceberg, which basically is a Python library you can use to manage Iceberg tables. What I’ve seen so far is how to leverage PyIceberg to create Iceberg tables using Parquet file schema, overwrite, and append data. I haven’t seen anything on merge yet.

## Data Ingestion Patterns

As for patterns, broadly speaking, there are basically two kinds of ingestion patterns you’ll have to consider:

- **Batch ingestion**:
  - Hold the data in memory, convert to a Parquet table, and write it into your Iceberg table.
  - Write the data to a location in your storage object bucket that’s a “Landing Zone” and write the data from that location into your Iceberg table.

The second option could probably also be considered as a more standard approach if you’re dealing with fairly large datasets you need to write into your lakehouse in batches.

- **Streaming ingestion**:
  I have no idea what the best pattern should be, but I imagine you’d want to consume from some sort of queue and write into your table. However, I wonder how the catalog will play out in this scenario because I’ve read there can be funny performance issues if you’re not doing it correctly.

## A Roadmap in the Horizon

So if you’re like me who loves a structured and systematic way to understand a concept before hacking at it, I’ll say you need to first take a step back and try to understand what a lakehouse is and why it’s even a thing. I can’t give you all the answers you’re looking for, tbh. I’m just at a point where I’ve made my peace with the idea of a lakehouse and I kind of have some sort of boundary in my head on what an antipattern could look like if you were implementing this architecture.

No, don’t write files in S3 and manually manage your partitions. Land the files somewhere else and essentially copy from there through the “gate” of your Iceberg table and let Iceberg and its catalog worry about partitioning and all those other tiny details. Think of Iceberg like you’d think of a Snowflake table or Postgres table, except you’re aware of where the physical data is being written into, and you can potentially go through the backdoor if you have to.

The cool thing is because of this thing called a catalog, anything that can plug into it and understand its “language” can at the very least query your data. Depending on how well it integrates with your catalog of choice, it can also write data back into the underlying table.

## A Roadmap Anyways

My systematic approach to understanding Iceberg will see me consider the following:

1. **Understand PyIceberg**: From the examples I’ve taken a glance at, they don’t seem to be connecting to any catalog. There seems to either be a default one that ships with PyIceberg or they’re doing something funny behind the scenes like using your file system to create and manage a naive version of what a catalog should be. I’ll basically spend some time going through the library’s documentation and poke around a little bit and see what comes up.
2. **Get comfortable with PyArrow**: This is mostly motivated by the fact that the examples I’ve seen so far leverage PyArrow while using PyIceberg. Nothing crazy, tbh, but I’ll want to be comfortable with the basics of PyArrow so I can take advantage of it.
3. **Get familiar with Avro and Parquet file formats**: You’ll probably be wondering why this didn’t come first, but I think they’re things you’d learn in parallel with the first two steps as they’ll naturally fit in. I love these file formats because they’re great for handling data and are more predictable and less hassle-free for ingestion and data storage compared to CSVs. They have rich metadata and they’ll most likely make your life easier if you were thinking of data quality at scale, for example.
4. **Consolidate my knowledge so far**: At this point, I would build a very basic lakehouse example where I read flat files and write their content into my Iceberg table via PyArrow and PyIceberg. I’ll explore how to leverage one or two catalogs and figure out MinIO, which will be my object storage. I’ll implement full and incremental workloads and see how PyIceberg helps to handle different update strategies.
5. **Plug in Dagster and DuckDB**: At this point, I’ll set up Dagster as an orchestrator, PyIceberg for writing data to my Iceberg table, and DuckDB (MotherDuck) as my query engine.
6. **Mature my architecture**: The next thing I’ll need to figure out is how to integrate other tools and engines for ELT workloads. Can I leverage a framework like dltHub to go end-to-end from extraction to loading? How about Sling? Would I use these frameworks to write to a landing area and then trigger a process to ingest the data in the landing area into my lakehouse? I’ll basically spend some time trying to integrate as many tools as possible into this framework.
7. **Play with Kafka, Flink, and Spark streaming**: What will a streaming ingestion pipeline look like? How do these different tools integrate with my lakehouse?
8. **Kappa!**: Implement an architecture that requires both streaming and batch processing.
9. **RBAC, Governance, and beyond**: Now, you know it. Well, how do you operationalize and secure the damn thing!


## Weird things along the way

- Name spaces in catalogs

- Pyiceberg gives the orm vibe, trino feels like a way to actually leverage sql based statements

- You’ll probably want o stage data in a temp table in something like postgres then do a merge into statement powered by spark or trino...idk, but temp iceberg tables sounds weird.



