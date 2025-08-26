from airflow.sdk import dag, task, Param, chain

_COLLECTION_NAME = "mycollection"
_WEAVIATE_CONN_ID = "weaviate_default"


@dag(
    params={
        "search_term": Param(
            type="string",
            default="banana",
        ),
        "match_terms": Param(
            type="array",
            default=["sun", "chair", "lemon", "happiness", "red"],
        ),
    },
    tags=["Pattern Example"]
)
def rag_example():

    @task
    def get_lists_of_texts(**context):
        match_terms = context["params"]["match_terms"]
        return match_terms

    _get_lists_of_texts = get_lists_of_texts()

    @task.embed(
        model_name="BAAI/bge-small-en-v1.5",
    )
    def embed_text(text: str):
        return text

    _embed_texts = embed_text.expand(text=_get_lists_of_texts)

    @task
    def zip_texts_and_embeds(texts: list, embeds: list):
        # convert to list of dicsts for expand_kwargs
        zipped = [{"text": text, "embeds": embed} for text, embed in zip(texts, embeds)]
        return zipped

    _zip_texts_and_embeds = zip_texts_and_embeds(
        texts=_get_lists_of_texts, embeds=_embed_texts
    )

    @task
    def load_embeddings_to_vector_db(text, embeds):
        from airflow.providers.weaviate.hooks.weaviate import WeaviateHook
        from weaviate.classes.data import DataObject

        hook = WeaviateHook(_WEAVIATE_CONN_ID)
        client = hook.get_conn()
        collection = client.collections.get(_COLLECTION_NAME)

        item = DataObject(
            properties={
                "text": text,
            },
            vector=embeds,
        )

        collection.data.insert_many([item])

    _load_embeddings_to_vector_db = load_embeddings_to_vector_db.expand_kwargs(
        _zip_texts_and_embeds
    )

    @task.embed(
        model_name="BAAI/bge-small-en-v1.5",
    )
    def embed_query(**context):
        search_term = context["params"]["search_term"]
        return search_term

    _embed_query = embed_query()

    @task
    def query_vector_db(embedded_query: list):
        from airflow.providers.weaviate.hooks.weaviate import WeaviateHook

        hook = WeaviateHook(_WEAVIATE_CONN_ID)
        client = hook.get_conn()
        collection = client.collections.get(_COLLECTION_NAME)

        results = collection.query.near_vector(
            near_vector=embedded_query,
            limit=1,
        )
        print(f"CLOSEST MATCH: {results.objects[0].properties['text']}")

    _query_vector_db = query_vector_db(embedded_query=_embed_query)

    chain(_load_embeddings_to_vector_db, _query_vector_db)


rag_example()
