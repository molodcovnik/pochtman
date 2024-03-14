document.querySelector('.navigation__menu').addEventListener('click', (e) => {
    let currentTarget = e.target.getAttribute('data-interval');
    console.log(currentTarget);
    if (currentTarget === 'day') {
        document.querySelector('.static_day').classList.toggle('hidden');
        document.querySelector('.static_week').classList.add('hidden');
        document.querySelector('.static_month').classList.add('hidden');
    } else if (currentTarget === 'week') {
        document.querySelector('.static_week').classList.toggle('hidden');
        document.querySelector('.static_day').classList.add('hidden');
        document.querySelector('.static_month').classList.add('hidden');
    } else if (currentTarget === 'month') {
        document.querySelector('.static_month').classList.toggle('hidden');
        document.querySelector('.static_week').classList.add('hidden');
        document.querySelector('.static_day').classList.add('hidden');
    }
});