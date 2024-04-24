import './QuizPage.css';
import React, { useState } from 'react';


function formatResponse(response) {
  const lines = response.split('\n');
  let isList = false;
  let listItems = [];
  const elements = lines.map((line, index) => {
    if (line.startsWith('##')) {
      const text = line.substring(2).trim();
      return <h1 key={index}>{text}</h1>;
    } else if (line.startsWith('**')) {
      isList = true;
      const text = line.substring(2).trim();
      listItems.push(<li key={index}>{text}</li>);
      return null; // Return null when adding list items
    } else {
      if (isList) {
        isList = false;
        const list = <ul key={index}>{listItems}</ul>;
        listItems = [];
        return list;
      } else {
        return <p key={index}>{line}</p>;
      }
    }
  }).filter(element => element !== null); // Filter out null elements
  if (isList) {
    elements.push(<ul key={lines.length}>{listItems}</ul>);
  }
  return elements;
}

function AnalysisComponent({responseString}) {
  return (
    <div className="App">
      {formatResponse(responseString)}
    </div>
  );
}

function QuizPage() {
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState([]);
  const [analysis, setAnalysis] = useState('');
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");

  const handleSubmitSubjectTopic = async (e) => {
    e.preventDefault();
    const subjectTopic= subject+":"+topic;
    try {
      // const res = await axios.post('/Questions', { subjectTopic });
      // setQuestions(res.data.response); // Assuming the API returns questions
      try {
        const response = await fetch('http://localhost:5000/Questions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ subjectTopic }),
        });
      
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
      
        const data = await response.json();
        setQuestions(data.response);
      } catch (error) {
        // Handle errors
        console.error('There was a problem with the fetch operation:', error);
      }
      
    } catch (error) {
      console.error('Error:', error);
    }
  };
  const handleSubmitResponses = async (e) => {
    e.preventDefault();
    try {
      try{
      const response = await fetch('http://localhost:5000/ResponseAnalysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({responses})
      });
    
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
    
      const data = await response.json();
      console.log(data.response)
      setAnalysis(data.response);
    } catch (error) {
      // Handle errors
      console.error('There was a problem with the fetch operation:', error);
  }
 } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className='quiz-page'>
      <div className="input_box">
      <h1>Test Your Knowledge</h1>
      <form onSubmit={handleSubmitSubjectTopic}>
        <input
          type="text"
          placeholder="Enter subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
        />
         <input
          type="text"
          placeholder="Enter topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <button type="submit">Start Test</button>
      </form>
      </div>
      {questions.length > 0 && (
        <div className='quiz-content'>
          <h2>Questions</h2>
          <form onSubmit={handleSubmitResponses}>
            {questions.map((question, index) => (
              <div key={index}>
                <p>{question["question"]}</p>
                <p>Choose one option</p>
                <ul>
                  <li>{question["options"][0]}</li>
                  <li>{question["options"][1]}</li>
                  <li>{question["options"][2]}</li>
                  <li>{question["options"][3]}</li>
                </ul>
                <input
                type="text"
                placeholder="Enter your response"
                value={responses[index] || ''}
                onChange={(e) => {
                  const newResponses = [...responses]; // Copy the current responses array
                  newResponses[index] = e.target.value; // Update the response at the current index
                  setResponses(newResponses); // Set the updated responses array
                }}
              />
              </div>
            ))}
            <button type="submit">Submit Responses</button>
          </form>
        </div>
      )}
      {analysis && (
        <div className='quiz-content'>
          <h2>Analysis</h2>
          
          <AnalysisComponent responseString={analysis}/>
        </div>
      )}
    </div>
  );
}
export default QuizPage;