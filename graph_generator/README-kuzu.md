# Graph Data Generation and Load into KUZU
## Pre-requisites

- Python 3 and KUZU database
	- On macOS install with 
	```
		brew install python3 kuzu
	```

# Generate Data

- Clone the repository 
	```
	git clone https://github.com/nmdp-bioinformatics/grimm`
	cd grimm
 	git checkout grimm_on_kuzu 
	```

- Setup Python3 virtual environment
    Create Virtual Environment
    ```
    virtualenv -p python3 venv
    source venv/bin/activate
    ```
 
    Install pandas and kuzu library
    ```
    pip3 install pandas kuzu==0.11.2
    ```
- Download and prepare wmda data. Python script downloads reference wmda data and untars it in wmda directory
  (This may need to be downloaded from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5089599/bin/TAN-87-439-s006.tgz and put it the graph_generator/data directory. )
	```
	cd graph_generator/data
	python wmda_download.py
	```

- Generate nodes/edges/toplinks from the reference wmda data. The freqs file is converted to HPF format first.
	```
	cd ..
	python3 wmda_to_hpf_csv.py
	python3 generate_kuzu_wmda_hpf.py
	```

- Generated nodes and edges files are in the output/csv directory.

	```
	output
	└── csv
	    ├── edges.csv
	    ├── nodes.csv
	    └── top_links.csv
	```

- Load the nodes/graph into kuzu db
	```
	python3 bulk_load_kuzu.py
	```
 - You should see `wmda.kuzu` directory with kuzu db files.

- If you look at the database you should see the Haplotype nodes available.
```
$ kuzu output/wmda.kuzu
Opening the database at path: wmda.kuzu in read-write mode.
Enter ":help" for usage hints.
kuzu> match (h:Haplotype) return count(h);
┌──────────────┐
│ COUNT(h._ID) │
│ INT64        │
├──────────────┤
│ 35412        │
└──────────────┘
(1 tuple)
(1 column)
Time: 14.46ms (compiling), 0.81ms (executing)

```

Run the Kuzu Explorer
```
❯ docker run -p 8000:8000 -v $PWD/output:/database -e KUZU_FILE=wmda.kuzu --rm kuzudb/explorer:0.11.2
[18:16:47.839] INFO (1): Using database file: wmda.kuzutabase -e KUZU_FILE=wmda.kuzu --rm kuzudb/explorer:0.11.2
[18:16:47.843] INFO (1): Access mode: READ_WRITE
[18:16:48.079] INFO (1): Version of Kuzu: 0.11.2
[18:16:48.079] INFO (1): Storage version of Kuzu: 39
[18:16:48.083] INFO (1): Deployed server started on port: 8000
```