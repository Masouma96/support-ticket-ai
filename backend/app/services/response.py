from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="gpt2"
)

def generate_response(text, intent):
  
    prompt = f"System: You are a helpful support assistant.\nUser: {text}\nAssistant:"
    
    result = generator(
        prompt,
        max_new_tokens=40,
        do_sample=True,
        top_k=50,            
        top_p=0.95,        
        temperature=0.6,     
        repetition_penalty=1.5
    )
    
    generated = result[0]["generated_text"]
    response = generated.replace("Assistant:", "").strip()
    return response
