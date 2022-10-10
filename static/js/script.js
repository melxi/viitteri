const URL = 'http://localhost:5000'

const followBtns = document.querySelectorAll('.btn-follow')

followBtns.forEach(followBtn => {
  followBtn.addEventListener('click', async ({ target }) => {
    const { user, csrf } = target.dataset
  
    const response = await fetch(`${URL}/follow`, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf
        },
        body: JSON.stringify(user)
      })
  
      return response.json()
  })
})