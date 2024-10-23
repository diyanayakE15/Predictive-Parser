export async function POST(request: Request) {
  const { grammar, inputString } = await request.json();

  const response = await fetch('http://127.0.0.1:5000/parse', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ grammar, inputString }),
  });

  const data = await response.json();
  return new Response(JSON.stringify({ result: data.result }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}
