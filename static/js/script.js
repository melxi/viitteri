const URL = 'http://localhost:5000'

async function followUser(userId, csrfToken) {
    const response = await fetch(`${URL}/follow`, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin':'*',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(userId)
    })

    return response.json()
}