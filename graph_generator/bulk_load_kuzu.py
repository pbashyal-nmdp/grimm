import kuzu

def main() -> None:
    # Create an empty on-disk database and connect to it
    db = kuzu.Database("output/wmda.kuzu")
    conn = kuzu.Connection(db)

    # Create schema
    conn.execute("CREATE NODE TABLE Haplotype(haplotype_id INT64, name STRING, loci STRING, frequency double, primary key(haplotype_id))")
    conn.execute("CREATE REL TABLE CP(FROM Haplotype TO Haplotype, cp double)")
    conn.execute("CREATE REL TABLE TOP(FROM Haplotype TO Haplotype)")

    # Insert data
    conn.execute('COPY Haplotype FROM "./output/csv/nodes.csv"')
    conn.execute('COPY CP FROM "./output/csv/edges.csv"')
    conn.execute('COPY TOP FROM "./output/csv/top_links.csv"')

    # Execute Cypher query
    response = conn.execute(
        """
        MATCH (h1:Haplotype)-[t:TOP]->(h2:Haplotype)
        RETURN h1.name, h2.name
        LIMIT 10; 
        """
    )
    while response.has_next():
        print(response.get_next())


if __name__ == '__main__':
    main()