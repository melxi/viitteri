const URL = 'https://viitteri.herokuapp.com'

const followBtns = document.querySelectorAll('.btn-follow')
const likeBtns = document.querySelectorAll('.btn-like')

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

likeBtns.forEach(likeBtn => {
  likeBtn.addEventListener('click', async ({ target }) => {
    const { tweet, csrf } = target.dataset

    if (target.firstElementChild.className.includes('fill')) {
      console.log(tweet)
      const response = await fetch(`${URL}/unlike`, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf
        },
        body: JSON.stringify(tweet)
      })
      
      const data = await response.json()

      if (!data.hasLiked) {
        const heartElement = target.firstElementChild
        heartElement.className = heartElement.className.replace('-fill','');
        heartElement.nextElementSibling.textContent--
      }

      return false;
    }

    const response = await fetch(`${URL}/like`, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf
      },
      body: JSON.stringify(tweet)
    })

    const data = await response.json()

    if (data.hasLiked) {
      const heartElement = target.firstElementChild
      heartElement.className += '-fill'
      heartElement.nextElementSibling.textContent++
    }

    return true
  })
})