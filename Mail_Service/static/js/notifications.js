const gridCells = document.querySelector('.wrapper-grid-table');

gridCells.addEventListener('mouseover', (e) => {
    let uid = e.target.getAttribute('data-uid');
    // let cellsUid = document.querySelectorAll(`[data-uid="${uid}"]`);
    let cellsUid = [].map.call(document.querySelectorAll(`[data-uid="${uid}"]`), function(el) {
        el.style.backgroundColor = '#e9dfdf';
        return el;
    })

});

gridCells.addEventListener('mouseout', (e) => {
    let uid = e.target.getAttribute('data-uid');
    let readed = e.target.getAttribute('data-readed');
    // let cellsUid = document.querySelectorAll(`[data-uid="${uid}"]`);
    let cellsUid = [].map.call(document.querySelectorAll(`[data-uid="${uid}"]`), function(el) {
        if (readed === "unreaded") {
            el.style.backgroundColor = '#91eaa5';
            return el;
        } else {
            el.style.backgroundColor = '#fff';
            return el;
        }
        
    })

});

gridCells.addEventListener('dblclick', (e) => {
    let uid = e.target.getAttribute('data-uid');
    window.location.pathname = window.location.pathname + uid + '/';
    // console.log(window.location.pathname);
});