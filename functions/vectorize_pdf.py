from llmsherpa.readers import LayoutPDFReader
import cohere
import numpy as np
import streamlit as st 

co = cohere.Client(st.secrets["COHERE_API_KEY"])

def ask(pdf_url, query):

  llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
  pdf_reader = LayoutPDFReader(llmsherpa_api_url)
  doc = pdf_reader.read_pdf(pdf_url)
  print(doc)

  contexts = []
  for chunk in doc.chunks():
    contexts.append(chunk.to_context_text())

  doc_emb = co.embed(texts=contexts,
                  model="embed-english-v3.0",
                  input_type="search_document"
                  ).embeddings

  doc_emb = np.asarray(doc_emb)

  #Encode your query with input type 'search_query'

  query_emb = co.embed(texts=[query],
                    model="embed-english-v3.0",
                    input_type="search_query",
                    ).embeddings

  query_emb = np.asarray(query_emb)
  query_emb.shape

  #Compute the dot product between query embedding and document embedding
  scores = np.dot(query_emb, doc_emb.T)[0]

  #Find the highest scores
  max_idx = np.argsort(-scores)
  most_relevant_contexts = []
  top_k = 10

  #Get only the top contexts to keep the context for openai small
  for idx in max_idx[0:top_k]:
    most_relevant_contexts.append(contexts[idx])

  #Call OpenAI to synthesize answers
  passages = "\n".join(most_relevant_contexts)
  prompt = f"Read the following passages and answer the question: {query}\n passages: {passages}"

  return prompt

