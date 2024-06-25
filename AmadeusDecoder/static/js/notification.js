(function(d){
    var notif_number = document.getElementById('notif_number');
    var badge = document.getElementById('badge');
    
    var int = window.setInterval(updateBadge, 2000); //Update the badge every 5 seconds
    var badgeNum;    
    function updateBadge(){//To rerun the animation the element must be re-added back to the DOM
          var badgeChild = badge.children[0];
              if(badgeChild.className==='badge-num')
                  badge.removeChild(badge.children[0]);
          
          badgeNum = document.createElement('div'); 
        badgeNum.setAttribute('class','badge-num');
             badgeNum.innerHTML = notif_number.value
          var insertedElement = badge.insertBefore(badgeNum,badge.firstChild); 
    }
  })(document);

  
  document.addEventListener('DOMContentLoaded', function() {
    const scrollingItems = document.querySelector('.scrolling-items');

    scrollingItems.addEventListener('mouseenter', function() {
        scrollingItems.style.animationPlayState = 'paused';
    });

    scrollingItems.addEventListener('mouseleave', function() {
        scrollingItems.style.animationPlayState = 'running';
    });
});