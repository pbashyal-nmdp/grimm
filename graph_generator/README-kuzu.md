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
  Make sure `virtualenv` is installed.
    ```
    pip3 install virtualenv
    ```

    Create Virtual Environment
 
    ```
    virtualenv -p python3 venv
    source venv/bin/activate
    ```
 
    Install pandas library
    ```
    pip3 install pandas kuzu==0.8.2
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
	python wmda_to_hpf_csv.py
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
$ kuzu wmda.kuzu
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