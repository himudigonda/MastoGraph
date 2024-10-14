# src/classification.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import networkx as nx
from tqdm import tqdm

def get_toxicity_score(text):
    template = """Analyze the following text for toxicity. Toxicity refers to harmful or abusive language, including insults, threats, harassment, or hate speech. Rate the toxicity on a scale from 0 to 1, where 0 is not toxic at all and 1 is extremely toxic. Only respond with the numeric score.

Text: {text}

Toxicity score:"""

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.1:8b-instruct-q6_K")
    chain = prompt | model

    result = chain.invoke({"text": text})
    try:
        score = float(result.strip())
        return min(max(score, 0), 1)  # Ensure score is between 0 and 1
    except ValueError:
        print(f"Error parsing toxicity score: {result}")
        return None

def classify_toxicity(network):
    print("Classifying toxicity in the network...")
    for node, data in tqdm(network.nodes(data=True), desc="Classifying nodes"):
        if 'content' in data:
            toxicity_score = get_toxicity_score(data['content'])
            if toxicity_score is not None:
                data['toxicity_score'] = toxicity_score
                data['is_toxic'] = toxicity_score > 0.5  # You can adjust this threshold

    toxic_nodes = sum(1 for _, data in network.nodes(data=True) if data.get('is_toxic', False))
    total_nodes = network.number_of_nodes()

    print(f"Classification complete. {toxic_nodes} out of {total_nodes} nodes classified as toxic.")
    return network
