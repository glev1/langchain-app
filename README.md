# LangChain Playground

This repository serves as a playground to demonstrate various tools and functionalities available in the LangChain framework. It includes implementations of two key use cases: **Simple RAG with PDF Loader** and **Adaptive RAG**. Both use cases are configured with monitoring using LangFuse and can be accessed via a FastAPI-based API.
## Structure

The solutions are configured inside ```app/chains/pdf_rag.py``` and ```app/graphs/adaptive_rag/```. The API is define on ```app/server.py```.

```
langchain-app
├── README.md
├── app
│   ├── chains       
│   │   └── pdf_rag.py      
│   ├── graphs                  
│   │   └── adaptive_rag    
│   │       ├── edges           
│   │       │   └── edges.py
│   │       ├── nodes
│   │       │   ├── answer_generator.py
│   │       │   ├── answer_grader.py
│   │       │   ├── hallucination_grader.py
│   │       │   ├── index.py
│   │       │   ├── question_re_writer.py
│   │       │   ├── question_router.py
│   │       │   ├── retrieval_grader.py
│   │       │   └── web_search.py
│   │       ├── graph.py
│   │       └── state.py
│   ├── client.py
│   ├── server.py
│   └── vectorstores
│       ├── chroma.py
│       ├── faiss.py
│       └── utils.py
├── docs
│   └── images
│       ├── adaptive_rag.png
│       ├── api.png
│       ├── client_script.png
│       ├── langfuse.png
│       └── pdf_chain.png
├── documents
│   ├── levisbk
│   │   ├── common_questions.txt
│   │   └── faiss_index
│   │       ├── index.faiss
│   │       └── index.pkl
│   └── nike_form_2023
│       ├── faiss_index
│       │   ├── index.faiss
│       │   └── index.pkl
│       └── nike_form_10k_2023.pdf
└── requirements.txt
```
## Use Cases

### 1. Simple RAG with PDF Loader

![Simple RAG with PDF Loader](./docs/images/pdf_chain.png)

This use case demonstrates a simple Retrieval-Augmented Generation (RAG) system where documents are loaded from PDFs. The text embeddings are stored in a vector store, which can be either **FAISS** or **ChromaDB**.

### 2. Adaptive RAG

![Adaptive RAG](./docs/images/adaptive.png)

This use case showcases a more complex RAG system that incorporates self-reflection and uses **LangGraph** to adaptively refine responses based on the retrieved information.

## Monitoring
Both use cases are integrated with **LangFuse** for real-time monitoring and analytics, allowing you to track the performance and usage of the RAG systems. For more information, refer to the [LangFuse Documentation](https://langfuse.com/docs).

![Langfuse](./docs/images/langfuse.png)

## Getting Started

### Prerequisites
- Python 3.9 or higher
- (Optional) Deploy [Langfuse](https://langfuse.com/docs/deployment/self-host)

### Installation

1. Clone this repository:
    ```bash
    cd $HOME && git clone git@github.com:glev1/langchain-app.git
    cd $HOME/langchain-playground
    ```

2. (Optional) Configure conda or venv
    ```bash
    conda create -n langchain-app python=3.11
    conda activate langchain-app
    ```

    or

    ```bash
    conda create -n langchain-app python=3.11
    conda activate langchain-app
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure your environment variables using a ```.env``` file.

    ```
    OPENAI_API_KEY=sk-***
    LANGFUSE_PUBLIC_KEY=pk-***
    LANGFUSE_SECRET_KEY=sk-***
    LANGFUSE_HOST=http://localhost:3000
    TAVILY_API_KEY=tvly-***
    ```

### Running the API

The use cases are accessible through a FastAPI-based API. To start the server, run the following command:

```bash
cd app
python3 server.py
```

You can access the Swagger documentation and test the endpoints directly via the browser on ```http://localhost:8000/docs```. 


![FastAPI](./docs/images/api.png)


Or run the client script:

```bash
cd app
python3 client.py
```

![Client script](./docs/images/client_script.png)
