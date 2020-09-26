# Graph Analysis

## Steps

1. Copy the downloaded data onto a folder named `finalData`.
2. Run `getEdgeList.py`. This gives the edges as  space separate list of nodes in `edgelist.txt`.
3. Run` getNodes.sh`. This gives all the unique nodes in `nodelist.unique`.
4. Run `python3 encoder.py ne`. This creates an encoding for nodes and edges. Useful for saving memory in Graph Analysis.
5. Run `fetch_cert_id.py`. This creates unique identifiers for certificates using our metric.
6. Run all cells of `idfy.ipynb` in a Jupyter environment. This finds out our suspect edges.
7. Run `getSuspectNodes.py `to get the suspect nodes from the edges. File name is `all_nodes_unique.txt` (little confusing. :sweat-smile:)

Output of this stage is `suspect_edges_diff_cert_id.pickle` and `all_nodes_unique.txt`.
Feed them to the whois stage.

I am not automating the steps as intermediate data files might need splitting into different servers.

## Dependencies

Python3, Jupyter Notebook, SNAP (snap.py), Pandas
