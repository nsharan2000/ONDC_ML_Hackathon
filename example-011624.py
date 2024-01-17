
""" Simple example to show the keys returned in a search query and how to view and adjust """

from llmware.library import Library
from llmware.retrieval import Query


#   set up library and  add files
lib = Library().create_new_library("my_lib")
lib.add_files("/path/to/files")

#   run a query
results = Query(lib).text_query("my query")

#   loop through the results found

for entry in results:

    #   each entry is a dictionary which includes all of the key attributes of that block
    #   e.g., "text", "page_num", "doc_ID", "content_type", etc.
    #   e.g., "coords_x", "coords_y"

    print("entry: ", entry)

    #   to view only the coords_x and coords_y
    print("coords_x: ", entry["coords_x"])
    print("coords_y: ", entry["coords_y"])


#   standard list of return keys are documented in the Query initialization ~ line 80 - copied below
"""
# self.query_result_standard_keys = ["_id", "text", "doc_ID", "block_ID", "page_num", "content_type",
                                   "author_or_speaker", "special_field1", "file_source", "added_to_collection",
                                   "table", "coords_x", "coords_y", "coords_cx", "coords_cy", "external_files",
                                   "score", "similarity", "distance", "matches"]
"""

#   to adjust the set of standard output keys, see the example - examples/Retrieval/text_retrieval.py - copied below

"""
def basic_text_retrieval_example (library):

    # Step 2 - the Query class executes queries against a Library

    # Create a Query instance
    q = Query(library)

    # Set the keys that should be returned - optional - full set of keys will be returned by default
    q.query_result_return_keys = ["file_source", "page_num", "matches", "doc_ID", "block_ID", "content_type", "text"]

    # Perform a simple query
    my_query = "total amount"
    query_results = q.text_query(my_query, result_count=20)

    print(f"\nQuery: {my_query}")

    # Iterate through query_results, which is a list of result dicts
    for i, result in enumerate(query_results):
        print("results - ", i, result)

    return query_results

"""
