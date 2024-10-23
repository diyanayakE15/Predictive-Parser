"use client"; // This directive makes the component a client component

const HomePage = () => {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent default form submission behavior

    const grammar = (document.getElementById('grammar') as HTMLTextAreaElement).value;
    const inputString = (document.getElementById('inputString') as HTMLInputElement).value;

    try {
      const response = await fetch('/api/parse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ grammar, inputString }),
      });

      // Check if the response is OK
      if (!response.ok) {
        const errorText = await response.text();
        alert('Error: ' + errorText);
        return;
      }

      // Attempt to parse the response as JSON
      const data = await response.json();

      // Check if the log exists in the data
      if (!data.log) {
        alert('Error: Log is undefined in the response.');
        return;
      }

      displayLog(data.log);
    } catch (error) {
      alert('An error occurred: ' + error);
      console.error(error); // Log the error for debugging
    }
  };

  const displayLog = (log: any[]) => {
    const tableBody = document.getElementById('logTableBody') as HTMLTableSectionElement;
    tableBody.innerHTML = ''; // Clear previous logs

    log.forEach(step => {
      const row = document.createElement('tr');

      const inputBufferCell = document.createElement('td');
      inputBufferCell.textContent = step.input_buffer;
      row.appendChild(inputBufferCell);

      const stackCell = document.createElement('td');
      stackCell.textContent = step.stack;
      row.appendChild(stackCell);

      const actionCell = document.createElement('td');
      actionCell.textContent = step.action;
      row.appendChild(actionCell);

      tableBody.appendChild(row);
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Predictive Parser</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            
            <textarea
              id="grammar"
              rows={5}
              cols={40}
              placeholder="Enter grammar here"
              required
              style={{ width: '100%' }}
            />
          </label>
        </div>
        <div>
          <label>
            Input String:
            <input
              type="text"
              id="inputString"
              placeholder="Enter input string here"
              required
              style={{ width: '100%' }}
            />
          </label>
        </div>
        <button type="submit">Parse</button>
      </form>

      <h2>Parsing Steps</h2>
      <table style={{ width: '100%', marginTop: '10px', border: '1px'}}>
        <thead>
          <tr>
            <th>Input Buffer</th>
            <th>Stack</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="logTableBody">
          {/* Parsing log will be inserted here */}
        </tbody>
      </table>
    </div>
  );
};

export default HomePage;
