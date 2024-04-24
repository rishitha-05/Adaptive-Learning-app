from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyA2uuj0NnZEdy5og9r9AK8MoBOwCHr3sWA")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = "here you will be provided with the subject and the topic student wants to learn in the form of subject:topic  ,then you need to test his level of knowledge by asking him some questions provide 4 options for each question and get reponses from him and evaluate them provide him with the detailed analysis  where he has gone wrong and what are the correct answers along with explainations tell him the areas he has to concentrate more on and recommend him to focus on the topics which he is weak at and also provide him with the links for him to prepare."

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["biology: animal kingdom"]
  },
  {
    "role": "model",
    "parts": ["## Animal Kingdom Knowledge Test\n\nLet's test your understanding of the animal kingdom!  Please answer the following multiple-choice questions to the best of your ability.\n\n*Question 1:* Which of the following is NOT a characteristic of all animals?\n\na) Multicellular  \nb) Heterotrophic  \nc) Eukaryotic  \nd) Photosynthetic\n\n*Question 2:* Animals with a segmented body and jointed appendages belong to which phylum?\n\na) Arthropoda  \nb) Annelida  \nc) Mollusca  \nd) Chordata \n\n*Question 3:* Sponges belong to which phylum?\n\na) Porifera  \nb) Cnidaria  \nc) Echinodermata  \nd) Platyhelminthes\n\n*Question 4:* Which phylum includes animals with a soft body, mantle, and usually a shell? \n\na) Mollusca  \nb) Annelida  \nc) Porifera  \nd) Cnidaria \n\n*Question 5:* Animals with radial symmetry and stinging cells belong to which phylum?\n\na) Cnidaria  \nb) Echinodermata  \nc) Arthropoda  \nd) Porifera \n\n\nPlease provide your answers for each question so I can evaluate your understanding and provide feedback."]
  },
  {
    "role": "user",
    "parts": ["a,b,c,d,c"]
  },
  {
    "role": "model",
    "parts": ["## Evaluation of Your Animal Kingdom Knowledge\n\nHere's an analysis of your answers:\n\n*Question 1: Correct!*  Option d) Photosynthetic is the answer. Animals are heterotrophic, meaning they obtain energy by consuming other organisms, not through photosynthesis. \n\n*Question 2: Correct!*  Arthropoda is the phylum characterized by segmented bodies and jointed appendages, including insects, spiders, and crustaceans. \n\n*Question 3: Correct!*  Sponges with their simple body structure belong to the phylum Porifera.\n\n*Question 4: Incorrect.* The correct answer is a) Mollusca.  This phylum includes animals like snails, clams, and octopuses, which have soft bodies, mantles, and often shells. \n\n*Question 5: Incorrect.* The correct answer is a) Cnidaria.  This phylum includes jellyfish and corals, known for their radial symmetry and stinging cells called cnidocytes. \n\n\n## Areas for Improvement and Recommendations\n\nIt appears you have a good understanding of the basic characteristics of animals and the classification of some phyla like Porifera and Arthropoda. However, you may want to focus on reviewing the characteristics of Mollusca and Cnidaria to differentiate them clearly. \n\nHere are some resources that can help you strengthen your understanding:\n\n* *Crash Course Biology:* This YouTube series offers engaging and informative videos on various biology topics, including the animal kingdom.\n* *Khan Academy:* Khan Academy provides comprehensive lessons and practice exercises on different aspects of biology, including animal classification.\n* *Your local library or bookstore:* Numerous biology textbooks and reference books offer detailed information on the animal kingdom.\n\n*Specifically, concentrate on:\n\n *Mollusca:* Learn about the different classes within this phylum, such as gastropods (snails and slugs), bivalves (clams and mussels), and cephalopods (octopuses and squids). Understand their unique features and adaptations.\n* *Cnidaria:* Study the two main body forms of cnidarians (polyp and medusa) and their life cycles. Learn about the different classes within this phylum, such as hydrozoa (hydra), scyphozoa (jellyfish), and anthozoa (corals and sea anemones). \n\nBy focusing on these areas and utilizing the recommended resources, you can gain a more comprehensive understanding of the animal kingdom. Let me know if you have any further questions or require additional support!"]
  },
])




#API route to get questions from the AI
@app.route('/Questions', methods=['POST'])
def Questions():
    data = request.json
    sub_topic=data.get('subjectTopic')
    print(sub_topic)
    response=convo.send_message(sub_topic)
    candidates = response._result.candidates
    if candidates:
      content_parts = candidates[0].content.parts
      if content_parts:
        content_text = content_parts[0].text
        # Parse content_text to extract questions and options
        # Parse content_text to extract questions and options
      questions = []
      options = []
      lines = content_text.split('\n')
      current_question = ''
      current_options = []
      for line in lines:
          if line.startswith("**Question"):
              if current_question:
                  questions.append(current_question)
                  options.append(current_options)
                  current_options = []
              current_question = line[3:].split(":")[1].strip()
          elif line.strip().startswith(("a)", "b)", "c)", "d)")):
              current_options.append(line.strip())
      # Append the last question and its options
      if current_question:
          questions.append(current_question)
          options.append(current_options)
      # Combine questions and options into a list of dictionaries
      response_data = [{"question": q, "options": o} for q, o in zip(questions, options)]
    print(response_data)  
    return jsonify({"response": response_data})

@app.route('/ResponseAnalysis', methods=['POST'])
def ResponseAnalysis():
    data = request.json
    print(data)
    data_res=','.join(data['responses'])
    print(data_res)
    response=convo.send_message(data_res)
    candidates = response._result.candidates
    if candidates:
      content_parts = candidates[0].content.parts
      if content_parts:
        content_text = content_parts[0].text
        print(content_text)  
    return jsonify({"response": content_text})


#students API route
@app.route("/Students")
def Students():
    return {"students":["Durgesh","Rishitha","Arjun"]}

if __name__=="__main__":
    app.run(debug=True)