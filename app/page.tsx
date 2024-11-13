// "use client";

// import React, { useState, useEffect } from 'react';
// import './PredictiveParser.css'; // Import the CSS file for styling

// const PredictiveParser = () => {
//   const [log, setLog] = useState([]);
//   const [inputString, setInputString] = useState('');
//   const [rules, setrules] = useState('');
//   const [animating, setAnimating] = useState(false); // State to control animation
//   const [displayedRows, setDisplayedRows] = useState([]); // State to control which rows are displayed

//   // States for FIRST, FOLLOW sets and parsing table
//   const [firsts, setFirsts] = useState({});
//   const [follows, setfollows] = useState({});
//   const [parsingTable, setParsingTable] = useState({});

//   const handleParse = async (e) => {
//     e.preventDefault();
//     setAnimating(true); // Start animation

//     // Send data to backend
//     const response = await fetch('http://127.0.0.1:5000/recursion', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({
//         rules: rules,
//         inputString: inputString,
//       }),
//     });

//     const data = await response.json();

//     // Check if response has log, FIRST, FOLLOW and parsing table
//     if (data.log) {
//       setLog(data.log);
//       setDisplayedRows([]); // Reset displayed rows
//       animateRows(data.log); // Start animating rows
//     }

//     if (data.firsts) {
//       setFirsts(data.firsts); // Set FIRST sets
//     }

//     if (data.follows) {
//       setfollows(data.follows); // Set FOLLOW sets
//     }

//     if (data.parsingTable) {
//       setParsingTable(data.parsing_table); // Set Parsing table
//     }

//     setAnimating(false); // End animation
//   };

//   // Function to animate row display
//   const animateRows = (rows) => {
//     rows.forEach((_, index) => {
//       setTimeout(() => {
//         setDisplayedRows((prev) => [...prev, rows[index]]);
//       }, index * 1000); // Delay each row by 1000ms (1 second)
//     });
//   };

//   return (
//     <div className="predictive-parser" style={{ padding: '20px' }}>
//       <form onSubmit={handleParse} style={{ marginBottom: '20px' }}>
//         <div>
//           <label>
//             rules:
//             <textarea
//               placeholder="Enter rules (e.g., S -> a A\nA -> b B | ε\nB -> c)"
//               value={rules}
//               onChange={(e) => setrules(e.target.value)}
//               style={{ width: '100%', height: '100px', marginTop: '5px' }}
//             />
//           </label>
//         </div>

//         <div style={{ marginTop: '15px' }}>
//           <label>
//             Input String:
//             <input
//               type="text"
//               placeholder="Enter Input String"
//               value={inputString}
//               onChange={(e) => setInputString(e.target.value)}
//               style={{ width: '100%', marginTop: '5px' }}
//             />
//           </label>
//         </div>

//         <div style={{ marginTop: '15px' }}>
//           <button type="submit">Parse</button>
//         </div>
//       </form>

//       {firsts && follows && parsingTable && (
//         <div>
//           <h2>FIRST and FOLLOW Sets</h2>
//           <table border="1" style={{ width: '100%', marginTop: '15px' }}>
//             <thead>
//               <tr>
//                 <th>Non-T</th>
//                 <th>FIRST</th>
//                 <th>FOLLOW</th>
//               </tr>
//             </thead>
//             <tbody>
//               {Object.keys(firsts).map((nonTerm) => (
//                 <tr key={nonTerm}>
//                   <td>{nonTerm}</td>
//                   <td>{Array.from(firsts[nonTerm] || []).join(', ')}</td>
//                   <td>{Array.from(follows[nonTerm] || []).join(', ')}</td>
//                 </tr>
//               ))}
//             </tbody>
//             </table>
//         </div>
//       )}

      
//       {displayedRows.length > 0 && (
//         <div>
//           <h2>Parsing Steps</h2>
//           <table border="1" style={{ width: '100%', marginTop: '15px' }}>
//             <thead>
//               <tr>
//                 <th>Input Buffer</th>
//                 <th>Stack</th>
//                 <th>Action</th>
//               </tr>
//             </thead>
//             <tbody>
//               {displayedRows.map((step, index) => (
//                 <tr key={index} className="row">
//                   <td>
//                     {step.input_buffer.split('').map((char, i) => (
//                       <span key={i} className={`input-buffer ${step.action === 'add' ? 'bounce-in' : ''}`}>
//                         {char}
//                       </span>
//                     ))}
//                   </td>
//                   <td>
//                     {step.stack.split('').map((char, i) => (
//                       <span key={i} className={`stack ${step.action === 'remove' ? 'bounce-out' : ''}`}>
//                         {char}
//                       </span>
//                     ))}
//                   </td>
//                   <td>{step.action}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}

