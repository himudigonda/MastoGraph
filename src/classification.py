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

    try:
        result = chain.invoke({"text": text})
        score = float(result.strip())
        return min(max(score, 0), 1)  # Ensure score is between 0 and 1
    except ValueError:
        print(f"Error parsing toxicity score: {result}")
        return None

def classify_toxicity(network):
    print("Classifying toxicity in the network...")
    toxic_count = 0
    total_count = network.number_of_nodes()

    for node, data in tqdm(network.nodes(data=True), desc="Classifying nodes"):
        if 'content' in data:
            toxicity_score = get_toxicity_score(data['content'])
            if toxicity_score is not None:
                data['toxicity_score'] = toxicity_score
                data['is_toxic'] = toxicity_score > 0.5  # Toxicity threshold
                if data['is_toxic']:
                    toxic_count += 1
    return network, toxic_count, total_count