//       {animating && (
//         <div className="animation-container">
//           {inputString.split('').map((char, index) => (
//             <span key={index} className={`animated-input bounce-in`}>
//               {char}
//             </span>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// };

// export default PredictiveParser;

"use client";

import React, { useState, useEffect } from 'react';
import './PredictiveParser.css'; // Import the CSS file for styling

const PredictiveParser = () => {
  const [log, setLog] = useState([]);
  const [inputString, setInputString] = useState('');
  const [rules, setrules] = useState('');
  const [animating, setAnimating] = useState(false);
  const [displayedRows, setDisplayedRows] = useState([]);
  const [firsts, setFirsts] = useState({});
  const [follows, setfollows] = useState({});
  const [parsingTable, setParsingTable] = useState([]);
  const [nonterm_userdef, setnonterm_userdef] = useState([]);
  const [term_userdef, setterm_userdef] = useState([]);

  const handleParse = async (e) => {
    e.preventDefault();
    setAnimating(true);

    const response = await fetch('http://127.0.0.1:5000/recursion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        rules: rules,
        inputString: inputString,
      }),
    });

    const data = await response.json();

    if (data.log) {
      setLog(data.log);
      setDisplayedRows([]);
      animateRows(data.log);
    }

    if (data.firsts) setFirsts(data.firsts);
    if (data.follows) setfollows(data.follows);
    
    // Handle parsing table and labels
    if (data.parsing_table && data.nonterm_userdef && data.term_userdef) {
      setParsingTable(data.parsing_table);
      setnonterm_userdef(data.nonterm_userdef);
      setterm_userdef(data.term_userdef);
    }

    setAnimating(false);
  };

  const animateRows = (rows) => {
    rows.forEach((_, index) => {
      setTimeout(() => {
        setDisplayedRows((prev) => [...prev, rows[index]]);
      }, index * 1000);
    });
  };

  return (
    <div className="predictive-parser" style={{ padding: '20px' }}>
      <form onSubmit={handleParse} style={{ marginBottom: '20px' }}>
        <div>
          <label>
            Rules:
            <textarea
              placeholder="Enter rules (e.g., S -> a A\nA -> b B | ε\nB -> c)"
              value={rules}
              onChange={(e) => setrules(e.target.value)}
              style={{ width: '100%', height: '100px', marginTop: '5px' }}
            />
          </label>
        </div>

        <div style={{ marginTop: '15px' }}>
          <label>
            Input String:
            <input
              type="text"
              placeholder="Enter Input String"
              value={inputString}
              onChange={(e) => setInputString(e.target.value)}
              style={{ width: '100%', marginTop: '5px' }}
            />
          </label>
        </div>

        <div style={{ marginTop: '15px' }}>
          <button type="submit">Parse</button>
        </div>
      </form>

      {firsts && follows && (
        <div>
          <h2>FIRST and FOLLOW Sets</h2>
          <table border="1" style={{ width: '100%', marginTop: '15px' }}>
            <thead>
              <tr>
                <th>Non-Terminal</th>
                <th>FIRST</th>
                <th>FOLLOW</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(firsts).map((nonTerm) => (
                <tr key={nonTerm}>
                  <td>{nonTerm}</td>
                  <td>{Array.from(firsts[nonTerm] || []).join(', ')}</td>
                  <td>{Array.from(follows[nonTerm] || []).join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {parsingTable.length > 0 && (
        <div>
          <h2>Parsing Table</h2>
          <table border="1" cellPadding="5" cellSpacing="0">
            <thead>
              <tr>
                <th>Non-Terminal</th>
                {term_userdef.map((terminal, idx) => (
                  <th key={idx}>{terminal}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {nonterm_userdef.map((nonTerm, rowIndex) => (
                <tr key={rowIndex}>
                  <td>{nonTerm}</td>
                  {parsingTable[rowIndex].map((cell, cellIndex) => (
                    <td key={cellIndex}>{cell || '-'}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {displayedRows.length > 0 && (
        <div>
          <h2>Parsing Steps</h2>
          <table border="1" style={{ width: '100%', marginTop: '15px' }}>
            <thead>
              <tr>
                <th>Input Buffer</th>
                <th>Stack</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {displayedRows.map((step, index) => (
                <tr key={index} className="row">
                  <td>{step.stack}</td>
                  <td>{step.input_buffer}</td>
                  <td>{step.action}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {animating && (
        <div className="animation-container">
          {inputString.split('').map((char, index) => (
            <span key={index} className={`animated-input bounce-in`}>
              {char}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default PredictiveParser;
